"""
Main application entry point for VideoFetcher
Combines GUI, configuration, and download management
"""

import tkinter as tk
import threading
import sys
import os
from pathlib import Path

import customtkinter as ctk
from tkinterdnd2 import TkinterDnD, DND_TEXT

from .config import ConfigManager
from .gui import Sidebar, SettingsPanel, DownloadProgress, DownloadItem
from .downloader import DownloadManager, DownloadSettings


class VideoFetcherApp:
    """Main application class"""
    
    def __init__(self):
        # Initialize configuration
        self.config_manager = ConfigManager()
        cfg = self.config_manager.config_data
        
        # Create main window with drag-and-drop support
        self.root = TkinterDnD.Tk()
        self.root.title("VideoFetcher v2.0")
        self.root.geometry("800x600")
        self.root.minsize(700, 500)
        
        # Set dark mode
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Configure window style
        self.root.configure(bg="#1a1a1a")
        
        # Initialize state variables
        self.output_var = tk.StringVar(value=cfg.output_path)
        self.dl_folder_var = tk.BooleanVar(value=cfg.download_options.dl_folder)
        self.uploader_folder_var = tk.BooleanVar(value=cfg.download_options.uploader_folder)
        self.playlist_folder_var = tk.BooleanVar(value=cfg.download_options.playlist_folder)
        self.notification_var = tk.BooleanVar(value=cfg.download_options.notification)
        self.meta_var = tk.BooleanVar(value=cfg.download_options.meta)
        self.thumbnail_var = tk.BooleanVar(value=cfg.download_options.thumbnail)
        self.video_codec_var = tk.StringVar(value=cfg.codec_options.video_codec)
        self.audio_codec_var = tk.StringVar(value=cfg.codec_options.audio_codec)
        self.resolution_var = tk.StringVar(value=cfg.codec_options.resolution)
        self.playlist_var = tk.BooleanVar(value=False)
        self.audio_only_var = tk.BooleanVar(value=False)
        
        # Setup UI components
        self.setup_ui()
        
        # Bind events
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.bind("<Return>", self.start_download)
        
        # Register drag-and-drop
        self.root.drop_target_register(DND_TEXT)
        self.root.dnd_bind('<<Drop>>', self.on_drop)
        
        print("✓ VideoFetcher initialized successfully")
    
    def setup_ui(self):
        """Initialize the user interface"""
        # Main container
        main_frame = ctk.CTkFrame(self.root, fg_color="#1a1a1a", corner_radius=0)
        main_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # URL input area
        url_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        url_frame.place(relx=0.32, rely=0.05, relwidth=0.65, relheight=0.08)
        
        self.url_entry = ctk.CTkEntry(
            url_frame,
            placeholder_text="🔗 Paste video URL here...",
            height=40,
            corner_radius=8,
            border_width=2,
            border_color="#3b8ed0",
        )
        self.url_entry.pack(fill=tk.X, expand=True)
        
        # Download button
        download_btn = ctk.CTkButton(
            main_frame,
            text="⬇️ Download",
            command=self.start_download,
            height=40,
            corner_radius=8,
            fg_color="#3b8ed0",
            hover_color="#36719f",
        )
        download_btn.place(relx=0.32, rely=0.14, relwidth=0.65)
        
        # Progress area
        progress_frame = ctk.CTkScrollableFrame(
            main_frame,
            fg_color="#1e1e1e",
            corner_radius=8,
            border_width=0,
        )
        progress_frame.place(relx=0.32, rely=0.22, relwidth=0.65, relheight=0.75)
        
        self.download_progress = DownloadProgress(progress_frame)
        
        # Initialize sidebar and settings panel
        self.settings_panel = SettingsPanel(self.root, self.config_manager)
        
        self.sidebar = Sidebar(
            self.root,
            self.settings_panel,
            self.output_var,
            self.dl_folder_var,
            self.uploader_folder_var,
            self.playlist_folder_var,
            self.notification_var,
            self.video_codec_var,
            self.resolution_var,
            self.audio_codec_var,
            self.meta_var,
            self.thumbnail_var,
            self.playlist_var,
            self.audio_only_var,
        )
        
        # Save config on setting changes
        for var in [
            self.dl_folder_var, self.uploader_folder_var,
            self.playlist_folder_var, self.notification_var,
            self.meta_var, self.thumbnail_var,
            self.video_codec_var, self.audio_codec_var,
            self.resolution_var,
        ]:
            if isinstance(var, tk.BooleanVar):
                var.trace_add("write", lambda *args: self.config_manager.save())
            else:
                var.trace_add("write", lambda *args: self.config_manager.save())
    
    def get_download_settings(self) -> DownloadSettings:
        """Build download settings from current UI state"""
        return DownloadSettings(
            meta=self.meta_var.get(),
            thumbnail=self.thumbnail_var.get(),
            notification=self.notification_var.get(),
            dl_folder=self.dl_folder_var.get(),
            uploader_folder=self.uploader_folder_var.get(),
            playlist_folder=self.playlist_folder_var.get(),
            video_codec=self.video_codec_var.get(),
            audio_codec=self.audio_codec_var.get(),
            resolution=self.resolution_var.get(),
            playlist=self.playlist_var.get(),
            audio_only=self.audio_only_var.get(),
        )
    
    def start_download(self, event=None):
        """Initiate download from URL entry"""
        url = self.url_entry.get().strip()
        if not url:
            self.show_error("Please enter a URL")
            return
        
        self.url_entry.delete(0, tk.END)
        self.perform_download(url)
    
    def on_drop(self, event):
        """Handle drag-and-drop URL"""
        url = event.data.strip()
        if url:
            self.perform_download(url)
    
    def perform_download(self, url: str):
        """Start download process"""
        settings = self.get_download_settings()
        downloader = DownloadManager(self.output_var.get(), settings)
        
        # Create progress indicator
        progress_item = self.download_progress.add_download(url)
        
        def progress_callback(status: str, **kwargs):
            """Update UI based on download progress"""
            if status == 'downloading':
                title = kwargs.get('title', 'Loading...')
                progress = kwargs.get('progress', 0)
                playlist_title = kwargs.get('playlist_title', '')
                playlist_index = kwargs.get('playlist_index', 0)
                playlist_count = kwargs.get('playlist_count', 0)
                
                index_str = f"{playlist_index}/{playlist_count}" if playlist_count else ""
                
                progress_item.update_progress(
                    title=title,
                    progress=progress,
                    playlist_title=playlist_title,
                    index=index_str,
                )
                
            elif status == 'finished':
                progress_item.update_progress(
                    title="Processing...",
                    progress=1.0,
                )
                
            elif status == 'complete':
                info = kwargs.get('info')
                if info and self.notification_var.get():
                    self.send_notification(info)
                progress_item.destroy()
                
            elif status == 'error':
                error = kwargs.get('error', 'Unknown error')
                progress_item.title_label.configure(text=f"❌ Error: {error}")
                progress_item.title_label.configure(text_color="#ff6b6b")
        
        # Start download
        downloader.download(url, progress_callback)
    
    def send_notification(self, info):
        """Send desktop notification (platform-specific)"""
        try:
            # Try Windows notifications
            import win11toast
            
            def notify():
                opts = {
                    'app_id': 'VideoFetcher',
                    'duration': 'short',
                    'title': info.uploader or 'Download Complete',
                    'body': info.title or '',
                }
                
                # Add buttons
                if info.output_path:
                    opts['buttons'] = [
                        {'activationType': 'protocol', 'arguments': info.output_path, 'content': 'Play'},
                        {'activationType': 'protocol', 'arguments': os.path.dirname(info.output_path), 'content': 'Open Folder'},
                    ]
                
                win11toast.toast(**opts)
            
            threading.Thread(target=notify, daemon=True).start()
        except ImportError:
            # Fallback to console message
            print(f"✓ Download complete: {info.title}")
    
    def show_error(self, message: str):
        """Display error message"""
        messagebox.showerror("Error", message)
    
    def on_close(self):
        """Handle application close"""
        self.config_manager.save()
        self.root.destroy()
    
    def run(self):
        """Start the application"""
        print("🚀 Starting VideoFetcher...")
        self.root.mainloop()


def main():
    """Application entry point"""
    app = VideoFetcherApp()
    app.run()


if __name__ == "__main__":
    main()
