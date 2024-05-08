# sudo apt update
# sudo apt install ffmpeg
ffmpeg -i input.mkv -acodec pcm_s16le -ar 16000 output.wav
