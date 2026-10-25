import os
from dotenv import load_dotenv
load_dotenv()

# ====== NICHE & CONTENT ======
NICHE = "Scary Horror Stories"  # Change to: Finance, History, Facts, Motivation
VIDEO_LENGTH_TARGET = "8 minutes"
LANGUAGE = "English"
TARGET_AUDIENCE = "USA"

# ====== AI SETTINGS ======
# Voice - Edge TTS free voices (no API needed)
# Options: en-US-GuyNeural, en-US-JennyNeural, en-US-AriaNeural, en-GB-RyanNeural
VOICE = "en-US-GuyNeural"

# ====== LOW SPEC PC OPTIMIZATION ======
# CRITICAL FOR i3 M370 + 3GB RAM - DO NOT CHANGE TO 1080p
RENDER_RESOLUTION = (1280, 720)  # 720p only for 3GB
FPS = 24
THREADS = 1  # 1 thread prevents RAM crash on 3GB
PRESET = "ultrafast"  # ultrafast, superfast, veryfast
BITRATE = "2000k"
MAX_CONCURRENT_CLIPS = 1

# Stock footage count
CLIPS_COUNT = 8
CLIP_DURATION = 5  # seconds per clip before cut

# ====== YOUTUBE ======
UPLOAD_PRIVACY = "private"  # private, public, unlisted
CATEGORY_ID = "24"  # 24=Entertainment, 27=Education, 26=Howto
MADE_FOR_KIDS = False

# ====== PATHS ======
OUTPUT_DIR = "output"
DOWNLOADS_DIR = "downloads"
FINAL_VIDEO_NAME = "final_video.mp4"
THUMBNAIL_NAME = "thumbnail.jpg"
VOICEOVER_NAME = "voiceover.mp3"
SCRIPT_NAME = "script.txt"
