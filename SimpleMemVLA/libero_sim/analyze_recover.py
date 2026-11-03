"""Post-hoc analysis of eval_recover.py logs.

For each episode it finds "stale-progress" windows: a goal object X is NOT held and its
goal predicate is False, yet the generated sub-task already belongs to a later phase
(place / pour / close / another object). It then measures

  * redo_delay  : steps (and seconds) from the window start until the model first
                  generates a sub-task that re-acquires X (reach / grasp / pick X)
  * redo_exec   : whether X is actually grasped within --exec_window steps after that
                  redo sub-task is generated

Outputs (next to the run): analysis/episodes.csv, analysis/delayed_recovery.csv,
analysis/timelines.md (sub-task timeline + flags per episode, for manual video review).
"""

from __future__ import annotations

import argparse
import csv
import glob
import json
import os
import re

PICK = re.compile(r"\b(reach|grasp|grab|pick|approach|go to|move to the|re-?grasp|lift)\b", re.I)
LATER = re.compile(r"\b(place|put|pour|drop|release|lower|insert|close|push|turn|stack|carry|transport|move .* (to|onto|into|over|toward)|bring)\b", re.I)


BRAND = {"akita", "chefmate", "porcelain", "box"}
ALL_OBJS: list[str] = []  # goal objects of the current episode, set in analyze_episode


def words(name: str) -> list[str]:
    # "akita_black_bowl_1" -> ["black", "bowl"]; "moka_pot_1" -> ["moka", "pot"]
    return [w for w in re.split(r"[_\d]+", name.lower()) if w and w not in BRAND]


def _score(text: str, obj: str) -> tuple[float, int]:
    """(fraction of obj's words present, count); 0 unless the noun (last word) is present.
    'book' matches black_book_1; 'white mug' prefers porcelain_mug_1 over white_yellow_mug_1."""
    ws = words(obj)
    t = re.sub(r"[^a-z ]", " ", text.lower()).split()
    if not ws or ws[-1] not in t:
        return (0.0, 0)
    hit = sum(w in t for w in ws)
    return (hit / len(ws), hit)


def mentions(text: str, obj: str) -> bool:
    """obj is named in text and no other goal object is a better match."""
    s = _score(text, obj)
    return s[1] > 0 and all(_score(text, o) <= s or o == obj for o in ALL_OBJS)


def classify(text: str, obj: str, others: list[str]) -> str:
    """'redo' = re-acquire obj; 'later' = a later phase of obj or another object; 'other'."""
    if mentions(text, obj) and PICK.search(text) and not re.search(r"\b(place|put|pour)\b", text, re.I):
        return "redo"
    if mentions(text, obj) and LATER.search(text):
        return "later"
    if any(mentions(text, o) for o in others):
        return "later"
    if LATER.search(text) and not PICK.search(text):
        return "later"
    return "other"


GENERIC = {"region", "the", "1", "2", "contain", "init", "cook", "side", "left", "right", "front", "back"}


CLOSE = re.compile(r"\b(close|closed|shut)\b", re.I)


def refers_to_later_goal(text: str, obj: str, goal_keys: list[str]) -> bool:
    """Sub-task closes the container obj still has to go into
    (e.g. 'push the bottom drawer closed' while 'in bowl white_cabinet_1_bottom_region' is unmet).
    BDDL lists predicates in no particular order, so the dependency is semantic."""
    if not CLOSE.search(text):
        return False
    t = set(re.sub(r"[^a-z ]", " ", text.lower()).split())
    for k in goal_keys:
        p = k.split()
        if len(p) == 3 and p[1] == obj and p[0] == "in":
            if (set(words(p[2])) - GENERIC - {"white", "wooden"}) & t:
                return True
    return False


def pred_for(obj: str, goal: dict) -> list[bool]:
    return [v for k, v in goal.items() if obj in k.split()[1:2]]


