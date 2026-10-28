#!/usr/bin/env bash
# universal MP4 for every platform: finalize.sh in.mp4 out.mp4
ffmpeg -y -loglevel error -i "$1" -c:v libx264 -preset slow -profile:v high -level:v 4.1 -pix_fmt yuv420p -color_range tv \
  -b:v 10M -maxrate 12M -bufsize 20M -r 30 -c:a aac -b:a 192k -ar 48000 -ac 2 -movflags +faststart "$2"
