import whisper_timestamped as whisper
import json
import os
import torch
from parse import convert_json_to_text
from pydub import AudioSegment
import datetime

def main():
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    model = whisper.load_model("large-v3", device=device, download_root='./cache')
    print("Model loaded successfully")

    # Remove all files in output folder
    for filename in os.listdir("output"):
        file_path = os.path.join("output", filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)
    
    # Iterate files in data
    for filename in sorted(os.listdir("input")):
        print(f"Transcribing {filename}")
        use_chunks = 0
        start_time = datetime.datetime.now()
        if not use_chunks:

            # Load the audio file
            file_path = f"input/{filename}"
            audio = AudioSegment.from_file(file_path)

            # Get the sample rate
            sample_rate = audio.frame_rate
            print("Sample rate:", sample_rate)
            # Convert to 16KHz
            if sample_rate != 16000:
                audio = audio.set_frame_rate(16000)
            print("Sample rate:", audio.frame_rate)

            # Export to ./temp folder
            audio.export(f"./temp/{filename}", format="wav")

            # audio = whisper.load_audio(f"input/{filename}")
            audio = whisper.load_audio(f"./temp/{filename}")

            # https://github.com/linto-ai/whisper-timestamped/blob/master/whisper_timestamped/transcribe.py
            result = whisper.transcribe(
                model, 
                audio,
                vad = 'auditok',
                remove_empty_words = True,
                temperature=0.8,
                # language="ru",
                verbose = False,
                )
            
            # naive_approach = True"""
            # 
            with open(f"output/{filename}.json", "w") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"Transcribed {filename}")

            # Delete the temporary chunk file
            os.remove(f"./temp/{filename}")
        
        else:
            # Load the audio file
            file_path = f"input/{filename}"
            audio = AudioSegment.from_file(file_path)

            # Get the sample rate
            sample_rate = audio.frame_rate
            print("Sample rate:", sample_rate)
            # Convert to 16KHz
            if sample_rate != 16000:
                audio = audio.set_frame_rate(16000)
                # audio.export(file_path, format="wav")
            print("Sample rate:", audio.frame_rate)

            # Define chunk duration in milliseconds
            chunk_duration = 300*1000 # 10 minutes

            # Iterate over the audio file in chunks
            for i, chunk_start in enumerate(range(0, len(audio), chunk_duration)):
                chunk_end = chunk_start + chunk_duration

                # Extract the chunk of audio
                chunk = audio[chunk_start:chunk_end]

                # Save the chunk to a temporary file
                chunk_file_path = f"./temp/filename_{i}.wav"
                chunk.export(chunk_file_path, format="wav")

                # Transcribe the chunk
                try:
                    result = whisper.transcribe(
                    model,
                    chunk_file_path,
                    vad = 'auditok'
                )
                    #compute_word_confidence = False,
                # naive_approach = True
                except Exception as e:
                    print(f'Error: {e}')
                    continue
                # language="ru"

                # Delete the temporary chunk file
                os.remove(chunk_file_path)

                # Save the transcription result
                result_file_path = f"output/{filename}_{i}.json"
                with open(result_file_path, "w") as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
        
        end_time = datetime.datetime.now()
        print(f"Transcribed {filename} in {end_time - start_time} seconds")

    convert_json_to_text()

if __name__ == "__main__":
    main()
