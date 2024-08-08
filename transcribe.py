import os
import sys
from pydub import AudioSegment
from pydub.silence import split_on_silence
import speech_recognition as sr
from tqdm import tqdm

def transcribe_audio(audio_file_path, output_path):
    # Ensure the output directory exists
    os.makedirs(output_path, exist_ok=True)
    
    audio_basename = os.path.basename(audio_file_path)
    wav_file_path = os.path.join(output_path, os.path.splitext(audio_basename)[0] + '.wav')
    transcription_file_path = os.path.join(output_path, os.path.splitext(audio_basename)[0] + '.txt')

    # Convert mp3 file to wav
    audio = AudioSegment.from_mp3(audio_file_path)
    audio.export(wav_file_path, format="wav")

    # Load the audio file
    audio = AudioSegment.from_wav(wav_file_path)

    # Split audio where silence is detected
    chunks = split_on_silence(audio, min_silence_len=1000, silence_thresh=audio.dBFS-14, keep_silence=500)

    # Initialize recognizer
    r = sr.Recognizer()

    # Process each chunk
    full_transcription = []
    for i, chunk in enumerate(tqdm(chunks, desc=f"Processing {audio_basename}")):
        chunk_silent = AudioSegment.silent(duration=10)
        audio_chunk = chunk_silent + chunk + chunk_silent
        chunk_filename = os.path.join(output_path, f"chunk{i}.wav")
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

    print(f"Transcription completed for {audio_basename}. Check the {transcription_file_path} file.")
    os.remove(wav_file_path)

if __name__ == "__main__":
    if len(sys.argv) > 2:
        audio_file_path = sys.argv[1]
        output_path = sys.argv[2]
        transcribe_audio(audio_file_path, output_path)
    else:
        print("Usage: python transcribe.py <audio_file_path> <output_path>")
