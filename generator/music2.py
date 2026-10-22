"""SystemForge music library: 8 distinct synthesized styles (our own music, no copyright).

Each video gets its own track (style + key + seed), so the same sound never repeats back to back.

Usage: python3 generator/music2.py out.wav seconds style [key_shift] [seed]
       styles: 0 lofi, 1 lofi-b, 2 ambient, 3 pluck-pop, 4 marimba, 5 felt-piano, 6 chill-house, 7 guitar
"""
import sys
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, lfilter

SR = 44100
STYLES = ['lofi', 'lofi-b', 'ambient', 'pluck-pop', 'marimba', 'felt-piano', 'chill-house', 'guitar']


def midi(n):
    return 440.0 * 2 ** ((n - 69) / 12)


def lp(x, cut, order=2):
    b, a = butter(order, min(cut, SR / 2 - 100) / (SR / 2))
    return lfilter(b, a, x)


def hp(x, cut):
    b, a = butter(2, cut / (SR / 2), 'high')
    return lfilter(b, a, x)


def tt(d):
    return np.arange(int(SR * d)) / SR


# ---------- instruments ----------
def epiano(f, d, v=0.15):
    t = tt(d)
    env = np.exp(-t * 2.2) * (1 - np.exp(-t * 80))
    s = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(4 * np.pi * f * t) * np.exp(-t * 4) + 0.08 * np.sin(6 * np.pi * f * t) * np.exp(-t * 6)
    return v * s * env * (1 + 0.06 * np.sin(2 * np.pi * 4.5 * t))


def felt(f, d, v=0.16):
    t = tt(d)
    env = np.exp(-t * 1.4) * (1 - np.exp(-t * 200))
    s = sum(np.sin(2 * np.pi * f * k * t) * np.exp(-t * k * 1.5) / k ** 1.6 for k in range(1, 6))
    return v * lp(s * env, 2500)


def pad(f, d, v=0.05, rng=None):
    t = tt(d)
    s = np.zeros_like(t)
    for det in (-0.12, 0.0, 0.11):
        ph = 2 * np.pi * f * (1 + det / 100) * t
        s += (2 * ((ph / (2 * np.pi)) % 1) - 1)  # saw
    att = min(1.5, d / 3)
    env = np.minimum(1, t / att) * np.minimum(1, (d - t) / att)
    return v * lp(s, 900 + 300 * np.sin(0.3 * f)) * env


def bell(f, d, v=0.05):
    t = tt(d)
    s = np.sin(2 * np.pi * f * t + 1.8 * np.sin(2 * np.pi * f * 3.5 * t) * np.exp(-t * 3))
    return v * s * np.exp(-t * 2.5)


def marimba(f, d, v=0.2):
    t = tt(min(d, 1.2))
    s = np.sin(2 * np.pi * f * t) * np.exp(-t * 6) + 0.25 * np.sin(2 * np.pi * f * 4 * t) * np.exp(-t * 30)
    return v * s * (1 - np.exp(-t * 400))


def pluck(f, d, v=0.22, bright=0.5, rng=None):
    """Karplus-Strong string."""
    n = int(SR * d)
    p = max(2, int(SR / f))
    rng = rng or np.random.default_rng(0)
    buf = lp(rng.uniform(-1, 1, p), 2000 + 6000 * bright)
    out = np.zeros(n)
    reps = n // p + 1
    cur = buf.copy()
    for r in range(reps):
        a, b = r * p, min(n, (r + 1) * p)
        out[a:b] = cur[:b - a]
        cur = 0.996 * 0.5 * (cur + np.roll(cur, 1))
    return v * out


def kick(v=0.5, d=0.35):
    t = tt(d)
    f = 110 * np.exp(-t * 18) + 45
    return v * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)


def hat(rng, v=0.05, d=0.06):
    nz = hp(rng.standard_normal(int(SR * d)), 7000)
    return v * nz * np.exp(-tt(d) * 60)


def snare(rng, v=0.12, d=0.2):
    t = tt(d)
    return v * (hp(rng.standard_normal(len(t)), 1500) * np.exp(-t * 18) + 0.4 * np.sin(2 * np.pi * 190 * t) * np.exp(-t * 25))


