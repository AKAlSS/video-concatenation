from moviepy.editor import *
import os

"""
combine_audio_visual.py
This script combines the extracted audio segments with the video clips to create final
clips that can be used for sharing on social media. Each final clip contains audio and
visuals aligned with key takeaways and themes.
"""

# Define paths
# Update the paths to point to the correct directories
visuals_path = os.path.expanduser('~/Desktop/BetterDaily/Visuals')
audio_clips_path = os.path.expanduser('~/Desktop/BetterDaily/Completed Clips')
output_path = os.path.expanduser('~/Desktop/BetterDaily/Posts')

# Ensure the output directory exists
os.makedirs(output_path, exist_ok=True)

# Check if visuals and audio clips directories exist
if not os.path.exists(visuals_path):
    print(f"Visuals directory not found: {visuals_path}")
    exit(1)

if not os.path.exists(audio_clips_path):
    print(f"Audio clips directory not found: {audio_clips_path}")
    exit(1)

# Get list of visual and audio files
visual_files = sorted([f for f in os.listdir(visuals_path) if f.endswith('.mp4') or f.endswith('.mov')])
audio_files = sorted([f for f in os.listdir(audio_clips_path) if f.endswith('.mp3')])

if not visual_files:
    print(f"No visual files found in {visuals_path}")
    exit(1)

if not audio_files:
    print(f"No audio files found in {audio_clips_path}")
    exit(1)

# Combine each visual with its corresponding audio
for i in range(len(audio_files)):
    audio_file = os.path.join(audio_clips_path, audio_files[i])
    output_file = os.path.join(output_path, f'BetterDaily_Post_{i+1}.mp4')

    # Randomly select a visual file
    visual_file = os.path.join(visuals_path, visual_files[i % len(visual_files)])

    # Load visual and audio
    video_clip = VideoFileClip(visual_file).subclip(0, AudioFileClip(audio_file).duration)
    audio_clip = AudioFileClip(audio_file)

    # Set the audio to the video
    final_clip = video_clip.set_audio(audio_clip)

    # Add overlay text if needed
    txt_clip = TextClip("BetterDaily Tip", fontsize=70, color='white', bg_color='black', size=video_clip.size)
    txt_clip = txt_clip.set_pos('center').set_duration(audio_clip.duration)

    # Combine everything
    final_clip = CompositeVideoClip([video_clip, txt_clip])

    # Write the video file
    final_clip.write_videofile(output_file, fps=24)

    print(f"Created {output_file}")

print("All posts have been created.")
