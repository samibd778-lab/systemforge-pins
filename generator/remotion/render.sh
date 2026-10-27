#!/usr/bin/env bash
# Render a SystemForge reel from specs/<id>.json.
#   ./render.sh <id> [still <frame>]
# Needs public/<spec.video> (the screen recording) next to the fonts.
# Writes ../../videos/<id>.mp4 (with our music) and ../../clips/<id>-nosound.mp4 (for TikTok).
set -euo pipefail
cd "$(dirname "$0")"
ID="$1"; SPEC="specs/$ID.json"
COMP=$(python3 -c "import json;print('ReelPro' if json.load(open('$SPEC')).get('style')=='pro' else 'Reel')")
BROWSER="${BROWSER:-/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell}"
[ -d node_modules ] || npm install --silent
mkdir -p out
if [ "${2:-}" = "still" ]; then
  npx remotion still src/index.ts "$COMP" "out/$ID-${3:-60}.png" --props="$SPEC" --frame="${3:-60}" --browser-executable="$BROWSER" --log=error
  echo "out/$ID-${3:-60}.png"; exit 0
fi
# our own synthesized music, long enough for the reel
SECS=$(python3 -c "import json;d=json.load(open('$SPEC'));print(int(sum(s['dur'] for s in d['segments'])+6))")
python3 - "$ID" "$SECS" <<'EOF'
import sys, os
sys.path.insert(0, os.path.abspath('..'))
import music2
music2.write_for(sys.argv[1], float(sys.argv[2]), 'public/music.wav')
EOF
[ "$COMP" = ReelPro ] && python3 sfx.py "$SPEC" "public/sfx-$ID.wav"
npx remotion render src/index.ts "$COMP" "out/$ID.mp4" --props="$SPEC" --codec=h264 --crf=16 --browser-executable="$BROWSER" --log=error
# universal MP4: yuv420p (plays on Windows/Mac/phones), High@4.1, 10 Mbps (platforms downgrade < 5 Mbps), AAC 48k, faststart
ffmpeg -y -loglevel error -i "out/$ID.mp4" -c:v libx264 -preset slow -profile:v high -level:v 4.1 -pix_fmt yuv420p -color_range tv \
  -b:v 10M -maxrate 12M -bufsize 20M -r 30 -c:a aac -b:a 192k -ar 48000 -ac 2 -movflags +faststart "out/$ID-web.mp4"
mv "out/$ID-web.mp4" "out/$ID.mp4"
cp "out/$ID.mp4" "../../videos/$ID.mp4"
mkdir -p ../../clips
ffmpeg -y -loglevel error -i "out/$ID.mp4" -c:v copy -an "../../clips/$ID-nosound.mp4"
ffmpeg -y -loglevel error -ss 4.5 -i "out/$ID.mp4" -frames:v 1 -q:v 2 "../../videos/$ID-cover.jpg"
echo "done: videos/$ID.mp4 clips/$ID-nosound.mp4"
