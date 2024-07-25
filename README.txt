README.txt

Project Workflow
This project involves processing podcast audio and anime video to create clips that align with key themes such as training, fight, struggle, and victory. Below are the steps to follow and the scripts to run in the correct order:

1. **Transcribe Podcast Audio**
   - Script: `transcribe.py`
   - Description: This script transcribes a podcast audio file into text. The transcription is then used to highlight key takeaways and practical use cases for further processing.
   - Command: `python transcribe.py`

2. **Highlight Key Points and Generate Timestamps**
   - Action: Share the transcription with the AI assistant to highlight key takeaways, practical use cases, and generate timestamps.

3. **Create Audio Segments**
   - Script: `audioseg.py`
   - Description: This script takes the transcription of a podcast along with highlighted key points and timestamps to create audio segments. The audio segments correspond to the key takeaways and practical use cases highlighted in the transcription.
   - Command: `python audioseg.py`

4. **Extract Video Clips from Anime Episode**
   - Script: `vidtoclips.py`
   - Description: This script processes an anime episode video to detect scenes, classify them into categories (training, fight, struggle, victory), and extract clips based on these classifications.
   - Command: `python vidtoclips.py`

5. **Extract Frames from Video (for model training)**
   - Script: `extract_frames.py`
   - Description: This script is used to extract frames from a video at specific intervals. The frames can be used for training a model or for manual classification of scenes.
   - Command: `python extract_frames.py`

6. **Combine Audio and Visual Clips**
   - Script: `combine_audio_visual.py`
   - Description: This script combines the extracted audio segments with the video clips to create final clips that can be used for sharing on social media. Each final clip contains audio and visuals aligned with key takeaways and themes.
   - Command: `python combine_audio_visual.py`

Additional Scripts:
- `visuals.py`: Manages the process of classifying and processing the extracted video frames into different categories such as training, fight, struggle, and victory.
- `video.py`: Provides utility functions for video processing, such as loading videos, saving processed videos, and other helper functions related to video handling.

Ensure you have all necessary dependencies installed before running the scripts. Refer to the comments at the top of each script for more details on their functionality and usage.

--------

Complete Workflow:
Transcribe Audio:

Place your long audio files in ~/Desktop/BetterDaily/Source Audio.
Run the transcription script to generate text transcriptions.
Identify Key Segments:

Identify the key segments and provide a segments.txt file with timestamps.
Extract Audio Segments:

Use the segments.txt file to extract audio segments from the long audio files.
Ensure the extracted audio clips are placed in ~/Desktop/BetterDaily/Completed Clips.
Combine Audio with Visual Clips:

Combine the extracted audio clips with visual clips to create the final videos.
