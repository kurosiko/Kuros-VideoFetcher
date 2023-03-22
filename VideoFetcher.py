import tkinter
from tkinter import filedialog,messagebox
import ctypes
import customtkinter
import os
import pystray
import configparser
import webbrowser
import PIL.Image
import PIL.ImageTk
import threading
import io
import requests
import win11toast
import math
import tkinterdnd2
from yt_dlp import YoutubeDL
import sys
#import pprint

customtkinter.set_appearance_mode("Dark")

sys.stdout = sys.stderr = open('nul', 'w')

ctypes.windll.shcore.SetProcessDpiAwareness(True)
config = configparser.ConfigParser()

class Config:

    def error(self):
        messagebox.showerror("KeyError","delete config file and restart again!")
        exit()

    def load(self):
        if not os.path.exists("./config.ini"):
            self.reset()
            with open("config.ini","w",encoding='utf-8') as ini_file:
                config.write(ini_file)
        config.read("config.ini",encoding='utf-8')
        data = {}
        for section in config.sections():
            data[section] = {}
            for option in config.options(section):
                if section in "dl_options":
                    data[section][option] = config.getboolean(section,option) 
                else:
                    data[section][option] = config.get(section,option)
        return data
    
    def save(self,event=None,exit_=False,reset=False):
        global config_data,meta,thumbnail,notification,dl_folder,uploader_folder,playlist_folder
        if not reset:
            config_data = {
                "path":
                {
                "main":output
                },
                "dl_options":
                {
                "meta":meta.get(),
                "thumbnail":thumbnail.get(),
                "notification":notification.get(),
                "dl_folder":dl_folder.get(),
                "uploader_folder":uploader_folder.get(),
                "playlist_folder":playlist_folder.get(),
                },
                "codec":
                {"audio_codec":audio_codec.get(),
                "video_codec":video_codec.get(),
                "resolution":resolution.get()
                }
            }
        for section,options in dict(config_data).items():
            config[section] = {}
            for option,value in dict(options).items():
                config[section][option] = str(value)
        with open('config.ini',"w",encoding='utf-8') as ini_file:
                config.write(ini_file)
        if exit_:
            root.destroy()
            icon.stop()
            exit()

    def reset(self):
        global config_data
        config_data = {
            "path":
            {
            "main":os.getcwd()
            },
            "dl_options":
            {
            "meta":False,
            "thumbnail":False,
            "notification":True,
            "dl_folder":True,
            "uploader_folder":True,
            "playlist_folder":True,
            },
            "codec":
            {"audio_codec":"Auto",
            "video_codec":"mp4",
            "resolution":"Auto"
            },
            }
        self.save(reset=True)

    def image(self):
        def run():
            global win_icon,icon
            win_icon = PIL.Image.open(io.BytesIO(requests.get("https://i.imgur.com/w5eKxTm.png",timeout=(5,5)).content))
            root.iconphoto(True,PIL.ImageTk.PhotoImage(win_icon))
            menu = pystray.Menu(
                pystray.MenuItem(
                "Info",
                "v1.2"
                ),
                pystray.MenuItem(
                "Jump To Homepage",
                lambda:webbrowser.open("https://kurosiko.github.io/")
                )
            )
            icon = pystray.Icon("Neural",icon=win_icon,menu=menu,title="VideoFetcher is running!")
            icon.run()
        threading.Thread(target=run,daemon=True).start()

