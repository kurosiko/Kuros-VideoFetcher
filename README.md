# VideoFetcher v2.0

A modern, sleek YouTube/video downloader with an intuitive GUI built using `customtkinter` and `yt-dlp`.

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![Python](https://img.shields.io/badge/python-3.10+-green)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

## ✨ Features

- 🎨 **Modern UI** - Clean, dark-themed interface with smooth animations
- 📥 **Video & Audio Download** - Support for multiple formats and resolutions
- 🎵 **Audio Extraction** - Convert to MP3, AAC, FLAC, and more
- 📁 **Smart Organization** - Auto-sort by uploader, playlist, or custom folders
- 🔔 **Notifications** - Desktop notifications when downloads complete
- 🖱️ **Drag & Drop** - Simply drag URLs into the app
- ⚙️ **Auto-Save Settings** - Your preferences are automatically saved

## 🚀 Quick Start

### Installation with uv (Recommended)

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and install
git clone <repository-url>
cd videofetcher
uv sync

# Run the application
uv run videofetcher
```

### Alternative: pip installation

```bash
pip install -e .
videofetcher
```

## 📋 Requirements

- Python 3.10+
- FFmpeg (for audio conversion and merging)

## ⚙️ Configuration

Settings are automatically saved to `vf_config.ini`. If the app fails to start, delete this file and restart.

### Options

#### General Settings
- **Output Path**: Choose where downloads are saved
- **Download Folder**: Create a `dl_videos` subfolder
- **Uploader Folder**: Organize by uploader name
- **Playlist Folder**: Separate folder for playlists
- **Notifications**: Enable desktop notifications

#### Video Settings
- **Format**: MP4, MKV, or WebM
- **Resolution**: From 144p to 4K (2160p)

#### Audio Settings
- **Format**: Auto, AAC, FLAC, MP3, M4A, Opus, Vorbis, WAV
- **Embed Metadata**: Include title, artist, etc.
- **Embed Thumbnail**: Include album art

## 🎯 Usage

1. **Enter URL**: Paste a video URL in the input field
2. **Configure Settings**: Use the sidebar to adjust download options
3. **Download**: Press Enter or click the Download button
4. **Drag & Drop**: Alternatively, drag a URL directly into the app

### Playlist Mode
Enable "Playlist Mode" in the sidebar to download entire playlists.

### Audio Only Mode
Enable "Audio Only" to extract and download just the audio track.

## 🛠️ Development

```bash
# Install with dev dependencies
uv sync --extra dev

# Run linting
uv run ruff check .
uv run black .

# Run tests
uv run pytest
```

## 📝 Notes

- FFmpeg is required for audio conversion and video merging
- Place `ffmpeg.exe` and `ffprobe.exe` in the same directory or add to PATH
- Windows notifications require the `win11toast` package (installed with `uv sync --extra windows`)

## 🐛 Troubleshooting

- **App won't start**: Delete `vf_config.ini` and restart
- **Download fails**: Ensure FFmpeg is installed and accessible
- **No notifications**: Check system notification settings

## 📬 Feedback

Found a bug or have suggestions? Please open an issue on GitHub!

## 📄 License

MIT License - See LICENSE file for details

## 👨‍💻 Author

Created by kurosiko

- Website: https://kurosiko.github.io/
- Twitter: https://twitter.com/kurosiko
- GitHub: https://github.com/kurosiko
