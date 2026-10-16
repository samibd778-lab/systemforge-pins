import os, sys, subprocess, tempfile
sys.path.insert(0, '/home/claude/systemforge-pins/generator')
import gen, reels
src, out, start, end, product, hook = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), sys.argv[5], sys.argv[6]
# two crops: A (top) and B (bottom), raw coords x,y,w,h
A = (1050, 350, 760, 520)
B = (120, 380, 760, 560)
W, H, VW = 1080, 1920, 960
ah = int(A[3] * VW / A[2]) // 2 * 2; bh = int(B[3] * VW / B[2]) // 2 * 2
work = tempfile.mkdtemp(); theme = 'sage'
top = 330; gap = 40
yA = top; yB = top + ah + gap
x = (W - VW) // 2
box = lambda y, h: f'<div style="position:absolute;left:{x-2}px;top:{y-2}px;width:{VW+4}px;height:{h+4}px;border-radius:24px;background:#fff;box-shadow:0 26px 60px rgba(46,42,37,.18)"></div>'
html = reels.frame(theme, f'''<div style="position:absolute;left:0;right:0;top:90px;text-align:center;{gen.SER};font-size:84px;line-height:1.05;font-weight:700;letter-spacing:-2px">{hook}</div>
{box(yA, ah)}{box(yB, bh)}
<div style="position:absolute;left:0;right:0;bottom:90px;display:flex;justify-content:space-between;padding:0 80px;align-items:center">{gen.logo()}
<span style="font-size:30px;font-weight:600;color:{gen.MUT}">{gen.PRODUCTS[product]}</span></div>''')
bgp, endp = os.path.join(work, 'bg.png'), os.path.join(work, 'end.png')
reels.render_png(html, bgp)
reels.render_png(reels.scene_html({'type': 'end'}, theme, product), endp)
dur = end - start
fc = (f"[0:v]split[s1][s2];[s1]crop={A[2]}:{A[3]}:{A[0]}:{A[1]},scale={VW}:{ah},setsar=1[a];"
      f"[s2]crop={B[2]}:{B[3]}:{B[0]}:{B[1]},scale={VW}:{bh},setsar=1[b];"
      f"[1:v][a]overlay={x}:{yA}:shortest=1[t];[t][b]overlay={x}:{yB},fps=30,format=yuv420p[m];"
      f"[2:v]scale={W}:{H},fps=30,format=yuv420p[e];[m][e]xfade=transition=fade:duration=0.3:offset={dur-0.3:.2f}[v]")
subprocess.run(['ffmpeg','-y','-loglevel','error','-ss',str(start),'-t',str(dur),'-i',src,'-loop','1','-t',str(dur),'-i',bgp,
  '-loop','1','-t','2.6','-i',endp,'-filter_complex',fc,'-map','[v]','-an','-c:v','libx264','-crf','20','-preset','medium','-movflags','+faststart',out],check=True)
print('ok', out, ah, bh)
