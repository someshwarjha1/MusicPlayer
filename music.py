from tkinter import *
from pygame import *
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

root =Tk()
root.title('Melody')
root.iconbitmap(r'images/music.ico')
root.geometry('650x450')

mixer.init()

def play_time():
    if stopped:
        return
    current_time=mixer.music.get_pos()/1000
    # slider_label.config(text=f"Slider: {int(my_slider.get()) }and Song Pos: {int(current_time)}")
    converted_current_time=time.strftime('%M:%S',time.gmtime(current_time))
    song = song_box.get(ACTIVE)
    song = f"C:/Users/asus/Desktop/music/{song}.mp3"
    song_mut=MP3(song)

    global song_length
    song_length=song_mut.info.length
    converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))
    current_time += 1

    if int(my_slider.get())== int(song_length):
        pass
    elif paused:
        pass
    elif int(my_slider.get())==int(current_time):
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(current_time))
    else:
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(my_slider.get()))

        converted_current_time = time.strftime('%M:%S', time.gmtime(int(my_slider.get())+1))
        status_bar.config(text=f"Time Elapsed : {converted_current_time}  of  {converted_song_length}  ")
        next_time=int(my_slider.get()) + 1
        my_slider.config(value=next_time)
    status_bar.after(1000,play_time)



def add_songs():
    song=filedialog.askopenfilename(initialdir='C:/Users/asus/Desktop/music/',title='Choose a song',filetypes=(('mp3 Files',"*.mp3"),))
    song=str(song)
    song=song.replace("C:/Users/asus/Desktop/music/","")
    song = song.replace(".mp3", "")
    song_box.insert(END,song)

def add_many_songs():
    songs = filedialog.askopenfilenames(initialdir='C:/Users/asus/Desktop/music/', title='Choose a song',filetypes=(('mp3 Files', "*.mp3"),))

    for song in songs:
        song = str(song)
        song = song.replace("C:/Users/asus/Desktop/music/", "")
        song = song.replace(".mp3", "")
        song_box.insert(END, song)

#Delete song
def dlt_song():
    stop()

    song_box.delete(ANCHOR)

    mixer.music.stop()

#Delete all songs
def dlt_all_songs():
    stop()

    song_box.delete(0,END)

    mixer.music.stop()

#sider function
def slide(x):
    song = song_box.get(ACTIVE)

    song = f"C:/Users/asus/Downloads/{song}.mp3"

    mixer.music.load(song)

    mixer.music.play(loops=0,start=int(my_slider.get()))

#create volume function
def volume(x):
    mixer.music.set_volume(volume_slider.get())
    # current_volume=mixer.music.get_volume()
    # slider_label.config(text=current_volume*100)

master_frame=Frame(root)
master_frame.pack(pady=20)

#create song list box
song_box=Listbox(master_frame,bg='black',fg='yellow',width=60,selectbackground='gray',selectforeground='black')

song_box.grid(row=0,column=0)


#play selected songs
def play():
   global stopped
   stopped=False
   my_slider.config(value=0)
   song=song_box.get(ACTIVE)
   song=f"C:/Users/asus/Downloads/{song}.mp3"
   mixer.music.load(song)
   mixer.music.play(loops=0)
   play_time()
   #get current volume
   # current_volume = mixer.music.get_volume()
   # slider_label.config(text=current_volume*100)

global stopped
stopped=False
#stop music
def stop():
    #Reset slider and status bar
    status_bar.configure(text='')
    my_slider.config(value=0)
    #Stop song from playing
    mixer.music.stop()
    song_box.selection_clear(ACTIVE)
    # status_bar.config(text='')
    global stopped
    stopped=True

#Pause/Unpause function
global paused
paused=False

def pause(is_paused):
    global paused
    paused=is_paused
    if paused:
        # unpause
        mixer.music.unpause()
        paused=False
    else:
        #pause
        mixer.music.pause()
        paused=True
