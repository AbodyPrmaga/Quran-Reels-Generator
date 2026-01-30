from moviepy.editor import VideoFileClip, concatenate_videoclips
import random
import requests
import os
import time
import math
import urllib3

urllib3.disable_warnings()

API_KEY = "52596033-b4348f2c9bdba23acdcab8117"
querys = ["nature", "sky", "garden", "forest", "mountains", "river", "trees", "flowers", "sunset", "landscape", "wildlife", "meadow", "ocean", "beach", "hills"]
query = random.choice(querys)
url = f"https://pixabay.com/api/videos/?key={API_KEY}&q={query}&per_page=10"

MAX_SIZE_MB = 20
RETRIES = 3

def get_video(final_file,dur):
    for attempt in range(1, RETRIES + 1):
        try:
            response = requests.get(url).json()

            if not response.get("hits"):
                print("❌ No Results!")
                return

            valid_videos = [
                v for v in response["hits"]
                if v["videos"]["small"]["size"] <= MAX_SIZE_MB * 1024 * 1024
            ]

            if not valid_videos:
                print("❌ No videos under size limit!")
                return

            video = random.choice(valid_videos)
            video_url = video["videos"]["small"]["url"]

            print("⬇️ Downloading video...")
            video_data = requests.get(video_url, verify=False).content

            temp_file = "temp_video.mp4"
            with open(temp_file, "wb") as f:
                f.write(video_data)

            print("🎬 Processing video...")
            clip = VideoFileClip(temp_file)

            clip = clip.resize(height=1920)
            clip = clip.crop(
                width=1080,
                height=1920,
                x_center=clip.w / 2,
                y_center=clip.h / 2
            )

            if clip.duration > dur:
                start = random.uniform(0, clip.duration - dur)
                clip = clip.subclip(start, start + dur)
            else:
                loops = math.ceil(dur/ clip.duration)
                clip = concatenate_videoclips([clip] * loops)
                clip = clip.subclip(0, dur)

            clip.write_videofile(
                final_file,
                codec="libx264",
                audio_codec="aac",
                fps=30,
                threads=4
            )

            clip.close()
            os.remove(temp_file)

            print(f"✅ Done! Video {video['id']} is ready ({dur}s)")
            break

        except Exception as e:
            print(f"⚠️ Attempt {attempt} failed: {e}")
            if attempt < RETRIES:
                print("⏳ Retrying in 5 seconds...")
                time.sleep(5)
            else:
                print("❌ All attempts failed!")
