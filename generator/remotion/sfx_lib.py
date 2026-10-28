"""SFX track for a pro reel (our own synthesized sounds, no copyright).
whoosh on every cut (starts 15 ms early), click on each UI action (ring), pop on each result badge,
soft impact on the end card.  Levels follow OpenMontage skills/creative/sound-design.md.
Usage: python3 sfx.py specs/<id>.json public/sfx-<id>.wav
"""
import json, sys
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, lfilter

SR = 44100
rng = np.random.default_rng(7)


def bp(x, lo, hi):
    b, a = butter(2, [lo / (SR / 2), hi / (SR / 2)], 'band')
    return lfilter(b, a, x)


def whoosh(d=0.42):
    n = int(SR * d); t = np.arange(n) / SR
    noise = rng.standard_normal(n)
    out = np.zeros(n)
    for i, f in enumerate(np.geomspace(500, 4500, 8)):
        seg = slice(int(i * n / 8), int((i + 1) * n / 8))
        out[seg] = bp(noise, f * 0.7, min(f * 1.4, 20000))[seg]
    env = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 2
    return 0.22 * out * env


def click():
    n = int(SR * 0.05); t = np.arange(n) / SR
    return 0.35 * np.sin(2 * np.pi * 2200 * t) * np.exp(-t * 180) + 0.15 * rng.standard_normal(n) * np.exp(-t * 400)


def pop():
    n = int(SR * 0.16); t = np.arange(n) / SR
    f = 520 + 900 * np.exp(-t * 30)
    return 0.32 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 22)


def impact():
    n = int(SR * 0.6); t = np.arange(n) / SR
    return 0.4 * np.sin(2 * np.pi * 70 * t) * np.exp(-t * 7) + 0.08 * bp(rng.standard_normal(n), 200, 3000) * np.exp(-t * 12)


