"""
Download manager for VideoFetcher
Handles yt-dlp operations and progress tracking
"""

import os
import threading
from typing import Optional, Dict, Any
from pathlib import Path
from dataclasses import dataclass, field

from yt_dlp import YoutubeDL


@dataclass
class DownloadInfo:
    """Information about a download"""
    title: Optional[str] = None
    uploader: Optional[str] = None
    is_playlist: bool = False
    playlist_title: Optional[str] = None
    playlist_count: Optional[int] = None
    playlist_index: Optional[int] = None
    thumbnail: Optional[str] = None
    output_path: Optional[str] = None


@dataclass
class DownloadSettings:
    """Download configuration"""
    meta: bool = False
    thumbnail: bool = False
    notification: bool = True
    dl_folder: bool = True
    uploader_folder: bool = True
    playlist_folder: bool = True
    video_codec: str = "mp4"
    audio_codec: str = "Auto"
    resolution: str = "Auto"
    playlist: bool = False
    audio_only: bool = False
    audio_extensions: Dict[str, str] = field(default_factory=lambda: {
        "aac": "m4a",
        "flac": "flac",
        "m4a": "m4a",
        "mp3": "mp3",
        "opus": "opus",
        "vorbis": "ogg",
        "wav": "wav",
    })


class ProgressHook:
    """yt-dlp progress hook for real-time updates"""
    
    def __init__(self, callback):
        self.callback = callback
        self.info = DownloadInfo()
    
    def __call__(self, data: Dict[str, Any]):
        """Called by yt-dlp during download"""
        if data['status'] == 'downloading':
            # Extract metadata
            info_dict = data.get('info_dict', {})
            self.info.title = info_dict.get('title')
            self.info.uploader = info_dict.get('uploader', info_dict.get('id'))
            
            # Handle playlist info
            if info_dict.get('playlist'):
                self.info.is_playlist = True
                self.info.playlist_title = info_dict.get('playlist_title')
                self.info.playlist_count = info_dict.get('playlist_count')
                self.info.playlist_index = info_dict.get('playlist_index')
            else:
                self.info.is_playlist = False
            
            # Calculate progress
            try:
                progress = data['downloaded_bytes'] / data['total_bytes']
            except (KeyError, TypeError, ZeroDivisionError):
                try:
                    progress = data['fragment_index'] / data['fragment_count']
                except (KeyError, TypeError, ZeroDivisionError):
                    progress = 0.0
            
            self.callback(
                status='downloading',
                title=self.info.title,
                progress=progress,
                playlist_title=self.info.playlist_title,
                playlist_index=self.info.playlist_index,
                playlist_count=self.info.playlist_count,
            )
            
        elif data['status'] == 'finished':
            self.callback(
                status='finished',
                title=self.info.title,
                progress=1.0,
            )


class DownloadManager:
    """Manages video/audio downloads using yt-dlp"""
    
    def __init__(self, output_path: str, settings: DownloadSettings):
        self.output_path = output_path
        self.settings = settings
        self.current_info = DownloadInfo()
    
    def build_ydl_options(self, progress_hook: ProgressHook) -> Dict[str, Any]:
        """Build yt-dlp options based on settings"""
        output_dir = self.output_path
        
        # Build output path
        if self.settings.dl_folder:
            output_dir = os.path.join(output_dir, 'dl_videos')
        if self.settings.uploader_folder:
            output_dir = os.path.join(output_dir, '%(uploader)s')
        
        # Handle playlist folder
        if not self.settings.playlist:
            noplaylist = True
        elif self.settings.playlist_folder and self.settings.dl_folder:
            output_dir = os.path.join(self.output_path, 'dl_videos', 'Playlist', '%(playlist)s')
            noplaylist = False
        elif self.settings.playlist_folder:
            output_dir = os.path.join(self.output_path, 'Playlist', '%(playlist)s')
            noplaylist = False
        else:
            noplaylist = False
        
        # Build format string
        if self.settings.audio_only:
            format_str = "bestaudio"
        elif self.settings.resolution == "Auto":
            format_str = "bv+ba[ext=m4a]/bv+ba/b"
        else:
            height = self.settings.resolution.replace('p', '')
            format_str = f"bv[height={height}]+ba[ext=m4a]/bv+ba[ext=m4a]/b"
        
        # Build post-processors for audio
        postprocessors = []
        if self.settings.audio_only:
            if self.settings.audio_codec != "Auto":
                postprocessors.append({
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': self.settings.audio_codec,
                })
            
            if self.settings.meta and self.settings.audio_codec not in ["aac", "vorbis", "wav"]:
                postprocessors.append({'key': 'FFmpegMetadata'})
            
            if self.settings.thumbnail and self.settings.audio_codec in ["m4a", "mp3"]:
                postprocessors.append({
                    'key': 'EmbedThumbnail',
                    'already_have_thumbnail': False,
                })
        
        opts = {
            'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
            'format': format_str,
            'progress_hooks': [progress_hook],
            'ignoreerrors': False,
            'noplaylist': noplaylist,
        }
        
        # Add video codec setting
        if not self.settings.audio_only and self.settings.video_codec != "webm":
            opts['merge_output_format'] = self.settings.video_codec
        
        # Add post-processors
        if postprocessors:
            opts['postprocessors'] = postprocessors
        
        return opts
    
    def download(self, url: str, progress_callback=None) -> threading.Thread:
        """Start download in background thread"""
        
        def run_download():
            progress_hook = ProgressHook(progress_callback) if progress_callback else None
            ydl_opts = self.build_ydl_options(progress_hook)
            
            try:
                with YoutubeDL(ydl_opts) as ydl:
                    data = ydl.extract_info(url, download=True)
                    
                    # Store download info
                    self.current_info.title = data.get('title')
                    self.current_info.uploader = data.get('uploader')
                    self.current_info.output_path = ydl.prepare_filename(data)
                    
                    # Handle playlist
                    if data.get('_type') == 'playlist':
                        self.current_info.is_playlist = True
                        self.current_info.playlist_title = data.get('title')
                        if data.get('entries'):
                            self.current_info.thumbnail = data['entries'][0].get('thumbnail')
                            self.current_info.output_path = data['entries'][0].get(
                                'requested_downloads', [{}]
                            )[0].get('__finaldir', self.current_info.output_path)
                    else:
                        self.current_info.is_playlist = False
                        self.current_info.thumbnail = data.get('thumbnail')
                    
                    # Adjust output path for audio conversion
                    if self.settings.audio_only and self.settings.audio_codec != "Auto":
                        ext = self.settings.audio_extensions.get(
                            self.settings.audio_codec, 
                            self.settings.audio_codec
                        )
                        base, _ = os.path.splitext(self.current_info.output_path)
                        self.current_info.output_path = f"{base}.{ext}"
                    
                    if progress_callback:
                        progress_callback(
                            status='complete',
                            info=self.current_info,
                        )
                        
            except Exception as e:
                if progress_callback:
                    progress_callback(
                        status='error',
                        error=str(e),
                        url=url,
                    )
        
        thread = threading.Thread(target=run_download, daemon=True)
        thread.start()
        return thread
