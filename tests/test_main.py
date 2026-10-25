import importlib
import sys
import types
from pathlib import Path


def load_main_module(monkeypatch):
    modules_pkg = types.ModuleType("modules")
    modules_pkg.__path__ = []
    monkeypatch.setitem(sys.modules, "modules", modules_pkg)

    for module_name, attr_names in {
        "script": ["generate_script"],
        "voice": ["generate_voiceover"],
        "visuals": ["get_stock_videos"],
        "editor": ["create_video"],
        "thumbnail": ["create_thumbnail"],
        "uploader": ["upload_video"],
    }.items():
        mod = types.ModuleType(f"modules.{module_name}")
        for attr in attr_names:
            setattr(mod, attr, lambda *args, **kwargs: None)
        monkeypatch.setitem(sys.modules, f"modules.{module_name}", mod)
        setattr(modules_pkg, module_name, mod)

    sys.modules.pop("main", None)
    return importlib.import_module("main")


def test_ensure_dirs_creates_output_and_downloads(monkeypatch, tmp_path):
    main = load_main_module(monkeypatch)
    monkeypatch.setattr(main.config, "OUTPUT_DIR", str(tmp_path / "output"), raising=False)
    monkeypatch.setattr(main.config, "DOWNLOADS_DIR", str(tmp_path / "downloads"), raising=False)

    main.ensure_dirs()

    output_dir = tmp_path / "output"
    downloads_dir = tmp_path / "downloads"
    assert output_dir.is_dir()
    assert downloads_dir.is_dir()
    assert (output_dir / ".gitkeep").exists()
    assert (downloads_dir / ".gitkeep").exists()


def test_run_pipeline_successful_with_mocked_dependencies(monkeypatch, tmp_path):
    main = load_main_module(monkeypatch)
    monkeypatch.setattr(main.config, "OUTPUT_DIR", str(tmp_path / "output"), raising=False)
    monkeypatch.setattr(main.config, "DOWNLOADS_DIR", str(tmp_path / "downloads"), raising=False)
    monkeypatch.setattr(main.config, "SCRIPT_NAME", "script.txt", raising=False)
    monkeypatch.setattr(main.config, "VOICEOVER_NAME", "voiceover.mp3", raising=False)
    monkeypatch.setattr(main.config, "FINAL_VIDEO_NAME", "final_video.mp4", raising=False)
    monkeypatch.setattr(main.config, "THUMBNAIL_NAME", "thumbnail.jpg", raising=False)

    uploaded = {}

    def fake_generate_script(topic):
        return "Test Title", "Test script", "Test description", ["tag1", "tag2"]

    def fake_generate_voiceover(script, audio_path):
        Path(audio_path).parent.mkdir(parents=True, exist_ok=True)
        Path(audio_path).write_text("audio", encoding="utf-8")

    def fake_get_stock_videos(script, audio_path):
        return ["clip1", "clip2"]

    def fake_create_video(audio_path, video_clips, final_video, script):
        Path(final_video).parent.mkdir(parents=True, exist_ok=True)
        Path(final_video).write_text("video", encoding="utf-8")

    def fake_create_thumbnail(title, thumb_path):
        Path(thumb_path).parent.mkdir(parents=True, exist_ok=True)
        Path(thumb_path).write_text("thumb", encoding="utf-8")

    def fake_upload_video(final_video, title, description, tags, thumb_path):
        uploaded["final_video"] = final_video
        uploaded["title"] = title
        uploaded["thumb_path"] = thumb_path

    monkeypatch.setattr(main, "generate_script", fake_generate_script)
    monkeypatch.setattr(main, "generate_voiceover", fake_generate_voiceover)
    monkeypatch.setattr(main, "get_stock_videos", fake_get_stock_videos)
    monkeypatch.setattr(main, "create_video", fake_create_video)
    monkeypatch.setattr(main, "create_thumbnail", fake_create_thumbnail)
    monkeypatch.setattr(main, "upload_video", fake_upload_video)

    final_video = main.run_pipeline(topic="Test topic", auto_upload=True)

    assert final_video == str(tmp_path / "output" / "final_video.mp4")
    assert uploaded["final_video"] == str(tmp_path / "output" / "final_video.mp4")
    assert (tmp_path / "output" / "script.txt").exists()
    assert (tmp_path / "output" / "voiceover.mp3").exists()
    assert (tmp_path / "output" / "final_video.mp4").exists()
    assert (tmp_path / "output" / "thumbnail.jpg").exists()
