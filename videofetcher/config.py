"""
Configuration management for VideoFetcher
Handles loading, saving, and resetting application settings
"""

import configparser
import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class DownloadOptions:
    """Download-related options"""
    meta: bool = False
    thumbnail: bool = False
    notification: bool = True
    dl_folder: bool = True
    uploader_folder: bool = True
    playlist_folder: bool = True


@dataclass
class AppOptions:
    """Application-related options"""
    background: bool = False


@dataclass
class CodecOptions:
    """Codec configuration"""
    audio_codec: str = "Auto"
    video_codec: str = "mp4"
    resolution: str = "Auto"


@dataclass
class AppConfig:
    """Main configuration container"""
    output_path: str = field(default_factory=lambda: str(Path.cwd()))
    download_options: DownloadOptions = field(default_factory=DownloadOptions)
    app_options: AppOptions = field(default_factory=AppOptions)
    codec_options: CodecOptions = field(default_factory=CodecOptions)
    channel_urls: list[str] = field(default_factory=list)


class ConfigManager:
    """Manages application configuration with automatic save/load"""
    
    CONFIG_FILE = "vf_config.ini"
    
    def __init__(self):
        self.config = configparser.ConfigParser()
        self._config: Optional[AppConfig] = None
    
    @property
    def config_data(self) -> AppConfig:
        """Lazy load configuration"""
        if self._config is None:
            self._config = self.load()
        return self._config
    
    def load(self) -> AppConfig:
        """Load configuration from file or create default"""
        if not os.path.exists(self.CONFIG_FILE):
            self.reset()
        
        self.config.read(self.CONFIG_FILE, encoding='utf-8')
        
        # Parse sections
        output_path = self.config.get("path", "main", fallback=str(Path.cwd()))
        
        download_opts = DownloadOptions(
            meta=self.config.getboolean("dl_options", "meta", fallback=False),
            thumbnail=self.config.getboolean("dl_options", "thumbnail", fallback=False),
            notification=self.config.getboolean("dl_options", "notification", fallback=True),
            dl_folder=self.config.getboolean("dl_options", "dl_folder", fallback=True),
            uploader_folder=self.config.getboolean("dl_options", "uploader_folder", fallback=True),
            playlist_folder=self.config.getboolean("dl_options", "playlist_folder", fallback=True),
        )
        
        app_opts = AppOptions(
            background=self.config.getboolean("app_options", "background", fallback=False),
        )
        
        codec_opts = CodecOptions(
            audio_codec=self.config.get("codec", "audio_codec", fallback="Auto"),
            video_codec=self.config.get("codec", "video_codec", fallback="mp4"),
            resolution=self.config.get("codec", "resolution", fallback="Auto"),
        )
        
        # Parse channel URLs
        channel_str = self.config.get("dl_channel", "URL", fallback='[]')
        try:
            import ast
            channel_urls = ast.literal_eval(channel_str)
        except (ValueError, SyntaxError):
            channel_urls = []
        
        return AppConfig(
            output_path=output_path,
            download_options=download_opts,
            app_options=app_opts,
            codec_options=codec_opts,
            channel_urls=channel_urls,
        )
    
    def save(self, exit_app: bool = False, reset: bool = False) -> None:
        """Save current configuration to file"""
        if reset or self._config is None:
            self.reset()
        
        cfg = self._config
        
        # Write all sections
        self.config["path"] = {"main": cfg.output_path}
        self.config["dl_options"] = {
            "meta": str(cfg.download_options.meta),
            "thumbnail": str(cfg.download_options.thumbnail),
            "notification": str(cfg.download_options.notification),
            "dl_folder": str(cfg.download_options.dl_folder),
            "uploader_folder": str(cfg.download_options.uploader_folder),
            "playlist_folder": str(cfg.download_options.playlist_folder),
        }
        self.config["app_options"] = {
            "background": str(cfg.app_options.background),
        }
        self.config["codec"] = {
            "audio_codec": cfg.codec_options.audio_codec,
            "video_codec": cfg.codec_options.video_codec,
            "resolution": cfg.codec_options.resolution,
        }
        self.config["dl_channel"] = {
            "URL": str(cfg.channel_urls),
        }
        
        with open(self.CONFIG_FILE, 'w', encoding='utf-8') as f:
            self.config.write(f)
    
    def reset(self) -> None:
        """Reset to default configuration"""
        self._config = AppConfig(
            output_path=str(Path.cwd()),
            download_options=DownloadOptions(),
            app_options=AppOptions(),
            codec_options=CodecOptions(),
            channel_urls=[],
        )
        self.save(reset=True)
    
    def update_output_path(self, path: str) -> None:
        """Update output path and save"""
        self._config.output_path = path
        self.save()
    
    def get_audio_extensions(self) -> dict[str, str]:
        """Get mapping of audio codec to file extension"""
        return {
            "aac": "m4a",
            "flac": "flac",
            "m4a": "m4a",
            "mp3": "mp3",
            "opus": "opus",
            "vorbis": "ogg",
            "wav": "wav",
        }
