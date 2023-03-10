from yt_dlp import YoutubeDL
import configparser
import threading
import tkinter
from tkinter import filedialog,ttk,messagebox
import tkinterdnd2
import PIL.Image,PIL.ImageTk
import requests
import os
import io
import ctypes
import pystray
import math
import win11toast
import subprocess
import webbrowser
#import pprint
import sys
#sys.stdout = sys.stderr = open('nul', 'w')
ctypes.windll.shcore.SetProcessDpiAwareness(True)
config = configparser.ConfigParser()
class Config:
  def load(self):
    if not os.path.exists("./config.ini"):
      self.reset()
      with open("config.ini","w") as ini_file:
        config.write(ini_file)
    config.read("config.ini",encoding='utf-8')
    data = {}
    for section in config.sections():
      data[section] = {}
      for option in config.options(section):
        if section in ["dl_options","app_options"]:
          data[section][option] = config.getboolean(section,option) 
        else:
          data[section][option] = config.get(section,option)
    return data
  def save(self,event=None,exit_=False,reset=False):
    global config_data,meta,thumbnail,notification,dl_folder,uploader_folder,playlist_folder
    if not reset:
          config_data = {
          "path":
          {"main":output},
          "dl_options":
          {
          "meta":meta.get(),
          "thumbnail":thumbnail.get(),
          "notification":notification.get(),
          "dl_folder":dl_folder.get(),
          "uploader_folder":uploader_folder.get(),
          "playlist_folder":playlist_folder.get()
          },
          "app_options":
          {
          "background":background.get()
          },
          "codec":
          {"audio_codec":audio_codec.get(),
           "video_codec":video_codec.get()
           },
        }
    for section,options in dict(config_data).items():
      config[section] = {}
      for option,value in dict(options).items():
        config[section][option] = str(value)
    with open('config.ini',"w") as ini_file:
      config.write(ini_file)
    if exit_:
      root.destroy()
      icon.stop()
      if not background:
        exit()
  def reset(self):
    global config_data
    config_data = {
      "path":
      {"main":os.getcwd()},
      "dl_options":
      {
      "meta":False,
      "thumbnail":False,
      "notification":False,
      "dl_folder":True,
      "uploader_folder":True,
      "playlist_folder":True
      },
      "app_options":
      {
      "background":True,
      },
      "codec":
      {"audio_codec":"mp3",
       "video_codec":"mp4"
       },
    }
    self.save(reset=True)
  def image(self):
    def run():
      global icon
      win_icon = PIL.Image.open(io.BytesIO(requests.get("https://i.imgur.com/w5eKxTm.png",timeout=(5,5)).content))
      root.iconphoto(True,PIL.ImageTk.PhotoImage(win_icon))
      menu = pystray.Menu(
        pystray.MenuItem(
        "Info",
        lambda:messagebox.showinfo("Info","""This softwere was made by kurosiko.\nIf you find any bugs or have suggestions for feature improvements, please contact us on Twitter!\nhttps://twitter.com/kurosiko""")
        ),
        pystray.MenuItem(
        "Other Version",
        lambda:webbrowser.open("https://mega.nz/folder/AfFRkJLK#BCLR8DbJeFrWuoarCFK8BA")
        ),
        pystray.MenuItem(
        "Jump To Dev Twitter",
        lambda:webbrowser.open("https://twitter.com/kurosiko")
        )
        )
      icon = pystray.Icon("Neural",icon=win_icon,menu=menu,title="youtube-dl is running!")
      icon.run()
      self.save(exit_=True)
    threading.Thread(target=run,daemon=True).start()
  def error(self):
    messagebox.showerror("KeyError","delete config file and restart again!")
    exit()
