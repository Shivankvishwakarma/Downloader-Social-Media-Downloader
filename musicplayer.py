import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from eyed3 import id3 as eye
from mutagen.mp3 import MP3
from PIL import Image as SM
from PIL import ImageFilter
from PIL import ImageTk
from tkinter import messagebox
import audio_metadata, time
import os
import pygame
import tempfile
import random

#Global Variables Declaration
songsdir,songname,filefound, = "","",""
global pausedornot, Mute, song_len, checksong, slide, pas, tl, tracklastpos, shuffle_database
checksong,slide,tl = "","",""
song_len = ""
pas = False
Mute = False
pausedornot = False
Stop = False
shufle = False
rep_all = True
rep_one = False
rep_none = False
shuf_ind = 0
songs_database = []
shuffle_database = []

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()

def show_volume_scale(_=None):
    """Show Volume Scale when volume image is clicked """
    volume_frame.place(x=324,y=190)
    
def hide_volume_scale(_=None):
    """Hide Volume Scale when volume image is clicked """
    volume_frame.place_forget()
def updatetitle(title):
    global tl
    tl = title
    title = title.replace('    ', '')
    global filefound
    if filefound != True:
        title = f'MusicByte - Add songs to playlist first! ' + title
        tab5.title(title)
        tab5.update()
        return
    title = f'MusicByte - Playing:   ' + title
    screen.title(title)
    screen.update()

def get_distinct_items(list1):
    """Removes duplicates from parameter,
        appends distinct only items to 'songs' list,
        returns list to be added to playlist"""

    # remove duplicates
    newlist1 = []
    for item in list1:
        if item not in newlist1:
            newlist1.append(item)
            
    global songs_database
    if not songs_database:
        songs_database = newlist1
        return newlist1
    else:
        list2 = []
        for item in newlist1:
            if not item in songs_database:
                songs_database.append(item)
                list2.append(item)
        return list2
    
def addlibFolder(_=None):
    global songsdir,musiclist,filefound
    songsdir = filedialog.askdirectory(title='Open Playlist or Folder...')
    try:
        songs = os.listdir(songsdir)
        filefound = True
    except FileNotFoundError:
        filefound = False
        return
    songs = get_distinct_items(songs)
    for i in songs:
        shuffle_database.append(i)
    random.shuffle(shuffle_database)
    playBTN.config(image=PLAYIcon)
    playBTN.img = PLAYIcon
    drag.destroy()
    dragtitle.destroy()
    musiclist.delete('0', 'end')
    musiclist.config(yscrollcommand=scroll.set)
    scroll.config(command=musiclist.yview)
    musiclist.insert(ANCHOR, "\n")
    for song in songs:
        musiclist.config(font=('AdobeClean-REGULAR', 10))
        musiclist.insert(END, f'    {song}')
    musiclist.config(height=14, width=55)
    addSongBTN.config(state='disabled')
    savePlaylistBTN.config(state='disabled')
    removeSongBTN.config(state='disabled')
    clearPlaylistBTN.config(state='normal')
    

def addSongs(_=None):
    global songsdir, filefound, playBTN, shuffle_database
    songFilename = filedialog.askopenfilenames(initialdir="/", title="Select one or more files to open",
                                          filetypes=(("mp3 files", "*.mp3"),("DownloaderMusicPlayer Playlist (*.dmp)", "*.dmp")))
    
    if songFilename == "":
        filefound = False
        return
    else:
        filefound = True
    tempFile = songFilename[0]
    _, fext = os.path.splitext(tempFile)

    if fext == '.dmp':
        if songFilename[0]:
            with open(songFilename[0], 'r', encoding='utf-8') as playlist_file:
                songs = playlist_file.readlines()
                songs = ''.join(songs).split('\n')
                songs = tuple(songs)
            playBTN.config(image=PLAYIcon)
            playBTN.img = PLAYIcon
            drag.destroy()
            dragtitle.destroy()
            musiclist.delete('0', 'end')
            musiclist.config(yscrollcommand=scroll.set)
            scroll.config(command=musiclist.yview)                      
            musiclist.insert(ANCHOR, " \n ")                                      
            for song in songs:                                 
                songname = os.path.basename(song)
                musiclist.config(font=('AdobeClean-REGULAR', 10))
                musiclist.insert(END, f'    {songname}')
            musiclist.config(height=14, width=55)
            try:
                path = songs[0]
            except IndexError:
                return
            songname = os.path.basename(path)
            path = path.replace(songname, "")
            songsdir = path.replace("\\", "/")
            openPlaylistBTN.config(state='disabled')
            savePlaylistBTN.config(state='normal')
            removeSongBTN.config(state='normal')
            clearPlaylistBTN.config(state='normal')                
    else:
        songFilename = list(songFilename)    
        songFilename = get_distinct_items(songFilename)
        for i in songFilename:
            shuffle_database.append(i)
        random.shuffle(shuffle_database)
        playBTN.config(image=PLAYIcon)
        playBTN.img = PLAYIcon
        drag.destroy()
        dragtitle.destroy()
        musiclist.delete('0', 'end')
        musiclist.config(yscrollcommand=scroll.set)
        scroll.config(command=musiclist.yview)                      
        musiclist.insert(ANCHOR, " \n ")                                      
        for song in songFilename:                                 
            songname = os.path.basename(song)
            musiclist.config(font=('AdobeClean-REGULAR', 10))
            musiclist.insert(END, f'    {songname}')
        musiclist.config(height=14, width=55)
        try:
            path = songFilename[0]
        except IndexError:
            return
        songname = os.path.basename(path)
        path = path.replace(songname, "")
        songsdir = path.replace("\\", "/")
        openPlaylistBTN.config(state='disabled')
        savePlaylistBTN.config(state='normal')
        removeSongBTN.config(state='normal')
        clearPlaylistBTN.config(state='normal')

def remove(typee, _=None):
    global Stop
    if typee == 'ONE':
        status = musiclist.size()
        if not status:
            messagebox.showinfo('Music Player','Playlist is empty!\n\nAdd some songs to the playlist to Remove One.')
        else:    
            #Reset Progress Slider
            currentsong = musiclist.curselection()
            progressBar.config(value=0)
            musiclist.delete(currentsong)
            pygame.mixer.music.stop()

            musiclist.selection_set(currentsong, last=None)
            nextsong = 0
            Stop = True
    elif typee == 'ALL':
        status = musiclist.size()
        if not status:
            messagebox.showinfo('Music Player','Playlist is empty!\n\nAdd some songs to the playlist to Clear Playlist.')
        else:    
            #Reset Progress Slider
            songs_database = []
            shuffle_database = []
            progressBar.config(value=0)
            musiclist.delete(0, END)
            openPlaylistBTN.config(state='normal')
            addSongBTN.config(state='normal')
            savePlaylistBTN.config(state='disabled')
            removeSongBTN.config(state='disabled')
            clearPlaylistBTN.config(state='disabled')
            pygame.mixer.music.stop()
            Stop = True
    else:
        pass

    
