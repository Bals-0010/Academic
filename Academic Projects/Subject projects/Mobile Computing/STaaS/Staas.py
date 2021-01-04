from tkinter import *
import os, zlib
from tkinter import filedialog, messagebox
import tkinter as tk
from dropbox import *
from os import walk
import time

class staas:
    def __init__(self, master):
        self.master = master
        self.master.title("STaaS Provider")
        self.master.geometry("800x450")
        self.master.resizable(width=False, height=False)
        self.cd_button = Button(master, text="      Connect      ", command=self.connect)
        self.cd_button.grid(row=1, column=1, sticky=W)
        self.upload_file_button = Button(master, text="    Upload File   ", command=self.upload_file)
        self.upload_file_button.grid(row=2, column=1, sticky=W)
        self.upload_folder_button=Button(master,text=" Upload Folder ",command=self.upload_folder)
        self.upload_folder_button.grid(row=3,column=1,sticky=W)
        self.dwnd_file_button = Button(master, text="  Download  File  ", command=self.download)
        self.dwnd_file_button.grid(row=1, column=2, sticky=W)
        self.dwnd_folder_button = Button(master, text="Download Folder")
        self.dwnd_folder_button.grid(row=2, column=2, sticky=W)
        self.exit_button = Button(master, text="            Exit            ", command=self.exit)
        self.exit_button.grid(row=3, column=2, sticky=W)
        self.l1 = Label(master, text="   ").grid(row=0, column=0)
        self.l2 = Label(master, text="    ").grid(row=1, column=3)
        global var_list, mclogs_file
        self.var_list = []
        self.mclogs_file = open("MClogs.txt", "w+")

    def val_list(self):
        global value_list
        value_list = []
        for entry in dbx.files_list_folder('').entries:
            value_list.append(entry.name)
        return value_list

    def res_selection(self,i):
        value_list=self.val_list()
        global temp_list
        temp_list=[]
        for i in range(len(value_list)):
            if int(self.var_list[i].get()) == 1:
                temp_list.append(value_list[i])
            elif int(self.var_list[i].get() == 0):
                temp_list.remove(value_list[i])
        return temp_list

    def printt(self):
        print(temp_list)
        print(type(temp_list))

    def logs(self):
        window1 = Tk()
        dirname, filename = os.path.split(os.path.abspath(__file__))
        a = dirname + "\\" + "MClogs.txt"
        window1.title("MCLogs")
        window1.resizable(0,0)
        t=open(a).read()
        T = Text(window1, height=20, width=80)
        T.pack()
        T.insert(END,t)

    def exit(self):
        self.mclogs_file = open("MClogs.txt", "w+")
        self.mclogs_file.truncate(0)
        self.mclogs_file.close()
        self.master.destroy()

    def u_refresh(self):
        value_list = self.val_list()
        for i, entry in zip(range(len(value_list)), dbx.files_list_folder('').entries):
            self.var_list.append(tk.StringVar())
            self.var_list[-1].set(0)
            dchkbtn = Checkbutton(self.master, text=value_list[i], variable=self.var_list[-1],
                                  command=lambda i=i: self.res_selection(i), onvalue=1, offvalue=0).grid(row=i + 5,column=4,sticky=W)
            try:
                dlbl = Label(self.master, text=entry.size).grid(row=i + 5, column=5, sticky=W)
            except AttributeError:
                dlbl = Label(self.master, text="Folder").grid(row=i + 5, column=5, sticky=W)

    def d_refresh(self):
        for dchkbtn in self.master.grid_slaves():
            if int(dchkbtn.grid_info()["row"]) > len(dbx.files_list_folder('').entries):
                dchkbtn.grid_forget()

        for dlbl in self.master.grid_slaves():
            if int(dlbl.grid_info()["row"]) > len(dbx.files_list_folder('').entries):
                dlbl.grid_forget()

        # self.l1 = Label(self.master, text="   ").grid(row=0, column=0)
        # self.l2 = Label(self.master, text="          ").grid(row=1, column=3)

    def connect(self):
        global l1, dbx
        dbx = dropbox.Dropbox('YOUR DROPBOX')
        temp_no=len(dbx.files_list_folder('').entries)
        if self.cd_button["text"] == "      Connect      ":
            self.cd_button["text"] = "    Disconnect   "
            messagebox.showinfo("DropBox Message", "Connected to DropBox !")
            self.file_name = Label(self.master, text="File/Folder Name")
            self.file_name.grid(row=4, column=4, sticky=W)
            self.file_size = Label(self.master, text="File size(in Bytes)")
            self.file_size.grid(row=4, column=5, sticky=W)
            self.u_refresh()
            # self.cut=Button(self.master,text="Cut")
            # self.cut.grid(row=1,column=4)
            self.copy = Button(self.master, text="   Copy  ", command=self.printt)
            self.copy.grid(row=1, column=6, sticky=W)
            self.paste = Button(self.master, text="   Paste  ")
            self.paste.grid(row=2, column=6, sticky=W)
            self.rename = Button(self.master, text="Rename")
            self.rename.grid(row=3, column=6, sticky=W)
            self.delete = Button(self.master, text="Delete", command=self.delete)
            self.delete.grid(row=1, column=8, sticky=W)
            self.up = Button(self.master, text="   Up   ")
            self.up.grid(row=1, column=7, sticky=W)
            self.down = Button(self.master, text="Down")
            self.down.grid(row=2, column=7, sticky=W)
            self.root = Button(self.master, text=" Root ")
            self.root.grid(row=3, column=7, sticky=W)
            self.logs = Button(self.master, text=" Logs ", command=self.logs)
            self.logs.grid(row=2, column=8, sticky=W)
            self.exit=Button(self.master,text="  Exit  ",command=self.exit)
            self.exit.grid(row=3,column=8,sticky=W)
        else:
            self.cd_button["text"] = "      Connect      "
            # l1.destroy()
            # l1 = Label(self.master, text="                                             ")
            # l1.grid(row=0, column=1, sticky=W)


    def upload_file(self):
        try:
            self.master.filename = filedialog.askopenfilename(title="Select a file to upload", initialdir="/",
filetypes=(("All files", "*.*"), ("", "")))
            pathname = self.master.filename
            filename = os.path.basename(pathname)
            dropbox_path = "/"
            if len(filename) > 0:
                with open(str(pathname), 'rb') as f:
                    dbx.files_upload(f.read(), dropbox_path + filename, mute=True)
                    messagebox.showinfo("Upload File !",
                                        "File " + "\"" + filename + "\"" + "  " + "uploaded successfully" + "\nFrom: " + pathname)
                    self.mclogs_file = open("MClogs.txt", "w+")
                    self.mclogs_file.write("Upload file: " + filename +" "+ time.ctime()+ "\n" )
                    self.mclogs_file.close()
                self.u_refresh()
            else:
                messagebox.showerror("File Upload Error", "No file selected")
            self.d_refresh()
        except NameError:
            messagebox.showerror("Dropbox connection !", "Dropbox not connected !")
        self.u_refresh()


    def upload_folder(self):
        files_list = []
        try:
            files_list.clear()
            folder = filedialog.askdirectory()
            folder_name = os.path.basename(folder)
            new_folder="/"+folder_name
            dbx.files_create_folder(new_folder)
            files_list.clear()
            for (dirpath, dirnames, filenames) in walk(folder):
                files_list.extend(filenames)
            if len(files_list)>0:
                for i in range(len(files_list)):
                    with open(str(folder+"/"+files_list[i]),'rb') as f:
                        dbx.files_upload(f.read(), new_folder +"/"+files_list[i], mute=True)
                self.d_refresh()
                messagebox.showinfo("Upload Folder !", "Folder uploaded successfully !" + "from\n" + folder)
                self.mclogs_file = open("MClogs.txt", "w+")
                self.mclogs_file.write("Upload folder: " + folder_name + "  "+time.ctime() +"\n")
                self.mclogs_file.close()
            else:
                messagebox.showerror("Folder Upload Error", "No folder selected")
            # self.d_refresh()
        except NameError:
            messagebox.showerror("Dropbox connection !", "Dropbox not connected !")
        self.u_refresh()
        files_list.clear()


    def download(self):
        try:
            for i in range(len(temp_list)):
                path="/"+temp_list[i]
                p = os.path.basename(path)
                self.master.filename = filedialog.asksaveasfilename(title="Save As", initialdir="/",
                                                                    initialfile=p,
                                                                    filetypes=(("All files", "*.*"), ("", "")))
                download_path = self.master.filename
                try:
                    dbx.files_download_to_file(download_path, path)
                    messagebox.showinfo("Download File !", "File successfully downloaded !\nPath: " + download_path)
                except FileNotFoundError:
                    messagebox.showerror("File Download Error", "No path selected for download")
        except NameError:
            messagebox.showerror("Dropbox connection !", "No File selected or Dropbox not connected !")


    def delete(self):
        try:
            for i in range(len(temp_list)):
                dbx.files_delete("/"+temp_list[i])
                self.mclogs_file = open("MClogs.txt", "w+")
                self.mclogs_file.write("delete files: " + temp_list[i] + "  " + time.ctime() + "\n")
                self.mclogs_file.close()
            self.u_refresh()
            messagebox.showinfo("Dropbox Deletion", "File(s) deleted successfully")
            self.d_refresh()
        except NameError:
            messagebox.showerror("Dropbox Deletion !","No File selected or Dropbox not connected !")
        self.u_refresh()


if __name__ == "__main__":
    root = Tk()
    staas(root)
    root.mainloop()