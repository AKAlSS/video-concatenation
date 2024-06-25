from scenedetect import VideoManager, SceneManager
from scenedetect.detectors import ContentDetector
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import cv2
import os

"""
visuals.py
This script manages the process of classifying and processing the extracted video frames
into different categories such as training, fight, struggle, and victory.
"""

def detect_scenes(video_path, threshold=30.0):
    video_manager = VideoManager([video_path])
    scene_manager = SceneManager()
    scene_manager.add_detector(ContentDetector(threshold=threshold))
    
    video_manager.start()
    scene_manager.detect_scenes(frame_source=video_manager)
    scene_list = scene_manager.get_scene_list(video_manager.get_base_timecode())
    video_manager.release()
    return scene_list

def extract_clips(video_path, scenes, output_folder, context_filter):
    for i, scene in enumerate(scenes):
        start_time = scene[0].get_seconds()
        end_time = scene[1].get_seconds()
        if context_filter[i]:  # Check if the scene matches the desired context
            output_path = f"{output_folder}/clip_{i+1}.mp4"
            ffmpeg_extract_subclip(video_path, start_time, end_time, targetname=output_path)

def classify_scene(frame):
    # Placeholder for a function that classifies the scene context (training, boxing, etc.)
    # This could be replaced with a more sophisticated model
    # For now, we will randomly classify scenes for demonstration purposes
    # Replace this with your own logic
    return "boxing"  # Example: Replace this with actual classification logic

def process_video(video_path, output_folder):
    # Step 1: Detect scenes
    scenes = detect_scenes(video_path)

    # Step 2: Classify scenes
    context_filter = []
    cap = cv2.VideoCapture(video_path)
    for scene in scenes:
        cap.set(cv2.CAP_PROP_POS_FRAMES, scene[0].get_frames())
        ret, frame = cap.read()
        if ret:
            context = classify_scene(frame)
            context_filter.append(context in ["training", "boxing", "struggling"])
        else:
            context_filter.append(False)
    cap.release()

    # Step 3: Extract and save clips
    extract_clips(video_path, scenes, output_folder, context_filter)

def main():
    video_path = "/Users/ahmadkaiss/Desktop/BetterDaily/Source Visual/anime_episode.mp4"
    output_folder = "/Users/ahmadkaiss/Desktop/BetterDaily/Visuals"
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    process_video(video_path, output_folder)

if __name__ == "__main__":
    main()