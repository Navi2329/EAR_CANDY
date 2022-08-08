import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askdirectory
import pygame
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk
import os


#creating the root ui
root=Tk()
root.title('MP3 Player')
root.geometry("1920x1080")
root.configure(bg='light blue')

b=0

#mixer initialize
pygame.mixer.init()

#playlist box
box=Listbox(root,bg='violet',fg='black',width=100,height=10,font=10)
box.pack()

#scroller
scroller=Scrollbar(root)
scroller.pack(side=RIGHT,fill=BOTH,ipadx=10)
box.config(yscrollcommand=scroller.set)
scroller.config(command=box.yview)

#Adding labels
label=tk.Label(root,text='My very first music player',font=8,fg='blue')
label.pack(pady=15)
playlist=[]

#Stop add a song to playlist
def add_song():
    song=filedialog.askopenfilename(title='Choose a song',filetypes=(("mp3 files","*.mp3"),("wav files","*.wav"),("ogg files","*.ogg"),))
    global playlist
    if song not in playlist:
        playlist.append(song)
        count=song.count('/')
        song=song.replace('/','',count-1)
        c=song.index('/')
        song=song[c+1::]
        box.insert(END,song)
        if len(playlist)==1:
            label.config(text='1 song in playlist')
        else:
            label.config(text=(str(len(playlist)) + ' songs in playlist'))
    else:
        label.config(text='Song is already in playlist,So it is ignored'+'\n'+(str(len(playlist)) + ' songs in playlist'))
    box.activate(0)
    box.select_set(0)
def add_many_songs():
    count=0
    songs= filedialog.askopenfilenames(title='Choose a song',filetypes=(("mp3 files", "*.mp3"), ("wav files", "*.wav"),))
    global playlist
    for song in songs:
        if song not in playlist:
            playlist.append(song)
            # Strips out path
            count = song.count('/')
            song = song.replace('/', '', count - 1)
            c = song.index('/')
            song = song[c + 1::]
            # Add song name to listbox
            box.insert(END, song)
            if len(playlist) == 1:
                label.config(text='1 song in playlist')
            else:
                label.config(text=(str(len(playlist)) + ' songs in playlist'))
        else:
            count=1
    if count==1:
        label.config(text='Some songs are already in playlist.They are ignored'+'\n'+(str(len(playlist)) + ' songs in playlist'))
    box.activate(0)
    box.select_set(0)
def add_directory():
    count=0
    path = askdirectory(title='Select Folder')
    for i in os.listdir(path):
        global playlist
        if (path+'/'+i) not in playlist:
            playlist.append(path+'/'+i)
            box.insert(END,i)
            label.config(text=(str(len(playlist)) + ' songs in playlist'))
        else:
            count=1
    if count==1:
        label.config(text='Some songs are already in playlist.They are ignored' + '\n' + (str(len(playlist)) + ' songs in playlist'))
    box.activate(0)
    box.select_set(0)
#To play song
def play():
    #stopped variable to False so song can play
    global stopped
    stopped=False
    global selected_song
    selected_song = box.curselection()
    status_bar.config(text='')
    slider.config(value=0)
    song=playlist[selected_song[0]]
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    label.config(text='Playing '+box.get(selected_song)+'\n'+'\n'+str(len(playlist))+' songs in playlist')
    if is_paused():
        pauseresume_button['text']='Pause'
    #Calling play_time function
    play_time()
#Song info
def play_time():
    # Check for double timing
    if stopped:
        return
    # Find Current Song Elapsed Time
    current_time = pygame.mixer.music.get_pos() / 1000
    # convert to time format
    converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))
    # Grab song title from playlist
    song = box.curselection()
    # add directory structure and mp3 to song title
    song = playlist[song[0]]
    # Load Song with Mutagen
    song_mod = MP3(song)
    # Get song Length
    global song_length
    song_length = song_mod.info.length
    # Convert to Time Format
    converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))

    # Increase current time by 1 second
    current_time += 1

    if int(slider.get()) == int(song_length):
        status_bar.config(text=f'Time Elapsed: {converted_song_length}  of  {converted_song_length}  ')
    elif is_paused():
        pass
    elif int(slider.get()) == int(current_time):
        # Update Slider To position
        slider_position=(song_length)
        slider.config(value=(current_time),to=slider_position)
    else:
        # Update Slider To position
        slider_position = (song_length)
        slider.config(value=(int(slider.get())),to=slider_position)
        # convert to time format
        converted_current_time = time.strftime('%M:%S', time.gmtime((int(slider.get()))))

        # Output time to status bar
        status_bar.config(text=f'Time Elapsed: {converted_current_time}  of  {converted_song_length}  ')

        # Move this thing along by one second
        slider.config(value=(int(slider.get()))+1)
    # update time
    status_bar.after(1000,play_time)

    while not pygame.mixer.music.get_busy():
        if is_paused():
            break
        else:
            if b == 1:
                break
            else:
                next()
def is_paused():
    if pauseresume_button['text']=='Pause':
        return False
    else:
        return True

global stopped
stopped=True
#To stop playing
def stop():
    #reset status and slider bars
    status_bar.config(text='')
    slider.config(value=0)
    pygame.mixer.music.stop()

    #Clear status bar
    status_bar.config(text='')
    label.config(text='My very first mp3 player')
    #status
    global stopped
    stopped=True

