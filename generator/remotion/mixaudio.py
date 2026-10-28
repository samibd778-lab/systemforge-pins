"""Music bed + SFX in one WAV (our own synthesized sounds).
Usage: python3 mixaudio.py out.wav seconds music_style seed 'whoosh:2.7,7.7' 'pop:0.6,1.0' 'click:6.5' 'impact:19.2'
music styles (generator/music2.py): 0 lofi 1 lofi-b 2 ambient 3 pluck-pop 4 marimba 5 felt-piano 6 chill-house 7 guitar
"""
import sys, os, importlib.util
import numpy as np
from scipy.io import wavfile
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(here))
import music2
spec = importlib.util.spec_from_file_location('sfxmod', os.path.join(here, 'sfx_lib.py'))
fx = importlib.util.module_from_spec(spec); spec.loader.exec_module(fx)
SR = 44100
out, secs, style, seed = sys.argv[1], float(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
m = music2.make(secs, style, 0, seed).astype(float)
if m.ndim > 1: m = m.mean(axis=1)
m = m / (np.abs(m).max() + 1e-9) * 0.30
n = int(secs * SR); mix = np.zeros(n); mix[:min(n, len(m))] += m[:n]
fade = int(0.8 * SR); mix[n - fade:] *= np.linspace(1, 0, fade)
for arg in sys.argv[5:]:
    kind, times = arg.split(':')
    for t in times.split(','):
        snd = getattr(fx, kind)(); i = max(0, int(float(t) * SR)); mix[i:i + len(snd)] += snd[:n - i]
mix = np.clip(mix, -0.95, 0.95)
wavfile.write(out, SR, (mix * 32767).astype(np.int16)); print('mix', out, secs)