def log_trajectory(steps, objs) -> str:
    """Compress the rollout into 'sub-task [facts] -> ...' using logged sim state only."""
    if not steps:
        return ""
    segs, cur = [], None
    for s in steps:
        if cur is None or s["subtask"] != cur["subtask"]:
            cur = {"subtask": s["subtask"], "rows": []}
            segs.append(cur)
        cur["rows"].append(s)
    z0 = {o: steps[0]["obj_pos"][o][2] for o in objs}
    out = []
    prev_goal = {k: v for k, v in steps[0]["goal"].items()}
    for seg in segs:
        rows = seg["rows"]
        facts = []
        held = sorted({o for r in rows for o in r["grasped"]})
        if held:
            facts.append("抓住" + "/".join(held))
        closed_empty = any(r["action"][6] > 0 and max(abs(r["gripper_qpos"][0]), abs(r["gripper_qpos"][1])) < 0.004
                           and not r["grasped"] for r in rows)
        if closed_empty:
            facts.append("夹爪闭合但未夹到物体(空抓)")
        for o in objs:
            dz = max(r["obj_pos"][o][2] for r in rows) - z0[o]
            if dz > 1.0:
                facts.append(f"{o}飞出场景(仿真异常)")
            elif dz > 0.03:
                facts.append(f"{o}被抬起{dz * 100:.0f}cm")
        lost = [o for o in objs if o in rows[0]["grasped"] and o not in rows[-1]["grasped"]]
        if lost:
            facts.append("松开/掉落" + "/".join(lost))
        for k, v in rows[-1]["goal"].items():
            if v and not prev_goal.get(k):
                facts.append(f"达成[{k}]")
            if not v and prev_goal.get(k):
                facts.append(f"失去[{k}]")
        prev_goal = dict(rows[-1]["goal"])
        out.append(f"{seg['subtask']}({rows[0]['t_sim'] - 0.05:.1f}-{rows[-1]['t_sim']:.1f}s"
                   + (": " + ", ".join(facts) if facts else "") + ")")
    return " -> ".join(out)


def load(ep_dir):
    steps = [json.loads(l) for l in open(os.path.join(ep_dir, "steps.jsonl"))]
    decs = [json.loads(l) for l in open(os.path.join(ep_dir, "decisions.jsonl"))]
    summ = json.load(open(os.path.join(ep_dir, "summary.json")))
    return steps, decs, summ


def movable_goal_objects(steps):
    if not steps:
        return []
    objs = list(steps[0]["obj_pos"].keys())
    # objects that are the first argument of an on/in goal predicate are the ones to carry
    carried = []
    for k in steps[0]["goal"]:
        p = k.split()
        if len(p) == 3 and p[1] in objs and p[1] not in carried:
            carried.append(p[1])
    return carried


