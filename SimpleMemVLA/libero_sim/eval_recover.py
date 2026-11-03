"""Closed-loop SimpleMemVLA evaluation on LIBERO-Recover failure scenes.

Scene protocol follows LIBERO-Recovery's ``eval_libero_custom_scene.py``: build the
env from ``<stem>.bddl``, load ``<stem>_sim_state.npy``, add a +-2 cm xy offset to
every free-joint object, re-anchor the OSC goal, drive the gripper open/closed for
``gripper_settle_steps`` and roll out for at most ``max_steps``. Policy, observation
and action handling follow SimpleMemVLA's ``libero_sim`` (unchanged).

Extra analysis logs (per episode, under ``<out_dir>/episodes/<tag>__trial<k>_<grip>/``):
  decisions.jsonl   one row per policy call: env step, wall time, latency, sub-task text,
                    whether it changed, the executed action chunk
  steps.jsonl       one row per env step: action, eef pos, gripper qpos, goal predicate
                    truth values, tracked object positions, which objects are grasped
  summary.json      success, length, sub-task timeline
  rollout.mp4       agentview | wrist, with step + current sub-task overlaid
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import pathlib
import re
import time

import numpy as np

from libero_sim._mujoco_env import prepare_mujoco_runtime

prepare_mujoco_runtime()

import imageio  # noqa: E402
import torch  # noqa: E402
from PIL import Image, ImageDraw, ImageFont  # noqa: E402

from libero_sim.libero_env import encode_frame, encode_state  # noqa: E402

DUMMY = [0.0] * 6 + [-1.0]


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--checkpoint", required=True)
    p.add_argument("--scene_dir", required=True)
    p.add_argument("--scene_list", default="", help="optional txt of bddl paths (one per line)")
    p.add_argument("--per_task", type=int, default=1, help="scenes sampled per task folder")
    p.add_argument("--num_scenes", type=int, default=10)
    p.add_argument("--num_open_trials", type=int, default=1)
    p.add_argument("--num_close_trials", type=int, default=0)
    p.add_argument("--obj_noise_xy", type=float, default=0.02)
    p.add_argument("--gripper_settle_steps", type=int, default=20)
    p.add_argument("--max_steps", type=int, default=520)
    p.add_argument("--execute_horizon", type=int, default=8)
    p.add_argument("--num_denoising_steps", type=int, default=10)
    p.add_argument("--eval_temperature", type=float, default=1.0)
    p.add_argument("--max_reasoning_tokens", type=int, default=256)
    p.add_argument("--compute_dtype", default="bfloat16")
    p.add_argument("--attn_implementation", default="flash_attention_2")
    p.add_argument("--seed", type=int, default=7)
    p.add_argument("--out_dir", required=True)
    return p.parse_args()


# ---------------------------------------------------------------- scene helpers
# (mirrors LIBERO-Recovery/examples/LIBERO/eval_files/eval_libero_custom_scene.py)

def parse_language(bddl_path):
    with open(bddl_path) as f:
        for line in f:
            m = re.search(r"\(:language\s+(.+?)\s*\)", line)
            if m:
                return m.group(1).strip()
    return pathlib.Path(bddl_path).stem


def free_joint_xy_adrs(env):
    model = env.env.sim.model
    out = []
    for name, body_id in getattr(env.env, "obj_body_id", {}).items():
        jnt = int(model.body_jntadr[body_id])
        if jnt < 0 or int(model.jnt_type[jnt]) != 0:
            continue
        adr = int(model.jnt_qposadr[jnt])
        # flattened sim state = [time, qpos..., qvel...]
        out.append((name, 1 + adr, 1 + adr + 1))
    return out


def perturb(flat_state, adrs, noise, rng):
    s = np.array(flat_state, dtype=np.float64, copy=True)
    deltas = {}
    for name, ax, ay in adrs:
        dx, dy = float(rng.uniform(-noise, noise)), float(rng.uniform(-noise, noise))
        s[ax] += dx
        s[ay] += dy
        deltas[name] = (dx, dy)
    return s, deltas


def reset_controller_goal(env):
    for robot in env.robots:
        robot.controller.update()
        robot.controller.update_initial_joints(robot.controller.joint_pos)
        robot.controller.reset_goal()


def build_env(bddl_path, seed, attempts=12):
    from libero.libero.envs import OffScreenRenderEnv
    from robosuite.utils.errors import RandomizationError

    for a in range(attempts):
        np.random.seed(seed + a)
        try:
            return OffScreenRenderEnv(bddl_file_name=bddl_path, camera_heights=256,
                                      camera_widths=256, controller="OSC_POSE")
        except RandomizationError:
            continue
    return None


def reset_env(env, seed, attempts=12):
    from robosuite.utils.errors import RandomizationError

    for a in range(attempts):
        np.random.seed(seed + a)
        try:
            env.reset()
            return True
        except RandomizationError:
            continue
    return False


def select_scenes(args):
    if args.scene_list:
        with open(args.scene_list) as f:
            return [l.strip() for l in f if l.strip()]
    rng = np.random.RandomState(args.seed)
    by_task = {}
    for b in sorted(glob.glob(os.path.join(args.scene_dir, "**", "*.bddl"), recursive=True)):
        if not os.path.isfile(b[:-5] + "_sim_state.npy"):
            continue
        task = os.path.relpath(b, args.scene_dir).split(os.sep)[0]
        by_task.setdefault(task, []).append(b)
    chosen = []
    for task in sorted(by_task):
        files = by_task[task]
        idx = rng.choice(len(files), size=min(args.per_task, len(files)), replace=False)
        chosen += [files[i] for i in sorted(idx)]
    return chosen[: args.num_scenes] if args.num_scenes > 0 else chosen


# ---------------------------------------------------------------- analysis probes

def goal_predicates(env):
    inner = env.env
    out = {}
    for st in inner.parsed_problem["goal_state"]:
        try:
            out[" ".join(st)] = bool(inner._eval_predicate(st))
        except Exception:
            out[" ".join(st)] = None
    return out


def goal_objects(env):
    names = []
    for st in env.env.parsed_problem["goal_state"]:
        for n in st[1:]:
            if n in env.env.obj_body_id and n not in names:
                names.append(n)
    return names


def object_positions(env, names):
    inner = env.env
    return {n: np.round(inner.sim.data.body_xpos[inner.obj_body_id[n]], 4).tolist() for n in names}


def grasped_objects(env, names):
    inner = env.env
    robot = inner.robots[0]
    out = []
    for n in names:
        obj = inner.objects_dict.get(n)
        if obj is None:
            continue
        try:
            if inner._check_grasp(gripper=robot.gripper, object_geoms=obj.contact_geoms):
                out.append(n)
        except Exception:
            pass
    return out


# ---------------------------------------------------------------- video

_FONT = None


def _font():
    global _FONT
    if _FONT is None:
        try:
            _FONT = ImageFont.truetype("DejaVuSans.ttf", 13)
        except OSError:
            _FONT = ImageFont.load_default()
    return _FONT


def overlay(frame, step, subtask, task, grasp, preds):
    top = np.concatenate([frame["image"], frame["wrist_image"]], axis=1)
    canvas = Image.new("RGB", (top.shape[1], top.shape[0] + 74), (0, 0, 0))
    canvas.paste(Image.fromarray(top), (0, 0))
    d = ImageDraw.Draw(canvas)
    y = top.shape[0] + 2
    d.text((4, y), f"step {step}  t={step / 20:.1f}s  grasp={','.join(grasp) or '-'}", fill=(255, 255, 0), font=_font())
    d.text((4, y + 18), f"subtask: {subtask}"[:80], fill=(0, 255, 0), font=_font())
    done = sum(bool(v) for v in preds.values())
    d.text((4, y + 36), f"goal {done}/{len(preds)}: " + " | ".join(
        ("T " if v else "F ") + k for k, v in preds.items())[:80], fill=(200, 200, 255), font=_font())
    d.text((4, y + 54), task[:80], fill=(180, 180, 180), font=_font())
    return np.asarray(canvas)


# ---------------------------------------------------------------- main loop

def run_episode(env, policy, base_state, adrs, task, grip_close, rng, args, ep_dir):
    obs = env.set_init_state(perturb(base_state, adrs, args.obj_noise_xy, rng)[0])
    reset_controller_goal(env)
    grip = [0.0] * 6 + [1.0 if grip_close else -1.0]
    for _ in range(args.gripper_settle_steps):
        obs, _, _, _ = env.step(grip)

    names = goal_objects(env)
    policy.reset()
    frame = encode_frame(obs)
    state = encode_state(obs)
    cam_map = {k.split(".")[-1]: k for k in policy.image_keys}
    policy.observe({cam_map.get(k, k): v for k, v in frame.items()})

    dec_f = open(ep_dir / "decisions.jsonl", "w", buffering=1)
    step_f = open(ep_dir / "steps.jsonl", "w", buffering=1)
    writer = imageio.get_writer(ep_dir / "rollout.mp4", fps=20, macro_block_size=1)

    t0 = time.time()
    step, success, prev_text, timeline = 0, False, None, []
    preds = goal_predicates(env)
    grasp = grasped_objects(env, names)
    writer.append_data(overlay(frame, 0, "-", task, grasp, preds))
    decision = 0
    while step < args.max_steps and not success:
        t_call = time.time()
        actions, text = policy.predict(task, state=state)
        infer_ms = (time.time() - t_call) * 1000
        chunk = [np.clip(np.asarray(a, dtype=np.float64).reshape(-1), -1, 1) for a in actions[: args.execute_horizon]]
        changed = text != prev_text
        if changed:
            timeline.append({"step": step, "t_sim": step / 20, "t_wall": round(t_call - t0, 2), "subtask": text})
        dec_f.write(json.dumps({
            "decision": decision, "env_step": step, "t_sim": step / 20,
            "t_wall": round(t_call - t0, 3), "infer_ms": round(infer_ms, 1),
            "subtask": text, "subtask_changed": changed,
            "chunk": [np.round(a, 4).tolist() for a in chunk],
            "exec_steps": [step, step + len(chunk) - 1],
            "goal_before": preds, "grasp_before": grasp,
        }, ensure_ascii=False) + "\n")
        prev_text = text
        decision += 1
        for a in chunk:
            obs, _, done, _ = env.step(a.tolist())
            step += 1
            frame, state = encode_frame(obs), encode_state(obs)
            policy.observe({cam_map.get(k, k): v for k, v in frame.items()})
            preds = goal_predicates(env)
            grasp = grasped_objects(env, names)
            step_f.write(json.dumps({
                "step": step, "t_sim": step / 20, "t_wall": round(time.time() - t0, 3),
                "decision": decision - 1, "subtask": text, "action": np.round(a, 4).tolist(),
                "eef_pos": np.round(obs["robot0_eef_pos"], 4).tolist(),
                "gripper_qpos": np.round(obs["robot0_gripper_qpos"], 4).tolist(),
                "goal": preds, "grasped": grasp, "obj_pos": object_positions(env, names),
            }, ensure_ascii=False) + "\n")
            writer.append_data(overlay(frame, step, text, task, grasp, preds))
            if done or env.env._check_success():
                success = True
                break
            if step >= args.max_steps:
                break
    dec_f.close()
    step_f.close()
    writer.close()
    return success, step, timeline, time.time() - t0


def main():
    args = parse_args()
    out = pathlib.Path(args.out_dir)
    (out / "episodes").mkdir(parents=True, exist_ok=True)
    json.dump(vars(args), open(out / "args.json", "w"), indent=2)

    from libero_sim.policy import LiberoPolicy, get_vla
    from transformers import AutoProcessor

    vla, unnorm, norm_state = get_vla(args.checkpoint, args.compute_dtype,
                                      attn_implementation=args.attn_implementation)
    processor = AutoProcessor.from_pretrained(args.checkpoint, trust_remote_code=True,
                                              padding_side="right", model_max_length=8192)
    policy = LiberoPolicy(vla=vla, processor=processor, unnormalize_action=unnorm,
                          normalize_state=norm_state, num_denoising_steps=args.num_denoising_steps,
                          temperature=args.eval_temperature,
                          max_reasoning_tokens=args.max_reasoning_tokens)

    scenes = select_scenes(args)
    print(f"[recover] {len(scenes)} scenes", flush=True)
    rng = np.random.RandomState(args.seed)
    torch.manual_seed(args.seed)
    plan = [("close", True)] * args.num_close_trials + [("open", False)] * args.num_open_trials
    results = []
    for si, bddl in enumerate(scenes):
        tag = os.path.relpath(bddl, args.scene_dir)[:-5].replace(os.sep, "__")
        task = parse_language(bddl)
        base = np.load(bddl[:-5] + "_sim_state.npy")
        env = build_env(bddl, args.seed + 1_000_001 * (si + 1))
        if env is None:
            print(f"[recover] {tag}: env build failed, skipped", flush=True)
            continue
        env.seed(args.seed)
        adrs = free_joint_xy_adrs(env)
        for ti, (label, close) in enumerate(plan):
            if not reset_env(env, args.seed + 1_000_001 * (si + 1) + 10_001 * (ti + 1)):
                continue
            ep_dir = out / "episodes" / f"{tag}__trial{ti}_{label}"
            ep_dir.mkdir(parents=True, exist_ok=True)
            ok, n, timeline, wall = run_episode(env, policy, base, adrs, task, close, rng, args, ep_dir)
            rec = {"scene": tag, "bddl": bddl, "task": task, "trial": ti, "gripper_init": label,
                   "success": ok, "steps": n, "wall_sec": round(wall, 1), "subtask_timeline": timeline}
            json.dump(rec, open(ep_dir / "summary.json", "w"), indent=2, ensure_ascii=False)
            os.replace(ep_dir / "rollout.mp4", ep_dir / f"rollout_{'success' if ok else 'failure'}.mp4")
            results.append(rec)
            print(f"[recover] {si + 1}/{len(scenes)} {tag} {label}: success={ok} steps={n} "
                  f"wall={wall:.0f}s", flush=True)
        env.close()

    n = len(results)
    summary = {
        "total_episodes": n,
        "total_successes": sum(r["success"] for r in results),
        "overall_rate": (sum(r["success"] for r in results) / n) if n else None,
        "episodes": [{k: r[k] for k in ("scene", "task", "gripper_init", "success", "steps", "wall_sec")}
                     for r in results],
    }
    json.dump(summary, open(out / "scene_summary.json", "w"), indent=2, ensure_ascii=False)
    print(f"[recover] DONE {summary['total_successes']}/{n} = {summary['overall_rate']}", flush=True)


if __name__ == "__main__":
    main()
