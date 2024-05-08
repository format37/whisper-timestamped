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


def convert_json_to_text_and_save():
    data = []
    speakers = {}

    # Read json files from ./output folder
    for filename in sorted(os.listdir("output")):
        if filename.endswith('.json'):
            print(f"Reading {filename}")
            speaker_name = filename.replace('.json', '')
            with open(f"output/{filename}") as file:
                speaker_data = json.load(file)
                data.append(speaker_data['segments'])
                # Initialize speaker text storage
                speakers[speaker_name] = []

    # Combine and sort segments
    combined_segments = [segment for speaker_segments in data for segment in speaker_segments]
    sorted_combined_segments = sorted(combined_segments, key=lambda x: x['start'])

    # Process and save text for each speaker
    for segment in sorted_combined_segments:
        for speaker_name in speakers:
            if segment in data[list(speakers.keys()).index(speaker_name)]:
                speakers[speaker_name].append(segment['text'])
                break

    # Write to files
    for speaker_name, texts in speakers.items():
        with open(f'{speaker_name}.txt', 'w') as file:
            file.write(' '.join(texts))

    return list(speakers.keys())

def main():
    convert_json_to_text()    
    # Execute the modified function and get the names of the files created
    created_files = convert_json_to_text_and_save()


if __name__ == '__main__':
    main()