def shaker(rng, v=0.03, d=0.09):
    t = tt(d)
    return v * hp(rng.standard_normal(len(t)), 5000) * np.sin(np.pi * t / d)


def bass(f, d, v=0.25):
    t = tt(d)
    return v * lp(np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t), 400) * np.minimum(1, t * 50) * np.exp(-t * 1.2)


# ---------- song ----------
PROGS = [
    [[48, 55, 59, 64], [45, 52, 55, 60], [41, 48, 52, 57], [43, 50, 53, 59]],
    [[41, 48, 52, 57], [43, 50, 55, 59], [40, 47, 52, 55], [45, 52, 55, 60]],
    [[45, 52, 55, 60], [41, 48, 53, 57], [48, 55, 60, 64], [43, 50, 55, 59]],
    [[48, 52, 55, 59], [43, 47, 50, 55], [45, 48, 52, 57], [41, 45, 48, 52]],
]


class Mix:
    def __init__(self, secs):
        self.n = int(SR * secs)
        self.L, self.R = np.zeros(self.n), np.zeros(self.n)

    def add(self, sig, start, pan=0.0):
        i = int(start * SR)
        if i >= self.n:
            return
        j = min(self.n, i + len(sig))
        self.L[i:j] += sig[:j - i] * (1 - max(0, pan))
        self.R[i:j] += sig[:j - i] * (1 + min(0, pan))


