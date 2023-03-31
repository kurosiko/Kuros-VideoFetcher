

<img width="303" alt="スクリーンショット 2023-03-17 214511" src="https://user-images.githubusercontent.com/101198724/225908683-5d356c6a-2b40-464c-94bd-99f6e4b2e2d8.png">

<br>
| VideoFetcher |

This is a YouTube downloader created using yt-dlp (Python).

Settings are automatically saved in config.ini.

| Note |

that FFmpeg.exe and FFprobe.exe are used. You do not need to set environment variables, but it is recommended that you place them in the same location as the downloader.

Automatic updates are not available.

| OPTIONS | ###############################################################

[General]

>OUTPUT

Select the working folder. Subfolders will be generated around that folder.

>FOLDER

This option allows you to select which folders to generate.
You can specify whether to generate the following floors

You can choose whether or not to generate the following folders

[selected folder]<br>
	&emsp;└─dl_videos<br>
	&emsp;&emsp;&emsp;&emsp;├─[uploader name]<br>
	&emsp;&emsp;&emsp;&emsp;└─Playlist<br>
	&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;└─[playlist title]<br>


DL FOLDER: Generates the "dl_videos" folder.
UPLOADER FOLDER: Generates the "[Uploader]" folder.
PLAYLIST FOLDER: Generates the "Playlist/[Playlist Title]" folder.

>FORMAT

Choose the file format to download. The top format is for audio only, and the bottom format is for video and audio.

Support Fomat:

Video:mp4, mkv,webm

Audio:acc,flac,mp3,m4a,opus,vorbis,wav,webm


>NOTIFICATION

Choose whether or not to display a notification when the download is complete. The notification has the following functions:

Play Button: Plays the downloaded file on the spot.
Open Folder Button: Opens the folder where the downloaded file is located.

| AUDIO | ###############################################################

(The following options are only available when downloading audio only.)

>META

Choose whether or not to embed metadata when downloading audio only.

>THUMBNAIL

Choose whether or not to embed the thumbnail when downloading audio only.

| OTHER | ###############################################################

>PLAYLIST

Enables downloading entire playlists. Since the program cannot automatically detect playlists, please enable this option only when downloading playlists. Otherwise, an "NA" folder will be generated inside the "Playlist" folder, and the downloaded files will be saved in there.

>AUDIO ONLY

Downloads only the audio file. The format can be selected from the FORMAT option.

| OTHER EXPLANATIONS | ###############################################################

>INPUT BOX

Paste the URL and press ENTER to start downloading.

>DND SUPPORT

The program supports drag and drop.

>TASKBAR  TRAY ICON

The program displays a small icon on the taskbar. Right-click to select various options.



For bug reports and feedback, please visit the following GitHub page:

| Github |

https://github.com/kurosiko
