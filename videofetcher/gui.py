"""
Modern GUI for VideoFetcher using customtkinter
Features a sleek, dark-themed interface with smooth animations
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import webbrowser
from typing import Optional, Callable
import customtkinter as ctk
from tkinterdnd2 import TkinterDnD, DND_TEXT

from .config import ConfigManager, AppConfig


class ModernFrame(ctk.CTkFrame):
    """Base frame with modern styling"""
    
    def __init__(self, master, corner_radius: int = 10, **kwargs):
        super().__init__(master, corner_radius=corner_radius, **kwargs)
        
    def place_relative(self, relx: float = 0, rely: float = 0, 
                       relwidth: float = 1, relheight: float = 1):
        """Convenience method for relative placement"""
        self.place(relx=relx, rely=rely, relwidth=relwidth, relheight=relheight)
        return self


class ModernButton(ctk.CTkButton):
    """Styled button with consistent appearance"""
    
    def __init__(self, master, text: str, command: Callable = None,
                 fg_color: str = "#3b8ed0", hover_color: str = "#36719f",
                 height: int = 40, corner_radius: int = 8, **kwargs):
        super().__init__(
            master, text=text, command=command,
            fg_color=fg_color, hover_color=hover_color,
            height=height, corner_radius=corner_radius,
            **kwargs
        )
    
    def place_relative(self, relx: float = 0, rely: float = 0,
                       relwidth: float = 0.9, relheight: float = 0.08):
        self.place(relx=relx, rely=rely, relwidth=relwidth, relheight=relheight)
        return self


class ModernSwitch(ctk.CTkSwitch):
    """Modern toggle switch"""
    
    def __init__(self, master, text: str, variable: tk.BooleanVar = None,
                 command: Callable = None, **kwargs):
        super().__init__(
            master, text=text, variable=variable, command=command,
            fg_color="#6a6a6a", progress_color="#3b8ed0",
            text_color=("gray90", "gray10"),
            **kwargs
        )
    
    def place_relative(self, relx: float = 0.05, rely: float = 0,
                       relwidth: float = 0.9, relheight: float = 0.06):
        self.place(relx=relx, rely=rely, relwidth=relwidth, relheight=relheight)
        return self


class ModernComboBox(ctk.CTkComboBox):
    """Styled combo box"""
    
    def __init__(self, master, values: list, variable: tk.StringVar = None,
                 command: Callable = None, **kwargs):
        super().__init__(
            master, values=values, variable=variable, command=command,
            state="readonly",
            **kwargs
        )
    
    def place_relative(self, relx: float = 0.05, rely: float = 0,
                       relwidth: float = 0.9, relheight: float = 0.08):
        self.place(relx=relx, rely=rely, relwidth=relwidth, relheight=relheight)
        return self


class SettingsPanel:
    """Manages settings panels that slide in from the side"""
    
    COLORS = {
        'bg_dark': "#1a1a1a",
        'bg_panel': "#2d2d2d",
        'bg_header': "#3b8ed0",
        'text_white': "#ffffff",
        'text_gray': "#a0a0a0",
    }
    
    def __init__(self, root: ctk.CTk, config_manager: ConfigManager):
        self.root = root
        self.config_manager = config_manager
        self.current_frame: Optional[ctk.CTkFrame] = None
        
    def create_header(self, parent: ctk.CTkFrame, title: str) -> ctk.CTkLabel:
        """Create a styled header label"""
        header = ctk.CTkLabel(
            parent, text=title,
            fg_color=self.COLORS['bg_header'],
            text_color=self.COLORS['text_white'],
            font=ctk.CTkFont(size=16, weight="bold")
        )
        header.place(relx=0, rely=0, relheight=0.08, relwidth=1)
        return header
    
    def clear_current_frame(self):
        """Remove current settings panel"""
        if self.current_frame is not None:
            self.current_frame.destroy()
            self.current_frame = None
    
    def show_general_settings(self, output_var: tk.StringVar,
                              dl_folder_var: tk.BooleanVar,
                              uploader_folder_var: tk.BooleanVar,
                              playlist_folder_var: tk.BooleanVar,
                              notification_var: tk.BooleanVar):
        """Display general settings panel"""
        self.clear_current_frame()
        
        self.current_frame = ModernFrame(self.root, fg_color=self.COLORS['bg_panel'])
        self.current_frame.place_relative(relx=0.3, relwidth=0.7)
        
        self.create_header(self.current_frame, "GENERAL SETTINGS")
        
        # Output path display and browse button
        path_label = ctk.CTkLabel(
            self.current_frame, textvariable=output_var,
            text_color=self.COLORS['text_white'],
            anchor="w"
        )
        path_label.place(relx=0.05, rely=0.12, relheight=0.08, relwidth=0.65)
        
        ModernButton(
            self.current_frame, text="📁 Browse",
            command=lambda: self.browse_output(output_var),
            fg_color="#4a4a4a"
        ).place_relative(relx=0.72, rely=0.12, relwidth=0.25)
        
        # Folder options
        ModernSwitch(
            self.current_frame, text="Download Folder",
            variable=dl_folder_var
        ).place_relative(rely=0.25)
        
        ModernSwitch(
            self.current_frame, text="Uploader Folder",
            variable=uploader_folder_var
        ).place_relative(rely=0.35)
        
        ModernSwitch(
            self.current_frame, text="Playlist Folder",
            variable=playlist_folder_var
        ).place_relative(rely=0.45)
        
        ModernSwitch(
            self.current_frame, text="Notifications",
            variable=notification_var
        ).place_relative(rely=0.55)
        
        # Close button
        ModernButton(
            self.current_frame, text="✕ Close",
            command=self.clear_current_frame,
            fg_color="#4a4a4a"
        ).place_relative(rely=0.85)
    
    def show_video_settings(self, video_codec_var: tk.StringVar,
                           resolution_var: tk.StringVar):
        """Display video settings panel"""
        self.clear_current_frame()
        
        self.current_frame = ModernFrame(self.root, fg_color=self.COLORS['bg_panel'])
        self.current_frame.place_relative(relx=0.3, relwidth=0.7)
        
        self.create_header(self.current_frame, "VIDEO SETTINGS")
        
        video_formats = ["mp4", "mkv", "webm"]
        resolutions = ["Auto", "144p", "240p", "360p", "480p", "720p", "1080p", "1440p", "2160p"]
        
        ctk.CTkLabel(
            self.current_frame, text="Video Format:",
            text_color=self.COLORS['text_white']
        ).place(relx=0.05, rely=0.12, relheight=0.06)
        
        ModernComboBox(
            self.current_frame, values=video_formats,
            variable=video_codec_var
        ).place_relative(rely=0.18)
        
        ctk.CTkLabel(
            self.current_frame, text="Resolution:",
            text_color=self.COLORS['text_white']
        ).place(relx=0.05, rely=0.30, relheight=0.06)
        
        ModernComboBox(
            self.current_frame, values=resolutions,
            variable=resolution_var
        ).place_relative(rely=0.36)
        
        ModernButton(
            self.current_frame, text="✕ Close",
            command=self.clear_current_frame,
            fg_color="#4a4a4a"
        ).place_relative(rely=0.85)
    
    def show_audio_settings(self, audio_codec_var: tk.StringVar,
                           meta_var: tk.BooleanVar,
                           thumbnail_var: tk.BooleanVar):
        """Display audio settings panel"""
        self.clear_current_frame()
        
        self.current_frame = ModernFrame(self.root, fg_color=self.COLORS['bg_panel'])
        self.current_frame.place_relative(relx=0.3, relwidth=0.7)
        
        self.create_header(self.current_frame, "AUDIO SETTINGS")
        
        audio_formats = ["Auto", "aac", "flac", "mp3", "m4a", "opus", "vorbis", "wav"]
        
        ctk.CTkLabel(
            self.current_frame, text="Audio Format:",
            text_color=self.COLORS['text_white']
        ).place(relx=0.05, rely=0.12, relheight=0.06)
        
        ModernComboBox(
            self.current_frame, values=audio_formats,
            variable=audio_codec_var
        ).place_relative(rely=0.18)
        
        ModernSwitch(
            self.current_frame, text="Embed Metadata",
            variable=meta_var
        ).place_relative(rely=0.32)
        
        ModernSwitch(
            self.current_frame, text="Embed Thumbnail",
            variable=thumbnail_var
        ).place_relative(rely=0.42)
        
        ModernButton(
            self.current_frame, text="✕ Close",
            command=self.clear_current_frame,
            fg_color="#4a4a4a"
        ).place_relative(rely=0.85)
    
    def show_about_panel(self):
        """Display about/credits panel"""
        self.clear_current_frame()
        
        self.current_frame = ModernFrame(self.root, fg_color=self.COLORS['bg_panel'])
        self.current_frame.place_relative(relx=0.3, relwidth=0.7)
        
        self.create_header(self.current_frame, "ABOUT")
        
        links = [
            ("🌐 Website", "https://kurosiko.github.io/"),
            ("⚙️ FFmpeg", "https://ffmpeg.org/"),
            ("💻 GitHub", "https://github.com/kurosiko/Kuros-VideoFetcher"),
            ("🐦 Twitter", "https://twitter.com/kurosiko"),
            ("📺 YouTube", "https://www.youtube.com/channel/UCkbPdwURHuIG63f5ZTj3fjw"),
        ]
        
        for i, (text, url) in enumerate(links):
            btn = ctk.CTkButton(
                self.current_frame, text=text,
                fg_color="transparent",
                text_color="#47bcf2",
                hover_color="#dee6ff",
                anchor="w",
                command=lambda u=url: webbrowser.open(u)
            )
            btn.place(relx=0.05, rely=0.15 + (i * 0.12), relheight=0.08, relwidth=0.9)
        
        ModernButton(
            self.current_frame, text="✕ Close",
            command=self.clear_current_frame,
            fg_color="#4a4a4a"
        ).place_relative(rely=0.85)
    
    def browse_output(self, output_var: tk.StringVar):
        """Open folder browser and update output path"""
        folder = filedialog.askdirectory()
        if folder:
            output_var.set(folder)
            self.config_manager.update_output_path(folder)


class Sidebar:
    """Left sidebar with navigation buttons"""
    
    COLORS = {
        'bg_sidebar': "#1e1e1e",
        'bg_header': "#000000",
        'text_white': "#ffffff",
    }
    
    def __init__(self, root: ctk.CTk, settings_panel: SettingsPanel,
                 output_var: tk.StringVar, dl_folder_var: tk.BooleanVar,
                 uploader_folder_var: tk.BooleanVar,
                 playlist_folder_var: tk.BooleanVar,
                 notification_var: tk.BooleanVar,
                 video_codec_var: tk.StringVar, resolution_var: tk.StringVar,
                 audio_codec_var: tk.StringVar, meta_var: tk.BooleanVar,
                 thumbnail_var: tk.BooleanVar,
                 playlist_var: tk.BooleanVar, audio_only_var: tk.BooleanVar):
        self.root = root
        self.settings_panel = settings_panel
        
        self.frame = ModernFrame(root, fg_color=self.COLORS['bg_sidebar'], corner_radius=0)
        self.frame.place_relative(relwidth=0.3)
        
        # Header
        header = ctk.CTkLabel(
            self.frame, text="⚙️ SETTINGS",
            fg_color=self.COLORS['bg_header'],
            text_color=self.COLORS['text_white'],
            font=ctk.CTkFont(size=18, weight="bold")
        )
        header.place(relx=0, rely=0, relheight=0.1, relwidth=1)
        
        # Navigation buttons
        buttons = [
            ("📋 General", lambda: settings_panel.show_general_settings(
                output_var, dl_folder_var, uploader_folder_var,
                playlist_folder_var, notification_var
            )),
            ("🎬 Video", lambda: settings_panel.show_video_settings(
                video_codec_var, resolution_var
            )),
            ("🎵 Audio", lambda: settings_panel.show_audio_settings(
                audio_codec_var, meta_var, thumbnail_var
            )),
            ("ℹ️ About", settings_panel.show_about_panel),
        ]
        
        for i, (text, cmd) in enumerate(buttons):
            ModernButton(
                self.frame, text=text, command=cmd,
                fg_color="transparent", hover_color="#3a3a3a"
            ).place_relative(rely=0.12 + (i * 0.1), relwidth=0.95, relx=0.025)
        
        # Quick toggles at bottom
        ctk.CTkLabel(
            self.frame, text="QUICK OPTIONS",
            text_color=self.COLORS['text_white'],
            font=ctk.CTkFont(weight="bold")
        ).place(relx=0.05, rely=0.65, relheight=0.06)
        
        ModernSwitch(
            self.frame, text="📁 Playlist Mode",
            variable=playlist_var,
            text_color=self.COLORS['text_white']
        ).place_relative(rely=0.73)
        
        ModernSwitch(
            self.frame, text="🎵 Audio Only",
            variable=audio_only_var,
            text_color=self.COLORS['text_white']
        ).place_relative(rely=0.82)


class DownloadProgress:
    """Displays download progress with modern styling"""
    
    COLORS = {
        'bg_frame': "#1a1a1a",
        'bg_playlist': "#404040",
        'bg_title': "#333333",
        'text_white': "#f7f7f8",
    }
    
    def __init__(self, parent):
        self.parent = parent
        self.frames = []
    
    def add_download(self, url: str) -> 'DownloadItem':
        """Create a new download progress item"""
        item = DownloadItem(self.parent, url, self.COLORS)
        self.frames.append(item)
        return item
    
    def remove_completed(self, item: 'DownloadItem'):
        """Remove completed download from list"""
        if item in self.frames:
            self.frames.remove(item)


class DownloadItem(ctk.CTkFrame):
    """Individual download progress indicator"""
    
    def __init__(self, parent, url: str, colors: dict):
        super().__init__(parent, fg_color=colors['bg_frame'], corner_radius=0)
        self.pack(fill=tk.X, padx=2, pady=2)
        
        # Playlist info (top left)
        self.playlist_label = ctk.CTkLabel(
            self, text="", anchor="w",
            fg_color=colors['bg_playlist'],
            text_color=colors['text_white'],
            corner_radius=0
        )
        self.playlist_label.place(relheight=0.35, relwidth=0.75)
        
        # Title (bottom left)
        self.title_label = ctk.CTkLabel(
            self, text=url, anchor="w",
            fg_color=colors['bg_title'],
            text_color=colors['text_white'],
            corner_radius=0
        )
        self.title_label.place(relheight=0.35, relwidth=0.75, rely=0.35)
        
        # Playlist index (top right)
        self.index_label = ctk.CTkLabel(
            self, text="", anchor="e",
            fg_color=colors['bg_playlist'],
            text_color=colors['text_white'],
            corner_radius=0
        )
        self.index_label.place(relheight=0.35, relwidth=0.25, relx=0.75)
        
        # Progress percentage (bottom right)
        self.progress_label = ctk.CTkLabel(
            self, text="", anchor="e",
            fg_color=colors['bg_title'],
            text_color=colors['text_white'],
            corner_radius=0
        )
        self.progress_label.place(relheight=0.35, relwidth=0.25, relx=0.75, rely=0.35)
        
        # Progress bar
        self.progressbar = ctk.CTkProgressBar(self, corner_radius=0)
        self.progressbar.set(0)
        self.progressbar.place(relheight=0.15, relwidth=1, rely=0.7)
    
    def update_progress(self, title: str, progress: float, 
                       playlist_title: str = "", index: str = ""):
        """Update progress display"""
        self.title_label.configure(text=title)
        self.progressbar.set(progress)
        self.progress_label.configure(text=f"{int(progress * 100)}%")
        
        if playlist_title:
            self.playlist_label.configure(text=playlist_title)
            self.index_label.configure(text=index)
    
    def destroy(self):
        """Clean up the widget"""
        try:
            super().destroy()
        except:
            pass
