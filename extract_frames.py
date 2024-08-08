import cv2
import os
import sys

def extract_frames(video_path, output_folder, interval=30):
    cap = cv2.VideoCapture(video_path)
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    count = 0
    frame_count = 0

    os.makedirs(output_folder, exist_ok=True)

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

if __name__ == "__main__":
    if len(sys.argv) > 2:
        video_path = sys.argv[1]
        output_folder = sys.argv[2]
        interval = int(sys.argv[3]) if len(sys.argv) > 3 else 30
        extract_frames(video_path, output_folder, interval)
    else:
        print("Usage: python extract_frames.py <video_path> <output_folder> [interval]")