class Gui:

    def __init__(self):
        self.current_frame = None

    def open_browser(self,URL):
        webbrowser.open(url=URL)

    def add_button(self, text=None, master=None, cmd=None, x=0, y=0, height=0.1, width=1,corner_radius=0,fg_color="transparent",anchor=tkinter.N):
        if master == None:
            master = self.current_frame
        button = customtkinter.CTkButton(master=master, text=text, command=cmd,
                                        corner_radius=corner_radius, height=40,border_spacing=10,
                                        fg_color=fg_color,hover_color=("gray70", "gray30"),
                                        anchor=anchor)
        button.place(relx=x, rely=y, relheight=height, relwidth=width)

    def add_checkbox(self, text, master=None, x=0, y=0, height=0.1, width=1,val=None,text_color="black"):
        if master == None:
            master=self.current_frame        
        checkbox = customtkinter.CTkSwitch(master=master,text=text,command=func_config.save,fg_color="red",progress_color="green",text_color=text_color,variable=val)
        checkbox.place(relx=x, rely=y, relheight=height, relwidth=width)

    def add_weblink(self,text,x=0,y=0,height=0.1,width=1,cmd=None):
        button  = customtkinter.CTkButton(master=self.current_frame,text=text,command=cmd,text_color="#47bcf2",fg_color="transparent",corner_radius=0,hover_color="#dee6ff")
        button.place(relx=x,rely=y,relheight=height,relwidth=width)
        
    def create_setting_frame(self, title):
        f_root = customtkinter.CTkFrame(root,corner_radius=0,fg_color="white")
        f_root.place(relx=0.3, rely=0, relheight=1, relwidth=0.7)
        customtkinter.CTkLabel(f_root, text=title, fg_color="#444444", text_color="white").place(relx=0, rely=0, relheight=0.1, relwidth=1)
        return f_root
    
    def general(self):
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = self.create_setting_frame("GENERAL")

        def browse():
            global output
            output_sub = filedialog.askdirectory()
            if output_sub:
                output = output_sub
                Path_Label.configure(text=output)
        Path_Label = customtkinter.CTkLabel(self.current_frame,text=output,text_color="black",anchor=tkinter.W)
        Path_Label.place(relx=0.05, rely=0.15, relheight=0.1, relwidth=0.65)
        self.add_button(text="Browse",cmd=browse,
                        fg_color="#444444",x=0.725,y=0.15,width=0.25)
        self.add_checkbox(text="DL Folder",x=0.05,y=0.3,val=dl_folder)
        self.add_checkbox(text="Uploader Folder",x=0.05,y=0.45,val=uploader_folder)
        self.add_checkbox(text="Playlist Folder",x=0.05,y=0.6,val=playlist_folder)
        self.add_checkbox(text="Notification",x=0.05,y=0.75,val=notification)
        self.add_button(text="Close",cmd=lambda:self.current_frame.destroy(),y=0.9,fg_color="#444444")

    def video(self):
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = self.create_setting_frame("VIDEO")
        video_codec_list = ["mp4","mkv","webm"]
        video_resolution = ["Auto","144p","240p","360p","480p","720p","1080p"]

        customtkinter.CTkComboBox(master=self.current_frame,values=video_codec_list,command=func_config.save,variable=video_codec
                                ).place(relx=0.05, rely=0.15, relheight=0.1, relwidth=0.9)
        customtkinter.CTkComboBox(master=self.current_frame,values=video_resolution,command=func_config.save,variable=resolution
                                ).place(relx=0.05, rely=0.3, relheight=0.1, relwidth=0.9)
        self.add_button(text="Close",cmd=lambda:self.current_frame.destroy(),y=0.9,fg_color="#444444")

    def audio(self):
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = self.create_setting_frame("AUDIO")

        audio_codec_list = ["Auto","aac","flac","mp3","m4a","opus","vorbis","wav"]

        customtkinter.CTkComboBox(master=self.current_frame,values=audio_codec_list,variable=audio_codec
                                ).place(relx=0.05, rely=0.15, relheight=0.1, relwidth=0.9)
        self.add_checkbox(text="Meta Data",x=0.05,y=0.3,val=meta)
        self.add_checkbox(text="Thumbnail",x=0.05,y=0.45,val=thumbnail)
        self.add_button(text="Close",cmd=lambda:self.current_frame.destroy(),y=0.9,fg_color="#444444")

    def other(self):
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = self.create_setting_frame("OTHER")

        self.add_weblink(text="WebPage",y=0.1,cmd=lambda:self.open_browser(URL="https://kurosiko.github.io/"))
        self.add_weblink(text="FFmpeg",y=0.2,cmd=lambda:self.open_browser(URL="https://ffmpeg.org"))
        self.add_weblink(text="Github",y=0.3,cmd=lambda:self.open_browser(URL="https://github.com/kurosiko/Kuros-VideoFetcher"))
        self.add_weblink(text="Twitter",y=0.4,cmd=lambda:self.open_browser(URL="https://twitter.com/kurosiko"))
        self.add_weblink(text="YouTube",y=0.5,cmd=lambda:self.open_browser(URL="https://www.youtube.com/channel/UCkbPdwURHuIG63f5ZTj3fjw"))
        self.add_button(text="Close",cmd=lambda:self.current_frame.destroy(),y=0.9,fg_color="#444444")


    
    def lunch(self):
        f_side = customtkinter.CTkFrame(root,corner_radius=0)
        f_side.place(relx=0, rely=0, relheight=1, relwidth=0.3)
        customtkinter.CTkLabel(f_side, text="SETTING", fg_color="black", text_color="white").place(relx=0, rely=0, relheight=0.1, relwidth=1)

        self.add_button(master=f_side,text= "GENERAL", y=0.1, cmd=self.general,anchor=tkinter.E)
        self.add_button(master=f_side,text= "VIDEO", y=0.2, cmd=self.video,anchor=tkinter.E)
        self.add_button(master=f_side,text= "AUDIO", y=0.3, cmd=self.audio,anchor=tkinter.E)
        self.add_button(master=f_side,text= "OTHER",y=0.4, cmd=self.other,anchor=tkinter.E)

        func_gui.add_checkbox(master=f_side,text="Playlist",x=0.05,y=0.7,val=playlist,text_color="white")
        func_gui.add_checkbox(master=f_side,text="Audio Only",x=0.05,y=0.8,val=audio_only,text_color="white")
        threading.Thread(target=func_config.image).start()

