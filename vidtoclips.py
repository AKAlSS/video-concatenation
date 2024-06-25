import cv2
import numpy as np
from scenedetect import VideoManager, SceneManager
from scenedetect.detectors import ContentDetector
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import os

"""
vidtoclips.py
This script processes an anime episode video to detect scenes, classify them into 
categories (training, fight, struggle, victory), and extract clips based on these classifications.
"""

# Load Haar cascades for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def detect_scenes(video_path, threshold=30.0):
    """
    Detects scenes in the given video based on content changes.
    :param video_path: Path to the video file.
    :param threshold: Sensitivity threshold for scene detection.
    :return: List of detected scenes.
    """
    try:
        video_manager = VideoManager([video_path])
        scene_manager = SceneManager()
        scene_manager.add_detector(ContentDetector(threshold=threshold))
        
        video_manager.start()
        scene_manager.detect_scenes(frame_source=video_manager)
        scene_list = scene_manager.get_scene_list(video_manager.get_base_timecode())
        video_manager.release()
        return scene_list
    except Exception as e:
        print(f"Error detecting scenes: {e}")
        return []

def extract_key_frames(video_path, scenes):
    """
    Extracts key frames from the detected scenes in the video.
    :param video_path: Path to the video file.
    :param scenes: List of detected scenes.
    :return: List of key frames.
    """
    try:
        cap = cv2.VideoCapture(video_path)
        key_frames = []
        for scene in scenes:
            cap.set(cv2.CAP_PROP_POS_FRAMES, scene[0].get_frames())
            ret, frame = cap.read()
            if ret:
                key_frames.append(frame)
        cap.release()
        return key_frames
    except Exception as e:
        print(f"Error extracting key frames: {e}")
        return []

def classify_scene(frame):
    """
    Classifies a frame into one of the categories: training, fight, struggle, victory, or other.
    :param frame: Frame image.
    :return: Category of the scene.
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    if detect_boxing_gloves(frame) or detect_training_pads(frame) or detect_training_pose(frame):
        return "training"
    elif detect_action_lines(gray) or detect_fighting_pose(gray):
        return "fight"
    elif detect_struggling_expression(gray) or detect_dejected_body_language(gray):
        return "struggle"
    elif detect_victory_pose(frame) or detect_victory_lighting(frame):
        return "victory"
    else:
        return "other"

def detect_boxing_gloves(frame):
    """
    Detects boxing gloves in the frame based on red color.
    :param frame: Frame image.
    :return: Boolean indicating presence of boxing gloves.
    """
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0, 120, 70])
    upper_red = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)

    lower_red = np.array([170, 120, 70])
    upper_red = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red, upper_red)

    mask = mask1 + mask2
    red_pixels = cv2.countNonZero(mask)
    total_pixels = frame.shape[0] * frame.shape[1]

    if red_pixels / total_pixels > 0.01:  # Adjust threshold as needed
        return True
    return False

def detect_training_pads(frame):
    """
    Detects training pads in the frame based on red color.
    :param frame: Frame image.
    :return: Boolean indicating presence of training pads.
    """
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0, 120, 70])
    upper_red = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)

    lower_red = np.array([170, 120, 70])
    upper_red = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red, upper_red)

    mask = mask1 + mask2
    red_pixels = cv2.countNonZero(mask)
    total_pixels = frame.shape[0] * frame.shape[1]

    if red_pixels / total_pixels > 0.01:  # Adjust threshold as needed
        return True
    return False

def detect_training_pose(frame):
    """
    Placeholder for detecting training poses.
    :param frame: Frame image.
    :return: Boolean indicating presence of training pose.
    """
    # Placeholder for a more advanced model or heuristic
    # Example: Pose estimation model to detect stretching poses
    return False

def detect_action_lines(gray_frame):
    """
    Detects action lines in the frame, indicating motion or action.
    :param gray_frame: Grayscale frame image.
    :return: Boolean indicating presence of action lines.
    """
    edges = cv2.Canny(gray_frame, 50, 150, apertureSize=3)
    if cv2.countNonZero(edges) > 1000:  # Adjust threshold as needed
        return True
    return False

def detect_fighting_pose(gray_frame):
    """
    Placeholder for detecting fighting poses.
    :param gray_frame: Grayscale frame image.
    :return: Boolean indicating presence of fighting pose.
    """
    # Placeholder for a more advanced model or heuristic
    # Example: Pose estimation model to detect fighting poses
    return False

def detect_gym_equipment(frame):
    """
    Placeholder for detecting gym equipment.
    :param frame: Frame image.
    :return: Boolean indicating presence of gym equipment.
    """
    # Detecting common gym equipment using template matching or context-based detection
    return False

def detect_struggling_expression(gray_frame):
    """
    Detects struggling expressions based on face detection and analysis.
    :param gray_frame: Grayscale frame image.
    :return: Boolean indicating presence of struggling expression.
    """
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5)
    for (x, y, w, h) in faces:
        face = gray_frame[y:y+h, x:x+w]
        # Further analysis for expressions can be done here
        return True
    return False

def detect_dejected_body_language(gray_frame):
    """
    Placeholder for detecting dejected body language.
    :param gray_frame: Grayscale frame image.
    :return: Boolean indicating presence of dejected body language.
    """
    # Placeholder for body pose detection
    # Example: Heuristic or pose estimation model to detect dejected postures
    return False

def detect_victory_pose(frame):
    """
    Placeholder for detecting victory poses.
    :param frame: Frame image.
    :return: Boolean indicating presence of victory pose.
    """
    # Placeholder function for victory pose detection
    # Example: Heuristic or pose estimation model to detect victory poses
    return False

def detect_victory_lighting(frame):
    """
    Detects victory lighting based on brightness.
    :param frame: Frame image.
    :return: Boolean indicating presence of victory lighting.
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Detect bright spots or lighting patterns indicating victory
    brightness = np.mean(gray)
    if brightness > 200:  # Adjust threshold as needed
        return True
    return False

def extract_clips(video_path, scenes, output_folder, context_filter):
    """
    Extracts clips from the video based on classified scenes.
    :param video_path: Path to the video file.
    :param scenes: List of detected scenes.
    :param output_folder: Directory to save the extracted clips.
    :param context_filter: List of classified contexts for each scene.
    """
    try:
        for i, (scene, context) in enumerate(zip(scenes, context_filter)):
            if context in ["training", "fight", "struggle", "victory"]:
                start_time = scene[0].get_seconds()
                end_time = scene[1].get_seconds()
                output_path = f"{output_folder}/clip_{context}_{i+1}.mp4"
                ffmpeg_extract_subclip(video_path, start_time, end_time, targetname=output_path)
    except Exception as e:
        print(f"Error extracting clips: {e}")

def process_video(video_path, output_folder):
    """
    Main function to process the video: detect scenes, classify them, and extract clips.
    :param video_path: Path to the video file.
    :param output_folder: Directory to save the extracted clips.
    """
    try:
        scenes = detect_scenes(video_path)
        key_frames = extract_key_frames(video_path, scenes)
        context_filter = [classify_scene(frame) for frame in key_frames]
        extract_clips(video_path, scenes, output_folder, context_filter)
    except Exception as e:
        print(f"Error processing video: {e}")

def main():
    """
    Entry point of the script. Defines video input and output paths and initiates the processing.
    """
    video_path = "/Users/ahmadkaiss/Desktop/BetterDaily/Source Visual/anime_episode.mp4"
    output_folder = "/Users/ahmadkaiss/Desktop/BetterDaily/Visuals"
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    process_video(video_path, output_folder)

if __name__ == "__main__":
    main()
