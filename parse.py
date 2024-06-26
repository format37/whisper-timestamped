import os
import json
from datetime import timedelta

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

def format_time(seconds):
    td = timedelta(seconds=seconds)
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = td.microseconds // 1000
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

def merge_short_captions(segments, min_words=10):
    merged_segments = []
    current_segment = None

    for segment in segments:
        if current_segment is None:
            current_segment = segment.copy()
        else:
            words_count = len(current_segment['text'].split())
            if words_count < min_words:
                # Merge with the next segment
                current_segment['end'] = segment['end']
                current_segment['text'] += ' ' + segment['text']
            else:
                # Add the current segment to the result and start a new one
                merged_segments.append(current_segment)
                current_segment = segment.copy()

    # Add the last segment
    if current_segment is not None:
        merged_segments.append(current_segment)

    return merged_segments

def generate_srt_from_multiple_jsons(output_folder, srt_output_file, min_words=10):
    data = []

    # Read json files from ./output folder
    for filename in sorted(os.listdir(output_folder)):
        if filename.endswith('.json'):
            print(f"Reading {filename}")
            with open(os.path.join(output_folder, filename)) as file:
                data.append(json.load(file))

    # Combining segments from all JSON files  
    combined_segments = []
    for speaker_data in data:
        combined_segments.extend(speaker_data['segments'])
        
    # Sort segments    
    sorted_combined_segments = sorted(combined_segments, key=lambda x: x['start'])

    # Merge short captions
    merged_segments = merge_short_captions(sorted_combined_segments, min_words)

    # Generate SRT file
    with open(srt_output_file, 'w', encoding='utf-8') as f:
        for i, segment in enumerate(merged_segments, 1):
            start_time = format_time(segment['start'])
            end_time = format_time(segment['end'])
            text = segment['text'].strip()

            f.write(f"{i}\n")
            f.write(f"{start_time} --> {end_time}\n")
            f.write(f"{text}\n\n")

def main():
    convert_json_to_text()    
    # Execute the modified function and get the names of the files created
    created_files = convert_json_to_text_and_save()
    
    # Generate youtube captions SRT file
    output_folder = "output"
    srt_output_file = "captions.srt"
    min_words = 10  # Minimum number of words for a caption
    generate_srt_from_multiple_jsons(output_folder, srt_output_file, min_words)


if __name__ == '__main__':
    main()