def save_playlist(_=None):
    """Save the current playlist as a local file"""
    
    extension = ".dmp"
    status = musiclist.size()
    if not status:
        messagebox.showinfo('Music Player','Playlist is empty!\n\nAdd some songs to the playlist to save it as a file.')            
    else:
        ftype = [("DownloaderMusicPlayer Playlist (*.dmp)", "*.dmp")]

        dir = os.path.expanduser('~') + "\\Documents\\DownloaderMusicPlayer"        
        try: os.mkdir(dir)
        except Exception as err: pass

        name = filedialog.asksaveasfilename(title='Save File', initialdir=dir, filetypes=ftype, defaultextension=extension)
        if name:
            with open(name, 'w', encoding='utf-8') as file:
                file.write('\n'.join(songs_database))
    
def slider(x):
    global slide
    try:
        pygame.mixer.music.load(slide)
        pygame.mixer.music.play(loops=0, start=int(progressBar.get()))
    except:
        pass
    
def volume(percent):
    pygame.mixer.music.set_volume(volumeSlider.get())
    vol = volumeSlider.get() * 100
    if vol == 0:
        volumeBTN.config(image=MUTEIcon)
        volumeBTN.img = MUTEIcon
    elif vol == 100:
        pygame.mixer.music.set_volume(1.0)
    else:
        volumeBTN.config(image=UNMUTEIcon)
        volumeBTN.img = UNMUTEIcon
    vLabelpercent.config(text=f'{int(vol)}%')
    
def mute(muteornot):
    global Mute, tracklastpos
    if muteornot:
        volumeSlider.set(tracklastpos)
        pygame.mixer.music.set_volume(volumeSlider.get())
        vol = volumeSlider.get() * 100
        vLabelpercent.config(text=f'{int(vol)}%')
        volumeBTN.config(image=UNMUTEIcon)
        volumeBTN.img = UNMUTEIcon
        Mute = False    
    else:
        tracklastpos = volumeSlider.get()
        pygame.mixer.music.set_volume(0)
        volumeSlider.set(0)
        vLabelpercent.config(text='Muted')
        volumeBTN.config(image=MUTEIcon)
        volumeBTN.img = MUTEIcon
        Mute = True
def increase_vol(event = None):
    volumeSlider.set(round(volumeSlider.get(), 2) + 0.05)
    pygame.mixer.music.set_volume(volumeSlider.get())
    vol =  round(volumeSlider.get(), 2) * 100
    if vol == 0:
        volumeBTN.config(image=MUTEIcon)
        volumeBTN.img = MUTEIcon
    elif vol == 100:
        pygame.mixer.music.set_volume(1.0)
    else:
        volumeBTN.config(image=UNMUTEIcon)
        volumeBTN.img = UNMUTEIcon
    vLabelpercent.config(text=f'{int(vol)}%')
def decrease_vol(event = None):
    volumeSlider.set(round(volumeSlider.get(), 2) - 0.05)
    pygame.mixer.music.set_volume(volumeSlider.get())
    vol = round(volumeSlider.get(), 2) * 100
    if vol == 0:
        volumeBTN.config(image=MUTEIcon)
        volumeBTN.img = MUTEIcon
    else:
        volumeBTN.config(image=UNMUTEIcon)
        volumeBTN.img = UNMUTEIcon
    vLabelpercent.config(text=f'{int(vol)}%')
    
def nextinfo(info):
    try:
        tag = eye.Tag()
        tag.parse(info)
        title = tag.title
        artist = tag.artist
        year = tag.getBestDate()
        filename = info
        filename = filename.replace(songsdir, '')
        filename = filename.replace('/', '')
        if title:            
            CNv1.set(f'Title: \t{title}')
        else:
            CNv1.set(f'Title: \t{filename}')
        if artist:
            CNv2.set(f'Artist: \t{artist}')
        else:
            CNv2.set("Artist: \tUnknown Artist")
        if year:    
            CNv3.set(f'Year: \t{year}')
        else:
            CNv3.set('Year: \tUnknown Year')
        load = MP3(info)
        songlen = load.info.length
        samplerate = load.info.sample_rate
        styme1 = time.strftime('%M:%S', time.gmtime(songlen))
        songbit = load.info.bitrate // 1000
        if samplerate:
            CNv4.set(f'Sample:\t{samplerate} Hz')
        else:
            CNv4.set("Sample:\tUnknown")
        if styme1:
            CNv5.set(f'Duration:\t{styme1}')
        else:
            CNv5.set("Duration:\tUnknown")
        if songbit:
            CNv6.set(f'Bitrate: \t{songbit} kbps')
        else:    
            CNv6.set("Bitrate: \tUnknown")
        cunext_des.config(text=CNv1.get()+"\n"+CNv2.get()+"\n"+CNv3.get()+"\n"+CNv4.get()+"\n"+CNv5.get()+"\n"+CNv6.get())
        filefound = True    
    except:
        pass

def getmetadata(filee):
    global filefound
    tag = eye.Tag()
    try:
        tag.parse(filee)
        title = tag.title
        artist = tag.artist
        year= tag.getBestDate()
        filename = filee
        filename = filename.replace(songsdir, '')
        filename = filename.replace('/', '')
        if title:            
            NPv1.set(f'Title: \t{title}')
        else:
            NPv1.set(f'Title: \t{filename}')
        if artist:
            NPv2.set(f'Artist: \t{artist}')
        else:
            NPv2.set("Artist: \tUnknown Artist")
        if year:    
            NPv3.set(f'Year: \t{year}')
        else:
            NPv3.set('Year: \tUnknown Year')
        load = MP3(filee)
        songlen = load.info.length
        samplerate = load.info.sample_rate
        styme1 = time.strftime('%M:%S', time.gmtime(songlen))
        songbit = load.info.bitrate // 1000
        if samplerate:
            NPv4.set(f'Sample: \t{samplerate} Hz')
        else:
            NPv4.set("Sample: \tUnknown")
        if styme1:
            NPv5.set(f'Duration:\t{styme1}')
        else:
            NPv5.set("Duration:\tUnknown")
        if songbit:
            NPv6.set(f'Bitrate: \t{songbit} kbps')
        else:    
            NPv6.set("Bitrate: \tUnknown")
        nowplaying_des.config(text=NPv1.get()+"\n"+NPv2.get()+"\n"+NPv3.get()+"\n"+NPv4.get()+"\n"+NPv5.get()+"\n"+NPv6.get())    
        filefound = True    
    except:
        pass
    

