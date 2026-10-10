"""Turn a raw Notion screen recording into a vertical Reel/TikTok/Short.

python3 generator/clip.py SRC OUT START END X0 Y0 X1 Y1 PRODUCT "HOOK<br>TEXT" [THEME]
- crops the recording to the box (x0,y0,x1,y1), keeps START..END seconds,
  puts it under a big hook, adds the SystemForge end card and calm music.
"""
import os, sys, subprocess, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen, reels, music
from scipy.io import wavfile

src, out, start, end = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4])
x0, y0, x1, y1 = map(int, sys.argv[5:9])
product, hook = sys.argv[9], sys.argv[10]
theme = sys.argv[11] if len(sys.argv) > 11 else 'sage'
W, H, VW = 1080, 1920, 1000
vh = int((y1 - y0) * VW / (x1 - x0)) // 2 * 2
work = tempfile.mkdtemp()

bg, c1, c2 = gen.THEMES[theme]
top = 230
html = reels.frame(theme, f'''<div style="position:relative;text-align:center;{gen.SER};font-size:92px;line-height:1.05;font-weight:700;letter-spacing:-2px">{hook}</div>
<div style="position:absolute;left:40px;top:{top + 330}px;width:{VW + 4}px;height:{vh + 4}px;border-radius:30px;background:#fff;box-shadow:0 30px 70px rgba(46,42,37,.18)"></div>
<div style="position:absolute;left:0;right:0;bottom:110px;display:flex;justify-content:space-between;padding:0 80px;align-items:center">{gen.logo()}
<span style="font-size:30px;font-weight:600;color:{gen.MUT}">{gen.PRODUCTS[product]}</span></div>''')
bgp, endp = os.path.join(work, 'bg.png'), os.path.join(work, 'end.png')
reels.render_png(html, bgp)
reels.render_png(reels.scene_html({'type': 'end'}, theme, product), endp)

dur = end - start
total = dur + 2.6
wav = os.path.join(work, 'm.wav')
wavfile.write(wav, music.SR, music.make(total + 0.5, shift=0 if product == 'fco' else 5, variant=1))
fc = (f"[0:v]crop={x1 - x0}:{y1 - y0}:{x0}:{y0},scale={VW}:{vh},setsar=1[c];"
      f"[1:v][c]overlay=42:{top + 332}:shortest=1,fps=30,format=yuv420p[a];"
      f"[2:v]scale={W}:{H},fps=30,format=yuv420p[e];"
      f"[a][e]xfade=transition=fade:duration=0.3:offset={dur - 0.3:.2f}[v]")
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', str(start), '-t', str(dur), '-i', src,
                '-loop', '1', '-t', str(dur), '-i', bgp, '-loop', '1', '-t', '2.9', '-i', endp, '-i', wav,
                '-filter_complex', fc, '-map', '[v]', '-map', '3:a', '-c:v', 'libx264', '-crf', '20', '-preset', 'medium',
                '-c:a', 'aac', '-b:a', '128k', '-shortest', '-movflags', '+faststart', out], check=True)
print('ok', out)
