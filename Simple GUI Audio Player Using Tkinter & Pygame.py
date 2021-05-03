#-----------------------------------------------------------------------------------------------------------------------------------------------#
# Modules required :
#random
#pygame (pip install pygame)
#tkinter (pip install tkinterx)
#tkfilebrowser (pip install tkfilebrowser)
#tinytag (pip install tinytag)
#mutagen (pip install mutagen)
#-----------------------------------------------------------------------------------------------------------------------------------------------#
import pygame
from pygame import mixer
#import tkfilebrowser
#from random import choice
#from random import shuffle
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog           # <- Suggested instead of tkfilebrowser
#from tinytag import TinyTag, TinyTagException   # import *
from mutagen.mp3 import MP3, EasyMP3     # <- Suggested instead of tinytag
#-----------------------------------------------------------------------------------------------------------------------------------------------#
mixer.init()
#-----------------------------------------------------------------------------------------------------------------------------------------------#
def browse():
    global a_list
    a_list = list(filedialog.askopenfilenames(initialdir="Z:\\", title="Select Files", \
                                                filetypes=[("MPEG Audio Layer 3 (.mp3)", "*.mp3"), \
                                                           ("Waveform Audio File Format (.wav)", "*.wav"), ("OGG (.ogg)", "*.ogg"),\
                                                           ("Windows Media Audio (.wmv)", "*.wmv"), ("WEBM (.webm)", "*.webm"),\
                                                           ("All Files", "*.*")]))
##    a_list = list(tkfileborwser.askopenfilenames(initialdir="C:\\", title="Select Files", \
##                                                filetypes=[("MPEG Audio Layer 3 (.mp3)", "*.mp3"), \
##                                                           ("Waveform Audio File Format (.wav)", "*.wav"), ("OGG (.ogg)", "*.ogg"),\
##                                                           ("Windows Media Audio (.wmv)", "*.wmv"), ("WEBM (.webm)", "*.webm"),\
##                                                           ("All Files", "*.*")]))
    if a_list == []:
        msgbox = messagebox.askretrycancel("No Files Selected", "No files were selected. Do you want to choose files again ?")
        if msgbox:
            browse()
        else:
            pass
    else:
        pass
    append_to_tree()
    #load_(a_list)
#-----------------------------------------------------------------------------------------------------------------------------------------------#
def append_to_tree():
    time = []
    for a in a_list:
##        try:
##            audio = TinyTag.get(a)
##        except TinyTagException:
##            pass
##        time_ = int(audio.duration)
        audio_1 = MP3(a)
        time_ = int(audio_1.info.length)
        time.append((str(time_)+"seconds"))
    song_name = []
    for b in a_list:
        try:
            audio_2 = EasyMP3(b)
            title = audio_2["title"]
            if title == None:
                title = "No title"
            else:
                title = title[0]
            song_name.append(title)
        except KeyError:
            song_name_ = []
            for i in range(-1, -(len(b)+1), -1):
                if b[i] == "\\":
                    break
                else:
                    song_name_.append(b[i])
            song_name_ = song_name_[::-1]
            song_name.append("".join(song_name_))
    tree_list = []
    for i, j, k in zip(song_name, time, a_list):
        tree_list.append((i, j, k))
    for items in tree_list:
        tree.insert("", tk.END, values=items)
#-----------------------------------------------------------------------------------------------------------------------------------------------#
def delete_from_tree():
    tree.delete(*tree.get_children())
    mixer.music.stop()
    mixer.music.unload()
#-----------------------------------------------------------------------------------------------------------------------------------------------#
def play():
    mixer.music.play()
#-----------------------------------------------------------------------------------------------------------------------------------------------#
def play_by_event(event):
    current_item = tree.focus()
    contents = tree.item(current_item)
    selected_item = contents["values"]
    song = selected_item[2]
    try:
        mixer.music.load(song)
    except pygame.error:
        pass
    play()
#-----------------------------------------------------------------------------------------------------------------------------------------------#
def vol_down():
    mixer.music.set_volume(mixer.music.get_volume() - 0.1)
#-----------------------------------------------------------------------------------------------------------------------------------------------#
def vol_up():
    mixer.music.set_volume(mixer.music.get_volume() + 0.1)
#-----------------------------------------------------------------------------------------------------------------------------------------------#
def exit_():
    mixer.music.stop()
    root.destroy()
#-----------------------------------------------------------------------------------------------------------------------------------------------#
root = tk.Tk()
root.geometry("600x300")
root.title("Audio Player")
ttk.Button(root, text="Choose/Add Files", command=browse).grid(row=0, column=0, padx=15)
ttk.Button(root, text="Delete List", command=delete_from_tree).grid(row=0, column=1, padx=20)
ttk.Button(root, text="Play", command=play).grid(row=0, column=2, padx=15)
ttk.Button(root, text="Stop", command=mixer.music.stop).grid(row=0, column=3, padx=20)
ttk.Button(root, text="Resume",command=mixer.music.unpause).grid(row=0, column=4, padx=20)
ttk.Button(root, text="Pause", command=mixer.music.pause).grid(row=1, column=1, padx=15, pady=25)
ttk.Button(root, text="Volume Down", command=vol_down).grid(row=1, column=2, padx=20, pady=25)
ttk.Button(root, text="Volume Up", command=vol_up).grid(row=1, column=3, padx=20, pady = 25)
ttk.Button(root, text="Exit", command=exit_).grid(row=2, column=2)
#-----------------------------------------------------------------------------------------------------------------------------------------------#
global tree
tree=ttk.Treeview(root)
tree["columns"]=("name","duration")
tree["show"]="headings"
tree.column("name", width=445)
tree.column("duration", width=150)
tree.column("#0", width=0)
tree.heading("name", text="Name",anchor=tk.N)
tree.heading("duration", text="Duration",anchor=tk.W)
vertical_scroll_bar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
vertical_scroll_bar.place(x=580, y=151, height=149)
tree.configure(yscrollcommand=vertical_scroll_bar.set)
tree.place(x=0, y=130)
tree.bind("<Double-Button-1>", play_by_event)
#-----------------------------------------------------------------------------------------------------------------------------------------------#
root.mainloop()
#-----------------------------------------------------------------------------------------------------------------------------------------------#