def getalbumArt(art, nextart):
    global filefound
    
    #Getting Metadata
    getmetadata(art)
    nextinfo(nextart)
    
    if filefound !=True:
        return
    
    image = 'Artwork-now.jpg'
    image2 = 'Artwork-next.jpg'
    backgroundIMG = 'bg.png'

    Folder = 'DownloaderMusicPlayer'
    workinfFolder = os.path.join(tempfile.gettempdir(), Folder)

    if not os.path.exists(workinfFolder):
        os.makedirs(workinfFolder)
    path = os.path.join(workinfFolder, image)

    path2 = os.path.join(workinfFolder, image2)
    BGPath = os.path.join(workinfFolder, backgroundIMG)
    # For Current Album Art
    try:
        metadata=audio_metadata.load(art)
        artwork = metadata.pictures[0].data
        with open(path, 'wb') as f:
            f.write(artwork)
        width = 170
        height = 130
        imggg = SM.open(path)
        imgg = imggg.resize((width,height), SM.ANTIALIAS)
        photoImg =  ImageTk.PhotoImage(imgg)
#For destroying        
#        for things in nowplayingIMG.winfo_children():
#            things.destroy()
        nowplayingLabel.config(image=photoImg)
        nowplayingLabel.img = photoImg

        left = 6
        top = screen_height / 2
        right = 900
        bottom = 2 * screen_height / 2
        im1 = imggg.crop((left, top, right, bottom))
        im2 = im1.resize((418,696), SM.ANTIALIAS)
        im2 = im2.filter(ImageFilter.GaussianBlur(radius=15)) 
        im2.save(BGPath)
        im2 = PhotoImage(file=BGPath)
        bg5.pack()
        bg5.config(image=im2)
        bg5.img=im2
                
    except:
        nowplayingLabel.config(image=ArtworkIcon)
        nowplayingLabel.img = ArtworkIcon                
        
    #For next album Art
    if nextart == None:
        pass
    else:
        try:
            metadata=audio_metadata.load(nextart)
            artwork = metadata.pictures[0].data
            with open(path2, 'wb') as f:
                f.write(artwork)
            width = 170
            height = 130
            img = SM.open(path2)
            img = img.resize((width,height), SM.ANTIALIAS)
            photoImg1 =  ImageTk.PhotoImage(img)
            cunextpicLabel.config(image=photoImg1)
            cunextpicLabel.img = photoImg1
        except:
            cunextpicLabel.config(image=ArtworkIcon)
            cunextpicLabel.img = ArtworkIcon
                
def getsongINFO():
    global pas, slide
    if Stop:
        return
    activeClick = musiclist.get(ACTIVE)
    activeClick = activeClick.replace('    ', '')
    song = os.path.join(songsdir, activeClick)
    try:
            song_load = MP3(slide)
    except:
        return
    global song_len
    song_len = song_load.info.length

    def gettime(_ = None):
        currentTIME = (pygame.mixer.music.get_pos() / 1000)
        ctyme = time.strftime('%M:%S', time.gmtime(currentTIME))
        styme = time.strftime('%M:%S', time.gmtime(song_len))
        if int(progressBar.get() == int(song_len)):            
            next()
        elif pausedornot:
            pass
        elif int(progressBar.get()) == int(currentTIME):
            #no movement to the slider
            sliderPOS = int(song_len)
            progressBar.config(to=sliderPOS, value=int(currentTIME))
        else:
            #slider moved
            sliderPOS = int(song_len)
            lag = int(pygame.mixer.music.get_pos()/1000) - progressBar.get()            
            progressBar.config(to=sliderPOS, value=int(progressBar.get()))
            ctyme = time.strftime('%M:%S', time.gmtime(int(progressBar.get())))
            endlbl.config(text=styme)
            startlbl.config(text=ctyme)
            nextt = int(progressBar.get()) + 1
            progressBar.config(to=sliderPOS, value=nextt)
            if lag >= 1:
                progressBar.config(to=sliderPOS, value=int(progressBar.get())+lag)
        startlbl.after(1000, gettime)
    if pas == False:
        gettime()
        pas = True
    else:
        pass
            
def playSongInitial(*args):
    play(pausedornot)
    
def play(check, event = None):
    global Stop, checksong, tl, slide
    global pausedornot, playBTN
    Stop = False
    activeClick = musiclist.get(ACTIVE)
    updatetitle(activeClick)
    song = os.path.join(songsdir, activeClick)
    song = song.replace('\\', '/')
    song = song.replace('    ', '')

    upnext = musiclist.curselection()
    musiclist.itemconfig(upnext[0],{'bg':'gray'})

    upnext = upnext[0]+1
    song2 = musiclist.get(upnext)
    filetype = song2[-3:]
    filetype = filetype.lower()
    if filetype == "mp3" or filetype == "wav" or filetype == "m4a" or filetype == "aac":
        path2 = os.path.join(songsdir, song2)
        path2 = path2.replace('\\', '/')
        path2 = path2.replace('    ', '')
    else:
        path2 = None

    if song != checksong:
        try:
            pygame.mixer.music.load(song)
            pygame.mixer.music.play(loops=0)
            slide = song
            playBTN.config(image=PAUSEIcon)
            playBTN.img = PAUSEIcon
            checksong = song
            pausedornot = False
            #Reset Progress Slider
            progressBar.config(value=0)
            getsongINFO()
        except:
            pass
    elif checksong == song:
        pausedornot = check
        if pausedornot:
            tl = tl.replace('    ', '')
            t = f'MusicByte - Playing:   ' + tl
            pygame.mixer.music.unpause()
            playBTN.config(image=PAUSEIcon)
            playBTN.img = PAUSEIcon
            screen.title(t)
            screen.update()
            pausedornot = False
        else:
            t = 'MusicByte - Paused'
            pygame.mixer.music.pause()
            playBTN.config(image=PLAYIcon)
            playBTN.img = PLAYIcon
            screen.title(t)
            screen.update()
            pausedornot = True
    getalbumArt(song, path2)

