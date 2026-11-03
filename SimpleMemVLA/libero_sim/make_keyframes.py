"""Make one contact sheet per episode: a frame every 40 steps, labelled with step + sub-task."""
import glob
import json
import os
import sys

import imageio.v2 as imageio
import numpy as np
from PIL import Image, ImageDraw

run = sys.argv[1]
for ep in sorted(glob.glob(os.path.join(run, "episodes", "*"))):
    vids = glob.glob(os.path.join(ep, "rollout_*.mp4"))
    if not vids:
        continue
    frames = imageio.mimread(vids[0], memtest=False)
    idx = list(range(0, len(frames), 40))
    if idx[-1] != len(frames) - 1:
        idx.append(len(frames) - 1)
    tiles = []
    for i in idx:
        im = Image.fromarray(frames[i]).resize((frames[i].shape[1] // 2, frames[i].shape[0] // 2))
        tiles.append(im)
    w, h = tiles[0].size
    cols = 5
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (w * cols, h * rows), (0, 0, 0))
    for k, t in enumerate(tiles):
        sheet.paste(t, ((k % cols) * w, (k // cols) * h))
    sheet.save(os.path.join(ep, "keyframes.jpg"), quality=85)
    print("ok", os.path.basename(ep), len(frames))
