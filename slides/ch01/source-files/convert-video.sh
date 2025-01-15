#!/bin/bash

# Check if input file is provided
if [ -z "$1" ]; then
    echo "Usage: ./convert-video.sh presentation-recording.webm"
    exit 1
fi

# Get input filename without extension
filename=$(basename -- "$1")
filename="${filename%.*}"

# Convert WebM to MP4 with high quality settings
ffmpeg -i "$1" -c:v libx264 -preset slow -crf 22 -c:a aac -b:a 192k "${filename}.mp4"

echo "Conversion complete! Output file: ${filename}.mp4"
