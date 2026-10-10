"""Calm lo-fi background loop, synthesized (no copyright). Writes a 44.1kHz stereo WAV.

Usage: python3 generator/music.py out.wav seconds [semitone_shift] [variant]
"""
import sys
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, lfilter

SR = 44100
BPM = 84
BEAT = 60 / BPM


def midi(n):
    return 440.0 * 2 ** ((n - 69) / 12)


def lowpass(x, cut):
    b, a = butter(2, cut / (SR / 2))
    return lfilter(b, a, x)


def epiano(freq, dur, vel=0.18):
    t = np.arange(int(SR * dur)) / SR
    env = np.exp(-t * 2.2) * (1 - np.exp(-t * 80))
    tone = (np.sin(2 * np.pi * freq * t) + 0.35 * np.sin(2 * np.pi * 2 * freq * t) * np.exp(-t * 4)
            + 0.08 * np.sin(2 * np.pi * 3 * freq * t) * np.exp(-t * 6))
    trem = 1 + 0.06 * np.sin(2 * np.pi * 4.5 * t)
    return vel * tone * env * trem


def kick(dur=0.35):
    t = np.arange(int(SR * dur)) / SR
    f = 110 * np.exp(-t * 18) + 45
    return 0.5 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)


def hat(rng, dur=0.06):
    n = rng.standard_normal(int(SR * dur))
    n = n - lowpass(n, 6000)
    return 0.05 * n * np.exp(-np.arange(len(n)) / SR * 60)


def add(buf, sig, start):
    i = int(start * SR)
    j = min(len(buf), i + len(sig))
    if i < len(buf):
        buf[i:j] += sig[:j - i]


def make(seconds, shift=0, variant=0):
    rng = np.random.default_rng(7 + variant)
    n = int(SR * seconds)
    L, R = np.zeros(n), np.zeros(n)
    progs = [
        [[48, 55, 59, 64], [45, 52, 55, 60], [41, 48, 52, 57], [43, 50, 53, 59]],  # Cmaj7 Am7 Fmaj7 G7sus-ish
        [[41, 48, 52, 57], [43, 50, 55, 59], [40, 47, 52, 55], [45, 52, 55, 60]],  # Fmaj7 G Em7 Am7
    ]
    prog = progs[variant % 2]
    bar = 4 * BEAT
    t = 0.0
    k = 0
    while t < seconds:
        chord = [x + shift for x in prog[k % 4]]
        for i, note in enumerate(chord):  # gently rolled chord
            s = epiano(midi(note + 12), bar * 1.1, 0.10)
            add(L, s * (0.8 if i % 2 else 1.0), t + i * 0.025)
            add(R, s * (1.0 if i % 2 else 0.8), t + i * 0.025)
        bass = epiano(midi(chord[0] - 12), bar, 0.22)
        add(L, bass, t); add(R, bass, t)
        for b in range(4):  # little melody on beats 2 and 4
            if b in (1, 3) and rng.random() < 0.8:
                m = epiano(midi(rng.choice(chord[1:]) + 24), BEAT * 1.5, 0.05)
                add(L, m * 0.7, t + b * BEAT + 0.5 * BEAT); add(R, m, t + b * BEAT + 0.5 * BEAT)
            if b in (0, 2):
                kk = kick(); add(L, kk * 0.6, t + b * BEAT); add(R, kk * 0.6, t + b * BEAT)
            hh = hat(rng); add(L, hh, t + b * BEAT + BEAT / 2); add(R, hh * 0.8, t + b * BEAT + BEAT / 2)
        t += bar; k += 1
    noise = lowpass(rng.standard_normal(n), 3000) * 0.004  # soft vinyl hiss
    L, R = lowpass(L + noise, 7000), lowpass(R + noise, 7000)
    fade = int(SR * 1.2)
    for ch in (L, R):
        ch[:int(SR * 0.3)] *= np.linspace(0, 1, int(SR * 0.3))
        ch[-fade:] *= np.linspace(1, 0, fade)
    st = np.stack([L, R], 1)
    st = st / np.max(np.abs(st)) * 0.7
    return (st * 32767).astype(np.int16)


if __name__ == '__main__':
    out, secs = sys.argv[1], float(sys.argv[2])
    shift = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    var = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    wavfile.write(out, SR, make(secs, shift, var))