def make(secs, style=0, shift=0, seed=0):
    rng = np.random.default_rng(1000 + seed * 17 + style)
    m = Mix(secs)
    st = STYLES[style % len(STYLES)]
    bpm = {'lofi': 84, 'lofi-b': 78, 'ambient': 60, 'pluck-pop': 104, 'marimba': 112,
           'felt-piano': 72, 'chill-house': 118, 'guitar': 92}[st]
    beat = 60 / bpm
    bar = 4 * beat
    prog = PROGS[(style + seed) % len(PROGS)]
    t, k = 0.0, 0
    while t < secs:
        ch = [x + shift for x in prog[k % 4]]
        if st in ('lofi', 'lofi-b'):
            for i, nt in enumerate(ch):
                m.add(epiano(midi(nt + 12), bar * 1.1, 0.10), t + i * 0.03, 0.3 if i % 2 else -0.3)
            m.add(epiano(midi(ch[0] - 12), bar, 0.2), t)
            for b in range(4):
                if b in (0, 2) or (st == 'lofi-b' and b == 3 and rng.random() < .5):
                    m.add(kick(0.35), t + b * beat)
                if b in (1, 3):
                    m.add(snare(rng, 0.035), t + b * beat + 0.02)
                    if rng.random() < .7:
                        m.add(epiano(midi(rng.choice(ch[1:]) + 24), beat * 1.5, 0.045), t + (b + .5) * beat, 0.4)
                m.add(hat(rng, 0.022), t + (b + .5) * beat + rng.uniform(0, .02), -0.2)
        elif st == 'ambient':
            for i, nt in enumerate(ch):
                m.add(pad(midi(nt), bar + 1.5, 0.035), t, (i - 1.5) / 3)
            m.add(pad(midi(ch[0] - 12), bar + 1.5, 0.04), t)
            for b in range(0, 8):
                if rng.random() < 0.45:
                    m.add(bell(midi(rng.choice(ch) + 24), 2.5, 0.035), t + b * beat / 2, rng.uniform(-.6, .6))
        elif st == 'pluck-pop':
            arp = ch + [ch[2] + 12, ch[1] + 12]
            for s16 in range(16):
                nt = arp[(s16 * 3) % len(arp)] + 12
                m.add(pluck(midi(nt), 0.6, 0.13, 0.3, rng), t + s16 * beat / 4, 0.35 if s16 % 2 else -0.35)
            m.add(bass(midi(ch[0] - 12), bar, 0.28), t)
            for b in range(4):
                m.add(kick(0.42), t + b * beat) if b in (0, 2) else m.add(snare(rng, 0.06), t + b * beat)
                m.add(hat(rng, 0.02), t + (b + .5) * beat)
        elif st == 'marimba':
            pat = [0, 2, 1, 3, 2, 1, 3, 2]
            for e in range(8):
                m.add(marimba(midi(ch[pat[e]] + 12), beat, 0.17), t + e * beat / 2, -0.3 if e % 2 else 0.3)
            m.add(marimba(midi(ch[0]), bar, 0.18), t)
            for e in range(8):
                m.add(shaker(rng, 0.025), t + e * beat / 2)
            m.add(kick(0.3), t)
            m.add(kick(0.25), t + 2.5 * beat)
        elif st == 'felt-piano':
            m.add(felt(midi(ch[0] - 12), bar * 1.3, 0.2), t)
            pat = [1, 2, 3, 2, 1, 2, 3, 2]
            for e in range(8):
                m.add(felt(midi(ch[pat[e]]), beat * 2, 0.11), t + e * beat / 2, (e % 3 - 1) * .3)
            if rng.random() < .7:
                m.add(felt(midi(rng.choice(ch[1:]) + 12), beat * 3, 0.07), t + 2 * beat, 0.4)
        elif st == 'chill-house':
            for b in range(4):
                m.add(kick(0.4), t + b * beat)
                m.add(hat(rng, 0.03), t + (b + .5) * beat, 0.3)
                if b in (1, 3):
                    m.add(snare(rng, 0.07), t + b * beat)
            for off in (0.5, 1.5, 2.75):
                for i, nt in enumerate(ch[1:]):
                    m.add(epiano(midi(nt + 12), beat * 0.6, 0.07), t + off * beat, (i - 1) * .4)
            for b in range(4):
                m.add(bass(midi(ch[0] - 12), beat * 0.9, 0.24), t + (b + .5) * beat)
            m.add(pad(midi(ch[2]), bar, 0.02), t)
        elif st == 'guitar':
            strums = [0, 1.5, 2, 3]
            for s in strums:
                for i, nt in enumerate(ch):
                    m.add(pluck(midi(nt), 1.2, 0.09, 0.15, rng), t + s * beat + i * 0.012, (i - 1.5) / 4)
            m.add(bass(midi(ch[0] - 12), bar, 0.2), t)
            for e in range(8):
                m.add(shaker(rng, 0.02 if e % 2 else 0.035), t + e * beat / 2)
            m.add(kick(0.25), t)
            m.add(snare(rng, 0.05), t + 2 * beat)
        t += bar
        k += 1
    L, R = m.L, m.R
    if st in ('lofi', 'lofi-b'):
        nz = lp(rng.standard_normal(m.n), 2500) * 0.002
        L, R = lp(L + nz, 7000), lp(R + nz, 7000)
    # simple room reverb (comb echoes)
    for dl, g in ((0.031, .18), (0.047, .14), (0.071, .1), (0.113, .07)):
        d = int(dl * SR)
        L[d:] += g * R[:-d]
        R[d:] += g * L[:-d]
    L, R = hp(L, 35), hp(R, 35)
    fi, fo = int(SR * 0.25), int(SR * 1.2)
    for ch in (L, R):
        ch[:fi] *= np.linspace(0, 1, fi)
        ch[-fo:] *= np.linspace(1, 0, fo)
    stereo = np.stack([L, R], 1)
    stereo = stereo / np.max(np.abs(stereo)) * 0.85
    return (stereo * 32767).astype(np.int16)


def pick(index, video_id):
    """Style for the n-th video in the rotation: cycles through all 8, key and seed from the id."""
    h = sum(map(ord, video_id))
    return index % len(STYLES), [0, 2, 5, -3, 7, -2][h % 6], h % 97


if __name__ == '__main__':
    out, secs, style = sys.argv[1], float(sys.argv[2]), int(sys.argv[3])
    shift = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    seed = int(sys.argv[5]) if len(sys.argv) > 5 else 0
    wavfile.write(out, SR, make(secs, style, shift, seed))


def write_for(video_id, seconds, path):
    """Write the track for a video: style follows its position in videos.json (so neighbours differ)."""
    import json, os
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    try:
        ids = [v['id'] for v in json.load(open(os.path.join(root, 'videos.json')))['videos']]
        idx = ids.index(video_id) if video_id in ids else len(ids) + sum(map(ord, video_id))
    except Exception:
        idx = sum(map(ord, video_id))
    style, shift, seed = pick(idx, video_id)
    wavfile.write(path, SR, make(seconds, style, shift, seed))
    return STYLES[style]
