import tkinter as tk
import time
import re
import socket
import platform
from pytube import YouTube
from tkinter import PhotoImage
from tkinter import Frame
from tkinter import Label
from tkinter import LabelFrame
from tkinter import Button
from tkinter import ttk
from tkinter import StringVar
from tkinter import Text
from tkinter import END
from tkinter import Entry
from tkinter import OptionMenu
from tkinter import messagebox
from tkinter import Menubutton
from tkinter import Menu
from tkinter.scrolledtext import ScrolledText

# function to change properties of button on hover
def changeOnHover(button, colorOnHover, colorOnLeave):
  
    # adjusting backgroung of the widget
    # background on entering widget
    button.bind("<Enter>", func=lambda e: button.config(
        background=colorOnHover, foreground= "white"))
  
    # background color on leving widget
    button.bind("<Leave>", func=lambda e: button.config(
        background=colorOnLeave, foreground= "black"))
    
#FUNCTION TO CHECK THE INTERNET CONNECTION
import requests
def connection(url = "http://www.google.com/", timeout = 5):
    try:
        req = requests.get(url, timeout=timeout)
        req.raise_for_status()
        print("You're connected to internet\n")
        return True
    except requests.HTTPError as e:
        print("Checking internet connection failed, status code {0}.".format(e.response.status_code))        
    except requests.ConnectionError:        
        print("No internet connection available.")        
    return False

#FUNCTION FOR OPENING THE LOCATION OF A FILE
from tkinter.filedialog import askdirectory
def openlocationYTD():
    location = askdirectory()
    if file_pathYTD.get() != "":
        file_pathYTD.delete(0, END)
        file_pathYTD.insert(0, location)
    else:
        file_pathYTD.insert(0, location)                

import pyspeedtest
def is_connected():
    try:
        socket.create_connection(("www.google.com", 80)) # better to set timeout as well
        state = "Online"
        test = pyspeedtest.SpeedTest("www.google.com")
        print(test.ping())
        s = round((test.download()/125000), 2)
        if  s <= 1.0:
            notificationBtn = Label(topFrame,
                         image = wifi,
                         relief = "flat")
            notificationBtn.place(x = 360, y = 10)            
            notificationBtn.image=wifi
        elif s > 1.0 and s <= 2.0:
            notificationBtn = Label(topFrame,
                         image = wifi1,
                         relief = "flat")
            notificationBtn.place(x = 360, y = 10)                        
            notificationBtn.image=wifi1
        elif s > 2.0 and s <= 3.0:
            notificationBtn = Label(topFrame,
                         image = wifi2,
                         relief = "flat")
            notificationBtn.place(x = 360, y = 10)                                    
            notificationBtn.image=wifi2
        elif s >= 3.0:
            notificationBtn = Label(topFrame,
                         image = wifi3,
                         relief = "flat")
            notificationBtn.place(x = 360, y = 10)                        
            notificationBtn.image=wifi3
        print(str(s) + " MB/s")
        l1.config(text = str(s) + " MB/s")
    except OSError:
        state = "Offline"
        notificationBtn = Label(topFrame,
                         image = wifi_off,
                         relief = "flat")
        notificationBtn.place(x = 360, y = 11)                        
        notificationBtn.image=wifi_off
    l.config(text=state)
    print(state)
    topFrame.after(1000, is_connected) # do checking again one second later
    
def coming_soon():
    messagebox.showinfo('Coming Soon','The Feature You Clicked Will Be Coming Soon.\n Please Wait For An Update. Stay Tuned')
    
#LINK ENTRY
#search youtube video link & open a video in browser
from youtube_search import YoutubeSearch
import webbrowser

def show_link():
    if connection() == False:
        messagebox.showerror("Error", "No INTERNET connection")

    elif ytdEntry.get() == "":
        messagebox.showerror("Error", "Enter SOMETHING to Search")
        
    elif ytdEntry.get() == "Copy or paste url or type name":
        messagebox.showerror("Error","Please Paste URL or Enter Name")                
        
    else:
        global linkEntry1, linkEntry2, linkEntry3
        global playBtn1, playBtn2, playBtn3
        global copyBtn1, copyBtn2, copyBtn3
        global linkRes
        
        l = ytdEntry.get()
        vid = l
        print(vid)
        consoleYTDtext.config(state = "normal")
        consoleYTDtext.insert(1.0, "Initializing links.....\n")
        consoleYTDtext.tag_add("sixth", "1.0", "1.23")
            
        #configuring a tag called start
        consoleYTDtext.tag_config("sixth", foreground="red")
        consoleYTDtext.insert(END, "Waiting for response  .........\n")
        consoleYTDtext.see(END)        
        consoleYTDtext.config(state = "disabled")
        consoleYTD.update()
        l = []
        linkRes = []        
        
        #10 video link is generated max_result=10 we can also change the range
        results = YoutubeSearch(vid, max_results=3).to_dict()
        for v in results:
            l.append(v['url_suffix'])
            linkRes.append('https://www.youtube.com' + v['url_suffix'])
            print('https://www.youtube.com' + v['url_suffix'])
            
        global lframe
        lframe = Frame(tab2, height = 100, width = 412, bd = 1, relief = "solid")
        lframe.place(x = 2, y = 243)
        
        linkEntry1 = Entry(lframe, width = 30, bg = "red", fg = "white", borderwidth = 2, font = ("verdana"), relief = "sunken")
        linkEntry1.place(x = 4, y = 5)
        linkEntry1.insert(0, linkRes[0])
    
        linkEntry2 = Entry(lframe, width = 30, bg = "red", fg = "white", borderwidth = 2, font = ("verdana"), relief = "sunken")
        linkEntry2.place(x = 4, y = 35)
        linkEntry2.insert(0, linkRes[1])

        linkEntry3 = Entry(lframe, width = 30, bg = "red", fg = "white", borderwidth = 2, font = ("verdana"), relief = "sunken")
        linkEntry3.place(x = 4, y = 65)
        linkEntry3.insert(0, linkRes[2])

        consoleYTDtext.config(state = "normal")
        consoleYTDtext.insert(3.0, "response recieved!\n")
        consoleYTDtext.config(state = "disabled")
        consoleYTD.update()

        def copy1():

            if ytdEntry.get() == linkEntry1.get():
                consoleYTDtext.config(state = "normal")
                consoleYTDtext.insert(END, "URL is already copied.\n")
                consoleYTDtext.see(END)
                consoleYTDtext.config(state = "disabled")
                consoleYTD.update()
            else:    
                ytdEntry.delete(0, END)
                ytdEntry.insert(0, linkEntry1.get())
                consoleYTDtext.config(state = "normal")
                consoleYTDtext.insert(END, "URL " + linkEntry1.get() + " Copied Successfully.\n")
                line, column = consoleYTDtext.index('end').split('.')
                s = str(int(line) - 2 + 0.4)
                e = str(int(line) - 2 + 0.47)
                consoleYTDtext.tag_add("first", s, e)
            
                #configuring a tag called start
                consoleYTDtext.tag_config("first", foreground="red")
                consoleYTDtext.see(END)
                consoleYTDtext.config(state = "disabled")
                consoleYTD.update()            
        def copy2():
            if ytdEntry.get() == linkEntry2.get():
                consoleYTDtext.config(state = "normal")
                consoleYTDtext.insert(END, "URL is already copied.\n")
                consoleYTDtext.see(END)
                consoleYTDtext.config(state = "disabled")
                consoleYTD.update()
            else:    
                ytdEntry.delete(0, END)
                ytdEntry.insert(0, linkEntry2.get())
                consoleYTDtext.config(state = "normal")
                consoleYTDtext.insert(END, "URL " + linkEntry2.get() + " Copied Successfully.\n")
                line, column = consoleYTDtext.index('end').split('.')
                s = str(int(line) - 2 + 0.4)
                e = str(int(line) - 2 + 0.47)
                consoleYTDtext.tag_add("second", s, e)
            
                #configuring a tag called start
                consoleYTDtext.tag_config("second", foreground="green")
                consoleYTDtext.see(END)
                consoleYTDtext.config(state = "disabled")
                consoleYTD.update()                        
        def copy3():
            if ytdEntry.get() == linkEntry3.get():
                consoleYTDtext.config(state = "normal")
                consoleYTDtext.insert(END, "URL is already copied.\n")
                consoleYTDtext.see(END)
                consoleYTDtext.config(state = "disabled")
                consoleYTD.update()
            else:
                ytdEntry.delete(0, END)
                ytdEntry.insert(0, linkEntry3.get())
                consoleYTDtext.config(state = "normal")
                consoleYTDtext.insert(END, "URL " + linkEntry3.get() + " Copied Successfully.\n")
                line, column = consoleYTDtext.index('end').split('.')
                s = str(int(line) - 2 + 0.4)
                e = str(int(line) - 2 + 0.47)
                consoleYTDtext.tag_add("third", s, e)
            
                #configuring a tag called start
                consoleYTDtext.tag_config("third", foreground="blue")
                consoleYTDtext.see(END)
                consoleYTDtext.config(state = "disabled")
                consoleYTD.update()                    
        def play1():
            n = linkEntry1.get()
            print(n)
            if(n!=""):
                try:
                    webbrowser.open(n)
                    l= linkEntry1.get()
                except:
                    print('Something Went Wrong..')
            else:
                print('Error')
        def play2():
            n = linkEntry2.get()
            print(n)
            if(n!=""):
                try:
                    webbrowser.open(n)
                    l= linkEntry2.get()
                except:
                    print('Something Went Wrong..')
            else:
                print('Error')
        def play3():
            n = linkEntry3.get()
            print(n)
            if(n!=""):
                try:
                    webbrowser.open(n)
                    l= linkEntry3.get()
                except:
                    print('Something Went Wrong..')
            else:
                print('Error')

                        
        #PLAY BUTTON            
        playBtn1 = Button(lframe,
                          width = 5,
                          command = play1,
                          bg = "white",
                          fg = "red",
                          text = "Play",
                          bd = 4,
                          font = ("verdana", 7, "bold"))
        playBtn1.place(x = 310, y = 5)
        playBtn2 = Button(lframe,
                          width = 5,
                          command = play2,
                          bg = "white",
                          fg = "red",
                          text = "Play",
                          bd = 4,
                          font = ("verdana", 7, "bold"))
        playBtn2.place(x = 310, y = 35)
        playBtn3 = Button(lframe,
                          width = 5,
                          command = play3,
                          bg = "white",
                          fg = "red",
                          text = "Play",
                          bd = 4,
                          font = ("verdana", 7, "bold"))                      
        playBtn3.place(x = 310, y = 65)


        #COPY BUTTON
        copyBtn1 = Button(lframe,
                          width = 5,
                          command = copy1,
                          bg = "red",
                          fg = "white",
                          text = "Copy",
                          bd = 4,
                          font = ("verdana", 7, "bold"))
        copyBtn1.place(x = 360, y = 5)
        copyBtn2 = Button(lframe,
                          width = 5,
                          command = copy2,
                          bg = "red",
                          fg = "white",
                          text = "Copy",
                          bd = 4,
                          font = ("verdana", 7, "bold"))
        copyBtn2.place(x = 360, y = 35)
        copyBtn3 = Button(lframe,
                          width = 5,
                          command = copy3,
                          bg = "red",
                          fg = "white",
                          text = "Copy",
                          bd = 4,
                          font = ("verdana", 7, "bold"))
        copyBtn3.place(x = 360, y = 65)