class Gui:
  def add_checkbox(self,master,text,variable,y,x=0,height=0.1,width=1):
    style = ttk.Style()
    style.theme_use('default')
    style.map('Toolbutton',
          foreground=[('selected', '#e484fa'), ('active', '#94bbd4'),('!disabled', '#f0f0f0')],
          background=[('selected', '#6b6b6b'), ('active', '#7d7d7d'), ('!disabled', '#454545')])
    style.configure('Toolbutton',borderwidth=0)
    checkbox = ttk.Checkbutton(master=master,text=text,variable=variable,style='Toolbutton',command=func_config.save)
    checkbox.place(relx=x,rely=y,relheight=height,relwidth=width)
  def add_button(self,master,text,cmd,y,x=0,height=0.1,width=1):
    def enter(event):
      button.configure(bg="#7d7d7d")
    def leave(event):
      button.configure(bg="#454545")
    button = tkinter.Button(master=master,text=text,command=cmd,bg="#454545",fg="#f0f0f0",activebackground="#7d7d7d",border=0,anchor=tkinter.W)
    button.place(relx=x,rely=y,relheight=height,relwidth=width)
    button.bind("<Enter>",enter)
    button.bind("<Leave>",leave)
  def add_label(self,master,text,x=0,y=0,height=0.1,width=1):
    label = tkinter.Label(master=master,text=text,bg="#000000",fg="#f0f0f0")
    label.place(relx=x,rely=y,relheight=height,relwidth=width)
  def lunch(self):
    def path():
      global output
      path = filedialog.askdirectory()
      if path:
        output = path
        label.configure(text=f"Output:{output}")
        func_config.save()
    f_side = tkinter.Frame(root,bg="#454545")
    f_side.place(relheight=1,relwidth=0.3)
    self.add_label(f_side,"O P T I O N S")
    self.add_button(f_side,"OUTPUT",cmd=path,y=0.1)
    self.add_button(f_side,"FOLDER",cmd=self.folder,y=0.2)
    self.add_button(f_side,"FORMAT",cmd=self.format,y=0.3)
    self.add_label(f_side,"A U D I O",y=0.4)
    self.add_checkbox(f_side,"META",variable=meta,y=0.5)
    self.add_checkbox(f_side,"THUMBNAIL",variable=thumbnail,y=0.6)
    self.add_label(f_side,"O T H E R",y=0.7)
    self.add_checkbox(f_side,"NOTIFICATION",variable=notification,y=0.8)
    self.add_checkbox(f_side,"BACKGROUND",variable=background,y=0.9)
    self.add_checkbox(root,"PLAYLIST",variable=playlist,x=0.3,y=0.9,width=0.35)
    self.add_checkbox(root,"AUDIO ONLY",variable=audio_only,x=0.65,y=0.9,width=0.35)
    label = tkinter.Label(root,text=f"Output:{output}",bg="#242424",fg="#f0f0f0")
    label.place(relx=0.3,rely=0,relheight=0.1,relwidth=0.7)
  def folder(self):
    f_side = tkinter.Frame(root,bg="#454545")
    f_side.place(relheight=1,relwidth=0.3)
    self.add_label(f_side,"F O L D E R")
    self.add_button(f_side,"B A C K",cmd=lambda:f_side.destroy(),y=0.1)
    self.add_checkbox(f_side,"DL FOLDER",variable=dl_folder,y=0.2)
    self.add_checkbox(f_side,"UPLOADER FOLDER",variable=uploader_folder,y=0.3)
    self.add_checkbox(f_side,"PLAYLIST FOLDER",variable=playlist_folder,y=0.4)
  def format(self):
    f_side = tkinter.Frame(root,bg="#454545")
    f_side.place(relheight=1,relwidth=0.3)
    self.add_label(f_side,"F O R M A T")
    self.add_button(f_side,"B A C K",cmd=lambda:f_side.destroy(),y=0.1)
    audio_codec_list = ["aac","flac","mp3","m4a","opus","vorbis","wav","auto"]
    video_codec_list = ["mp4","mkv","webm"]
    style = ttk.Style()
    style.theme_use('default')
    style.configure('TCombobox', foreground='black',background="#797774")
    audio_list = ttk.Combobox(f_side,state="readonly",textvariable=audio_codec,values=audio_codec_list,style='TCombobox')
    video_list = ttk.Combobox(f_side,state="readonly",textvariable=video_codec,values=video_codec_list,style='TCombobox')
    audio_list.bind("<<ComboboxSelected>>",func_config.save)
    video_list.bind("<<ComboboxSelected>>",func_config.save)
    tkinter.Label(f_side,text="AUDIO",bg="#0b0b0b",fg="#f0f0f0",anchor=tkinter.W).place(rely=0.2,relheight=0.1,relwidth=1)
    audio_list.place(rely=0.3,relheight=0.1,relwidth=1)
    tkinter.Label(f_side,text="VIDEO",bg="#0b0b0b",fg="#f0f0f0",anchor=tkinter.W).place(rely=0.4,relheight=0.1,relwidth=1)
    video_list.place(rely=0.5,relheight=0.1,relwidth=1)
