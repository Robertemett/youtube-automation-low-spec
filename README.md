[README.md](https://github.com/user-attachments/files/33931512/README.md)
# 🎬 YouTube Automation - Low Spec PC Edition

> **Built for:** Intel i3 M370 @ 2.40GHz + 3GB RAM + Windows 10 Pro (Micro 10)  
> **Status:** ✅ Production Ready | MIT License

End-to-end YouTube automation that runs on a 2010 Mini PC. No GPU needed. All AI is cloud-based.

## 🚀 Features
- [x] Auto Script Generation (Groq Llama 3.3 70B - FREE)
- [x] Auto Voiceover (Edge TTS - FREE, 0% RAM)
- [x] Auto Stock Footage (Pexels API - FREE)
- [x] Auto Video Editing (MoviePy - 720p optimized for 3GB RAM)
- [x] Auto Thumbnail (Pillow)
- [x] Auto Upload + Thumbnail to YouTube (YouTube Data API v3)
- [x] Auto Description & Tags

## 📁 Full File Structure
```
├── main.py
├── config.py
├── requirements.txt
├── .env.example
├── client_secret.example.json
├── modules/
│   ├── __init__.py
│   ├── script.py
│   ├── voice.py
│   ├── visuals.py
│   ├── editor.py
│   ├── thumbnail.py
│   └── uploader.py
├── assets/
│   └── (optional fonts, overlays)
├── output/ (gitignored)
├── downloads/ (gitignored)
└── .github/workflows/
    └── daily-upload.yml
```

## ⚡ Quick Start - For Your Specs

### 1. Clone
```bash
git clone https://github.com/YOUR_USERNAME/youtube-automation.git
cd youtube-automation
```

### 2. Install Python 3.10
Download from python.org - check "Add to PATH"

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Get FREE API Keys
- **Groq:** https://console.groq.com/keys (Free 14k req/day)
- **Pexels:** https://www.pexels.com/api/ (Free 200 req/hour)

Create `.env` file from `.env.example`:
```
GROQ_API_KEY=gsk_xxxx
PEXELS_API_KEY=xxxx
OPENAI_API_KEY=optional
```

### 5. Run
```bash
python main.py
```
Output: `output/final_video.mp4` + `output/thumbnail.jpg`

## ⚙️ Config (config.py)
Designed for 3GB RAM crash prevention:
- Resolution: 1280x720 (DON'T USE 1080p)
- FPS: 24
- Threads: 1 (prevents RAM crash)
- Preset: ultrafast

Change niche in config.py:
```python
NICHE = "Scary Stories"
```

## 📤 YouTube Auto Upload
1. Go to console.cloud.google.com
2. Create Project -> Enable YouTube Data API v3
3. Credentials -> OAuth Consent Screen -> External
4. Create OAuth Client ID -> Desktop App -> Download JSON
5. Rename to `client_secret.json` and put in root
6. Run `python main.py` and say `y` to upload

## 🖥️ Performance on i3 M370 + 3GB
- 8 min video: ~15 min render
- RAM usage: <2.5GB
- CPU: 100% during render (normal)
- Tip: Close Chrome, use ReadyBoost USB

## 🔄 GitHub Actions (Auto Daily Upload)
Push to GitHub, add secrets in repo Settings -> Secrets:
- GROQ_API_KEY
- PEXELS_API_KEY
Workflow will create 1 video daily automatically.

## 📄 License
MIT - Use commercially on YouTube. No attribution needed.

## 🙏 Credits
Optimized for Micro 10 Mini PC owners.