def dl_start(event):
    if textbox.get():
        URL = textbox.get()
        textbox.delete(0,tkinter.END)
    else:
        URL = event.data
    info = {}
    setting = {
        'meta': meta.get(),
        'thumbnail': thumbnail.get(),
        'notification': notification.get(),
        'dl_folder': dl_folder.get(),
        'uploader_folder': uploader_folder.get(),
        'playlist_folder': playlist_folder.get(),
        'video_codec': video_codec.get(),
        'audio_codec': audio_codec.get(),
        'resolution':resolution.get(),
        'playlist':playlist.get(),
        'audio_only':audio_only.get(),
        'audio_ext':{
            "aac":"m4a",
            "flac":"flac",
            "m4a":"m4a",
            "mp3":"mp3",
            "opus":"opus",
            "vorbis":"ogg",
            "wav":"wav"
        }
    }

    progress = 0
    frame = customtkinter.CTkFrame(f_log,fg_color="black",height=50,corner_radius=0)

    l_playlist = customtkinter.CTkLabel(frame,anchor=tkinter.W,fg_color="#404040",text_color="#f7f7f8",corner_radius=0,text=None)
    l_playlist.place(relheight=0.4,relwidth=0.75)

    l_title = customtkinter.CTkLabel(frame,anchor=tkinter.W,fg_color="#333333",text_color="#f7f7f8",corner_radius=0,text=URL)
    l_title.place(relheight=0.4,relwidth=0.75,rely=0.4)

    l_playlist_index = customtkinter.CTkLabel(frame,anchor=tkinter.E,fg_color="#404040",text_color="#f7f7f8",corner_radius=0,text=None)
    l_playlist_index.place(relheight=0.4,relwidth=0.25,relx=0.75)

    l_progress = customtkinter.CTkLabel(frame,anchor=tkinter.E,fg_color="#333333",text_color="#f7f7f8",corner_radius=0,text=None)
    l_progress.place(relheight=0.4,relwidth=0.25,relx=0.75,rely=0.4)

    progressbar = customtkinter.CTkProgressBar(frame,corner_radius=0)
    progressbar.set(0)
    progressbar.place(relheight=0.2,relwidth=1,rely=0.8)
    frame.pack(fill=tkinter.X)

    def hook(data,URL=URL):
        nonlocal info,progress
        if data['status'] == 'downloading':
            info['title'] = data['info_dict']['title']
            try:
                info['uploader'] = data['info_dict']['uploader']
            except:
                info['uploader'] = data['info_dict']['id']
            if not data['info_dict']['playlist'] == None:
                info['is_playlist'] = True
                info['playlist_title'] = data['info_dict']['playlist_title']
                info['playlist_count'] = data['info_dict']['playlist_count']
                info['playlist_index'] = data['info_dict']['playlist_index']
                l_playlist.configure(text=info['playlist_title'])
                l_playlist_index.configure(text=f"{info['playlist_index']}/{info['playlist_count']}")
            else:
                info['is_playlist'] = False
            try:
                progress = math.floor(float(data['downloaded_bytes']/data['total_bytes'])*100)/100
            except:
                try:
                    progress = math.floor(float(data['fragment_index']/data['fragment_count'])*100)/100
                except:
                    progress = progressbar.getint()
            l_title.configure(text=info['title'])
            l_progress.configure(text=f"{math.floor(progress*100)}%")
            progressbar.set(progress)
        elif data['status'] == 'finished':
            l_title.configure(text='Exporting :D')

    def destory(is_error=False):
        frame.destroy()

        if setting['notification'] or is_error:
            def error():
                nonlocal notification_opts
                notification_opts.update({
                    "title":'ERROR',
                    "body":URL,
                    "button":{'activationType': 'protocol', 'arguments':URL, 'content': 'Open URL'}
                    }
                )
            notification_opts = {}
            notification_opts['app_id'] = 'VideoFetcher'
            notification_opts['duration'] = 'short'
            try:
                PIL.Image.open(io.BytesIO(requests.get(info['thumbnail'],timeout=(10,10)).content)).save('thumbnail.png')
                notification_opts['image'] = {
                    'src': os.path.join(os.getcwd(),"thumbnail.png"),
                    'placement': 'hero'
                }
            except:
                pass
            if is_error:
                error()
            elif info['is_playlist']:
                notification_opts.update({
                    'title':info['title'],
                    'body':'Finish download playlist!',
                    'button':{'activationType': 'protocol', 'arguments': info['path'], 'content': 'Opef Folder'}
                })
            elif info['title']:
                notification_opts.update({
                    "title":info['uploader'],
                    "body":info['title'],
                    "buttons":[
                    {'activationType': 'protocol', 'arguments': info['path'], 'content': 'Play'},
                    {'activationType': 'protocol','arguments':os.path.dirname(info['path']), 'content': 'Open Folder'},
                    ]
                })
            else:
                error()
            threading.Thread(target=win11toast.toast, kwargs=notification_opts).start()
    def dl(URL,setting=setting):
        nonlocal info
        output_dl = output
        ydl_opts = {}
        ydl_opts['ignoreerrors'] = False

        if setting['dl_folder']:
            output_dl = os.path.join(output_dl,'dl_videos')
        if setting['uploader_folder']:
            output_dl = os.path.join(output_dl,'%(uploader)s')
        if not setting['playlist']:
            ydl_opts['noplaylist'] = True
        elif setting['playlist_folder'] and setting['dl_folder']:
            output_dl = os.path.join(output,'dl_videos','Playlist','%(playlist)s')
        elif setting['playlist_folder'] and not setting['dl_folder']:
            output_dl = os.path.join(output,'Playlist','%(playlist)s')

        ydl_opts['outtmpl'] = os.path.join(output_dl,'%(title)s.%(ext)s')

        if setting['audio_only']:
            ydl_opts['format'] = "bestaudio"
            postprocessor = []
            if not setting['audio_codec'] == "Auto":
                postprocessor.append({'key': 'FFmpegExtractAudio','preferredcodec':setting['audio_codec']})
            if setting['meta'] and not any(x in setting['audio_codec'] for x in ["aac","vorbis","wav"]):
                postprocessor.append({'key': 'FFmpegMetadata'})
            if setting['thumbnail'] and any(x in setting['audio_codec'] for x in ["m4a","mp3"]):
                ydl_opts['writethumbnail'] = True
                postprocessor.append({'key': 'EmbedThumbnail','already_have_thumbnail': False})
            if postprocessor:
                ydl_opts['postprocessors'] = postprocessor
        else:
            if setting['resolution'] == 'Auto':
                ydl_opts['format'] = "bv+ba[ext=m4a]/bv+ba/b"
            else:
                ydl_opts['format'] = f"bv[height={str(setting['resolution']).replace('p','')}]+ba[ext=m4a]/bv+ba[ext=m4a]/b"
            if setting['video_codec'] != "webm":
                ydl_opts['merge_output_format'] = setting['video_codec']

        ydl_opts['progress_hooks'] = [hook]
        try:
            with YoutubeDL(ydl_opts) as ydl:
                try:
                    data = ydl.extract_info(URL,download=True)
                except:
                    return destory(is_error=True)
                else:
                    print("\033[32m"+"DL"+"\033[0m")
                info['path'] = ydl.prepare_filename(data)
            info['title'] = data['title']
            info['uploader'] = data['uploader']
            if '_type' in data and data['_type'] == 'playlist':
                info['is_playlist'] = True
                info['thumbnail'] = data['entries'][0]['thumbnail']
                info['path'] = data['entries'][0]['requested_downloads'][0]['__finaldir']
            else:
                info['is_playlist'] = False
                info['thumbnail'] = data['thumbnail']
            if setting['audio_only'] and not setting['audio_codec'] == 'Auto':
                info['path'] = f"{os.path.splitext(info['path'])[0]}.{setting['audio_ext'][setting['audio_codec']]}"                
        except:
            return destory(is_error=True)
        else:
            print("\033[32m"+"Get Info"+"\033[0m")
        return destory()
    threading.Thread(target=dl,args=(URL,)).start()