def shuffle(_=None):
    # Play Music Random when Repeat Mode is set to ALL.s
    global shufle
    global rep_one, rep_none, rep_all
    if shufle:
        shuffleBTN.config(image=shuffleOffIcon)
        shufflemode_des.config(text="Shuffle Mode: off\nShortcut: Alt+S")
        shufle = False
    elif rep_one:
        shuffleBTN.config(image=shuffleOnIcon)
        shufflemode_des.config(text="Shuffle Mode: on\nShortcut: Alt+S")        
        shufle = True
        rep_all = True
        rep_one = False
        rep_none = False
        repeatBTN.config(image=repeatAllIcon)
        repeatmode_des.config(text='Repeat Mode: All\nShortcut: Alt+R')
    elif rep_none:
        shuffleBTN.config(image=shuffleOnIcon)
        shufflemode_des.config(text="Shuffle Mode: on\nShortcut: Alt+S")        
        shufle = True
        rep_all = True
        rep_one = False
        rep_none = False
        repeatBTN.config(image=repeatAllIcon)
        repeatmode_des.config(text='Repeat Mode: All\nShortcut: Alt+R')
    elif rep_all:
        shuffleBTN.config(image=shuffleOnIcon)
        shufflemode_des.config(text="Shuffle Mode: on\nShortcut: Alt+S")        
        shufle = True
        rep_all = True
        rep_one = False
        rep_none = False
        repeatBTN.config(image=repeatAllIcon)
        repeatmode_des.config(text='Repeat Mode: All\nShortcut: Alt+R')        
    else:
        shuffleBTN.config(image=shuffleOnIcon)
        shufflemode_des.config(text="Shuffle Mode: on\nShortcut: Alt+S")        
        shufle = True
        rep_all = True
        rep_one = False
        rep_none = False
        repeatBTN.config(image=repeatAllIcon)
        repeatmode_des.config(text='Repeat Mode: All\nShortcut: Alt+R')
        
def repeat(_=None):
    # Play the current Song Once when Repeat Mode is set to None and Stop the Player.
    # Play Song next to next when Repeat Mode is set to All.
    # Play the current Song Repeatedly when Repeat Mode is set to One.
    global shufle
    global rep_one, rep_none, rep_all
    if rep_one:
        rep_one = False
        shufle = False
        shuffleBTN.config(image=shuffleOffIcon)
        shufflemode_des.config(text="Shuffle Mode: off\nShortcut: Alt+S")        
        rep_none = True
        rep_all = False        
        repeatBTN.config(image=repeatNoneIcon)
        repeatmode_des.config(text="Repeat Mode: None\nShortcut: Alt+R")

    elif rep_all:
        rep_all = False
        shufle = False
        shuffleBTN.config(image=shuffleOffIcon)
        shufflemode_des.config(text="Shuffle Mode: off\nShortcut: Alt+S")        
        rep_one = True
        rep_none = False
        repeatBTN.config(image=repeatOneIcon)
        repeatmode_des.config(text="Repeat Mode: One\nShortcut: Alt+R")
        
    elif rep_none:
        rep_none = False
        shufle = False
        shuffleBTN.config(image=shuffleOffIcon)
        shufflemode_des.config(text="Shuffle Mode: off\nShortcut: Alt+S")        
        rep_all = True
        rep_one = False
        repeatBTN.config(image=repeatAllIcon)
        repeatmode_des.config(text="Repeat Mode: All\nShortcut: Alt+R")        
    else:
        pass
        
def next(event = None):
    global playBTN, pausedornot, checksong, slide, shuf_ind
    global shuffle, rep_all, rep_one, rep_none, shuffle_database
    playBTN.config(image=PAUSEIcon)
    playBTN.img = PAUSEIcon
    #Reset Progress Slider
    progressBar.config(value=0)
    startlbl.config(text='--:--')
    endlbl.config(text='--:--')

    # If Shuffle Mode is ON
    if shufle == True and rep_all == True:
        try:
            song = shuffle_database[shuf_ind]
            nextsong = shuffle_database[shuf_ind+1]
        except:
            shuf_ind = 0
            nextsong = shuffle_database[shuf_ind]    
        slide = song
        if not song.startswith(songsdir):
            path = os.path.join(songsdir, song)
            path = path.replace('\\', '/')
            path = path.replace('    ', '')
            song = path
            path2 = os.path.join(songsdir, nextsong)
            path2 = path2.replace('\\', '/')
            path2 = path2.replace('    ', '')
            nextsong = path2        
        try:
            pygame.mixer.music.load(song)
            pygame.mixer.music.play(loops=0)
            slide = song
            pausedornot = False
            checksong = song
            getsongINFO()
        except:
            pass
        nextinfo(nextsong)
        getalbumArt(song, nextsong)
        try:
            musiclist.selection_clear(0, END)
            song = song.replace(songsdir,'')
            if not song.startswith('/'):
                song = '    ' + song
            else:
                song = song.replace('/', '    ')
            n = musiclist.get(0, 'end').index(song)    
            musiclist.activate(n)
            musiclist.selection_set(n, last=None)
            musiclist.see(n)
            musiclist.itemconfig(n,{'bg':'#a1a0a2'})
            updatetitle(musiclist.get(ACTIVE))
        except:
            pass
        shuf_ind += 1
            
    # If Shuffle Mode is OFF
    else:
        # If Repeat One is ON
        if rep_one == True:
            pygame.mixer.music.load(slide)
            pygame.mixer.music.play(loops=-1)
            playBTN.config(image=PAUSEIcon)
            playBTN.img = PAUSEIcon
            checksong = slide
            pausedornot = False
            #Reset Progress Slider
            progressBar.config(value=0)

        # If Repeat All is ON    
        elif rep_all == True:
            #Get the current song number
            slide = slide.replace(songsdir, '')
            try:
                slide = '    ' + slide
                currsong = musiclist.get(0, 'end').index(slide)
            except:
                slide = slide.replace('    ','')
                slide = slide.replace('/', '    ')
                currsong = musiclist.get(0, 'end').index(slide)
            try:
                #Get the next song number
                nextsong = currsong+1
                i1 = musiclist.get(nextsong)
                musiclist.get(0, 'end').index(i1)
            # Playing from Starting if it reached End of List    
            except:
                nextsong = 1
                
            try:
                #Get the upnext song number (Tuple Number)
                upnext = nextsong+1
                i2 = musiclist.get(upnext)
                musiclist.get(0, 'end').index(i2)
            except:
                upnext = 1

            song2 = musiclist.get(upnext)
            filetype = song2[-3:]
            filetype = filetype.lower()
            if filetype == "mp3" or filetype == "wav" or filetype == "m4a" or filetype == "aac":
                path2 = os.path.join(songsdir, song2)
                path2 = path2.replace('\\', '/')
                path2 = path2.replace('    ', '')
            else:
                path2 = None                
                
            song = musiclist.get(nextsong)
            if song == "" or song == None:
                return
            path = os.path.join(songsdir, song)
            path = path.replace('\\', '/')
            path = path.replace('    ', '')
            slide = path
            try:
                pygame.mixer.music.load(path)
                pygame.mixer.music.play(loops=0)
                slide = path
                pausedornot = False
                checksong = path
                getsongINFO()
            except:
                pass
            try:
                musiclist.selection_clear(0, END)
                musiclist.activate(nextsong)
                musiclist.selection_set(nextsong, last=None)
                musiclist.see(nextsong)
                musiclist.itemconfig(nextsong,{'bg':'#a1a0a2'})
                updatetitle(musiclist.get(ACTIVE))
            except:
                pass
            nextinfo(path2)
            getalbumArt(path, path2)

        # If Repeat None is ON    
        elif rep_none == True:
            pygame.mixer.music.stop()
            progressBar.config(value=0)
            startlbl.config(text='--:--')
            endlbl.config(text='--:--')
            nowplayingLabel.config(image=ArtworkIcon)
            cunextpicLabel.config(image=ArtworkIcon)
            playBTN.config(image=PLAYIcon)
            NPv1.set("Title: ")
            NPv2.set("Artist: ")
            NPv3.set("Year: ")
            NPv4.set("Sample: ")
            NPv5.set("Duration: ")
            NPv6.set("Bitrate: ")
            nowplaying_des.config(text=NPv1.get()+"\n"+NPv2.get()+"\n"+NPv3.get()+"\n"+NPv4.get()+"\n"+NPv5.get()+"\n"+NPv6.get())
            CNv1.set("Title: ")
            CNv2.set("Artist: ")
            CNv3.set("Year: ")
            CNv4.set("Sample: ")
            CNv5.set("Duration: ")
            CNv6.set("Bitrate: ")
            cunext_des.config(text=CNv1.get()+"\n"+CNv2.get()+"\n"+CNv3.get()+"\n"+CNv4.get()+"\n"+CNv5.get()+"\n"+CNv6.get())
        else:
            pass
        
    
