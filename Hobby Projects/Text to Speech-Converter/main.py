
class tts_gui:
    def browse_func(self):
        self.filename = filedialog.askopenfilename(title="Select a file to upload", initialdir="/",
                                              filetypes=( ('Text files', '*.txt'), ('PDF files', '*.pdf'), ('Word files', '*.docx'), ('All files', '*') ))
        self.extension=os.path.splitext(self.filename)[1]

        if self.extension=='.docx':
            self.data=docx2txt.process(self.filename)
            messagebox.showinfo("Upload Folder !", "Folder uploaded successfully" + "\nfrom\n" + self.filename)
        elif self.extension=='.pdf':
            read_pdf = PyPDF2.PdfFileReader(self.filename)
            self.data = []
            for i in range(read_pdf.getNumPages()):
                page = read_pdf.getPage(i)
                # print('Page No - ' + str(1 + read_pdf.getPageNumber(page)))
                page_content = page.extractText()
                self.data.append(page_content)
            messagebox.showinfo("Upload Folder !", "Folder uploaded successfully" + "\nfrom\n" + self.filename)
        elif self.extension=='.txt':
            self.data=open(self.filename,'r').read()
            messagebox.showinfo("Upload Folder !", "Folder uploaded successfully" + "\nfrom\n" + self.filename)
        else:
            messagebox.showerror("Select a valid format","You must select a text document")

    def save(self):
        try:
            if self.v.get() not in [1, 2]:
                messagebox.showwarning("Select a language", "You must select your language of the document !")
            elif self.filename == '':
                messagebox.showwarning("Select a text file", "You must select a file to convert !")
            elif self.v.get() == 1 and self.filename != '':
                self.savefilename = filedialog.asksaveasfilename(title="Select a file to upload", initialdir="/",
                                                                 filetypes=(("All files", "*.mp3*"), ("", "")))
                if self.savefilename != '':
                    tts = gTTS(text=str(self.data), lang='ta')
                    tts.save(self.savefilename + ".mp3")
                    messagebox.showinfo("Save File !", "File saved successfully!\nIn: " + self.savefilename + ".mp3")
                    self.logs("SUCCESS")
                else:
                    messagebox.showwarning("File name", "No file has been saved")
            elif self.v.get() == 2 and self.filename != '':
                self.savefilename = filedialog.asksaveasfilename(title="Select a file to upload", initialdir="/",
                                                                 filetypes=(("All files", "*.mp3*"), ("", "")))
                if self.savefilename != '':
                    tts = gTTS(text=str(self.data), lang='en')
                    tts.save(self.savefilename + ".mp3")
                    messagebox.showinfo("Save File ?", "File saved successfully!\nPath: " + self.savefilename + ".mp3")
                    self.logs("SUCCESS")
                else:
                    messagebox.showwarning("What's the file name ?", "No file has been saved")

        except AttributeError:
            messagebox.showwarning("Select a text file !", "You must select a file to convert !")

    def logs(self,conv):
        dest=self.savefilename+'_logs.txt'
        lang_dict=["","Tamil","English"]
        tf=open(dest,'w+')
        tf.write("---------------------")
        tf.write("\nCONVERSION DETAILS:\n")
        tf.write("---------------------")
        tf.write("\n\nLanguage:\n")
        tf.write(lang_dict[self.v.get()])
        tf.write('\n\nText File:\n'+self.filename+'\n')
        tf.write('\nAudio File:\n'+self.savefilename+".mp3"+"\n")
        tf.write("\nConversion:\n")
        tf.write(conv)
        tf.close()

    def exit_func(self):
        self.window.destroy()

    def __init__(self,window):
        self.v=IntVar()
        self.window=window
        self.window.title("Text to Audio Application")
        self.window.geometry("350x170")
        self.window.resizable(width=0,height=0)
        self.label=Label(window,text="""Select the language of the document
        ( supported types: .docx, .pdf , .txt)""")
        self.label.grid()
        self.tamil_radio=Radiobutton(window,text='Tamil',variable=self.v,value=1)
        self.tamil_radio.grid(row=1,column=0)
        self.english_radio=Radiobutton(window,text='English',variable=self.v,value=2)
        self.english_radio.grid(row=1,column=1)
        self.browse_button = Button(window, text="Select your text file", command=self.browse_func)
        self.browse_button.grid()
        self.save_file = Button(window, text="Save as audio file (.mp3)", command=self.save)
        self.save_file.grid()
        self.exit_button = Button(window, text="Exit the application", command=self.exit_func)
        self.exit_button.grid()


def main():
    window=Tk()
    tts_gui(window)
    window.mainloop()

if __name__=="__main__":
    import PyPDF2 ,os, docx2txt
    from tkinter import *
    from tkinter import filedialog, messagebox
    from gtts import gTTS
    main()