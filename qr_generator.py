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

# function to change properties of button on hover
def changeOnHover(button, colorOnHover, colorOnLeave): 
  
    # adjusting backgroung of the widget
    # background on entering widget
    button.bind("<Enter>", func=lambda e: button.config(
        background=colorOnHover, foreground= "white"))
  
    # background color on leving widget
    button.bind("<Leave>", func=lambda e: button.config(
        background=colorOnLeave, foreground= "black"))

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
tab5 = Frame(note_book)
note_book.add(tab5, text = "    QrCode    ")

note_book.place(x = 10, y = 30)
note_book.pack(expand = True, fill = "both")
    
#INSTAGRAM ICON
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
data_entry.place(x=125, y=10)
data_entry.insert('1.0', "type message here.....")
data_entry.focus()

save_label = Label(frame1, text='Enter name \n to save with', font = ("verdana 10 bold"), bg='white')
save_label.place(x=0, y=45)
save_entry = Entry(frame1, width=30, font = ("verdana 10 bold"), relief='sunken', bd=2)
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