#To play the previous song
def previous():
    status_bar.config(text='')
    slider.config(value=0)
    current_song=box.curselection()
    previous_song=current_song[0]-1
    if previous_song!=-1:
        box.yview_scroll(-1,"unit")
        pygame.mixer.music.load(playlist[previous_song])
        box.select_clear(0, END)
        pygame.mixer.music.play(loops=0)
        box.activate(previous_song)
        box.select_set(previous_song)
        label.config(text='Playing '+box.get(ACTIVE)+'\n'+'\n'+str(len(playlist))+' songs in playlist')
    else:
        box.yview_scroll(len(playlist)-1, "unit")
        previous_song=len(playlist)-1
        pygame.mixer.music.load(playlist[previous_song])
        box.select_clear(0, END)
        pygame.mixer.music.play(loops=0)
        box.activate(previous_song)
        box.select_set(previous_song)
        label.config(text='Playing '+box.get(ACTIVE)+'\n'+'\n'+str(len(playlist))+' songs in playlist')

#To play the next song
def next():
    global b
    status_bar.config(text='')
    slider.config(value=0)
    current_song=box.curselection()
    next_song=current_song[0]+1
    if next_song<len(playlist):
        box.yview_scroll(1, "unit")
        pygame.mixer.music.load(playlist[next_song])
        box.select_clear(0, END)
        pygame.mixer.music.play(loops=0)
        box.activate(next_song)
        box.select_set(next_song)
        label.config(text='Playing '+box.get(ACTIVE)+'\n'+'\n'+str(len(playlist))+' songs in playlist')
    else:
        box.yview_scroll(-1*(len(playlist)-1), "unit")
        next_song=0
        pygame.mixer.music.load(playlist[next_song])
        box.select_clear(0, END)
        pygame.mixer.music.play(loops=0)
        box.activate(next_song)
        box.select_set(next_song)
        label.config(text='Playing '+box.get(ACTIVE)+'\n'+'\n'+str(len(playlist))+' songs in playlist')

#To pause or resume based on current status of song
def pause_resume():
    global pauseresume_button
    if pauseresume_button["text"]=='Pause':
        pygame.mixer.music.pause()
        pauseresume_button["text"]='Resume'
    elif pauseresume_button["text"]=='Resume':
        pygame.mixer.music.unpause()
        pauseresume_button["text"]='Pause'

def delete_song():
    stop()
    global playlist
    current_song = box.get(ACTIVE)
    for i in playlist:
        if current_song in i:
            ind=playlist.index(i)
            playlist.pop(ind)
            break
    box.delete(ANCHOR)
    pygame.mixer.music.stop()
    label.config(text=str(len(playlist))+' songs in playlist')
    box.activate(ind)
    box.select_set(ind)
def delete_songs():
    stop()
    box.delete(0,END)
    pygame.mixer.music.stop()
    global playlist
    playlist=[]
    label.config(text='My first MP3 player')

#position slider
def slide(x):
    selected_song=box.get(ACTIVE)
    for i in playlist:
        if selected_song in i:
            song=i
            break
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0,start=((int(slider.get()))))

#buttons images
pauseresume_button_image=PhotoImage(file="icons/pause.png")
play_button_image=PhotoImage(file="icons/play.png")
next_button_image=PhotoImage(file="icons/next.png")
previous_button_image=PhotoImage(file="icons/previous.png")
stop_button_image=PhotoImage(file="icons/stop.png")
background_image=PhotoImage(file="icons/music.gif")

#Frame defenition
frame=tk.Frame(root,bg='light blue')
frame.pack()

#background label
back_label=Label(frame,image=background_image,bg='light blue')
back_label1=Label(frame,image=background_image,bg='light blue')

#buttons defenition
pauseresume_button=tk.Button(frame,image=pauseresume_button_image,text='Pause',bg='black',borderwidth=0,command=pause_resume)
play_button=tk.Button(frame,image=play_button_image,text='play',bg='black',borderwidth=0,command=play)
stop_button=tk.Button(frame,image=stop_button_image,text='stop',bg='black',borderwidth=0,command=stop)
next_button=tk.Button(frame,image=next_button_image,text='next',bg='black',borderwidth=0,command=next)
previous_button=tk.Button(frame,image=previous_button_image,text='previous',bg='black',borderwidth=0,command=previous)

#song menu
my_menu=Menu(root)
root.config(menu=my_menu)

#Add song to menu
add_song_menu=Menu(my_menu)
my_menu.add_cascade(label='Add Songs',menu=add_song_menu)
add_song_menu.add_command(label='Add one song to playlist',command=add_song)
add_song_menu.add_command(label='Add many songs to playlist',command=add_many_songs)
add_song_menu.add_command(label='Add a directory to playlist',command=add_directory)
#Remove song menu
remove_song_menu=Menu(my_menu)
my_menu.add_cascade(label='Remove Songs',menu=remove_song_menu)
remove_song_menu.add_command(label='Delete one song from playlist',command=delete_song)
remove_song_menu.add_command(label='Delete all songs from playlist',command=delete_songs)

#Creating the duration bar
status_bar=Label(root,text='',bd=1,bg='black',fg='white',font=20)
status_bar.pack(pady=50,fill=X,side=TOP,ipady=2)

#create position slider
slider=ttk.Scale(root,from_=0,to=100,orient=HORIZONTAL,value=0,length=1000,command=slide)
slider.pack(ipady=20)


#button grid
back_label.grid(row=0,column=1,ipadx=50)
previous_button.grid(row=0,column=2,padx=20,pady=20)
stop_button.grid(row=0,column=3,padx=20,pady=20)
play_button.grid(row=0,column=4,padx=20,pady=20)
pauseresume_button.grid(row=0,column=5,padx=20,pady=20)
next_button.grid(row=0,column=6)
back_label1.grid(row=0,column=7,ipadx=40)
root.mainloop()
