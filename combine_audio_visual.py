import os
import sys
from moviepy.editor import *

def combine_audio_visual(audio_dir, visual_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    visual_files = sorted([f for f in os.listdir(visual_dir) if f.endswith('.mp4') or f.endswith('.mov')])
    audio_files = sorted([f for f in os.listdir(audio_dir) if f.endswith('.mp3')])

    if not visual_files:
        print(f"No visual files found in {visual_dir}")
        return

    if not audio_files:
        print(f"No audio files found in {audio_dir}")
        return

    for i in range(len(audio_files)):
        audio_file = os.path.join(audio_dir, audio_files[i])
        output_file = os.path.join(output_dir, f'BetterDaily_Post_{i+1}.mp4')

        visual_file = os.path.join(visual_dir, visual_files[i % len(visual_files)])

        video_clip = VideoFileClip(visual_file).subclip(0, AudioFileClip(audio_file).duration)
        audio_clip = AudioFileClip(audio_file)

        final_clip = video_clip.set_audio(audio_clip)

        txt_clip = TextClip("BetterDaily Tip", fontsize=70, color='white', bg_color='black', size=video_clip.size)
        txt_clip = txt_clip.set_pos('center').set_duration(audio_clip.duration)

        final_clip = CompositeVideoClip([video_clip, txt_clip])

        final_clip.write_videofile(output_file, fps=24)

        print(f"Created {output_file}")

    print("All posts have been created.")

if __name__ == "__main__":
    if len(sys.argv) > 3:
        audio_dir = sys.argv[1]
        visual_dir = sys.argv[2]
        output_dir = sys.argv[3]
        combine_audio_visual(audio_dir, visual_dir, output_dir)
    else:
        print("Usage: python combine_audio_visual.py <audio_dir> <visual_dir> <output_dir>")
