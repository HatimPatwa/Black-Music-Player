from os import path
from threading import Thread
from time import sleep
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

from mutagen.mp3 import MP3
from pygame import mixer
from ttkthemes import themed_tk as tk

root = tk.ThemedTk()
root.get_themes()
root.set_theme("radiance")
root.geometry("700x320")
root.maxsize(width=700, height=350)
root.minsize(width=550, height=300)
root.iconbitmap("photos/playicon.ico")
root.title("Black player")

mixer.init()

filename_path = NONE
muted = False
paused = False
selected = False

label_call = ttk.Label(root, text="Let's play some Music")
label_call.pack()

status_bar = ttk.Label(root, text="Welcome to BLACK PLAYER", relief=GROOVE, anchor=W, font='comicsansMS 8 italic')
status_bar.pack(side=BOTTOM, fill=X)

# start def 2

playlist = []


def about_us():
    messagebox._show("Black  player", "Hey welcome to BLACK MUSIC PLAYER"
                                      "\n copyright@ : Hatim creations")


def open_file():
    global filename_path
    filename_path = filedialog.askopenfilename()
    add_to_playlist(filename_path)
    return filename_path


def add_to_playlist(filename):
    filename = path.basename(filename)
    index = 0
    list_box.insert(index, filename)
    playlist.insert(index, filename_path)
    index += 1


def on_closing():
    if messagebox.askyesno('BLACK MUSIC PLAYER', 'Do you want to really quit'):
        stp_music()
        root.destroy()


# frame
left_frame = Frame(root)
left_frame.pack(side=LEFT)

list_box = Listbox(left_frame)
list_box.grid(row=0, padx=20, columnspan=2)

add_btn = ttk.Button(left_frame, text=" Add ", command=open_file)
add_btn.grid(row=1, column=0, pady=5)


def del_song():
    selected_song = list_box.curselection()  # gives index of the file in playlist
    selected_song = int(selected_song[0])
    list_box.delete(selected_song)
    playlist.pop(selected_song)


del_btn = ttk.Button(left_frame, text=" Del ", command=del_song)
del_btn.grid(row=1, column=1, pady=5)

right_frame = Frame(root)
right_frame.pack()

# menu
menubar = Menu(root)
root.config(menu=menubar)

# submenu
submenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Commands", menu=submenu)
submenu.add_command(label="open", command=open_file)
submenu.add_command(label="exit", command=on_closing)

# submenu 2
submenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=submenu)
submenu.add_command(label="about us", command=about_us)

# photos
play_btn_img = PhotoImage(file="photos/play.png")
stop_btn_img = PhotoImage(file="photos/stop.png")
pause_btn_img = PhotoImage(file="photos/pause.png")
rew_btn_img = PhotoImage(file="photos/rewind.png")
mute_btn_img = PhotoImage(file="photos/mute.png")
volume_btn_img = PhotoImage(file="photos/speaker.png")


# def
def show_details(play_song):
    label_call['text'] = "Now Playing : " + path.basename(play_song)
    file_data = path.splitext(play_song)

    if file_data[1] == '.mp3':
        audio = MP3(play_song)
        total_length = audio.info.length
    else:
        a = mixer.Sound(play_song)
        total_length = a.get_length()
    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    time_format = '{:02d}:{:02d}'.format(mins, secs)
    length_label['text'] = "Total length : " + time_format

    t1 = Thread(target=start_count, args=(total_length,))
    t1.start()


def play_music():
    global paused

    if paused == True:
        mixer.music.unpause()
        status_bar["text"] = "Playing Music : " + path.basename(filename_path)
        paused = False
    else:
        try:
            stp_music()
            sleep(1)
            selected_song = list_box.curselection()  # gives index of the file in listbox
            selected_song = int(selected_song[0])
            play_it = playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            status_bar["text"] = "Playing Music : " + path.basename(play_it)
            show_details(play_it)
        except:
            messagebox.showerror("ohh!", "Error- Choose a file to play")
            open_file()


def stp_music():
    mixer.music.stop()
    status_bar['text'] = "Music Stopped"


def pause_music():
    global paused
    paused = True
    mixer.music.pause()
    status_bar['text'] = "Music paused"


def vol(val):
    volume = float(val) / 100
    mixer.music.set_volume(volume)


def mute_music():
    global muted
    if muted:
        vol_scl.configure(state=NORMAL)
        mixer.music.set_volume(0.7)
        vol_scl.set(70)
        mute_btn.configure(image=volume_btn_img)
        muted = False
    else:
        vol_scl.set(0)
        mixer.music.set_volume(0)
        mute_btn.configure(image=mute_btn_img)
        vol_scl.configure(state=DISABLED)
        muted = True


def rew_music():
    play_music()
    status_bar['text'] = "Music rewinded : " + path.basename(filename_path)


def start_count(t):
    global paused
    while t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(t, 60)
            mins = round(mins)
            secs = round(secs)
            time_format = '{:02d}:{:02d}'.format(mins, secs)
            remain_label['text'] = "Remaining Time : " + time_format
            sleep(1)
            t -= 1


# widgets


# Top_frame -start
top_frame = Frame(right_frame)
top_frame.pack(pady=10)

length_label = ttk.Label(top_frame, text="Total length : --:--")
length_label.grid(column=0, row=1, pady=6, padx=45)

remain_label = ttk.Label(top_frame, text="Remaining Time : --:--")
remain_label.grid(column=1, row=1, pady=6, padx=45)

# top frame -end
# middle frame  -start

middle_frame = Frame(right_frame)
middle_frame.pack(pady=30)

play_btn = ttk.Button(middle_frame, image=play_btn_img, command=play_music )
play_btn.grid(row=0, column=0, padx=10)

stp_btn = ttk.Button(middle_frame, image=stop_btn_img, command=stp_music)
stp_btn.grid(row=0, column=1, padx=10)

pas_btn = ttk.Button(middle_frame, image=pause_btn_img, command=pause_music)
pas_btn.grid(row=0, column=2, padx=10)

# middle frame -end
# bottom frame -start

bottom_frame = Frame(right_frame)
bottom_frame.pack(side=BOTTOM)

rew_btn = ttk.Button(bottom_frame, image=rew_btn_img, command=rew_music)
rew_btn.grid(row=0, column=0, padx=10)

mute_btn = ttk.Button(bottom_frame, image=volume_btn_img, command=mute_music)
mute_btn.grid(row=0, column=1, padx=10)

vol_scl = ttk.Scale(bottom_frame, from_=0, to_=100, orient=HORIZONTAL, command=vol, state=ACTIVE)
vol_scl.set(70)
vol_scl.grid(row=0, column=3, padx=10)


# bottom frame -end

# key binds

def spacebar(event):
    if paused == True:
        play_music()
    else:
        pause_music()


def m(event):
    mute_music()


def ctrl(event):
    open_file()


# key presses

root.bind("<space>", spacebar)
root.bind("<m>", m)
root.bind("<Control-o>", ctrl)

# end
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