def previous(event = None):
    global playBTN, pausedornot, checksong, slide
    
    # If Shuffle Mode is ON
    if shufle == True and rep_all == True:
        pass
    # If Shuffle Mode is OFF
    else:
        # If Repeat One is ON
        if rep_one == True:
            pass
        # If Repeat All is ON    
        elif rep_all == True:
            pass
        # If Repeat None is ON    
        elif rep_none == True:
            pass
        else:
            pass
    playBTN.config(image=PAUSEIcon)
    playBTN.img = PAUSEIcon
    upnext = musiclist.curselection()

    previoussong = musiclist.curselection()
    previoussong = previoussong[0]-1
    song = musiclist.get(previoussong)

    upnext = upnext[0]
    song2 = musiclist.get(upnext)

    if previoussong <=0:
        return

    try:
        path2 = os.path.join(songsdir, song2)
        path2 = path2.replace('\\', '/')
        path2 = path2.replace('    ', '')
    except:
        path2 = None

    nextinfo(path2)
    path = os.path.join(songsdir, song)
    path = path.replace('\\', '/')
    path = path.replace('    ', '')


    try:
        #Reset Progress Slider
        progressBar.config(value=0)

        pygame.mixer.music.load(path)
        pygame.mixer.music.play(loops=0)
        pausedornot = False
        checksong = path
        slide = path
        getsongINFO()
    except:
        pass

    try:
        musiclist.selection_clear(0, END)
        musiclist.activate(previoussong)
        musiclist.selection_set(previoussong, last=None)
        updatetitle(musiclist.get(ACTIVE))
    except:
        pass
    getalbumArt(path, path2)

def stop(_=None):
    pygame.mixer.music.stop()
    progressBar.config(value=0)
    startlbl.config(text='--:--')
    endlbl.config(text='--:--')
    nowplayingLabel.config(image=ArtworkIcon)
    cunextpicLabel.config(image=ArtworkIcon)
    playBTN.config(image=PLAYIcon)
    NPv1.set("Title: ")
    NPv2.set("Artist: ")
    NPv3.set("Year: ")
    NPv4.set("Sample: ")
    NPv5.set("Duration: ")
    NPv6.set("Bitrate: ")
    nowplaying_des.config(text=NPv1.get()+"\n"+NPv2.get()+"\n"+NPv3.get()+"\n"+NPv4.get()+"\n"+NPv5.get()+"\n"+NPv6.get())
    CNv1.set("Title: ")
    CNv2.set("Artist: ")
    CNv3.set("Year: ")
    CNv4.set("Sample: ")
    CNv5.set("Duration: ")
    CNv6.set("Bitrate: ")
    cunext_des.config(text=CNv1.get()+"\n"+CNv2.get()+"\n"+CNv3.get()+"\n"+CNv4.get()+"\n"+CNv5.get()+"\n"+CNv6.get())
    
def rewind(event = None):
    value = int(progressBar.get())
    if value >= 2:
        progressBar.set(value - 2)
    else:
        progressBar.set(0)
        
def forward(event = None):
    value = int(progressBar.get())
    if int(pygame.mixer.music.get_pos() / 1000) >= int(progressBar.get()) + 2:
        progressBar.set(value + 2)
    elif int(pygame.mixer.music.get_pos() / 1000) > 0:
        progressBar.set(int(pygame.mixer.music.get_pos() / 1000))        
    else:
        progressBar.set(0)        
#SETTING SCREEN WINDOW
screen = tk.Tk()

screen.geometry("418x696+400+0")
screen.maxsize(418, 696)
screen.minsize(418, 696)

screen.title("Downloader")
screen.iconbitmap(r'./Image/down_arrow_0of_icon.ico')
screen.config(bg = "grey17")
screen_width = screen.winfo_screenwidth()
screen_height = screen.winfo_screenheight()

#TOP NAVIGATION BAR
topFrame = Frame(screen)
topFrame.pack(side = "top", fill = "x")

#HEADER LABEL TEXT
homeLabel = Label(topFrame,
                  text = "DOWNLOADER",
                  font = ("jost", 15, "bold", "underline"),
                  height = 2,
                  fg = "red",
                  padx = 120)
homeLabel.pack(side = "top")