#|DONWLOAD THREAD|
def dl_start(event):
  if textbox.get():
    URL = textbox.get()
    textbox.delete(0,tkinter.END)
  else:
    URL = event.data
  #|DATA|
  info = {
      'title': None,
      'uploader': None,
      'is_playlist': None,
      'playlist_title': None,
      'playlist_index': None,
      'playlist_count': None,
      'already_dl': None,
      'path': None,
  }
  setting = {
      'meta': meta.get(),
      'thumbnail': thumbnail.get(),
      'notification': notification.get(),
      'dl_folder': dl_folder.get(),
      'uploader_folder': uploader_folder.get(),
      'playlist_folder': playlist_folder.get(),
      'video_codec': video_codec.get(),
      'audio_codec': audio_codec.get(),
      'playlist':playlist.get(),
      'audio_only':audio_only.get(),
      'audio_ext':
      {
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
  #|PROGRESSBAR (GUI)|
  style = ttk.Style()
  style.configure("Horizontal.TProgressbar", thickness=20, background="#729f59",troughcolor="#ffffff",bordercolor="#242424",darkcolor="#242424",lightcolor="#242424")
  frame = tkinter.Frame(log)
  label_playlist = tkinter.Label(frame,anchor=tkinter.W,bg="#404040",fg="#f7f7f8")
  label_playlist.place(relheight=0.35,relwidth=0.75)
  label_playlist_index = tkinter.Label(frame,anchor=tkinter.W,bg="#404040",fg="#f7f7f8")
  label_playlist_index.place(relheight=0.35,relwidth=0.25,relx=0.75)
  label_title = tkinter.Label(frame,anchor=tkinter.W,bg="#333333",fg="#f7f7f8")
  label_title.place(relheight=0.35,relwidth=0.75,rely=0.35)
  label_progress = tkinter.Label(frame,anchor=tkinter.E,bg="#333333",fg="#f7f7f8")
  label_progress.place(relheight=0.35,relwidth=0.25,relx=0.75,rely=0.35)
  progressbar = ttk.Progressbar(frame,style="Horizontal.TProgressbar")
  progressbar.place(relheight=0.7,relwidth=1,rely=0.7)
  frame.configure(height=75)
  frame.pack(fill=tkinter.X)
  #|PROGRESSBAR (CHANGE VAL)|
  def hook(data,URL=URL):
    nonlocal info,progress
    if data['status'] == "downloading":
      if not info['title'] == data['info_dict']['title']:
        info['title'] = data['info_dict']['title']
        info['uploader'] = data['info_dict']['uploader']
        if not data['info_dict']['playlist'] == None:
          info['is_playlist'] = True
          info['playlist_title'] = data['info_dict']['playlist_title']
          info['playlist_count'] = data['info_dict']['playlist_count']
          info['playlist_index'] = data['info_dict']['playlist_index']
          label_playlist.configure(text=info['playlist_title'])
          label_playlist_index.configure(text=f"{info['playlist_index']}/{info['playlist_count']}")
        else:
          info['is_playlist'] = False
      try:
          progress = math.floor(float(data['downloaded_bytes']/data['total_bytes'])*100)
      except:
        try:
          progress = math.floor(float(data['fragment_index']/data['fragment_count'])*100)
        except:
          progress = progressbar.getint()
      label_title.configure(text=info['title'])
      progressbar.configure(value=progress)
      label_progress.configure(text=f"{progress}%")
    elif data['status'] == "finished":
      label_title.configure(text="Exporting :D")
  #|PROGRESSBAR (DESTROY)+ NOTIFICATION|
  def destroy():
    frame.destroy()
    if notification.get():
      def open(event):
        if info['is_playlist']:
          os.startfile(info['path'])
        else:
          subprocess.Popen(f'explorer.exe /select,"{info["path"]}"')
      notification_option = {}
      notification_option['app_id'] = "youtube-dl"
      notification_option['duration'] = "short"
      if info['is_playlist']:
       notification_option.update({
        "title":info['playlist_title'],
        "body":"Finish download playlist!",
        "on_click":open
       })
      elif info['already_dl']:
        notification_option.update({
          "title":info['uploader'],
          "body":f"{info['title']}\nYou've already donwloaded",
          "buttons":[
          {'activationType': 'protocol', 'arguments': info['path'], 'content': 'Play'},
          {'activationType': 'protocol','arguments':os.path.dirname(info['path']), 'content': 'Open Folder'},
          ]
        })
      elif info['title']:
        notification_option.update({
          "title":info['uploader'],
          "body":info['title'],
          "buttons":[
          {'activationType': 'protocol', 'arguments': info['path'], 'content': 'Play'},
          {'activationType': 'protocol','arguments':os.path.dirname(info['path']), 'content': 'Open Folder'},
          ]
        })
      else:
          notification_option.update({
            "title":"ERROR",
            "body":"It's error :(",
            "button":{'activationType': 'protocol', 'arguments': URL, 'content': 'Open Source'}
          })
      threading.Thread(target=win11toast.toast, kwargs=notification_option).start()
  #|DOWNLOAD|
  def dl(URL,setting=setting):
    nonlocal info
    ydl_opts = {}
    output_dl = output
    ydl_opts['ignoreerrors'] = True
    if setting['dl_folder']:
      output_dl = os.path.join(output_dl,'dl_videos')
    if setting['uploader_folder']:
      output_dl = os.path.join(output_dl,'%(uploader)s')
    output_dl = os.path.join(output_dl,'%(title)s.%(ext)s')
    if not setting['playlist']:
      ydl_opts['noplaylist'] = True
    elif setting['playlist_folder'] and setting['dl_folder']:
      output_dl = os.path.join(output,'dl_videos','Playlist','%(playlist)s','%(title)s.%(ext)s')
    elif setting['playlist_folder'] and not setting['dl_folder']:
      output_dl = os.path.join(output,'Playlist','%(playlist)s','%(title)s.%(ext)s')
    if setting['audio_only']:
      ydl_opts['format'] = "bestaudio"
      postprocessor = []
      if not setting['audio_codec'] == "auto":
        postprocessor.append({'key': 'FFmpegExtractAudio','preferredcodec':setting['audio_codec']})
      if setting['meta'] and not any(x in setting['audio_codec'] for x in ["aac","vorbis","wav"]):
        postprocessor.append({'key': 'FFmpegMetadata'})
      if setting['thumbnail'] and any(x in setting['audio_codec'] for x in ["m4a","mp3"]):
        ydl_opts['writethumbnail'] = True
        postprocessor.append({'key': 'EmbedThumbnail','already_have_thumbnail': False})
      if postprocessor:
        ydl_opts['postprocessors'] = postprocessor
    else:
      ydl_opts['format'] = "bv+ba[ext=m4a]/bv+ba/b"
      ydl_opts['merge_output_format'] = setting['video_codec']
    ydl_opts['outtmpl'] = output_dl
    ydl_opts['progress_hooks'] = [hook]
    with YoutubeDL(ydl_opts) as ydl:
      try:
        data = ydl.extract_info(URL,download=True)
        print(data)
        #|You've already downloaded|
        info['path'] = ydl.prepare_filename(data)
        if setting['audio_only'] and setting['audio_codec'] == "auto":
          info['path'] = f"{os.path.splitext(info['path'])[0]}.{data['ext']}"
        elif setting['audio_only']:
          info['path'] = f"{os.path.splitext(info['path'])[0]}.{setting['audio_ext'][setting['audio_codec']]}"
        if '_type' in data and data['_type'] == "playlist":
          info['is_playlist'] = True
          playlist_title = data['title']
          info['path'] = output
          if dl_folder.get():
            info['path'] = os.path.join(info['path'],"dl_videos")
          if playlist_folder.get():
            info['path'] = os.path.join(info['path'],"Playlist",playlist_title)
        else:
          info['is_playlist'] = False
        if not info['title']:
          info['already_dl'] = True
          info['title'] = data['title']
          info['uploader'] = data['uploader']
        else:
          info['already_dl'] = False
        return destroy()
      except:
        win11toast.toast(
          "ERROR","This URL is not able to download.",
          button={'activationType': 'protocol', 'arguments': URL, 'content': 'Open Source'}
          )
  threading.Thread(target=dl,args=(URL,)).start()
func_config = Config()
func_gui = Gui()
try:
  config_data = func_config.load()
except:
  func_config.error()
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
root.geometry("600x480")
root.minsize(600,480)
root.title("youtube-dl")
root.configure(bg="#242424")
output = config_data["path"]["main"]
#|READ DATA|
try:
  meta = tkinter.BooleanVar(value=config_data["dl_options"]["meta"])
  thumbnail = tkinter.BooleanVar(value=config_data["dl_options"]["thumbnail"])
  notification = tkinter.BooleanVar(value=config_data["dl_options"]["notification"])
  dl_folder = tkinter.BooleanVar(value=config_data["dl_options"]["dl_folder"])
  uploader_folder = tkinter.BooleanVar(value=config_data["dl_options"]["uploader_folder"])
  playlist_folder = tkinter.BooleanVar(value=config_data["dl_options"]["playlist_folder"])
  background = tkinter.BooleanVar(value=config_data["app_options"]["background"])
  audio_codec = tkinter.StringVar(value=config_data["codec"]["audio_codec"])
  video_codec = tkinter.StringVar(value=config_data["codec"]["video_codec"])
except:
    func_config.error()
####################################
playlist = tkinter.BooleanVar(value=False)
audio_only = tkinter.BooleanVar(value=False)
textbox = tkinter.Entry(root,border=0)
textbox.bind("<Return>",dl_start)
textbox.place(relx=0.325,rely=0.1,relheight=0.1,relwidth=0.65)
root.dnd_bind("<<Drop>>",dl_start)
def lunch():
  func_gui.lunch()
  root.lift()
  threading.Thread(target=func_config.image()).start()
root.after(0,lunch)
log = tkinter.Frame(root,bg="#242424")
log.place(relx=0.325,rely=0.225,relheight=0.65,relwidth=0.65)
root.mainloop()