#SPEECH SEARCH
import pyttsx3
import speech_recognition as sr
import os

global search_result

def search():
    if connection() == False:
        messagebox.showerror("Error", "No INTERNET connection")
    else:
        global search_result
        search_result = []
        r = sr.Recognizer()
    
        with sr.Microphone() as source:
            print('Listening')
            r.pause_threshold = 0.5
            
            # storing audio/sound to audio variable
            audio = r.listen(source)
            try:
                print("Recognizing")
                
                # Recognizing audio using google api
                Query = r.recognize_google(audio)
                print("the query is printed='", Query, "'")
                search_result.append(Query)
                print(search_result)
            except Exception as e:
                print(e)
                print("Say that again sir")
                
                # returning none if there are errors
                return "None"
            
        # returning audio as text
        ytdEntry.delete(0, END)
        ytdEntry.insert(0, str(search_result[0]))
        show_link()
        import time
        time.sleep(2)
        return Query
        
def downloadYTD():
    if connection() == False:
        messagebox.showerror("Error","No INTERNET connection")
        
    elif ytdEntry.get() == "":
        messagebox.showerror("Error","Please Paste URL or Enter Name")
        
    elif re.match(r'^(http(s)??\:\/\/)?(www\.youtube\.com\/watch\?v=)|(youtu.be\/)([a-zA-Z0-9\-_])+$/g', ytdEntry.get()) == None:
        messagebox.showerror("Error","Please enter a valid url")
                        
    elif file_pathYTD.get() == "":
        messagebox.showerror("Error","Please provide Path")
                
    else:
        consoleYTDtext.config(state = "normal")
        consoleYTDtext.insert(END, "Starting download......\n")
        consoleYTDtext.insert(END, "If downloading not start in few 10 seconds try Best Available in Quality\n")
        line, column = consoleYTDtext.index('end').split('.')
        print(line)
        s = str(int(line) - 2 + 0.0)
        print(s)
        e = str(int(line) - 1 + 0.21)
        print(e)
        consoleYTDtext.tag_add("fourth", s, e)
            
        #configuring a tag called start
        consoleYTDtext.tag_config("fourth", foreground="orange")
        consoleYTDtext.see(END)
        consoleYTDtext.config(state = "disabled")
        consoleYTD.update()                            

        def progress_bar(stream, chunk, bytes_remaining):
            percent = int(100 - ((100 * bytes_remaining) / filesize))
            progressbarYTD["value"] = percent
            style.configure('text.Horizontal.TProgressbar', text='{:s} %'.format(str(percent)))  # update label
            tab2.update()
            print("{:00.0f}%".format(percent))
  
        def complete(chunk, bytes_remaining):
            consoleYTDtext.config(state = "normal")
            consoleYTDtext.insert(END, "Downloading Complete\n")
            line, column = consoleYTDtext.index('end').split('.')
            print(line)
            s = str(int(line) - 2 + 0.0)
            print(s)
            e = str(int(line) - 2 + 0.21)
            print(e)
            consoleYTDtext.tag_add("fifth", s, e)
            
            #configuring a tag called start
            consoleYTDtext.tag_config("fifth", foreground="green")
            consoleYTDtext.see(END)
            consoleYTDtext.config(state = "disabled")
            consoleYTD.update()
            messagebox.showinfo("SUCCESSFULLY", "DOWNLOADED AND SAVED IN\n" + file_pathYTD.get())
            

        try:
            global filesize
            url = ytdEntry.get()
            print(url)
            path = file_pathYTD.get()
            print(path)
            qual = variable1.get()
            print(qual)
            yt = YouTube(url, on_complete_callback = complete)
            yt.register_on_progress_callback(progress_bar)                        
            if qual == "Best Available":
                stream = yt.streams.filter(progressive = True, file_extension = "mp4").first()
            elif qual == "1080-Video-Only":
                itag = 137
                stream = yt.streams.get_by_itag(itag)
            elif qual == "720p-Video-Only":
                itag = 136
                stream = yt.streams.get_by_itag(itag)
            elif qual == "480p-Video-Only":
                itag = 135
                stream = yt.streams.get_by_itag(itag)
            elif qual == "360p-Dual":
                itag = 134
                stream = yt.streams.get_by_itag(itag)
            elif qual == "Audio-Only-50kbps":
                itag = 249
                stream = yt.streams.get_by_itag(itag)
            elif qual == "Audio-Only-Best":                        
                stream = yt.streams.filter(type = "audio").first()
    
            filesize = stream.filesize
            size_inBytes = filesize
            size_inMB = size_inBytes / 1024000
            mb = str(round(size_inMB, 2)) + " MB"
            consoleYTDtext.config(state = "normal")
            consoleYTDtext.insert(END, "Total size : " + mb + "\n")
            consoleYTDtext.see(END)
            consoleYTDtext.config(state = "disabled")
            consoleYTD.update()
            stream.download(path)
                                                
        except Exception as e:
            time.sleep(10)
            print(e)
            messagebox.showerror("Error","Unable to Download Video | Something went wrong !!")        


