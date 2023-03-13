# Kuros-VideoFetcher 
This is a YouTube downloader created using yt-dlp. The available options upon startup are expressed with the ">" symbol, and their details with the "・" symbol. The settings are automatically saved to config.ini.

FFmpeg.exe and FFprove.exe are used, so they do not need to be added to the system's PATH variable, but should be placed in the same directory as the downloader.

|OPTIONS|###############################################################

    OUTPUT
    Selects the working folder, where subfolders will be generated.

    FOLDER
    Configures the folder generation settings. If all options are enabled, the folder tree will be as follows (the [] part may vary depending on the context):

[Selected output folder]
└─dl_videos
├─Playlist
│ └─[Playlist title]
└─[uploader]

The options for generating the folders are:
・DL FOLDER: Generates the 'dl_videos' folder.
・UPLOADER FOLDER: Generates the '[uploader]' folder.
・PLAYLIST FOLDER: Generates the 'Playlist' and '[Playlist title]' folders.

    FORMAT
    Selects the format of the files to download. The first option is for downloading only the audio, while the second includes the video as well.

|AUDIO|###############################################################
(Options available when downloading audio only)

    META
    Enables/disables embedding metadata when downloading audio only.

    THUMBNAIL
    Enables/disables embedding thumbnails when downloading audio only.

|OTHER|###############################################################

    NOTIFICATION
    Enables/disables notifications when downloads are complete. The notification has the following options:
    ・Play button: Plays the downloaded file immediately.
    ・Open Folder button: Opens the folder where the downloaded file is located.
    ・Notification click: Opens the downloaded folder when downloading a playlist.

    BACKGROUND
    Not yet implemented. This feature allows downloads to continue in the background even if the window is closed. The process ends when the download is complete.

|OTHER OPTIONS|###############################################################

    PLAYLIST
    Downloads an entire playlist. This option should only be enabled when downloading a playlist, as otherwise an 'NA' folder will be generated inside the 'Playlist' folder and the downloaded files will be saved there.

    AUDIO ONLY
    Downloads only the audio. The format can be selected using the FORMAT option.

|OTHER INFORMATION|==============================================================================

    Input box
    Allows for pasting a URL and starting the download by pressing ENTER.

    DND support
    Supports drag and drop.

    Taskbar icon
    Displays a small icon in the taskbar. Right-clicking on it displays a menu with various options.

If you encounter any bugs or have feedback, please contact the developer via DM on Twitter:
|Twitter|
https://twitter.com/Bkurosiko

|MEGA|

    youtube-dl old ver
    https://mega.nz/folder/pSlmgbQA#MpLR8fWfKuGUeUEmwteODg

    youtube-dl new ver
    https://mega.nz/folder/AfFRkJLK#BCLR8DbJeFrWuoarCFK8BA

    other
    https://mega.nz/fm/BPszyKjS


|Translate by ChatGPT|