l = Label(topFrame,
                  font = ("verdana 8 bold"),
                  fg = "red")
l.place(x = 305, y = 25)

l1 = Label(topFrame,
                  text = "0.0 MB/s",
                  font = ("verdana 7 bold"),
                  fg = "red")
l1.place(x = 305, y = 10)

ArtworkIcon = PhotoImage(file = "./icon/Artwork-default.png")
#VARIOUS TABS
note_book = ttk.Notebook(screen, padding=0)
tab4 = Frame(note_book, bg='white')
bg5 = Label(tab4)
note_book.add(tab4, text = "    Music Player    ")        
note_book.place(x = 0, y = 30)
note_book.pack(expand = True, fill = "both")


def on_enter_search(event):
    nowplaying_des.place(x=10,y=10)
def on_leave_search(event):
    nowplaying_des.place(x=1000,y=1000)
    
#NOW PLAYING
nowplaying = Frame(tab4, height=160, width=170, bd=0, relief='flat')
nowplaying.place(x=6,y=6)
nowplaying.bind('<Enter>',on_enter_search)
nowplaying.bind('<Leave>',on_leave_search)
nowtext = Frame(nowplaying,height=30,width=170,bg='red')
nowtext.place(x=0,y=0)
nowlabel = Label(nowtext, text="Now Playing",bg='red',fg='white',font=('AdobeClean-Bold', 13))
nowlabel.place(x=36,y=0)
nowplayingIMG = Frame(nowplaying, height=130, width=170, bg='gray')
nowplayingIMG.place(x=0, y=30)
nowplayingLabel = Label(nowplayingIMG, height=130, width=170, image=ArtworkIcon, bd=0)
nowplayingLabel.place(x=0,y=0)
NPv1 = StringVar(tab4)
NPv1.set("Title: ")
NPv2 = StringVar(tab4)
NPv2.set("Artist: ")
NPv3 = StringVar(tab4)
NPv3.set("Year: ")
NPv4 = StringVar(tab4)
NPv4.set("Sample: ")
NPv5 = StringVar(tab4)
NPv5.set("Duration: ")
NPv6 = StringVar(tab4)
NPv6.set("Bitrate: ")
nowplaying_des = Label(tab4.winfo_toplevel(),
                       text=NPv1.get()+"\n"+NPv2.get()+"\n"+NPv3.get()+"\n"+NPv4.get()+"\n"+NPv5.get()+"\n"+NPv6.get(),
                       justify = "left", bd = 1, relief='solid', font = "verdana 8")


def on_enter_search(event):
    cunext_des.place(x=100,y=10)
def on_leave_search(event):
    cunext_des.place(x=1000,y=1000)
    
cunext = Frame(tab4, height=160, width=170, bd=0, relief='flat')
cunext.place(x=215,y=6)
cunext.bind('<Enter>',on_enter_search)
cunext.bind('<Leave>',on_leave_search)
cunexttext = Frame(cunext, height=30, width=170,bg='red')
cunexttext.place(x=0, y=0)
cunextlbl = Label(cunexttext, text='Comming Up Next',fg='white', bg='red',font=('AdobeClean-Bold', 13))
cunextlbl.place(x=20,y=0)##0f51c9
cunextpic = Frame(cunext, height=130, width=170, bg='#d0d0d0')
cunextpic.place(x=0,y=30)
cunextpicLabel = Label(cunextpic, height=130, width=170, image=ArtworkIcon, bd=0)
cunextpicLabel.place(x=0, y=0)
CNv1 = StringVar(tab4)
CNv1.set("Title: ")
CNv2 = StringVar(tab4)
CNv2.set("Artist: ")
CNv3 = StringVar(tab4)
CNv3.set("Year: ")
CNv4 = StringVar(tab4)
CNv4.set("Sample: ")
CNv5 = StringVar(tab4)
CNv5.set("Duration: ")
CNv6 = StringVar(tab4)
CNv6.set("Bitrate: ")
cunext_des = Label(tab4.winfo_toplevel(),
                   text=CNv1.get()+"\n"+CNv2.get()+"\n"+CNv3.get()+"\n"+CNv4.get()+"\n"+CNv5.get()+"\n"+CNv6.get(),
                   justify = "left", bd = 1, relief='solid', font = "verdana 8")

#CONTROL FRAME (MAIN)-------------------------------------------------------------------------
controlFRAME = Frame(tab4,height=90, width = 414, bd=0, relief = "flat")
controlFRAME.place(x=0,y=200)
controlFRAME.bind('<Button-1>', hide_volume_scale)

#Duration Label
startlbl = Label(controlFRAME, text='--:--')
startlbl.place(x=5,y=7)
endlbl = Label(controlFRAME, text='--:--')
endlbl.place(x=372,y=7)

#SLIDER 
progressBar = ttk.Scale(controlFRAME, from_=0, to=100, orient=HORIZONTAL, value=0, length=310, command=slider)
progressBar.place(x=50, y=4)

#CONTROLS
controlFrame1 = Frame(controlFRAME, height=45, width = 410)
controlFrame1.place(x=0,y=38)
controlFrame1.bind('<Button-1>', hide_volume_scale)

PLAYIcon = PhotoImage(file = "./icon/play.png")
PLAYIcon = PLAYIcon.subsample(3)
PAUSEIcon = PhotoImage(file = "./icon/pause.png")
PAUSEIcon = PAUSEIcon.subsample(3)
NEXTIcon = PhotoImage(file = "./icon/next.png")
NEXTIcon = NEXTIcon.subsample(3)
PREVIOUSIcon = PhotoImage(file = "./icon/previous.png")
PREVIOUSIcon = PREVIOUSIcon.subsample(3)
FORWARDIcon = PhotoImage(file = "./icon/forward.png")
FORWARDIcon = FORWARDIcon.subsample(3)
REWINDIcon = PhotoImage(file = "./icon/rewind.png")
REWINDIcon = REWINDIcon.subsample(3)
STOPIcon = PhotoImage(file = "./icon/stop.png")
STOPIcon = STOPIcon.subsample(3)

repeatNoneIcon = PhotoImage(file = "./icon/repeat-none.png")
repeatNoneIcon = repeatNoneIcon.subsample(3)
repeatOneIcon = PhotoImage(file = "./icon/repeat-one.png")
repeatOneIcon = repeatOneIcon.subsample(3)
repeatAllIcon = PhotoImage(file = "./icon/repeat-all.png")
repeatAllIcon = repeatAllIcon.subsample(3)
shuffleOnIcon = PhotoImage(file = "./icon/shuffle-on.png")
shuffleOnIcon = shuffleOnIcon.subsample(3)
shuffleOffIcon = PhotoImage(file = "./icon/shuffle-off.png")
shuffleOffIcon = shuffleOffIcon.subsample(3)

