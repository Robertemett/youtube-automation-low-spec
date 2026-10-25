#!/usr/bin/env python3
"""
YOUTUBE AUTOMATION - COMPLETE END TO END
Optimized for: Intel i3 M370 @ 2.4GHz + 3GB RAM + Win10 Pro
Author: Low Spec PC Build
License: MIT
"""
import os
import sys
import time
import argparse
from dotenv import load_dotenv
load_dotenv()

import config
from modules.script import generate_script
from modules.voice import generate_voiceover
from modules.visuals import get_stock_videos
from modules.editor import create_video
from modules.thumbnail import create_thumbnail
from modules.uploader import upload_video

def ensure_dirs():
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)
    os.makedirs(config.DOWNLOADS_DIR, exist_ok=True)
    # gitkeep files
    open(os.path.join(config.OUTPUT_DIR, ".gitkeep"), "a").close()
    open(os.path.join(config.DOWNLOADS_DIR, ".gitkeep"), "a").close()

def run_pipeline(topic=None, auto_upload=False):
    print(r"""
  __   __  ____  _   _ _____ _   _ ____  _____ 
  \ \ / / / ___|| | | |_   _| | | | __ )| ____|
   \ V /  \___ \| | | | | | | | | |  _ \|  _|  
    | |    ___) | |_| | | | | |_| | |_) | |___ 
    |_|   |____/ \___/  |_|  \___/|____/|_____|
                                                  
  AUTOMATION - LOW SPEC EDITION (i3 M370 + 3GB)
    """)
    print(f"Niche: {config.NICHE} | Resolution: {config.RENDER_RESOLUTION} | Voice: {config.VOICE}")
    ensure_dirs()

    # 1. SCRIPT
    print("\n[1/5] 📝 Generating viral script (Groq Cloud)...")
    if not topic:
        topic = f"Generate a viral topic for {config.NICHE} for USA audience"
    try:
        title, script, description, tags = generate_script(topic)
        print(f"  ✅ Title: {title}")
        with open(os.path.join(config.OUTPUT_DIR, config.SCRIPT_NAME), "w", encoding="utf-8") as f:
            f.write(f"TITLE: {title}\n\nSCRIPT:\n{script}\n\nDESCRIPTION:\n{description}\n\nTAGS:\n{','.join(tags)}")
    except Exception as e:
        print(f"  ❌ Script failed: {e}")
        return

    # 2. VOICEOVER
    print("\n[2/5] 🎙️ Generating voiceover (Edge TTS - 0% RAM)...")
    audio_path = os.path.join(config.OUTPUT_DIR, config.VOICEOVER_NAME)
    try:
        generate_voiceover(script, audio_path)
        print(f"  ✅ Voice saved: {audio_path}")
    except Exception as e:
        print(f"  ❌ Voice failed: {e}")
        return

    # 3. VISUALS
    print("\n[3/5] 🎬 Downloading stock footage (Pexels - Cloud)...")
    try:
        video_clips = get_stock_videos(script, audio_path)
        print(f"  ✅ Downloaded {len(video_clips)} clips")
    except Exception as e:
        print(f"  ⚠️ Visuals warning: {e}, will use solid background")
        video_clips = []

    # 4. EDIT
    print(f"\n[4/5] ✂️ Editing video (720p ultrafast, threads={config.THREADS})...")
    print(f"  ⏳ This will take ~2x video length on i3 M370, please wait...")
    final_video = os.path.join(config.OUTPUT_DIR, config.FINAL_VIDEO_NAME)
    try:
        create_video(audio_path, video_clips, final_video, script)
        print(f"  ✅ Video ready: {final_video}")
    except Exception as e:
        print(f"  ❌ Edit failed: {e}")
        import traceback; traceback.print_exc()
        return

    # 5. THUMBNAIL
    print("\n[5/5] 🖼️ Creating thumbnail...")
    thumb_path = os.path.join(config.OUTPUT_DIR, config.THUMBNAIL_NAME)
    try:
        create_thumbnail(title, thumb_path)
        print(f"  ✅ Thumbnail: {thumb_path}")
    except Exception as e:
        print(f"  ❌ Thumbnail failed: {e}")
        thumb_path = None

    print("\n" + "="*60)
    print(f"🎉 DONE! All files in /{config.OUTPUT_DIR}/ folder")
    print(f"   Video: {config.FINAL_VIDEO_NAME}")
    print(f"   Thumbnail: {config.THUMBNAIL_NAME}")
    print(f"   Script: {config.SCRIPT_NAME}")
    print("="*60)

    if auto_upload:
        print("\n📤 Auto uploading to YouTube...")
        upload_video(final_video, title, description, tags, thumb_path)
    else:
        ask = input("\nUpload to YouTube now? (y/n): ").strip().lower()
        if ask == 'y':
            upload_video(final_video, title, description, tags, thumb_path)

    return final_video

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YouTube Automation Low Spec")
    parser.add_argument("--topic", type=str, help="Custom topic")
    parser.add_argument("--auto-upload", action="store_true", help="Auto upload without prompt")
    args = parser.parse_args()
    run_pipeline(topic=args.topic, auto_upload=args.auto_upload)