def analyze_episode(ep_dir, exec_window):
    steps, decs, summ = load(ep_dir)
    objs = movable_goal_objects(steps)
    ALL_OBJS[:] = objs
    events = []
    for obj in objs:
        others = [o for o in objs if o != obj]
        held = [obj in s["grasped"] for s in steps]
        done = [all(pred_for(obj, s["goal"])) if pred_for(obj, s["goal"]) else False for s in steps]
        ever_held = False
        i = 0
        while i < len(decs):
            d = decs[i]
            st = d["env_step"]
            sidx = max(0, st - 1)
            is_held = obj in d["grasp_before"]
            ever_held = ever_held or is_held
            obj_done = all(pred_for(obj, d["goal_before"])) if pred_for(obj, d["goal_before"]) else False
            kind = classify(d["subtask"], obj, others)
            # stale-progress: obj not held, not at goal, but sub-task is a later phase
            # (only after obj was handled once, or obj is the subject of the sub-task)
            if (not is_held and not obj_done and kind == "later"
                    and (ever_held or mentions(d["subtask"], obj)
                         or refers_to_later_goal(d["subtask"], obj, list(d["goal_before"])))):
                start = st
                start_dec = i
                stale_texts = []
                j = i
                while j < len(decs):
                    dj = decs[j]
                    if obj in dj["grasp_before"] or (pred_for(obj, dj["goal_before"]) and all(pred_for(obj, dj["goal_before"]))):
                        break
                    if classify(dj["subtask"], obj, others) == "redo":
                        break
                    stale_texts.append(dj["subtask"])
                    j += 1
                redo_step = decs[j]["env_step"] if j < len(decs) and classify(decs[j]["subtask"], obj, others) == "redo" else None
                redo_text = decs[j]["subtask"] if redo_step is not None else None
                executed = None
                if redo_step is not None:
                    win = held[redo_step: redo_step + exec_window]
                    executed = any(win)
                resolved_by = ("redo" if redo_step is not None else
                               ("grasped_without_redo_text" if j < len(decs) and obj in decs[j]["grasp_before"] else
                                ("goal_reached" if j < len(decs) else "never")))
                events.append({
                    "object": obj, "stale_start_step": start, "stale_start_t": start / 20,
                    "stale_decisions": j - start_dec,
                    "stale_subtasks": " | ".join(dict.fromkeys(stale_texts)),
                    "redo_step": redo_step, "redo_text": redo_text,
                    "redo_delay_steps": (redo_step - start) if redo_step is not None else None,
                    "redo_delay_s": ((redo_step - start) / 20) if redo_step is not None else None,
                    "redo_executed": executed, "resolved_by": resolved_by,
                })
                i = max(j, i + 1)
                continue
            i += 1
    summ["log_trajectory"] = log_trajectory(steps, objs)
    return summ, decs, events


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dir")
    ap.add_argument("--exec_window", type=int, default=80, help="steps allowed to re-grasp after redo text")
    ap.add_argument("--late_steps", type=int, default=40, help="delay >= this counts as 'late'")
    a = ap.parse_args()
    out = os.path.join(a.run_dir, "analysis")
    os.makedirs(out, exist_ok=True)
    ep_rows, ev_rows, md = [], [], ["# Sub-task timelines\n"]
    for ep in sorted(glob.glob(os.path.join(a.run_dir, "episodes", "*"))):
        if not os.path.exists(os.path.join(ep, "summary.json")):
            continue
        summ, decs, events = analyze_episode(ep, a.exec_window)
        name = os.path.basename(ep)
        flagged = [e for e in events if e["redo_delay_steps"] is None or e["redo_delay_steps"] >= a.late_steps
                   or e["redo_executed"] is False]
        ep_rows.append({"episode": name, "task": summ["task"], "success": summ["success"],
                        "steps": summ["steps"], "n_subtask_switches": len(summ["subtask_timeline"]),
                        "n_stale_events": len(events), "phenomenon": bool(flagged),
                        "log_trajectory": summ["log_trajectory"]})
        for e in events:
            ev_rows.append({"episode": name, "task": summ["task"], "success": summ["success"],
                            "late_or_not_executed": e in flagged, **e})
        md.append(f"## {name}\n- task: {summ['task']}\n- success: {summ['success']}  steps: {summ['steps']}\n"
                  f"- log trajectory (from sim state, not video): {summ['log_trajectory']}\n")
        md.append("| step | t(s) | wall(s) | sub-task | goal | grasped |\n|---|---|---|---|---|---|")
        prev = None
        for d in decs:
            if d["subtask"] != prev:
                g = ", ".join(("T " if v else "F ") + k for k, v in d["goal_before"].items())
                md.append(f"| {d['env_step']} | {d['t_sim']:.1f} | {d['t_wall']:.1f} | {d['subtask']} | {g} | {','.join(d['grasp_before']) or '-'} |")
                prev = d["subtask"]
        if events:
            md.append("\n**stale-progress events:**\n")
            for e in events:
                md.append(f"- `{e['object']}` from step {e['stale_start_step']} ({e['stale_start_t']:.1f}s): "
                          f"sub-tasks while not held = [{e['stale_subtasks']}] -> redo at "
                          f"{e['redo_step']} (delay {e['redo_delay_s']}s, '{e['redo_text']}'), "
                          f"re-grasp executed: {e['redo_executed']}, resolved_by: {e['resolved_by']}")
        md.append("\n**manual trajectory (fill in after watching video):** \n\n")
    for fn, rows in (("episodes.csv", ep_rows), ("delayed_recovery.csv", ev_rows)):
        with open(os.path.join(out, fn), "w", newline="", encoding="utf-8-sig") as f:
            if rows:
                w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
                w.writeheader()
                w.writerows(rows)
    open(os.path.join(out, "timelines.md"), "w", encoding="utf-8").write("\n".join(md))
    n = len(ep_rows)
    print(f"episodes {n}, success {sum(r['success'] for r in ep_rows)}, "
          f"with stale events {sum(r['n_stale_events'] > 0 for r in ep_rows)}, "
          f"flagged (late/not executed) {sum(r['phenomenon'] for r in ep_rows)}")


if __name__ == "__main__":
    main()
