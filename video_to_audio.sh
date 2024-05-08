#!/bin/bash

# Check if the input file is provided
if [ $# -eq 0 ]; then
    echo "Please provide the path to the MKV file."
    exit 1
fi

# Get the input file path
input_file="$1"

# Check if the input file exists
if [ ! -f "$input_file" ]; then
    echo "File '$input_file' does not exist."
    exit 1
fi

# Get the base name of the input file (without the extension)
base_name=$(basename "$input_file" .mkv)

# Set the output file name
output_file="${base_name}_audio.mp3"

# Extract the audio using ffmpeg
ffmpeg -i "$input_file" -vn -acodec libmp3lame -b:a 192k "$output_file"

echo "Audio extraction complete. Output file: $output_file"
