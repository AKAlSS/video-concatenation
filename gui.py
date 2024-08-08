import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, scrolledtext
import subprocess

def run_script(script, args):
    try:
        subprocess.run(["python", script] + args, check=True)
        messagebox.showinfo("Success", f"{script} executed successfully.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def transcribe_audio():
    audio_file = filedialog.askopenfilename(title="Select Audio File", filetypes=[("MP3 files", "*.mp3")])
    if not audio_file:
        return
    output_dir = filedialog.askdirectory(title="Select Output Directory")
    if not output_dir:
        return
    run_script("transcribe.py", [audio_file, output_dir])

def create_audio_segments():
    transcription_file = filedialog.askopenfilename(title="Select Transcription File", filetypes=[("Text files", "*.txt")])
    if not transcription_file:
        return
    audio_file = filedialog.askopenfilename(title="Select Audio File", filetypes=[("MP3 files", "*.mp3")])
    if not audio_file:
        return
    output_dir = filedialog.askdirectory(title="Select Output Directory")
    if not output_dir:
        return
    run_script("audioseg.py", [transcription_file, audio_file, output_dir])

def extract_video_clips():
    video_file = filedialog.askopenfilename(title="Select Video File", filetypes=[("MP4 files", "*.mp4")])
    if not video_file:
        return
    output_dir = filedialog.askdirectory(title="Select Output Directory")
    if not output_dir:
        return
    run_script("vidtoclips.py", [video_file, output_dir])

def extract_frames():
    video_file = filedialog.askopenfilename(title="Select Video File", filetypes=[("MP4 files", "*.mp4")])
    if not video_file:
        return
    output_dir = filedialog.askdirectory(title="Select Output Directory")
    if not output_dir:
        return
    interval = simpledialog.askinteger("Input", "Enter frame extraction interval (seconds):", minvalue=1, maxvalue=600)
    if not interval:
        return
    run_script("extract_frames.py", [video_file, output_dir, str(interval)])

def combine_audio_visual():
    audio_dir = filedialog.askdirectory(title="Select Audio Clips Directory")
    if not audio_dir:
        return
    visual_dir = filedialog.askdirectory(title="Select Visual Clips Directory")
    if not visual_dir:
        return
    output_dir = filedialog.askdirectory(title="Select Output Directory")
    if not output_dir:
        return
    run_script("combine_audio_visual.py", [audio_dir, visual_dir, output_dir])

def process_videos():
    visuals_path = filedialog.askdirectory(title="Select Visuals Directory")
    if not visuals_path:
        return
    audio_clips_path = filedialog.askdirectory(title="Select Audio Clips Directory")
    if not audio_clips_path:
        return
    output_path = filedialog.askdirectory(title="Select Output Directory")
    if not output_path:
        return
    run_script("video.py", [visuals_path, audio_clips_path, output_path])

def process_visuals():
    video_file = filedialog.askopenfilename(title="Select Video File", filetypes=[("MP4 files", "*.mp4")])
    if not video_file:
        return
    output_dir = filedialog.askdirectory(title="Select Output Directory")
    if not output_dir:
        return
    run_script("visuals.py", [video_file, output_dir])

def show_instructions():
    instructions = (
        "Instructions:\n\n"
        "1. Transcribe Audio: Select an audio file (MP3) to transcribe into text.\n"
        "2. Create Audio Segments: Select a transcription file (TXT) and an audio file (MP3) to create audio segments based on the transcription.\n"
        "3. Extract Video Clips: Select a video file (MP4) to detect scenes and classify them into categories.\n"
        "4. Extract Frames: Select a video file (MP4) to extract frames at specific intervals.\n"
        "5. Combine Audio & Visual: Select directories containing audio clips and visual clips to combine them into final videos.\n"
        "6. Process Videos: Select directories containing visuals and audio clips to process and create final videos.\n"
        "7. Process Visuals: Select a video file (MP4) to classify scenes and extract clips based on context.\n"
    )
    instructions_window = tk.Toplevel(app)
    instructions_window.title("Instructions")
    instructions_window.geometry("600x400")
    text_area = scrolledtext.ScrolledText(instructions_window, wrap=tk.WORD)
    text_area.pack(expand=True, fill='both')
    text_area.insert(tk.INSERT, instructions)
    text_area.configure(state='disabled')

app = tk.Tk()
app.title("Video Concatenation Project")
app.geometry("800x600")

frame = tk.Frame(app)
frame.pack(pady=20)

title_label = tk.Label(frame, text="Video Concatenation Project", font=("Helvetica", 16))
title_label.pack(pady=10)

instructions_button = tk.Button(frame, text="Instructions", command=show_instructions)
instructions_button.pack(pady=5)

btn_transcribe = tk.Button(frame, text="Transcribe Audio", command=transcribe_audio)
btn_transcribe.pack(pady=5)

btn_audio_segments = tk.Button(frame, text="Create Audio Segments", command=create_audio_segments)
btn_audio_segments.pack(pady=5)

btn_video_clips = tk.Button(frame, text="Extract Video Clips", command=extract_video_clips)
btn_video_clips.pack(pady=5)

btn_extract_frames = tk.Button(frame, text="Extract Frames", command=extract_frames)
btn_extract_frames.pack(pady=5)

btn_combine = tk.Button(frame, text="Combine Audio & Visual", command=combine_audio_visual)
btn_combine.pack(pady=5)

btn_process_videos = tk.Button(frame, text="Process Videos", command=process_videos)
btn_process_videos.pack(pady=5)

btn_process_visuals = tk.Button(frame, text="Process Visuals", command=process_visuals)
btn_process_visuals.pack(pady=5)

app.mainloop()
