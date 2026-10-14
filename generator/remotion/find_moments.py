"""Help pick segment times and camera boxes for a Remotion reel.

  python3 find_moments.py public/rec-<id>.mp4 sheet            -> out/sheet.png   (20 frames of the whole video, with times)
  python3 find_moments.py public/rec-<id>.mp4 strips Y H [STEP] -> out/strips_N.png (band y=Y..Y+H every STEP s, with times)
  python3 find_moments.py public/rec-<id>.mp4 zoom T0 T1 X Y W H -> out/zoom.png  (crop X,Y,W,H every 0.25 s from T0 to T1)

Read the PNGs to see exactly when a value changes (e.g. "Send second reminder" -> "Reminded today").
All coordinates are in recording pixels (usually 1920x1080), the same units the spec uses.
"""
import glob
import os
import subprocess
import sys

from PIL import Image

os.makedirs('out', exist_ok=True)


def dur(path):
    return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path]))


def grid(files, cols, out):
    ims = [Image.open(f) for f in files]
    w, h = ims[0].size
    rows = (len(ims) + cols - 1) // cols
    sheet = Image.new('RGB', (w * cols, h * rows), 'white')
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % cols) * w, (i // cols) * h))
    sheet.save(out)
    for f in files:
        os.remove(f)
    print(out, sheet.size)


def run(args):
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error'] + args, check=True)


video, mode = sys.argv[1], sys.argv[2]
stamp = "drawtext=text='%{pts\\:hms}':x=8:y=8:fontsize=24:fontcolor=red:box=1"
if mode == 'sheet':
    d = dur(video)
    run(['-i', video, '-vf', f'fps=20/{d},scale=480:-1,{stamp}', '-frames:v', '20', 'out/_s_%02d.png'])
    grid(sorted(glob.glob('out/_s_*.png')), 4, 'out/sheet.png')
elif mode == 'strips':
    y, h = int(sys.argv[3]), int(sys.argv[4])
    step = float(sys.argv[5]) if len(sys.argv) > 5 else 2
    run(['-i', video, '-vf', f'fps=1/{step},crop=1920:{h}:0:{y},scale=960:-1,{stamp}', 'out/_t_%03d.png'])
    files = sorted(glob.glob('out/_t_*.png'))
    for k in range(0, len(files), 16):
        grid(files[k:k + 16], 1, f'out/strips_{k // 16}.png')
elif mode == 'zoom':
    t0, t1, x, y, w, h = map(float, sys.argv[3:9])
    run(['-ss', str(t0), '-t', str(t1 - t0), '-i', video, '-vf',
         f"fps=4,crop={int(w)}:{int(h)}:{int(x)}:{int(y)},drawtext=text='{t0}+%{{pts\\:hms}}':x=5:y=5:fontsize=18:fontcolor=red:box=1",
         'out/_z_%03d.png'])
    grid(sorted(glob.glob('out/_z_*.png')), 6, 'out/zoom.png')