UNMUTEIcon = PhotoImage(file = "./icon/unmute.png")
UNMUTEIcon = UNMUTEIcon.subsample(3)
MUTEIcon = PhotoImage(file = "./icon/mute.png")
MUTEIcon = MUTEIcon.subsample(3)
DRAGANDDROPIcon = PhotoImage(file = "./icon/draganddrop.png")



play_des = Label(tab4.winfo_toplevel(), text="Play/Pause\nShortcut: Spacebar", justify = "left", bd=1, relief='solid', font = "verdana 8")
def on_enter_search(event):
    play_des.place(x=20,y=360)
def on_leave_search(event):
    play_des.place(x=1000,y=1000)
    
playBTN = Button(controlFrame1, image=PLAYIcon, bd = 0, command=lambda: play(pausedornot))
playBTN.place(x=5,y=6)
playBTN.bind('<Enter>',on_enter_search)
playBTN.bind('<Leave>',on_leave_search)

prev_des = Label(tab4.winfo_toplevel(), text="Previous Track\nShortcut: Alt+P", justify = "left", bd=1, relief='solid', font = "verdana 8")
def on_enter_search(event):
    prev_des.place(x=68,y=360)
def on_leave_search(event):
    prev_des.place(x=1000,y=1000)
    
prevBTN = Button(controlFrame1, image=PREVIOUSIcon, bd = 0, command = previous)
prevBTN.place(x=50,y=6)
prevBTN.bind('<Enter>',on_enter_search)
prevBTN.bind('<Leave>',on_leave_search)


rewind_des = Label(tab4.winfo_toplevel(), text="-2s/Long press to Rewind\nShortcut: Ctrl+Alt+P", justify = "left", bd=1, relief='solid', font = "verdana 8")
def on_enter_search(event):
    rewind_des.place(x=105,y=360)
def on_leave_search(event):
    rewind_des.place(x=1000,y=1000)
    
rewindBTN = Button(controlFrame1, image=REWINDIcon, bd = 0, command=rewind)
rewindBTN.place(x=86,y=6)
rewindBTN.bind('<Enter>',on_enter_search)
rewindBTN.bind('<Leave>',on_leave_search)

stop_des = Label(tab4.winfo_toplevel(), text="Stop\nShortcut: Alt+X", justify = "left", bd = 1, relief='solid', font = "verdana 8")
def on_enter_search(event):
    stop_des.place(x=140,y=360)

def on_leave_search(event):
    stop_des.place(x=1000,y=1000)
stopBTN = Button(controlFrame1, image=STOPIcon, bd=0, command=stop)
stopBTN.place(x=122,y=6)
stopBTN.bind('<Enter>',on_enter_search)
stopBTN.bind('<Leave>',on_leave_search)

forward_des = Label(tab4.winfo_toplevel(), text="+2s/Long press to Fast Forward\nShortcut: Ctrl+Alt+N", justify = "left", bd = 1, relief='solid', font = "verdana 8")
def on_enter_search(event):
    forward_des.place(x=173,y=360)

def on_leave_search(event):
    forward_des.place(x=1000,y=1000)
forwardBTN = Button(controlFrame1, image=FORWARDIcon, bd = 0, command = forward)
forwardBTN.place(x=158,y=6)
forwardBTN.bind('<Enter>',on_enter_search)
forwardBTN.bind('<Leave>',on_leave_search)


next_des = Label(tab4.winfo_toplevel(), text="Next Track\nShortcut: Alt+N", justify = "left", bd = 1, relief='solid', font = "verdana 8")
def on_enter_search(event):
    next_des.place(x=210,y=360)

def on_leave_search(event):
    next_des.place(x=1000,y=1000)
nextBTN = Button(controlFrame1, image=NEXTIcon, bd = 0, command = next)
nextBTN.place(x=194,y=6)
nextBTN.bind('<Enter>', on_enter_search)
nextBTN.bind('<Leave>', on_leave_search)

repeatmode_des = Label(tab4.winfo_toplevel(), text="Repeat Mode: All\nShortcut: Alt+R", justify = "left", bd = 1, relief='solid', font = "verdana 8")
def on_enter_search(event):
    repeatmode_des.place(x=258,y=360)
def on_leave_search(event):
    repeatmode_des.place(x=1000,y=1000)                
repeatBTN = Button(controlFrame1, image=repeatAllIcon, bd=0, command=repeat)
repeatBTN.place(x=240,y=6)
repeatBTN.bind('<Enter>', on_enter_search)
repeatBTN.bind('<Leave>', on_leave_search)

shufflemode_des = Label(tab4.winfo_toplevel(), text="Shuffle Mode: off\nShortcut: Alt+S", justify = "left", bd = 1, relief='solid', font = "verdana 8")
def on_enter_search(event):
    shufflemode_des.place(x=293,y=360)
def on_leave_search(event):
    shufflemode_des.place(x=1000,y=1000)                
shuffleBTN = Button(controlFrame1, image=shuffleOffIcon, bd=0, command=shuffle)
shuffleBTN.place(x=276,y=6)
shuffleBTN.bind('<Enter>', on_enter_search)
shuffleBTN.bind('<Leave>', on_leave_search)

volume_des = Label(tab4.winfo_toplevel(), text="Volume\nShortcut '+': Ctrl+Up\nShortcut '-' : Ctrl+Down", justify = "left", bd = 1, relief='solid', font = "verdana 8")
def on_enter_search(event):
    volume_des.place(x=270,y=360)
def on_leave_search(event):
    volume_des.place(x=1000,y=1000)                
volumeBTN = Button(controlFrame1, image=UNMUTEIcon, bd = 0, command=lambda: mute(Mute))
volumeBTN.place(x=320,y=6)
volumeBTN.bind('<Enter>', show_volume_scale)
volumeBTN.bind('<Enter>', on_enter_search, add='+')
volumeBTN.bind('<Leave>', on_leave_search)
vLabelpercent = Label(controlFrame1, text='75%', font = "bold")
vLabelpercent.place(x=356, y=12)

# Volume slider's Frame
volume_frame = Frame(tab4.winfo_toplevel(), bd = 1, relief='ridge')
volume_frame.place(x=327,y=190)
volume_frame.place_forget()
tab4.bind('<Button-1>', hide_volume_scale)