func_config = Config()
config_data = func_config.load()
root = tkinterdnd2.Tk()
root.drop_target_register(tkinterdnd2.DND_TEXT)
def titlebar(window):#By Unnamedbuthere_
  window.update()
  DWMWA_USE_IMMERSIVE_DARK_MODE = 20
  set_window_attribute = ctypes.windll.dwmapi.DwmSetWindowAttribute
  get_parent = ctypes.windll.user32.GetParent
  hwnd = get_parent(window.winfo_id())
  rendering_policy = DWMWA_USE_IMMERSIVE_DARK_MODE
  value = 3
  value = ctypes.c_int(value)
  set_window_attribute(hwnd,rendering_policy,ctypes.byref(value),ctypes.sizeof(value))
titlebar(root)
output = config_data["path"]["main"]
try:
    meta = tkinter.BooleanVar(value=config_data["dl_options"]["meta"])
    thumbnail = tkinter.BooleanVar(value=config_data["dl_options"]["thumbnail"])
    notification = tkinter.BooleanVar(value=config_data["dl_options"]["notification"])
    dl_folder = tkinter.BooleanVar(value=config_data["dl_options"]["dl_folder"])
    uploader_folder = tkinter.BooleanVar(value=config_data["dl_options"]["uploader_folder"])
    playlist_folder = tkinter.BooleanVar(value=config_data["dl_options"]["playlist_folder"])
    resolution = tkinter.StringVar(value=config_data["codec"]["resolution"])
    audio_codec = tkinter.StringVar(value=config_data["codec"]["audio_codec"])
    video_codec = tkinter.StringVar(value=config_data["codec"]["video_codec"])
except:
    func_config.error()

root.title("VideoFetcher")
root.geometry("600x480")
root.configure(bg="#242424")
root.minsize(600,480)
root.attributes('-topmost',True)
root.dnd_bind('<<Drop>>',dl_start)

textbox = customtkinter.CTkEntry(root,placeholder_text="Enter URL")
textbox.place(relx=0.35,rely=0.05,relwidth=0.6)
textbox.bind("<Return>",dl_start)

playlist = tkinter.BooleanVar(value=False)
audio_only  = tkinter.BooleanVar(value=False)

f_log = customtkinter.CTkFrame(root,corner_radius=5)
f_log.place(relx=0.35,rely=0.2,relwidth=0.6,relheight=0.75)

func_gui = Gui()
func_gui.lunch()

root.protocol("WM_DELETE_WINDOW",lambda:func_config.save(exit_=True))
root.update()
root.mainloop()