#Moving Forward in list
def next_song():
    if stopped:
        return
    status_bar.configure(text='')
    my_slider.config(value=0)
    next_one=song_box.curselection()
    next_one=next_one[0]+1
    song=song_box.get(next_one)

    song = f"C:/Users/asus/Downloads/{song}.mp3"
    mixer.music.load(song)
    mixer.music.play(loops=0)

    song_box.selection_clear(0,END)
    song_box.activate(next_one)
    song_box.selection_set(next_one,last=None)

#Play previous song
def prev_song():
    if stopped:
        return
    status_bar.configure(text='')
    my_slider.config(value=0)
    next_one = song_box.curselection()
    next_one = next_one[0] - 1
    song = song_box.get(next_one)

    song = f"C:/Users/asus/Downloads/{song}.mp3"
    mixer.music.load(song)
    mixer.music.play(loops=0)

    song_box.selection_clear(0, END)
    song_box.activate(next_one)
    song_box.selection_set(next_one, last=None)

# Mute volume
Muted=False
def Mute_music():
    global Muted
    if Muted:
        volumebtn.configure(image=volumephoto)
        mixer.music.set_volume(0.5)
        Muted=False
    else:
        volumebtn.configure(image=Mutephoto)
        mixer.music.set_volume(0)
        Muted=TRUE

#Placing images on interface
back_btn_image=PhotoImage(file='image/back.png')
forward_btn_image=PhotoImage(file='image/forward.png')
play_btn_image=PhotoImage(file='image/playbut.png')
pause_btn_image=PhotoImage(file='image/pause.png')
stop_btn_image=PhotoImage(file='image/stop.png')
Mutephoto=PhotoImage(file='images/vol_mute.png')
volumephoto=PhotoImage(file='images/volume.png')

contri_frame=Frame(master_frame)
contri_frame.grid(row=1,column=0,pady=20)
#create volume label frame
volume_frame=LabelFrame(master_frame,text="volume")
volume_frame.grid(row=0,column=1,padx=20)

# Converting images into buttons
back_button=Button(contri_frame,image=back_btn_image,borderwidth=0,command=prev_song)
forward_button=Button(contri_frame,image=forward_btn_image,borderwidth=0,command=next_song)
play_button=Button(contri_frame,image=play_btn_image,borderwidth=0,command=play)
pause_button=Button(contri_frame,image=pause_btn_image,borderwidth=0,command=lambda:pause(paused))
stop_button=Button(contri_frame,image=stop_btn_image,borderwidth=0,command=stop)

# Placing of buttons in specific positions
back_button.grid(row=0,column=0,padx=10)
forward_button.grid(row=0,column=1,padx=10)
play_button.grid(row=0,column=2,padx=10)
pause_button.grid(row=0,column=3,padx=10)
stop_button.grid(row=0,column=4,padx=10)


my_menue=Menu(root)
root.config(menu=my_menue)
#Add song menu
add_song=Menu(my_menue,tearoff=0)
my_menue.add_cascade(label='ADD ',menu=add_song)
add_song.add_command(label='Add Song',command=add_songs)
add_song.add_command(label='Add many Song',command=add_many_songs)
#Remove song menu
remove_song_menu=Menu(my_menue,tearoff=0)
my_menue.add_cascade(label='Remove',menu=remove_song_menu)
remove_song_menu.add_command(label='Remove song',command=dlt_song)
remove_song_menu.add_command(label='Clear',command=dlt_all_songs)

status_bar=Label(root,text='',bd=1,relief=GROOVE,anchor=E)
status_bar.pack(fill=X,side=BOTTOM,ipady=2)

#song position slider
my_slider=ttk.Scale(master_frame,from_=0,to=100,orient=HORIZONTAL,value=0,command=slide,length=360)
my_slider.grid(row=2,column=0,pady=10)

#create volume slider
volume_slider=ttk.Scale(volume_frame,from_=0,to=1,orient=VERTICAL,value=0.7,command=volume,length=125)
volume_slider.pack(pady=10)

volumebtn=Button(volume_frame,image=volumephoto,borderwidth=0,command=Mute_music)
volumebtn.pack(ipady=0,padx=10,pady=0)
# slider_label=Label(root,text='0')
# slider_label.pack(pady=10)

root.mainloop()