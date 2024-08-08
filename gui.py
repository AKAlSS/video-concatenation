import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import subprocess

def run_script(script, args):
    try:
        subprocess.run(["python", script] + args, check=True)
        messagebox.showinfo("Success", f"{script} executed successfully.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def transcribe_audio():
    audio_file = filedialog.askopenfilename(title="Select Audio File", filetypes=[("MP3 files", "*.mp3")])
    output_dir = filedialog.askdirectory(title="Select Output Directory")
    if audio_file and output_dir:
        run_script("transcribe.py", [audio_file, output_dir])

def create_audio_segments():
    transcription_file = filedialog.askopenfilename(title="Select Transcription File", filetypes=[("Text files", "*.txt")])
    audio_file = filedialog.askopenfilename(title="Select Audio File", filetypes=[("MP3 files", "*.mp3")])
    output_dir = filedialog.askdirectory(title="Select Output Directory")
    if transcription_file and audio_file and output_dir:
        run_script("audioseg.py", [transcription_file, audio_file, output_dir])

def extract_video_clips():
    video_file = filedialog.askopenfilename(title="Select Video File", filetypes=[("MP4 files", "*.mp4")])
    output_dir = filedialog.askdirectory(title="Select Output Directory")
    if video_file and output_dir:
        run_script("vidtoclips.py", [video_file, output_dir])

def extract_frames():
    video_file = filedialog.askopenfilename(title="Select Video File", filetypes=[("MP4 files", "*.mp4")])
    output_dir = filedialog.askdirectory(title="Select Output Directory")
    interval = simpledialog.askinteger("Input", "Enter frame extraction interval (seconds):", minvalue=1, maxvalue=600)
    if video_file and output_dir and interval is not None:
        run_script("extract_frames.py", [video_file, output_dir, str(interval)])

def combine_audio_visual():
    audio_dir = filedialog.askdirectory(title="Select Audio Clips Directory")
    visual_dir = filedialog.askdirectory(title="Select Visual Clips Directory")
    output_dir = filedialog.askdirectory(title="Select Output Directory")
    if audio_dir and visual_dir and output_dir:
        run_script("combine_audio_visual.py", [audio_dir, visual_dir, output_dir])

app = tk.Tk()
app.title("Video Concatenation Project")

frame = tk.Frame(app)
frame.pack(pady=20)

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

app.mainloop()
