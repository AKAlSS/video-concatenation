import cv2
import numpy as np
from scenedetect import VideoManager, SceneManager
from scenedetect.detectors import ContentDetector
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import os

# Load Haar cascades for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def detect_scenes(video_path, threshold=30.0):
    video_manager = VideoManager([video_path])
    scene_manager = SceneManager()
    scene_manager.add_detector(ContentDetector(threshold=threshold))
    
    video_manager.start()
    scene_manager.detect_scenes(frame_source=video_manager)
    scene_list = scene_manager.get_scene_list(video_manager.get_base_timecode())
    video_manager.release()
    return scene_list

def extract_key_frames(video_path, scenes):
    cap = cv2.VideoCapture(video_path)
    key_frames = []
    for scene in scenes:
        cap.set(cv2.CAP_PROP_POS_FRAMES, scene[0].get_frames())
        ret, frame = cap.read()
        if ret:
            key_frames.append(frame)
    cap.release()
    return key_frames

def classify_scene(frame):
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

    if red_pixels / total_pixels > 0.01:
        return True
    return False

def detect_training_pads(frame):
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

    if red_pixels / total_pixels > 0.01:
        return True
    return False

def detect_training_pose(frame):
    return False

def detect_action_lines(gray_frame):
    edges = cv2.Canny(gray_frame, 50, 150, apertureSize=3)
    if cv2.countNonZero(edges) > 1000:
        return True
    return False

def detect_fighting_pose(gray_frame):
    return False

def detect_struggling_expression(gray_frame):
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5)
    for (x, y, w, h) in faces:
        face = gray_frame[y:y+h, x:x+w]
        return True
    return False

def detect_dejected_body_language(gray_frame):
    return False

def detect_victory_pose(frame):
    return False

def detect_victory_lighting(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    brightness = np.mean(gray)
    if brightness > 200:
        return True
    return False

def extract_clips(video_path, scenes, output_folder, context_filter):
    for i, (scene, context) in enumerate(zip(scenes, context_filter)):
        if context in ["training", "fight", "struggle", "victory"]:
            start_time = scene[0].get_seconds()
            end_time = scene[1].get_seconds()
            output_path = f"{output_folder}/clip_{context}_{i+1}.mp4"
            ffmpeg_extract_subclip(video_path, start_time, end_time, targetname=output_path)

def process_video(video_path, output_folder):
    scenes = detect_scenes(video_path)
    key_frames = extract_key_frames(video_path, scenes)
    context_filter = [classify_scene(frame) for frame in key_frames]
    extract_clips(video_path, scenes, output_folder, context_filter)

def main():
    if len(sys.argv) > 2:
        video_path = sys.argv[1]
        output_folder = sys.argv[2]
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        process_video(video_path, output_folder)
    else:
        print("Usage: python vidtoclips.py <video_path> <output_folder>")

if __name__ == "__main__":
    main()
