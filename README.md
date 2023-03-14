| VideoFetcher |
<img width="302" alt="スクリーンショット 2023-03-14 230005" src="https://user-images.githubusercontent.com/101198724/225025920-8de58130-f76d-4347-b0aa-589e478c560e.png">

This is a YouTube downloader created using yt-dlp (Python).

Settings are automatically saved in config.ini.

Note that FFmpeg.exe and FFprobe.exe are used. You do not need to set environment variables, but it is recommended that you place them in the same location as the downloader.

Automatic updates are not available.

| OPTIONS | ###############################################################

>OUTPUT

Select the working folder. Subfolders will be generated around that folder.

>FOLDER

This option allows you to select which folders to generate. If you enable all options, the folder tree will look like this (the [] parts may vary depending on the situation):

[Selected Output Folder]
	└─dl_videos
		├─Playlist
		│ └─[Playlist Title]
		└─[Uploader]

You can choose whether or not to generate the following folders:

DL FOLDER: Generates the "dl_videos" folder.
UPLOADER FOLDER: Generates the "[Uploader]" folder.
PLAYLIST FOLDER: Generates the "Playlist/[Playlist Title]" folder.

>FORMAT

Choose the file format to download. The top format is for audio only, and the bottom format is for video and audio.

| AUDIO | ###############################################################

(The following options are only available when downloading audio only.)

>META

Choose whether or not to embed metadata when downloading audio only.

>THUMBNAIL

Choose whether or not to embed the thumbnail when downloading audio only.

| OTHER | ###############################################################

>NOTIFICATION

Choose whether or not to display a notification when the download is complete. The notification has the following functions:

Play Button: Plays the downloaded file on the spot.
Open Folder Button: Opens the folder where the downloaded file is located.
BACKGROUND

(Not implemented yet, but under consideration.) This feature allows the download to continue in the background even if the window is closed. The process ends after the download is complete.

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