def clearYTD():
    try:
        
        ytdEntry.delete(0, END)
        ytdEntry.insert(0, "Copy or paste url or type name")        
        
        consoleYTDtext.config(state = "normal")
        consoleYTDtext.delete(1.0, END)
        consoleYTDtext.config(state = "disabled")
        
        linkEntry1.destroy()
        linkEntry2.destroy()
        linkEntry3.destroy()
        playBtn1.destroy()
        playBtn2.destroy()
        playBtn3.destroy()
        copyBtn1.destroy()
        copyBtn2.destroy()
        copyBtn3.destroy()
        
        file_pathYTD.delete(0, END)
        progressbar["value"] = 0
        style.configure('text.Horizontal.TProgressbar', text='0 %')

    except:
        pass


#SETTING SWITCH FUNCTION
#SETTING SWITCH STATE

btnState = False
def switch():
    global btnState    
    if btnState is True:
        #CREATING ANIMATED NAVBAR (CLOSING)   
        for x in range(0, 301, 20):
            navBarRoot.place(x = -x, y = 0)
            topFrame.update()

        #resetting widget colors:
        #homeLabel.config(bg = "gray17")        
        #topFrame.config(bg = "gray17")
        #screen.config(bg = "gray17")

        #turning button OFF:
        btnState = False
    else:
        
        #make root dim:
        #homeLabel.config(bg = "gray17")
        #topFrame.config(bg = "gray17")
        #screen.config(bg = "gray17")

        #CREATING ANIMATED NAVBAR (OPENING)
        for x in range(-301, 0, 10):        
            navBarRoot.place(x = x, y = 0)
            topFrame.update()

        #turning button ON:
        btnState = True

def help():
    main_menu = Menu(navBarRoot, tearoff=0)
    navBarRoot.configure(menu=main_menu)
    
def feedback():
    feed = Frame(screen, height = 675, width = 400, bd = 1, relief = "solid")
    feed.place(x = 10, y = 10)
    
    headerLbl = Label(feed,
                      text = "FEEDBACK",
                      font = "Arial 20 bold underline",
                      fg = "red")
    headerLbl.place(x = 120, y = 30)

    messageLbl = Label(feed,
                       text = "PLEASE TELL US WHAT YOU THINK",
                       fg = "red",
                       font = "Arial 11")
    messageLbl.place(x = 80, y = 90)

    myvar = StringVar()
    var = StringVar()
    # cmnt= StringVar()

    nameLbl = Label(feed, text = "Name: ", font = "Arial 11 bold")
    nameLbl.place(x = 10, y = 130)

    nameEntry = Entry(feed, width = 35, relief = "solid", font = "Arial", textvariable=myvar)
    nameEntry.place(x = 70, y = 130)


    emailLbl = Label(feed, text = "Email: ", font = "Arial 11 bold")
    emailLbl.place(x = 10, y = 170)
    
    emailEntry = Entry(feed, width = 35, relief = "solid", font = "Arial", textvariable=var)
    emailEntry.place(x = 70, y = 170)

    commentLbl = Label(feed, text = "Comment: ", font = "Arial 11 bold")
    commentLbl.place(x = 10, y = 215)

    textcomment = Text(feed, width = 47, height = 16, relief = "solid")
    textcomment.place(x = 10, y = 252)
    textcomment.config(wrap = "word")

    footerTitleLbl = Label(feed,
                           text = "Version 1.0.0",
                           font = "Bahnschrift 10 bold underline",
                           width = 55,
                           height = 2,
                           bg = "red").place(x = 4, y = 630)    

    def clear():
        if(messagebox.askokcancel("Confirm", "Do you want to clear?")):
            nameEntry.delete(0, END)
            emailEntry.delete(0, END)
            textcomment.delete(1.0, END)


    def submit():
        print('Name: {}'.format(myvar.get()))
        print('Email: {}'.format(var.get()))
        print('Comment: {}'.format(textcomment.get(1.0, END)))
        if (messagebox.askyesno("Confirm", "Do you want to submit?")):
            messagebox.showinfo("Submitted", "Thank you for your Feedback.\nYour Comments are Successfully Submitted.")
            nameEntry.delete(0, END)
            emailEntry.delete(0, END)
            textcomment.delete(1.0, END)

    clearBtn = Button(feed,
                      text = "Clear",
                      width = 12,
                      bg = "red",
                      fg = "white",
                      font = ("jost", 11, "bold"),                      
                      relief = "flat",
                      command = clear).place(x = 60, y = 530)
    submitBtn = Button(feed,
                       text = "Submit",
                       width = 12,
                       bg = "red",
                       fg = "white",
                       font = ("jost", 11, "bold"),                                             
                       relief = "flat",
                       command = submit).place(x = 220,y = 530)



    def closedButton():
        feed.place(x = -1000, y = 0)
        feed.update()

    backBtn = Button(feed,
                     image = BackIcon,
                     relief = "flat",
                     command = closedButton).place(x = 360, y = 2)

def aboutus():
    aboutus = Frame(screen, height = 675, bg = "white", width = 400, bd = 1, relief = "solid")
    aboutus.place(x = 10, y = 10)

    headerLbl = Label(aboutus,
                      text = "About Us",
                      font = "Arial 30 bold underline",
                      bg = "white")
    headerLbl.place(x = 120, y = 30)

    headerLbl1 = Label(aboutus,
                      text = "We",
                      font = "verdana 50 bold",
                      fg = "red",
                      bg = "white")
    headerLbl1.place(x = 140, y = 100)

    headerLbl2 = Label(aboutus,
                      text = "Are",
                      font = "verdana 60 bold",
                      fg = "red",
                      bg = "white")
    headerLbl2.place(x = 120, y = 200)

    headerLbl3 = Label(aboutus,
                      text = "Engineers",
                      font = "verdana 50 bold",
                      fg = "red",
                      bg = "white")
    headerLbl3.place(x = 5, y = 300)

    textLbl = Label(aboutus,
                      text = "Shivank Vishwakarma\nAddhayayan Pandey\nAtul Bajpai\n(Information Technology)",
                      font = "verdana 15 bold",
                      bg = "white")
    textLbl.place(x = 60, y = 420)


    footerLbl = Label(aboutus,
                      text = "Copyright © 2022 Downloader",
                      font = "verdana 10 bold",
                      fg = "red",
                      bg = "white")
    footerLbl.place(x = 170, y = 650)
    
    def closedButton():
        aboutus.place(x = -1000, y = 0)
        aboutus.update()

    backBtn = Button(aboutus,
                     image = BackIcon,
                     relief = "flat",
                     bg = "white",
                     activebackground = "white",
                     command = closedButton).place(x = 360, y = 2)

