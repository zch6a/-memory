# SimpleMemVLA × LIBERO-Recover 小样本测试

把 [SimpleMemVLA](https://github.com/OpenBMB/SimpleMemVLA)（官方 checkpoint `simplememvla_libero`，未重新训练）接入 [LIBERO-Recover](https://github.com/liulin815/LIBERO-Recovery) 失败场景做闭环评测。目的是看 baseline 的"前一步物体状态没达成，却继续执行后续动作，重做指令生成得很晚或生成后不执行"这个问题，是不是 RoboMemArena 独有的。

- 汇报：[`REPORT_汇报.md`](REPORT_汇报.md)
- 逐 episode 详细结果：[`DETAILS_详细结果.md`](DETAILS_详细结果.md)（文件开头有更正说明，以汇报为准）

## 结果

| 测试 | 成功率 |
|---|---|
| LIBERO-Recover（LIBERO-10 失败场景，每个任务 1 个，共 10 次） | **2/10（20%）** |
| 原版 LIBERO-10 对照（SimpleMemVLA 原版评测脚本，每个任务 1 次） | 8/10（80%） |

脚本自动标出 6 次"未达成就推进"。逐个看视频核实后：确认 3 次（#10 书、#02 碗、#05 汤罐头），大概率 1 次（#07），存疑 1 次（#01），误判 1 次（#09）。

## 目录

```
REPORT_汇报.md                     汇报（汇报里写的 run10/ 就是这里的 results/run10/）
DETAILS_详细结果.md                逐 episode 详细结果和统计表
videos_汇总/LIBERO-Recover/        10 个测试视频（画面下方叠加了当前指令、步数、是否抓住物体、目标达成情况）
videos_汇总/原版LIBERO-10对照/     原版对照的 10 个视频
results/run10/                     LIBERO-Recover 小样本
  scene_summary.json               成功率
  args.json                        运行参数
  episodes/<场景>/
    decisions.jsonl                每条指令：生成步数、仿真时间、实际时间、推理耗时、指令文本、接下来执行的 8 步动作
    steps.jsonl                    每一步：执行的动作、时间、末端位置、夹爪开合、抓住的物体、物体坐标、目标谓词真假
    summary.json                   是否成功、步数、子任务时间线
    rollout_*.mp4, keyframes.jpg   视频和关键帧拼图
  analysis/                        自动统计：episodes.csv、delayed_recovery.csv、timelines.md
results/orig_libero10_1ep/         原版 LIBERO-10 对照的结果和视频
logs/                              两次评测的完整运行日志
SimpleMemVLA/                      SimpleMemVLA 代码（MIT），加上我们新增的文件（见下）
UPSTREAM_COMMITS.txt               两个上游仓库所用的 commit
```

## 我们新增的文件

SimpleMemVLA 原有代码没有改动，只新增了这三个文件：

- `SimpleMemVLA/libero_sim/eval_recover.py`：在 LIBERO-Recover 场景上评测，并记录上面列出的逐指令、逐步日志
- `SimpleMemVLA/libero_sim/analyze_recover.py`：自动统计"未达成就推进"和重做延迟
- `SimpleMemVLA/libero_sim/make_keyframes.py`：生成关键帧拼图

LIBERO-Recovery 没有写开源许可证，所以这里不包含它的代码，只在 `UPSTREAM_COMMITS.txt` 里记了所用版本。

## 复现

环境：Ubuntu 22.04，单卡 RTX 4090，CUDA 12.x 驱动。

```bash
# 1. 代码
git clone https://github.com/liulin815/LIBERO-Recovery.git   # 用 UPSTREAM_COMMITS.txt 里的 commit
# SimpleMemVLA 用本仓库里的 SimpleMemVLA/ 目录

# 2. 环境（Python 3.10）
conda create -p ./envs/smv python=3.10 -y && conda activate ./envs/smv
cd SimpleMemVLA
pip install -r requirements.txt && pip install -e . --no-deps
pip install "transformers==5.11.0"     # 5.20 要求 torch>=2.6，和锁定的 torch 2.4.1 冲突
pip install "robosuite==1.4.0" "mujoco==2.3.2" "bddl==1.0.1" easydict future "gym==0.25.2" cloudpickle hydra-core thop "imageio[ffmpeg]" matplotlib
pip install --no-deps https://github.com/Dao-AILab/flash-attention/releases/download/v2.7.4.post1/flash_attn-2.7.4.post1+cu12torch2.4cxx11abiFALSE-cp310-cp310-linux_x86_64.whl
pip install --no-deps "flash-linear-attention==0.2.2" && pip install --no-build-isolation "causal-conv1d==1.5.2"
apt-get install -y libegl1 libgl1 libglvnd0 libglib2.0-0     # EGL 离屏渲染
# 让 libero 指向 LIBERO-Recovery 自带的 LIBERO（场景文件依赖它）
echo /path/to/LIBERO-Recovery/LIBERO > $(python -c "import sysconfig;print(sysconfig.get_paths()['purelib'])")/zz_libero_repo.pth

# 3. 权重和场景（ModelScope）
modelscope download --model keithyc/simplememvla_libero --local_dir ckpt/simplememvla_libero
modelscope download --dataset ataier/LIBERO_Recovery_Assets --local_dir data/LIBERO_Recovery_Assets
cd data/LIBERO_Recovery_Assets && mkdir small && tar xzf scenes.tar.gz -C small && cd -

# 4. 评测（在 SimpleMemVLA/ 下）
export MUJOCO_GL=egl PYTHONPATH=$PWD HF_HUB_OFFLINE=1
python -m libero_sim.eval_recover --checkpoint ckpt/simplememvla_libero \
  --scene_dir data/LIBERO_Recovery_Assets/small/scenes/selected_bddl_scenes_10 \
  --per_task 1 --num_scenes 10 --num_open_trials 1 --num_close_trials 0 --out_dir results/run10
python libero_sim/analyze_recover.py results/run10

# 原版对照
CHECKPOINT=ckpt/simplememvla_libero TASK_SUITES=libero_10 EPISODES_PER_TASK=1 GROUP_SIZE=1 bash scripts/eval_libero.sh
```

第一次推理时 Triton 要编译内核，会比较慢；之后每个 episode 约 1–3 分钟。

## 和官方协议的差异

- 只跑了夹爪张开起步、每个场景 1 次（官方是张开、闭合各 5 次）。
- LIBERO-Recovery 官方的 `perturb_object_xy` 下标少加了 1。仿真状态向量第 0 位是时间，所以官方实际扰动的是"前一个状态量 + x"。`eval_recover.py` 按本意改成扰动 x 和 y。
- 记忆冷启动：没有失败之前的视频历史，与论文协议一致。
- 自动统计依赖仿真的抓取检测，会漏判（#09 就是），必须结合视频看。
