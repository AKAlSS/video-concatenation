import cv2
import os

"""
extract_frames.py
This script is used to extract frames from a video at specific intervals. The frames
can be used for training a model or for manual classification of scenes.
"""

def extract_frames(video_path, output_folder, interval=30):
    cap = cv2.VideoCapture(video_path)
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    count = 0
    frame_count = 0

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if count % int(frame_rate * interval) == 0:
            frame_path = os.path.join(output_folder, f"frame_{frame_count}.jpg")
            cv2.imwrite(frame_path, frame)
            frame_count += 1
        count += 1

    cap.release()
    print(f"Extracted {frame_count} frames from the video.")

video_path = "/Users/ahmadkaiss/Desktop/BetterDaily/Source Visual/anime_episode.mp4"
output_folder = "/Users/ahmadkaiss/Desktop/BetterDaily/Visuals/frames"
extract_frames(video_path, output_folder, interval=5)  # Extract a frame every 5 seconds