# Volume Slider
volumeSlider = ttk.Scale(volume_frame, from_=1, to=0, orient=VERTICAL, value=0.75, length=120, command=volume)
volumeSlider.grid(row=0, column=0, pady=1)
pygame.mixer.music.set_volume(volumeSlider.get())

openPlaylistIcon = PhotoImage(file = "./icon/open-playlist.png")
openPlaylistIcon = openPlaylistIcon.subsample(3)

addSongIcon = PhotoImage(file = "./icon/add-song.png")
addSongIcon = addSongIcon.subsample(3)

savePlaylistIcon = PhotoImage(file = "./icon/save-playlist.png")
savePlaylistIcon = savePlaylistIcon.subsample(3)

removeSongIcon = PhotoImage(file = "./icon/remove-song.png")
removeSongIcon = removeSongIcon.subsample(3)

clearPlaylistIcon = PhotoImage(file = "./icon/clear-playlist.png")
clearPlaylistIcon = clearPlaylistIcon.subsample(3)

#CONTROL FRAME (MAIN)-------------------------------------------------------------------------
manageFRAME = Frame(tab4, height=34, width=414, bd=0, relief = 'flat')
manageFRAME.place(x=0,y=295)
manageFRAME.bind('<Button-1>', hide_volume_scale)

open_des = Label(tab4.winfo_toplevel(), text="Open Playlist or Folder...\nShortcut: Ctrl+F", justify = "left", bd = 1, relief='solid', font = "verdana 8")
def on_enter_search(event):
    open_des.place(x=20,y=410)
def on_leave_search(event):
    open_des.place(x=1000,y=1000)                
openPlaylistBTN = Button(manageFRAME, image=openPlaylistIcon, bd = 0, command=addlibFolder) #ADD FOLDER TO LIBRARY)
openPlaylistBTN.place(x=5,y=1)
openPlaylistBTN.bind('<Enter>', on_enter_search)
openPlaylistBTN.bind('<Leave>', on_leave_search)

addsong_des = Label(tab4.winfo_toplevel(), text="Open File...\nShortcut: Ctrl+O", justify = "left", bd = 1, relief='solid', font = "verdana 8")
def on_enter_search(event):
    addsong_des.place(x=58,y=410)
def on_leave_search(event):
    addsong_des.place(x=1000,y=1000)                
addSongBTN = Button(manageFRAME, image=addSongIcon, bd=0, command=addSongs)
addSongBTN.place(x=42,y=2)
addSongBTN.bind('<Enter>', on_enter_search)
addSongBTN.bind('<Leave>', on_leave_search)

save_des = Label(tab4.winfo_toplevel(), text="Save Playlist\nShortcut: Ctrl+Y", justify = "left", bd = 1, relief='solid', font = "verdana 8")
def on_enter_search(event):
    save_des.place(x=95,y=410)
def on_leave_search(event):
    save_des.place(x=1000,y=1000)                
savePlaylistBTN = Button(manageFRAME, image=savePlaylistIcon, bd=0, command=save_playlist)
savePlaylistBTN.place(x=78,y=1)
savePlaylistBTN.bind('<Enter>', on_enter_search)
savePlaylistBTN.bind('<Leave>', on_leave_search)

remove_des = Label(tab4.winfo_toplevel(), text="Remove Selected\nShortcut: delete", justify = "left", bd = 1, relief='solid', font = "verdana 8")
def on_enter_search(event):
    remove_des.place(x=128,y=410)
def on_leave_search(event):
    remove_des.place(x=1000,y=1000)                
removeSongBTN = Button(manageFRAME, image=removeSongIcon, bd=0, command=lambda: remove('ONE'))
removeSongBTN.place(x=112,y=1)
removeSongBTN.bind('<Enter>', on_enter_search)
removeSongBTN.bind('<Leave>', on_leave_search)

clear_des = Label(tab4.winfo_toplevel(), text="Clear Playlist\nShortcut: None", justify = "left", bd = 1, relief='solid', font = "verdana 8")
def on_enter_search(event):
    clear_des.place(x=161,y=410)
def on_leave_search(event):
    clear_des.place(x=1000,y=1000)                
clearPlaylistBTN = Button(manageFRAME, image=clearPlaylistIcon, bd=0, command=lambda: remove('ALL'))
clearPlaylistBTN.place(x=145,y=1)
clearPlaylistBTN.bind('<Enter>', on_enter_search)
clearPlaylistBTN.bind('<Leave>', on_leave_search)

#MUSIC LIST DISPLAY BOX
musicboxFRAME = LabelFrame(tab4, text = "Playlist",
                           font = "BahnschriftLight 15 bold",
                           height=275, width=408, bg="white",fg="red",borderwidth=5,relief="sunken",highlightcolor="red",highlightbackground="red")
musicboxFRAME.place(x=0,y=335)
musicboxFRAME.bind('<Button-1>', hide_volume_scale)
musiclist = Listbox(musicboxFRAME,selectforeground='black', selectbackground='#bee0fa', activestyle='dotbox', height=15, width=64, bd = 0)
musiclist.pack(side='left', fill='y')

scroll = Scrollbar(musicboxFRAME, orient='vertical')
scroll.pack(side='right', fill='y')

drag = Label(tab4, text = "Playlist", image=DRAGANDDROPIcon,                
                height=138, width=141, bd = 0)
drag.place(x=130,y=370)
dragtitle = Label(tab4, bg="white", text = "Playlist is currently empty.\nDrop a file here or select a media source from the left.",)                                
dragtitle.place(x=60,y=520)
def e(event=None):
    if note_book.index(note_book.select()) == 0: # bind event for the first tab.
        musiclist.bind('<Double-Button>', playSongInitial)
        musiclist.bind('<Return>', playSongInitial)
        screen.bind('<Control-F>', addlibFolder)
        screen.bind('<Control-f>', addlibFolder)
        screen.bind('<space>', lambda event: play(pausedornot))
        screen.bind('<Alt-N>', next)
        screen.bind('<Alt-n>', next)
        screen.bind('<Alt-P>', previous)
        screen.bind('<Alt-p>', previous)
        screen.bind('<Control-Up>', increase_vol)
        screen.bind('<Control-Down>', decrease_vol)
        screen.bind('<Alt-S>', shuffle)
        screen.bind('<Alt-s>', shuffle)
        screen.bind('<Alt-R>', repeat)
        screen.bind('<Alt-r>', repeat)
        
    else:
        screen.unbind("<space>")

screen.bind('<<NotebookTabChanged>>', e)