from io import BytesIO
from PIL import Image, ImageTk
def check():
    if connection() == False:
        messagebox.showerror("Error","No INTERNET connection")

    elif ytdEntry.get() == "":
        messagebox.showerror("Error","Please Paste URL or Enter Name")
        
    elif ytdEntry.get() == "Copy or paste url or type name":
        messagebox.showerror("Error","Please Paste URL or Enter Name")        
            
    elif re.match(r'^(http(s)??\:\/\/)?(www\.youtube\.com\/watch\?v=)|(youtu.be\/)([a-zA-Z0-9\-_])+$/g', ytdEntry.get()) == None:
        messagebox.showerror("Error","Please enter valid url")
        
    elif variable.get() == "SELECT QUALITY":
        messagebox.showerror("Error","Please Select Quality")
        
    else:
        
        def check1():    
            url = ytdEntry.get()
            yt = YouTube(url)
            qual = variable.get()
            try:
                if qual == "Best Available":
                    stream = yt.streams.filter(progressive = True, file_extension = "mp4").first()
                elif qual == "1080-Video-Only":
                    itag = 137
                    stream = yt.streams.get_by_itag(itag)
                elif qual == "720p-Video-Only":
                    itag = 136
                    stream = yt.streams.get_by_itag(itag)
                elif qual == "480p-Video-Only":
                    itag = 135
                    stream = yt.streams.get_by_itag(itag)
                elif qual == "360p-Dual":
                    itag = 134
                    stream = yt.streams.get_by_itag(itag)
                elif qual == "Audio-Only-50kbps":
                    itag = 249
                    stream = yt.streams.get_by_itag(itag)
                elif qual == "Audio-Only-Best":                        
                    stream = yt.streams.filter(type = "audio").first()
                    
                filesize = stream.filesize
                size_inBytes = filesize
                size_inMB = size_inBytes / 1024000
                mb = str(round(size_inMB, 2)) + " MB"
                                                
            except Exception as e:
                time.sleep(10)
                print(e)
                messagebox.showerror("Error","Unable to Download Video | Something went wrong !!")
            
            res = requests.get(yt.thumbnail_url)
            file = BytesIO(res.content)
            img = Image.open(file)
            img = img.resize((140, 105), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
    
            l1 = Label(tab2, width = 30,text = "title", wraplength = 250, font = ("verdana", 8, "bold"))
            l1.place(x = 160,y = 240)
        
            video_size = Label(tab2, text = 'Total Size: 0MB', font = "verdana 10 bold")
            video_size.place(x = 180, y = 310)
        
            f1 = Frame(tab2, height = 105, width = 140, bg = "white", relief = "solid")
            f1.place(x = 5, y = 236)

            l2 = Label(f1, text = 'Video \n Thumbnail', font = ('times new roman', 15), bg = 'lightgrey', bd = 2, relief = "ridge", image = img)
            l2.place(x = 0,y = 0)
        
            l2.image = img
            l1.config(text = yt.title)        
            video_size.config(text = f'Total Size: {mb}')
            
        try:
            if lframe.winfo_exists():
                lframe.destroy()
            check1()
        except:
            check1()

def aboutwindow():
    def licenses():
        line1.destroy()
        aboutframe.destroy()
        footer1.destroy()
        lbl2.destroy()
        lbl3.destroy()
        lbl4.destroy()
        lbl5.destroy()
        mit = Label(infoframe, text='MIT License')
        mit.place(x=160,y=80)
        copyryt = Label(infoframe, text='Copyright (c) 2022 Downloader')
        copyryt.place(x=110,y=105)

        bottomfrm = Frame(win, height=290, width=420)
        bottomfrm.place(x=310, y=160)
        textlbl = Label(bottomfrm, text='Permission is hereby granted, free of charge, to any person obtaining a copy\n'\
                                        'of this software and associated documentation files (the "Software"), to deal\n'\
                                        'in the Software without restriction, including without limitation the rights to\n'\
                                        'use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies\n'\
                                        'of the Software, and to permit persons to whom the Software is furnished to \n'\
                                        'do so, subject to the following conditions:\n\n'\
                                        'The above copyright notice and this permission  notice shall be included in\n'\
                                        'all copies or substantial portions of the Software.\n\n'\
                                        'THE  SOFTWARE  IS  PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,\n'\
                                        'EXPRESS  OR  IMPLIED, INCLUDING  BUT NOT LIMITED TO THE WARRANTIES \n'\
                                        'OF MERCHANTABILITY, FITNESS  FOR  A  PARTICULAR PURPOSE AND NON-\n'\
                                        'INFRINGEMENT.IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLD-\n'\
                                        'ERS BE  LIABLE  FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER\n'\
                                        'IN AN ACTION  OF CONTRACT, TORT  OR OTHERWISE, ARISING FROM, OUT\n'\
                                        'OF  OR  IN  CONNECTION  WITH  THE  SOFTWARE  OR  THE  USE  OR OTHER\n'\
                                        'DEALINGS IN THE SOFTWARE.', justify='left')
        textlbl.place(x=0,y=0)

    
    width = 745
    height = 570
    win = tk.Toplevel(screen)
    win.wm_title("Downloader - About")
    screen_width = screen.winfo_screenwidth()
    screen_height = screen.winfo_screenheight()

    x = int((screen_width/2) - (width/2))
    y = int((screen_height/2) - (height/2))

    win.geometry("{}x{}+{}+{}".format(width, height, x, y))
    win.resizable(False, False)
    win.focus_set()
    win.iconbitmap(r'./Image/down_arrow_0of_icon.ico')

    host = socket.gethostname()
    processor = platform.processor()
    System = f'{platform.system()}, {platform.version()}, {platform.architecture()[0]}'
    Machine = processor.split(',')
    
    b = PhotoImage(file = "./Image/b2.png")
    logoframe = Frame(win, height=400, width=260)    
    logoframe.place(x=25,y=50)
    logo = Label(logoframe, image=b)
    logo.img = b
    logo.place(x=0,y=0)

    infoframe = Frame(win, height=165, width=390)
    infoframe.place(x=320,y=15)
    lbl1 = Label(infoframe, text='Downloader - Social Media Downloader', font='AdobeClean-Bold 13 bold')
    lbl1.place(x=40,y=5)
    vlbl = Label(infoframe, text='Version 1.0.0')
    vlbl.place(x=160,y=30)
    line = Frame(win, height=1, width=397, highlightthickness=1, highlightbackground='black',bd = 2, relief="solid")
    line.place(x=315, y=80)
    lbl2 = Label(infoframe, text=f'Host Machine: {host}')
    lbl2.place(x=30, y=80)
    lbl3 = Label(infoframe, text=f'Current System: {System}')
    lbl3.place(x=30, y=100)
    lbl4 = Label(infoframe, text=f'Processor: {processor}')
    lbl4.place(x=30, y=120)
    lbl5 = Label(infoframe, text=f'Machine Type: {Machine[1]}')
    lbl5.place(x=30, y=140)
    
    line1 = Frame(win, height=1, width=397, highlightthickness=1, highlightbackground='black')
    line1.place(x=315, y=190)

    aboutframe = Frame(win, height=230, width=420)
    aboutframe.place(x=310, y=205)
    about = Label(aboutframe, text='MusicByte is a Stylish, Powerful and  Fast Music Player  with  elegant design. \n'\
                                    'It lets you manage all your music files and folder quickly and easily. \n\n'\
                                    'This audio  player  supports  almost all types of music files such as mp3, aac, \n' \
                                    'wav and m4a audio formats. Easily browse and play music songs by albums, \n'\
                                    'artists , songs and folder.', justify='left')
    about.place(x=0,y=0)
    
    features = Label(aboutframe, text='Currently MusicByte fully Supports (Features): \n\n'\
                                        '    - A simple, flat and material UI design\n'\
                                        '    - Audio file formats such as MP3, WAV, M4A and AAC\n'\
                                        '    - Volume Slider and ProgressBar works fine\n'\
                                        '    - Add Songs via Folder or you can select single audio files\n'\
                                        '    - Remove songs, (current or all songs)', justify='left')
    features.place(x=0, y=100)

    footer1 = Frame(win, height=60, width=420)
    footer1.place(x=310,y=430)
    footerlbl = Label(footer1, text='MusicByte player is a Music  Player  for  Windows. Send  me  the feedbacks,\n'\
                                    'bug-reports and suggestions about Downloader to:', justify='left')
    footerlbl.place(x=0,y=0)
    emaillbl = Label(footer1, text='downloader@gmail.com',fg="blue", cursor="hand2")
    emaillbl.place(x=130,y=35)
    
    footer2 = Frame(win, height=50, width=745, bg ='#c3c3c3', relief='flat')
    footer2.place(x=0,y=520)

    authorsBtn = Button(footer2, text='Authors', activeforeground ='blue', activebackground ='#c3c3c3', bd=0, bg ='#c3c3c3', fg='blue', font='AdobeClean-Bold 9 underline', height=3, width=34, relief='flat', cursor="hand2", command=coming_soon)
    authorsBtn.place(x=0,y=0)
    licenseBtn = Button(footer2, text='License', activeforeground ='blue', activebackground ='#c3c3c3', bd=0, bg ='#c3c3c3', fg='blue', font='AdobeClean-Bold 9 underline', height=3, width=34, relief='flat', cursor="hand2", command=licenses)
    licenseBtn.place(x=248,y=0)
    creditsBtn = Button(footer2, text='Credits', activeforeground ='blue', activebackground ='#c3c3c3', bd=0, bg ='#c3c3c3', fg='blue', font='AdobeClean-Bold 9 underline', height=3, width=34, relief='flat', cursor="hand2", command=coming_soon)
    creditsBtn.place(x=497,y=0)

    b = ttk.Button(win, text="Close", command=win.destroy)
    b.place(x=480, y=490)
    
#SETTING SCREEN WINDOW
screen = tk.Tk()

screen.geometry("418x696+939+0")
screen.maxsize(418, 696)
screen.minsize(418, 696)

screen.title("Downloader")
screen.iconbitmap(r'./Image/down_arrow_0of_icon.ico')
screen.config(bg = "grey17")
screen_width = screen.winfo_screenwidth()
screen_height = screen.winfo_screenheight()

#LOADING NAVBAR ICON IMAGE
NavIcon = PhotoImage(file = "./Image/menu.png")
CloseIcon = PhotoImage(file = "./Image/close.png")
SettingIcon = PhotoImage(file = "./Image/setting.png")
DownloadIcon = PhotoImage(file = "./Image/direct-download.png")
FeedbackIcon = PhotoImage(file = "./Image/feedback.png")
HomeIcon = PhotoImage(file = "./Image/home.png")
AboutIcon = PhotoImage(file = "./Image/about.png")
YouTubeIcon = PhotoImage(file = "./Image/youtube.png")
NotificationIcon = PhotoImage(file = "./Image/notification.png")
ListenIcon = PhotoImage(file = "./Image/listener.png")
SearchIcon = PhotoImage(file = "./Image/search.png")
BackIcon = PhotoImage(file = "./Image/back.png")
HELPIcon = PhotoImage(file = "./Image/help.png")

CheckIcon = PhotoImage(file = "./Image/arrow.png")

FBIcon = PhotoImage(file = "./Image/facebookicon.png")
INSTAIcon = PhotoImage(file = "./Image/instagramicon.png")
YTIcon = PhotoImage(file = "./Image/youtubeicon.png")
LinIcon = PhotoImage(file = "./Image/linkedinicon.png")

wifi = PhotoImage(file = "./Image/wifi.png")
wifi1 = PhotoImage(file = "./Image/wifi1.png")
wifi2 = PhotoImage(file = "./Image/wifi2.png")
wifi3 = PhotoImage(file = "./Image/wifi3.png")
wifi_off = PhotoImage(file = "./Image/wifi_off.png")

#TOP NAVIGATION BAR
topFrame = Frame(screen, bg='white')
topFrame.pack(side = "top", fill = "x")

#HEADER LABEL TEXT
homeLabel = Label(topFrame,
                  text = "DOWNLOADER",
                  font = ("jost", 15, "bold", "underline"),
                  height = 2,
                  bg='white',
                  fg = "red",
                  padx = 120)
homeLabel.pack(side = "top")

#NOTIFICATION BUTTON
notificationBtn = Label(topFrame,
                         image = wifi,
                         bg='white',
                         relief = "flat")
notificationBtn.place(x = 360, y = 11)

l = Label(topFrame,
                  font = ("verdana 8 bold"),
                  bg='white',
                  fg = "red")
l.place(x = 305, y = 25)

l1 = Label(topFrame,
                  text = "0.0 MB/s",
                  font = ("verdana 7 bold"),
                  bg='white', 
                  fg = "red")
l1.place(x = 305, y = 10)

#VARIOUS TABS
note_book = ttk.Notebook(screen)
tab1 = Frame(note_book, bg="white")
tab2 = Frame(note_book)
tab3 = Frame(note_book)
tab4 = Frame(note_book, bg="white")
tab5 = Frame(note_book)
bg5 = Label(tab5)
note_book.add(tab1, text = "    Home    ")
note_book.add(tab2, text = "    YouTube      ")
note_book.add(tab3, text = "    Instagram    ")
note_book.add(tab4, text = "    Music Player    ")
note_book.add(tab5, text = "      QrCode      ")        

note_book.place(x = 10, y = 30)
note_book.pack(expand = True, fill = "both")

"""lframe = Frame(tab2, height = 100, width = 412, bd = 1, relief = "solid")
lframe.place(x = 2, y = 243)

linkEntry1 = Entry(lframe, width = 30, bg = "red", fg = "white", borderwidth = 2, font = ("verdana"), relief = "sunken")
linkEntry1.place(x = 4, y = 5)
    
linkEntry2 = Entry(lframe, width = 30, bg = "red", fg = "white", borderwidth = 2, font = ("verdana"), relief = "sunken")
linkEntry2.place(x = 4, y = 35)

linkEntry3 = Entry(lframe, width = 30, bg = "red", fg = "white", borderwidth = 2, font = ("verdana"), relief = "sunken")
linkEntry3.place(x = 4, y = 65)

playBtn1 = Button(lframe,width = 5,bg = "white", fg = "red", text = "Play",bd = 4,font = ("verdana", 7, "bold"))
playBtn1.place(x = 310, y = 5)
playBtn2 = Button(lframe,width = 5,bg = "white", fg = "red", text = "Play",bd = 4,font = ("verdana", 7, "bold"))
playBtn2.place(x = 310, y = 35)
playBtn3 = Button(lframe,width = 5,bg = "white", fg = "red", text = "Play",bd = 4,font = ("verdana", 7, "bold"))                      
playBtn3.place(x = 310, y = 65)

#COPY BUTTON
copyBtn1 = Button(lframe,width = 5,bg = "red",fg = "white",text = "Copy",bd = 4,font = ("verdana", 7, "bold"))
copyBtn1.place(x = 360, y = 5)
copyBtn2 = Button(lframe,width = 5,bg = "red",fg = "white",text = "Copy",bd = 4,font = ("verdana", 7, "bold"))
copyBtn2.place(x = 360,y = 35)
copyBtn3 = Button(lframe,width = 5,bg = "red",fg = "white",text = "Copy",bd = 4,font = ("verdana", 7, "bold"))
copyBtn3.place(x = 360, y = 65)"""

b = PhotoImage(file = "./Image/b1.png")

banner1 = Label(tab1, image = b, bg="white", bd=0,
                height = 480, width = 340, relief = "flat")
banner1.place(x = 36,y = 20)

banner = Label(tab1,
               text = "Follow Us On", bg="white", bd=0,               
               foreground = "red",
               anchor = "center",
               font = ("verdana 12 bold")).place(x = 150,y = 520)
facebook = Button(tab1,
               image = FBIcon,
               bd = 0, bg="white", activebackground='white',
               relief = "flat").place(x = 90,y = 550)

instagram = Button(tab1,
               image = INSTAIcon,
               bd = 0, bg="white", activebackground='white',    
               relief = "flat").place(x = 150,y = 550)

youtube = Button(tab1,
               image = YTIcon,
               bd = 0, bg="white", activebackground='white',  
               relief = "flat").place(x = 210,y = 550)

linkedin = Button(tab1,
               image = LinIcon,
               bd = 0, bg="white", activebackground='white',   
               relief = "flat").place(x = 270,y = 550)


#YOUTUBE ICON
banner = Label(tab2,
               image = YouTubeIcon,
               bd = 2).place(x = 0,y = 0)

#ENTRY BOX
ytdEntryVar = StringVar(tab2)
ytdEntry = Entry(tab2,
                 width = 32,
                 textvariable = ytdEntryVar,
                 borderwidth = 2,
                 font = ("verdana"),
                 relief = "sunken")
ytdEntry.focus()
ytdEntry.place(x = 4, y = 104)
ytdEntry.insert(0, "Copy or paste url or type name")

#CHECK BUTTON
check_des = Label(tab2, text='check', bd=1, relief='solid', font="verdana 8")
def on_enter_check(event):
    check_des.place(x=330,y=132)
def on_leave_check(event):
    check_des.place(x=1000,y=1000)    
checkBtn = Button(tab2,
                image = CheckIcon,
                height = 18,
                command = check,
                bd = 0,
                relief = "flat")
checkBtn.place(x = 338, y = 104)
checkBtn.bind('<Enter>',on_enter_check)
checkBtn.bind('<Leave>',on_leave_check)

#MIC BUTTON
mic_des = Label(tab2, text='mic', bd=1, relief='solid', font="verdana 8")
def on_enter_mic(event):
    mic_des.place(x=360,y=132)
def on_leave_mic(event):
    mic_des.place(x=1000,y=1000)
micBtn = Button(tab2,
                image = ListenIcon,
                height = 18,
                command = search,
                bd=0,
                relief = "flat")
micBtn.place(x = 362, y = 104)
micBtn.bind('<Enter>',on_enter_mic)
micBtn.bind('<Leave>',on_leave_mic)

#SEARCH BUTTON
search_des = Label(tab2, text='search', bd=1, relief='solid', font="verdana 8")
def on_enter_search(event):
    search_des.place(x=370,y=132)
def on_leave_search(event):
    search_des.place(x=1000,y=1000)    
searchBtn = Button(tab2,
                   image = SearchIcon,
                   height = 18,
                   command = show_link,
                   bd=0,
                   relief = "flat")
searchBtn.place(x = 387, y = 104)
searchBtn.bind('<Enter>',on_enter_search)
searchBtn.bind('<Leave>',on_leave_search)


Label(tab2,
      text = "Select Path",
      font = ('verdana', 10, 'bold')).place(x = 8, y = 134)

#ENTRY PATH FOR YouTube
file_pathYTD = Entry(tab2,
                  width = 33,
                  relief = "sunken",
                  borderwidth = 2,
                  bg = "red",
                  fg = "white",
                  font = ("verdana", 10, "bold"))
file_pathYTD.place(x = 4, y = 161)

#Select Folder BUTTON TO SAVE THE FILE FOR YouTube
browserBtn = Button(tab2,
                    text = "Browser",
                    command = openlocationYTD,
                    width = 12,
                    bg = "white",
                    fg = "red",
                    font = ("verdana", 8, "bold"),
                    relief = "raised")
browserBtn.place(x = 304, y = 160)
changeOnHover(browserBtn, "black", "white")

#Option for Quality
variable = StringVar(tab2)
variable.set("SELECT QUALITY") # default value
w1 = OptionMenu(tab2,
                variable,
                "Best Available",
                "1080-Video-Only",
                "720p-Video-Only",
                "480p-Video-Only",
                "360p-Dual",
                "Audio-Only-50kbps",
                "Audio-Only-Best")
w1.config(width = 14,
          font = ("verdana", 9, "bold"),
          bg = "white",
          fg = "red",
          activeforeground = "white",
          activebackground = "red")
w1.place(x = 121, y = 200)

#CLEAR BUTTON FOR YouTube
clearBtn = Button(tab2,
                  text = "CLEAR",
                  width = 11,
                  bg = "white",
                  font = ("verdana", 10, "bold"),
                  command = clearYTD,
                  relief = "raised")#flat, groove, raised, ridge, solid, or sunken
clearBtn.place(x = 4, y = 201)
changeOnHover(clearBtn, "red", "white")

#DOWNLOAD BUTTON FOR YouTube
downloadBtn = Button(tab2,
                     text = "DOWNLOAD",
                     width = 11,
                     bg = "white",
                     font = ("verdana", 10, "bold"),
                     command = downloadYTD,
                     relief = "raised")
downloadBtn.place(x = 301, y = 201)
changeOnHover(downloadBtn, "red", "white")

#NAVIGATION BAR BUTTON
navBarBtn = Button(topFrame,
                   image = NavIcon,
                   padx = 20,
                   bg='white', activebackground='white',   
                   bd=0,
                   relief = "flat",
                   command = switch)
navBarBtn.pack()
navBarBtn.place(x = 8, y = 8)

#SETTING NAVIGATION BAR FRAME
navBarRoot = Frame(screen,
                height = 696,
                width = 255)
navBarRoot.place(x = -300, y = 0)
headerLbl = Label(navBarRoot,
      font = "Bahnschrift 15",
      bg = "red",
      height = 3,
      width = 300)
headerLbl.place(x = 0, y = 0)
titleLbl = Label(navBarRoot,
                 text = "DOWNLOADER",
                 font = "Bahnschrift 18 bold underline",
                 bg = "red",
                 fg='white')
titleLbl.place(x = 10, y = 10)

footerLbl = Label(navBarRoot,
                      text = "Copyright © 2022 Downloader",
                      font = "verdana 10 bold",
                      fg = "red")
footerLbl.place(x = 15, y = 612)

footerLbl = Label(navBarRoot,
      font = "Bahnschrift 15",
      bg = "red",
      height = 2,
      width = 300)
footerLbl.place(x = 0, y = 640)
footerTitleLbl = Label(navBarRoot,
                 text = "Version 1.0.0",
                 font = "Bahnschrift 15 bold underline",
                 bg = "red",
                 fg='white')
footerTitleLbl.place(x = 70, y = 650)

def select():
    note_book.select(tab1)
    global btnState
    if btnState is True:
        #CREATING ANIMATED NAVBAR (CLOSING)   
        for x in range(0, 301, 20):
            navBarRoot.place(x = -x, y = 0)
            topFrame.update()

        #turning button OFF:
        btnState = False    

#NAVIGATION BAR OPTION BUTTON
Button(navBarRoot,
           text = "   Home",
           font = "BahnschriftLight 15",
           relief = "flat",
           bd = 0,
           width=17,
           anchor='w',
           command = select).place(x = 45, y = 70)
Button(navBarRoot,
           text = "     Downloads",
           font = "BahnschriftLight 15",
           image = DownloadIcon,
           bd=0,
           compound = 'left',
           relief = "flat",
           width=230,
           anchor='w',
           command = coming_soon).place(x = 10, y = 130)
Button(navBarRoot,
           text = "     Feedback",
           font = "BahnschriftLight 15",
           image = FeedbackIcon,
           bd=0,
           compound = 'left',
           relief = "flat",
           width=230,
           anchor='w',
           command = feedback).place(x = 10, y = 190)
Button(navBarRoot,
           text = "     Settings",
           font = "BahnschriftLight 15",
           image = SettingIcon,
           bd=0,
           compound = 'left',
           relief = "flat",
           width=230,
           anchor='w',
           command = coming_soon).place(x = 10, y = 250)
Button(navBarRoot,
           text = "     About US",
           font = "BahnschriftLight 15",
           image = AboutIcon,
           bd=0,
           compound = 'left',
           relief = "flat",
           width=230,
           anchor='w',
           command = aboutus).place(x = 10, y = 310)
helpBtn = Menubutton(navBarRoot,
           text = "    Help",
           font = "BahnschriftLight 15",
           image = HELPIcon,
           bd=0,          
           compound = 'left',
           relief = "flat",
           width=230,
           anchor='w',)
helpBtn.place(x = 13, y = 370)

helpBtn.menu = Menu(helpBtn, tearoff = 0)
helpBtn["menu"] = helpBtn.menu
helpBtn.menu.add_command(image=HELPIcon, label='    Help', compound='left', accelerator="F1", command=coming_soon)
helpBtn.menu.add_command(label='     Check for Updates...', command=coming_soon)
helpBtn.menu.add_separator()
helpBtn.menu.add_command(label='     About', accelerator='Shift+F1', command=aboutwindow)

#NAVIGATION BAR CLOSE BUTTON
closeBtn = Button(navBarRoot,
                  image = CloseIcon,
                  bd=0,
                  relief = "flat",
                  command = switch)
closeBtn.place(x = 210, y = 10)

#NAVIGATION BAR HOME ICON
homeIcon = Label(navBarRoot,
                 image = HomeIcon,
                 activebackground = "red")
homeIcon.place(x = 10, y = 78)

consoleYTD = LabelFrame(tab2,
           text = "Console",
           labelanchor = "n",
           font = "BahnschriftLight 15 bold",
           height = 228,
           width = 405,bg="white",fg="red",borderwidth=5,relief="sunken",highlightcolor="red",highlightbackground="red")
consoleYTD.place(x = 5, y = 348)
consoleYTDtext = ScrolledText(consoleYTD,
                     state = "disabled",
                     font = "verdana 8 bold",
                     height = 15,                 
                     width = 47,bg = "white",fg="black",relief="flat",highlightcolor="red",highlightbackground="red", wrap = "word")
consoleYTDtext.place(x = 0, y = 0)

style = ttk.Style(tab2)
# add label in the layout
style.layout('text.Horizontal.TProgressbar', 
             [('Horizontal.Progressbar.trough',
               {'children': [('Horizontal.Progressbar.pbar',
                              {'side': 'left', 'sticky': 'ns'})],
                'sticky': 'nswe'}), 
              ('Horizontal.Progressbar.label', {'sticky': 'nswe'})])
# set initial text
style.configure('text.Horizontal.TProgressbar', text='0 %', anchor='center', font = ("verdana", 10, "bold"))

#PROGRESS BAR for YouTube
progressbarYTD = ttk.Progressbar(tab2,
                              orient = "horizontal",
                              length = 400,
                              mode = "determinate",
                              style='text.Horizontal.TProgressbar')
progressbarYTD.place(x = 8, y = 588)


#=================================   INSTAGRAM   =============================

#FUNCTION FOR OPENING THE LOCATION OF A FILE FOR INSTAGRAM
from tkinter.filedialog import askdirectory
def openlocationINSTA():
    location = askdirectory()
    if file_pathINSTA.get() != "":
        file_pathINSTA.delete(0, END)
        file_pathINSTA.insert(0, location)
    else:
        file_pathINSTA.insert(0, location)
        
def downloadINSTA():
    if connection() == False:
        messagebox.showerror("Error", "No INTERNET connection")

    if instaEntry.get() == "":
        messagebox.showerror("Error", "Please Paste URL or Enter Name")
        
    elif file_pathINSTA.get() == "":
        messagebox.showerror("Error", "Please provide Path")
        
    else:        
        def downloadPP(username):
            url = "https://www.instagram.com/{}/".format(username)
            x = re.match(r'^(https:)[/][/]www.([^/]+[.])*instagram.com', url)

            if x:
                check_url1 = re.match(r'^(https:)[/][/]www.([^/]+[.])*instagram.com[/].*\?hl=[a-z-]{2,5}', url)
                check_url2 = re.match(r'^(https:)[/][/]www.([^/]+[.])*instagram.com$|^(https:)[/][/]www.([^/]+[.])*instagram.com/$', url)
                check_url3 = re.match(r'^(https:)[/][/]www.([^/]+[.])*instagram.com[/][a-zA-Z0-9_]{1,}$', url)
                check_url4 = re.match(r'^(https:)[/][/]www.([^/]+[.])*instagram.com[/][a-zA-Z0-9_]{1,}[/]$', url)

                if check_url3:
                    final_url = url + '/?__a=1'

                if check_url4:
                    final_url = url + '?__a=1'

                if check_url2:
                    final_url = print("Please enter an URL related to a profile")
                    exit()

                if check_url1:
                    alpha = check_url1.group()
                    final_url = re.sub('\\?hl=[a-z-]{2,5}', '?__a=1', alpha)
            
            try:
                if check_url3 or check_url4 or check_url2 or check_url1:
                    req = requests.get(final_url)
                    get_status = requests.get(final_url).status_code
                    get_content = req.content.decode('utf-8')

                if get_status == 200:
                    print("\nDownloading the image...")
                    find_pp = re.search(r'profile_pic_url_hd\":\"([^\'\" >]+)', get_content)
                    pp_link = find_pp.group()
                    pp_final = re.sub('profile_pic_url_hd":"', '', pp_link)
                    file_size_request = requests.get(pp_final, stream=True)
                    file_size = int(file_size_request.headers['Content-Length'])
                    block_size = 1024 
                    t=tqdm(total=file_size, unit='B', unit_scale=True, desc=username, ascii=True)
                    with open(username + '.jpg', 'wb') as f:
                        for data in file_size_request.iter_content(block_size):
                            t.update(len(data))
                            f.write(data)
                    t.close()
                    #Show image  
                    im = Image.open(username +".jpg")  
                    im.show() 
                    print("Profile picture downloaded successfully")

            except Exception as e:
                print(e)
                print('error')
            
        def downloadIMG_VID():
            pass
        
        username = instaEntry.get()
        print(username)
        path = file_pathINSTA.get()
        print(path)
        choice = variable.get()
        print(choice)
        if choice == "Profile Photo":
            downloadPP(username)
        if choice == "Image" or choice == "Video":
            downloadIMG_VID()

def clearINSTA():
    try:
        instaEntry.delete(0, END)
        instaEntry.insert(0, "Type username")

        consoleINSTAtext.config(state = "normal")
        consoleINSTAtext.delete(1.0, END)
        consoleINSTAtext.config(state = "disabled")        
        
        file_pathINSTA.delete(0, END)
        progressbarINSTA["value"] = 0
        style.configure('text.Horizontal.TProgressbar', text='0 %')
        
    except:
        pass
    
#INSTAGRAM ICON
InstagramIcon = PhotoImage(file="./Image/instagram.png")

banner = Label(tab3,
               image = InstagramIcon,
               bd = 2).place(x = 0, y = 0)

#ENTRY BOX
instaEntryVar = StringVar(tab3)
instaEntry = Entry(tab3,
                   width = 32,
                   textvariable = instaEntryVar,
                   borderwidth = 2,
                   font = ("verdana"),
                   relief = "sunken")
instaEntry.focus()
instaEntry.place(x = 35, y = 104)
instaEntry.insert(0, "Type username")

#CHECK BUTTON
checkBtn = Button(tab3,
                image = CheckIcon,
                height = 18,
                bd = 2,
                relief = "flat")
checkBtn.place(x = 370, y = 104)

Label(tab3,
      text = "Select Path",
      font = ('verdana', 10, 'bold')).place(x = 8, y = 134)

#ENTRY PATH FOR INSTAGRAM
file_pathINSTA = Entry(tab3,
                  width = 33,
                  relief = "sunken",
                  borderwidth = 2,
                  bg = "red",
                  fg = "white",
                  font = ("verdana", 10, "bold"))
file_pathINSTA.place(x = 4, y = 161)

#Select Folder BUTTON TO SAVE THE FILE FOR INSTAGRAM
browserBtn = Button(tab3,
                    text = "Browser",
                    command = openlocationINSTA,
                    width = 12,
                    bg = "white",
                    fg = "red",
                    font = ("verdana", 8, "bold"),
                    relief = "raised")
browserBtn.place(x = 304, y = 160)
changeOnHover(browserBtn, "black", "white")

#Option for Type (INSTAGRAM)
variable = StringVar(tab3)
variable.set("SELECT TYPE") # default value
w2 = OptionMenu(tab3,
                variable,
                "Profile Photo",
                "Video",
                "Image")
w2.config(width = 14,
          font = ("verdana", 9, "bold"),
          bg = "white",
          fg = "red",
          activeforeground = "white",
          activebackground = "red")
w2.place(x = 121, y = 200)

#CLEAR BUTTON FOR INSTAGRAM
clearBtn = Button(tab3,
                  text = "CLEAR",
                  width = 11,
                  bg = "white",
                  font = ("verdana", 10, "bold"),
                  command = clearINSTA,
                  relief = "raised")#flat, groove, raised, ridge, solid, or sunken
clearBtn.place(x = 4, y = 201)
changeOnHover(clearBtn, "red", "white")

#DOWNLOAD BUTTON FOR INSTAGRAM
downloadBtn = Button(tab3,
                     text = "DOWNLOAD",
                     width = 11,
                     bg = "white",
                     font = ("verdana", 10, "bold"),
                     command = downloadINSTA,
                     relief = "raised")
downloadBtn.place(x = 301, y = 201)
changeOnHover(downloadBtn, "red", "white")

#CONSOLE for INSTAGRAM
consoleINSTA = LabelFrame(tab3,
           text = "Console",
           labelanchor = "n",
           font = "BahnschriftLight 15 bold",
           height = 228,
           width = 405,bg="white",fg="red",borderwidth=5,relief="sunken",highlightcolor="red",highlightbackground="red")
consoleINSTA.place(x = 5, y = 348)
consoleINSTAtext = ScrolledText(consoleINSTA,
                     state = "disabled",
                     font = "verdana 8 bold",
                     height = 15,                 
                     width = 47,bg = "white",fg="black",relief="flat",highlightcolor="red",highlightbackground="red", wrap = "word")
consoleINSTAtext.place(x = 0, y = 0)

#PROGRESS BAR for INSTAGRAM
progressbarINSTA = ttk.Progressbar(tab3,
                              orient = "horizontal",
                              length = 400,
                              mode = "determinate",
                              style='text.Horizontal.TProgressbar')
progressbarINSTA.place(x = 8, y = 588)

#=================================   MUSIC PLAYER   =================================
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

ArtworkIcon = PhotoImage(file = "./icon/Artwork-default.png")
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

#===============================   QrCode Generator   ===============================
import tkinter as tk
import os
from tkinter import ttk
from tkinter import Frame
from tkinter import PhotoImage
from tkinter import Label
from tkinter import LabelFrame
from tkinter import StringVar
from tkinter import Entry
from tkinter import Button
from tkinter import OptionMenu
from tkinter import Toplevel
from tkinter import messagebox
from tkinter import Canvas
from tkinter import Text
from tkinter.scrolledtext import ScrolledText
from PIL import Image
from PIL import ImageTk
from pyzbar.pyzbar import decode
import pyqrcode

def generate():
    global location
    if data_entry.get('1.0', 'end-1c') == '' or data_entry.get('1.0', 'end-1c') == "type message here.....":
        messagebox.showerror("Error","Please type message ")
    elif save_entry.get() == '' or save_entry.get() == "type filename here.....":
        messagebox.showerror("Error","Please type filename")
    elif file_pathQR.get() == "":
        messagebox.showerror("Error","Please provide Path")        
    else:    
        qr = pyqrcode.create(data_entry.get('1.0', 'end'))
        img = qr.png(location+ '/' +save_entry.get()+".png", scale = variable.get())
        info = Label(frame1, text=":::::::::::: Generated QR code ::::::::::::", font = ("verdana 10 bold"))
        info.place(x=65, y=160)
        img = Image.open(location+ '/' +save_entry.get()+".png")
        img = ImageTk.PhotoImage(img)
        canvas1.create_image(200, 180, image=img, tag='bg1')
        canvas1.image=img

from tkinter import filedialog        
def selected():
    global consoleqrcode
    try:
        img_path = filedialog.askopenfilename(initialdir=os.getcwd(),
                                     title="Select Image", filetype=(
                                         ("PNG file", "*.png"), ("All files", "*.*")))
        img = Image.open(img_path)
        img = ImageTk.PhotoImage(img)
        canvas2.create_image(200, 190, image=img, tag='bg2')
        canvas2.image=img                                                                                                                                                                                                                 
        d = decode(Image.open(img_path))
        data = d[0].data.decode()
        consoleqrcode = LabelFrame(frame2,
                               text="Scanned Message",
                               labelanchor="n",
                               font="BahnschriftLight 15 bold",
                               height=85,
                               width=408,
                               bg="white",
                               fg="red",
                               borderwidth=5,
                               relief="sunken",
                               highlightcolor="red",
                               highlightbackground="red")
        consoleqrcode.place(x=0, y=400)
        consoleqrcodetext = ScrolledText(consoleqrcode,
                                     font = "verdana 8 bold",
                                     height = 3,                 
                                     width = 47,
                                     bg = "white",
                                     fg="black",
                                     relief="flat",
                                     highlightcolor="red",
                                     highlightbackground="red",
                                     wrap = "word")
        consoleqrcodetext.place(x=0, y=0)    
        consoleqrcodetext.insert('1.0', data)
        consoleqrcodetext.config(state = "disabled")
    except:
        pass
    
def clearGQR():
    try:
        data_entry.delete('1.0', 'end-1c')
        data_entry.insert('1.0', "type message here.....")

        save_entry.delete(0, 'end')
        save_entry.insert(0, "type filename here.....")

        file_pathQR.delete(0, 'end')

        canvas1.delete('bg1')
    except:
        pass
    
def clearRQR():
    global consoleqrcode
    try:
        canvas2.delete('bg2')
        consoleqrcode.destroy()
    except:
        pass    
        
#FUNCTION FOR OPENING THE LOCATION OF A FILE FOR INSTAGRAM
from tkinter.filedialog import askdirectory
def openlocationQR():
    global location
    location = askdirectory()
    if file_pathQR.get() != "":
        file_pathQR.delete(0, END)
        file_pathQR.insert(0, location)
    else:
        file_pathQR.insert(0, location)        
    
#QRCODE ICON
QrCodeIcon = PhotoImage(file="./Image/qrcode.png")

banner = Label(tab5,
               image = QrCodeIcon,
               bd = 2).place(x = 0, y = 0)

note = ttk.Notebook(tab5, height=490)
note.place(x=0,y=100)
# create frames to add on tabs
frame1=Frame(note, bd=0, bg='white')
frame1.pack(fill="both",expand=True)
frame2=Frame(note, bd=0, bg='white')
frame2.pack(fill="both",expand=True)
note.add(frame1,text=":::::::::::::::: Generate  QR  Code ::::::::::::::::")
note.add(frame2,text="::::::::::::::::: Read  QR  Code :::::::::::::::::")
# create canvas to display image
canvas1 = Canvas(frame1, width="405", height="335", relief='solid', bd=1)
canvas1.place(x=0,y=150)
canvas2 = Canvas(frame2, width="405", height="335", relief='solid', bd=1)
canvas2.place(x=0,y=5)

data_label = Label(frame1, text='Enter message:', font = ("verdana 10 bold"), bg='white')
data_label.place(x=0, y=15)
data_entry = Text(frame1, width=35, height=2, font = ("verdana 10"), relief='solid', bd=1, wrap='word')
data_entry.focus()
data_entry.place(x=125, y=10)
data_entry.insert('1.0', "type message here.....")


save_label = Label(frame1, text='Enter name \n to save with', font = ("verdana 10 bold"), bg='white')
save_label.place(x=0, y=45)
save_entry = Entry(frame1, width=30, font = ("verdana 10 bold"), relief='sunken', bd=2)
save_entry.focus()
save_entry.place(x=125, y=55)
save_entry.insert(0, "type filename here.....")

Label(frame1,
      text = "Select Path", bg='white',
      font = ('verdana', 10, 'bold')).place(x=0, y=85)

#ENTRY PATH FOR YouTube
file_pathQR = Entry(frame1,
                  width = 23,
                  relief = "sunken",
                  borderwidth = 2,
                  bg = "red",
                  fg = "white",
                  font = ("verdana", 10, "bold"))
file_pathQR.place(x=90, y = 86)

#Select Folder BUTTON TO SAVE THE FILE FOR YouTube
browserBtn = Button(frame1,
                    text = "Browser",
                    width = 12,
                    bg = "white",
                    fg = "red",
                    font = ("verdana", 8, "bold"),
                    relief = "raised",
                    command=openlocationQR)
browserBtn.place(x=303, y = 85)
changeOnHover(browserBtn, "black", "white")

Label(frame1,
      text = "Scale", bg='white',
      font = ('verdana', 10, 'bold')).place(x=0, y=120)

variable = StringVar(frame1)
variable.set("5")
w1 = OptionMenu(frame1, variable,"1","2","3","4","5","6","7","8","9","10")
w1.config(bg = "white",
          fg = "red",
          activeforeground = "white",
          activebackground = "red",
          font = ("verdana", 9, "bold"),
          bd=0, relief='flat')
w1.place(x=50, y=120)

btn1 = Button(frame1, text="Generate", width=11, bg='white', font = ("verdana 9 bold"), relief='raised', command=generate)
btn1.place(x=180, y=120)
changeOnHover(btn1, "red", "white")
btn2 = Button(frame1, text="Clear", width=11, bg='white', font = ("verdana 9 bold"), relief='raised', command=clearGQR)
btn2.place(x=300, y=120)
changeOnHover(btn2, "red", "white")
btn3 = Button(frame2, text="Select Image", width=11, bg='white', font = ("verdana 9 bold"), relief='raised', command=selected)
btn3.place(x=100, y=360)
changeOnHover(btn3, "red", "white")
btn4 = Button(frame2, text="Clear", width=11, bg='white', font = ("verdana 9 bold"), relief='raised', command=clearRQR)
btn4.place(x=200, y=360)
changeOnHover(btn4, "red", "white")

#topFrame.after(1000, is_connected)
screen.mainloop()
