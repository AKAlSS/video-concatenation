import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
import speech_recognition as sr
from tqdm import tqdm

"""
transcribe.py
This script is used to transcribe a podcast audio file into text. The transcription
is then used to highlight key takeaways and practical use cases for further processing.
"""

# Define paths
source_audio_path = os.path.expanduser('~/Desktop/BetterDaily/Source Audio')
completed_transcription_path = os.path.expanduser('~/Desktop/BetterDaily/Completed Transcriptions')

# Ensure the Completed Transcriptions directory exists
os.makedirs(completed_transcription_path, exist_ok=True)

# Initialize recognizer
r = sr.Recognizer()

# Process each audio file in the source directory
for audio_filename in os.listdir(source_audio_path):
    if audio_filename.endswith('.mp3'):
        audio_file_path = os.path.join(source_audio_path, audio_filename)
        wav_file_path = os.path.join(source_audio_path, os.path.splitext(audio_filename)[0] + '.wav')
        transcription_file_path = os.path.join(completed_transcription_path, os.path.splitext(audio_filename)[0] + '.txt')

        print(f"Processing file: {audio_filename}")

        # Convert mp3 file to wav
        try:
            print("Converting MP3 to WAV...")
            audio = AudioSegment.from_mp3(audio_file_path)
            audio.export(wav_file_path, format="wav")
        except Exception as e:
            print(f"An error occurred while converting {audio_filename} to WAV: {e}")
            continue

        # Load the audio file
        try:
            print("Loading the WAV file...")
            audio = AudioSegment.from_wav(wav_file_path)
        except Exception as e:
            print(f"An error occurred while loading the WAV file for {audio_filename}: {e}")
            continue

        # Split audio where silence is detected
        try:
            print("Splitting the audio into chunks based on silence...")
            chunks = split_on_silence(
                audio,
                min_silence_len=1000,
                silence_thresh=audio.dBFS-14,
                keep_silence=500
            )
        except Exception as e:
            print(f"An error occurred while splitting {audio_filename} into chunks: {e}")
            continue

        # Process each chunk
        full_transcription = []
        chunk_count = len(chunks)
        print(f"Processing {chunk_count} chunks...")

        for i, chunk in enumerate(tqdm(chunks, desc=f"Processing {audio_filename}")):
            chunk_silent = AudioSegment.silent(duration=10)
            audio_chunk = chunk_silent + chunk + chunk_silent
            chunk_filename = os.path.join(source_audio_path, f"chunk{i}.wav")
            audio_chunk.export(chunk_filename, format="wav")

            with sr.AudioFile(chunk_filename) as source:
                audio_data = r.record(source)
                try:
                    text = r.recognize_google(audio_data)
                    full_transcription.append(text)
                except sr.UnknownValueError:
                    print(f"Chunk {i+1}: Google Speech Recognition could not understand the audio.")
                except sr.RequestError as e:
                    print(f"Chunk {i+1}: Could not request results from Google Speech Recognition service; {e}")

            # Optionally, delete the chunk file to save space
            os.remove(chunk_filename)

        # Save the full transcription to a text file
        with open(transcription_file_path, "w") as file:
            file.write(" ".join(full_transcription))

        print(f"Transcription completed for {audio_filename}. Check the {transcription_file_path} file.")

        # Remove the intermediate WAV file
        os.remove(wav_file_path)

print("All files processed.")
