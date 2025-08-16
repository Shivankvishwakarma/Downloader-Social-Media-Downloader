import tkinter as tk
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
from tkinter.scrolledtext import ScrolledText
import instaloader
import glob
from PIL import Image as SM
from PIL import ImageTk

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
    
#FUNCTION FOR OPENING THE LOCATION OF A FILE FOR INSTAGRAM
from tkinter.filedialog import askdirectory
def openlocationINSTA():
    location = askdirectory()
    if file_pathINSTA.get() != "":
        file_pathINSTA.delete(0, END)
        file_pathINSTA.insert(0, location)
    else:
        file_pathINSTA.insert(0, location)

def check(username):
    if connection() == False:
        messagebox.showerror("Error","No INTERNET connection")

    elif instaEntry.get() == "":
        messagebox.showerror("Error","Please Type username")

    elif instaEntry.get() == "Type username":
        messagebox.showerror("Error","Please Type username")                        

    else:
        response = requests.get("https://instagram.com/" + username + "/")
        if response.status_code == 404 :
            messagebox.showinfo("Not Found",username + " - Account Not Found!!" +"\n"+ username + " is not an existance Account.")
        else:
            try:
                L = instaloader.Instaloader()
                profile = instaloader.Profile.from_username(L.context, username)
                if profile.is_private:            
                    messagebox.showinfo("Private",username + " - Account Found!!" +"\nBut "
                                    + username + " is a Private Account.\n\u25CF You can "
                                    + "download it's Profile Pic only by selecting Profile "
                                    + "Pic    Option.\n\u25CF If you wants to download it's "
                                    + "posts then you need to login.\n(Note:- This Account "
                                    + "Must be followed by loggedin Account).")
                else:
                    messagebox.showinfo("Public",username + " - Account Found!!" +"\nBut "+ username + " is a Public Account.")
            except Exception as e:
                print(e)
                messagebox.showinfo("Deactivated",username + " - Account Found!!" +"\nBut "+ username + " is Currently Deactivated.")
        
def preview_fun(username):
    path = file_pathINSTA.get()        
    global screen_width, screen_height
    profile_dis = Toplevel(screen)
    profile_dis.title("Profile Pic - " + username)
    profile_dis.iconbitmap(r'./Image/down_arrow_0of_icon.ico')
    x = int((screen_width/2) - (320/2))
    y = int((screen_height/2) - (320/2))

    profile_dis.geometry("{}x{}+{}+{}".format(320, 320, x, y))
    profile_dis.resizable(False, False)
    b = Label(profile_dis, bg='gray', bd=0, relief='flat')
    b.pack()
    path1 = path +"/"+ username + "/*.jpg"
    for img in glob.glob(path1):
        try:
            profile = SM.open(img)
            profile = ImageTk.PhotoImage(profile)
            b.config(image=profile)
            b.image=profile            
        except Exception as e:
            print(e)
            
def downloadINSTA():
    if connection() == False:
        messagebox.showerror("Error", "No INTERNET connection")

    if instaEntry.get() == "":
        messagebox.showerror("Error", "Please Paste URL or Enter Name")
        
    elif file_pathINSTA.get() == "":
        messagebox.showerror("Error", "Please provide Path")
        
    else:        
        def downloadProfilePic(username, path):
            try:
                ig = instaloader.Instaloader(dirname_pattern=path + "/{target}")
                ig.download_profile(username, profile_pic_only=True)                
                messagebox.showinfo("Success",username + "'s Profile Pic Downloaded Successfully.\n\nAnd Saved to " + path +"/"+ username +".")
            except:
                pass
            
        def downloadPosts():
            pass
        
        username = instaEntry.get()
        print(username)
        path = file_pathINSTA.get()        
        print(path)
        choice = variable.get()
        print(choice)
        if choice == "Profile Pic":
            downloadProfilePic(username, path)
        if choice == "Image" or choice == "Video":
            downloadPosts(username)

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

wifi = PhotoImage(file = "./Image/wifi.png")
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
tab3 = Frame(note_book)
note_book.add(tab3, text = "    Instagram    ")

note_book.place(x = 10, y = 30)
note_book.pack(expand = True, fill = "both")
    
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

CheckIcon = PhotoImage(file = "./Image/arrow.png")
#CHECK BUTTON
checkBtn = Button(tab3,
                image = CheckIcon,
                height = 18,
                bd=0,
                relief = "flat",
                command=lambda : check(instaEntry.get()))
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
                "Profile Pic",
                "Posts",
                "IGTV",
                "Story")
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

#Show Profile BUTTON FOR INSTAGRAM
showBtn = Button(tab3,
                     text = "Show Profile",
                     width = 11,
                     bg = "white",
                     font = ("verdana", 10, "bold"),
                     command=lambda : preview_fun(instaEntry.get()),
                     relief = "raised")
showBtn.place(x = 301, y = 250)
changeOnHover(showBtn, "red", "white")

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
