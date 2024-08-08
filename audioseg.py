import os
import sys
from pydub import AudioSegment

def create_audio_segments(transcription_file, source_audio_path, output_path):
    # Ensure the Completed Clips directory exists
    os.makedirs(output_path, exist_ok=True)
    
    with open(transcription_file, 'r') as file:
        lines = file.readlines()
    
    audio_basename = os.path.basename(source_audio_path)
    audio = AudioSegment.from_mp3(source_audio_path)
    
    for i, line in enumerate(lines):
        if line.strip():
            start, end = map(int, line.split(','))
            clip = audio[start:end]
            clip_filename = os.path.join(output_path, f"{os.path.splitext(audio_basename)[0]}_clip{i+1}.mp3")
            clip.export(clip_filename, format="mp3")
            print(f"Exported clip {i+1} for {audio_basename} to {clip_filename}")
    
    print("All files processed.")

if __name__ == "__main__":
    if len(sys.argv) > 3:
        transcription_file = sys.argv[1]
        source_audio_path = sys.argv[2]
        output_path = sys.argv[3]
        create_audio_segments(transcription_file, source_audio_path, output_path)
    else:
        print("Usage: python audioseg.py <transcription_file> <source_audio_path> <output_path>")
