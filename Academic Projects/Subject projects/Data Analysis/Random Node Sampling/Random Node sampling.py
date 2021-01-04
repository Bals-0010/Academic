
from tkinter import *
# import tkinter as tk
from PIL import ImageTk, Image
# from tkinter.filedialog import askopenfilename
from tkinter import filedialog
from tkinter import messagebox

window=Tk()
window.title("Data Analysis II - Random Node Sampling")
window.geometry("700x550")
window.configure(background="black")

# photo=PhotoImage(file="C:/Users/Bala/Downloads/RNpic.gif")
# Label(window, image=photo,bg="black").grid(row=0,column=2,sticky=W)

Label(window,text="",bg="black",fg="white",font="TimesNewRoman 12 ").grid(row=0,column=2,sticky=W)
Label(window,text="            Data Analysis II",bg="black",fg="limegreen",font="TimesNewRoman 15").grid(row=1,column=2,sticky=W)
Label(window,text="     Random Node Sampling",bg="black",fg="cadet blue",font="TimesNewRoman 15").grid(row=2,column=2,sticky=W)
Label(window,text="\t           By",bg="black",fg="White",font="TimesNewRoman 12 italic").grid(row=3,column=2,sticky=W)
Label(window,text="    Balakothandaraman Mani",bg="black",fg="orange",font="Verdana 13").grid(row=4,column=2,sticky=W)
Label(window,text="",bg="black",fg="white",font="TimesNewRoman 12 ").grid(row=5,column=2,sticky=W)
Label(window,text="",bg="black",fg="white",font="TimesNewRoman 12 ").grid(row=6,column=2,sticky=W)

# ###################################
Label(window, text="   Browse to import DataSet  ",bg="black",fg="white",font="TimesNewRoman 12 ").grid(row=7,column=1,sticky=W)
Entry(window, text="" ,bg="black",fg="white",font="TimesNewRoman 12",width=30).grid(row=7,column=2)

#Browse option
def browsefunc():   
    window.filename=filedialog.askopenfilename(title="Select a Dataset (xlsx files)",initialdir="/",filetypes=(("All files", "*.*"),("Excel files", "*.xlsx")))
    filename=window.filename

    if not filename.endswith('.xlsx'):
        messagebox.showerror("Import error", "Filetype must be a .xlsx")
    else:  	
    	messagebox.showinfo("Open Source File","Import Successful !\n\n'%s'"%filename)
    	# print("File Name:",filename)
    	Label(window, text=filename,bg="black",fg="white",font="TimesNewRoman 10",width=32).grid(row=7,column=2)

def exit():
	window.Exit()

def save():
	messagebox.showinfo("Save","Settings saved Successfully !")

def text():
	m=filedialog.asksaveasfile(mode='w', defaultextension=".txt")
	messagebox.showinfo("Save as Text File","Output and settings saved in a Text file Successfully !")

def viewcode():
	import os
	window1=Tk()
	dirname, filename = os.path.split(os.path.abspath(__file__))
	a=dirname+"\\"+ filename
	window1.title(a)
	t=open(a).read()
	T=Text(window1,height=47,width=170)
	T.pack()
	T.insert(END,t)


def random_node():
    pass

Label(window,text="\t\t\t",bg="black",fg="white",font="Comicsans 12").grid(row=9,column=3)

Label(window,text="Enter Probability (%)",bg="black",fg="white",font="Comicsans 12").grid(row=10,column=1)
Entry(window, text="",bg="black",fg="white",font="TimesNewRoman 12",width=30).grid(row=10,column=2)
Button(window, text="Save Settings",font="Comicsans 12",command=save).grid(row=10,column=3)

Button(window, text="Browse File", font="Comicsans 12", command=browsefunc).grid(row=7,column=3)
Label(window,text="",bg="black",fg="white",font="Comicsans 12").grid(row=11,column=2)
Label(window,text="",bg="black",fg="white",font="Comicsans 12").grid(row=13,column=2)

Label(window, text="Total Number of Nodes",bg="black",fg="white",font="Comicsans 12").grid(row=12,column=1)
Entry(window, text="",bg="black",fg="white",font="Comicsans 12",width=30).grid(row=12,column=2)
Button(window, text="Save as Text File",font="Comicsans 12",command=text).grid(row=12,column=3)

Label(window, text="No. of Nodes Connected",bg="black",fg="white",font="Comicsans 12").grid(row=14,column=1)
Entry(window, text="",bg="black",fg="white",font="Comicsans 12",width=30).grid(row=14,column=2)
Button(window, text=" Exit Window", font="Comicsans 12", command=window.destroy).grid(row=14,column=3)

Label(window,text="",bg="black",fg="white",font="Comicsans 12").grid(row=15,column=2)
Label(window,text="",bg="black",fg="white",font="Comicsans 12").grid(row=16,column=2)
Button(window, text="View Source Code", font="Comicsans 12",command=viewcode).grid(row=17,column=2)


window.mainloop()