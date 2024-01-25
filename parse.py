import os
import json

def convert_json_to_text():
    data = []
    speakers = []

    # Read json files from ./output folder
    for filename in sorted(os.listdir("output")):
        print(f"Reading {filename}")
        speaker_name = filename.replace('.json', '')
        speakers.append(speaker_name)
        with open(f"output/{filename}") as file:
            data.append(json.load(file))

    # Combining segments from all JSON files  
    combined_segments = []
    for speaker_data in data:
        combined_segments.extend(speaker_data['segments'])
        
    # Sort segments    
    sorted_combined_segments = sorted(combined_segments, key=lambda x: x['start'])

    # Prepare conversation text
    conversation_text = []
    current_speaker = None
    speaker_text = []
    
    for segment in sorted_combined_segments:
        speaker = speakers[data.index(next(d for d in data if segment in d['segments']))]        
        if speaker != current_speaker:
            if current_speaker:
                conversation_text.append(f"- {current_speaker}: {' '.join(speaker_text)}")
            current_speaker = speaker
            speaker_text = []
        speaker_text.append(segment['text'])

    if current_speaker:
        conversation_text.append(f"- {current_speaker}: {' '.join(speaker_text)}")

    # Output to file
    conversation_str = '\n'.join(conversation_text)  
    with open('transcript.txt', 'w') as file:
        file.write(conversation_str)

def main():
    convert_json_to_text()    

if __name__ == '__main__':
    main()