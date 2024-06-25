import os
from pydub import AudioSegment

"""
audioseg.py
This script takes the transcription of a podcast along with highlighted key points and
timestamps to create audio segments. The audio segments correspond to the key takeaways
and practical use cases highlighted in the transcription.
"""

# Define paths
source_audio_path = os.path.expanduser('~/Desktop/BetterDaily/Source Audio')
completed_clips_path = os.path.expanduser('~/Desktop/BetterDaily/Completed Clips')
segments_file_path = os.path.expanduser('~/Desktop/BetterDaily/segments.txt')

# Ensure the Completed Clips directory exists
os.makedirs(completed_clips_path, exist_ok=True)

# Function to read segments from the file
def read_segments(file_path):
    segments = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
        current_file = None
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line.endswith('.mp3'):
                current_file = line
                segments[current_file] = []
            else:
                start, end = map(int, line.split(','))
                segments[current_file].append((start, end))
    return segments

# Read the segments from the file
identified_segments = read_segments(segments_file_path)

# Process each audio file in the source directory
for audio_filename in os.listdir(source_audio_path):
    if audio_filename.endswith('.mp3'):
        audio_file_path = os.path.join(source_audio_path, audio_filename)
        print(f"Processing file: {audio_filename}")

        # Load the audio file
        try:
            print("Loading the MP3 file...")
            audio = AudioSegment.from_mp3(audio_file_path)
        except Exception as e:
            print(f"An error occurred while loading the MP3 file for {audio_filename}: {e}")
            continue

        # Check if we have identified segments for this file
        if audio_filename in identified_segments:
            segments = identified_segments[audio_filename]
            for idx, (start, end) in enumerate(segments):
                clip = audio[start:end]
                clip_filename = os.path.join(completed_clips_path, f"{os.path.splitext(audio_filename)[0]}_clip{idx+1}.mp3")
                clip.export(clip_filename, format="mp3")
                print(f"Exported clip {idx+1} for {audio_filename} to {clip_filename}")

print("All files processed.")
