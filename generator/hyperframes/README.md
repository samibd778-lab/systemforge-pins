# HyperFrames reels

Each folder is one reel (HTML + GSAP rendered to video).
`assets/rec.mp4` is the screen recording and is not committed (too big): copy it from `generator/remotion/public/rec-n*.mp4`
(c03 = rec-n3, b02 = rec-n5, f04 = rec-n2).

Render:
```
export HYPERFRAMES_BROWSER_PATH=/opt/pw-browsers/chromium-1194/chrome-linux/chrome
npx --yes hyperframes@0.8.209 check --json
npx --yes hyperframes@0.8.209 render . -q high -o renders/video.mp4
../../remotion/finalize.sh renders/video.mp4 ../../../videos/<id>.mp4
```
Music + SFX: `python3 ../../remotion/mixaudio.py assets/mix.wav 22 <style> <seed> 'whoosh:..' 'pop:..' 'click:..' 'impact:..'`
