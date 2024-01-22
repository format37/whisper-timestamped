import whisper_timestamped as whisper
import json
import os
import torch
from parse import convert_json_to_text

def main():
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    model = whisper.load_model("large-v3", device=device, download_root='./cache')
    print("Model loaded successfully")
    
    # Iterate files in data
    for filename in sorted(os.listdir("input")):
        print(f"Transcribing {filename}")
        audio = whisper.load_audio(f"input/{filename}")
        # https://github.com/linto-ai/whisper-timestamped/blob/master/whisper_timestamped/transcribe.py
        result = whisper.transcribe(
            model, 
            audio, 
            language="ru"            
            )
        with open(f"output/{filename}.json", "w") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"Transcribed {filename}")
    
    convert_json_to_text()

if __name__ == "__main__":
    main()
