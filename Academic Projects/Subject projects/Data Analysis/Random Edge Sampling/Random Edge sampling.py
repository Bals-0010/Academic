import random, xlrd, os
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import xlsxwriter

window = Tk()
window.title("Data Analysis II - Random Edge Sampling")
window.resizable(width=False, height=False)
window.geometry("775x475")
window.configure(background="sandy Brown")

Label(window, text="", bg="sandy Brown", fg="black", font="Comicsans 10 ").grid(row=0, column=2, sticky=W)
Label(window, text="Data Analysis II - Random Edge Sampling", bg="sandy Brown", fg="black", font="Comicsans 15").grid(
    row=1, column=2, sticky=W)
# Label(window,text="",bg="sandy Brown",fg="cadet blue",font="Comicsans 15").grid(row=2,column=2,sticky=W)

Label(window, text="", bg="sandy Brown", fg="black", font="Comicsans 10 ").grid(row=5, column=2, sticky=W)
Label(window, text="", bg="sandy Brown", fg="black", font="Comicsans 10 ").grid(row=6, column=2, sticky=W)

# ###################################
Label(window, text="        Browse for a DataSet ", bg="sandy Brown", fg="black", font="Comicsans 12").grid(row=7,
                                                                                                            column=1,
                                                                                                            sticky=W)
a = Label(window, text="", fg="sandy Brown", bg="white", font="Comicsans 12", width=30).grid(row=7, column=2)

Label(window, text="\t\t\t", bg="sandy Brown", fg="white", font="Comicsans 12").grid(row=9, column=3)

Label(window, text="Enter Probability (%)", bg="sandy Brown", fg="black", font="Comicsans 12").grid(row=10, column=1)
p = Entry(window, fg="black", bg="white", font="TimesNewRoman 12", width=30, justify='left')
p.grid(row=10, column=2)
p.focus_set()


Label(window, text="", bg="sandy Brown", fg="sandy Brown", font="Comicsans 12").grid(row=15, column=2)
Label(window, text="", bg="sandy Brown", fg="sandy Brown", font="Comicsans 12").grid(row=17, column=2)
Label(window, text="", bg="sandy Brown", fg="sandy Brown", font="Comicsans 12").grid(row=18, column=2)
Label(window, text="", bg="sandy Brown", fg="sandy Brown", font="Comicsans 12").grid(row=20, column=2)

Label(window, text="     No. of Edges", bg="sandy Brown", fg="black", font="Comicsans 12").grid(row=14, column=1)
Label(window, text="", fg="black", bg="white", font="Comicsans 12", width=30).grid(row=14, column=2)
Button(window, text="           Exit             ", font="Comicsans 12", command=window.destroy).grid(row=19, column=2)

Label(window, text="Sample Size", bg="sandy Brown", fg="black", font="Comicsans 12").grid(row=16, column=1)
Label(window, text="", fg="black", bg="white", font="Comicsans 12", width=30).grid(row=16, column=2)

# Browse option
def browsefunc():
    window.filename = filedialog.askopenfilename(title="Select a Dataset (xlsx files)", initialdir="/",
                                                 filetypes=(("All files", "*.*"), ("Excel files", "*.xlsx")))
    global filename, b
    filename = window.filename

    if not filename.endswith('.xlsx'):
        messagebox.showerror("Import error", "Filetype must be a .xlsx")
    else:
        b = Entry(window, fg="white", bg="black", font="TimesNewRoman 12", width="30")
        b.grid(row=7, column=2)
        b.insert(12, filename)
        messagebox.showinfo("Open Source File", "Import Successful !\n\n'%s'" % filename)
        browsefunc.filename = filename


def save():
    try:
        dirname, Filename = os.path.split(os.path.abspath(__file__))
        if int(p.get()) == int and a.get() != "":
            messagebox.showinfo("Save settings ?","Processing.....")
        Random_Edge_selection(filename, ((int(p.get())) / 100) )

    except ValueError:
        messagebox.showerror("Save ?", "Invalid Format on Probability OR Filepath is not entered")

    except AttributeError:
        messagebox.showerror("Save ?","Filepath is not entered\nPlease select a file")
        browsefunc()


def clear():
    p.delete(first=0, last=len(p.get()))
    Label(window, text="", bg="white", fg="black", font="Comicsans 12", width=30).grid(row=12, column=2)
    Label(window, text="", bg="white", fg="black", font="Comicsans 12", width=30).grid(row=14, column=2)
    Label(window, text="", bg="white", fg="black", font="Comicsans 12", width=30).grid(row=16, column=2)
    Label(window, text="", bg="white", fg="black", font="TimesNewRoman 12", width=30).grid(row=7, column=2)
    try:
        b.delete(first=0, last=len(b.get()))
    except NameError:
        pass


def Random_Edge_selection(file, prob):
    import sys
    wb = xlrd.open_workbook(file)
    sheet = wb.sheet_by_index(0)
    dirname, filename = os.path.split(os.path.abspath(__file__))
    if dirname.endswith('\\'):
        xl = dirname + "Output.xlsx"
        aa = dirname + "Output.txt"
    else:
        xl = dirname + "\\" + "Output.xlsx"
        aa = dirname + "\\" + "Output.txt"
    sys.stdout = open(aa, "wt")
    adjacencyList = {}
    edgeList = []
    a = sheet.col_values(0, 0)
    b = sheet.col_values(1, 0)
    aa = [int(a[i]) for i in range(0, len(a))]
    bb = [int(b[i]) for i in range(0, len(b))]
    print("\nGraph Adjacency List:")

    for i in range(len(a)):
        adjacencyList.setdefault(aa[i], [])
        adjacencyList[aa[i]].append(bb[i])
        adjacencyList.setdefault(bb[i], [])
        adjacencyList[bb[i]].append(aa[i])
    print(adjacencyList)


    i = 0
    while i < len(aa):
        edgeList.append([(aa[i]), (bb[i])])
        i = i + 1

    # for i in range(0, len(edgeList)):
    #     print(edgeList[i])

    print("\n\nNumber of Nodes in Total:")
    N = max(adjacencyList)
    print(N)
    Label(window, text=N, fg="black", bg="white", font="Comicsans 12", width=30).grid(row=12, column=2)
    print("\n\nMain Graph Total Number of Edges:")
    le = len(edgeList)
    print(le)
    Label(window, text=le, fg="black", bg="white", font="Comicsans 12", width=30).grid(row=14, column=2)
    print("\n\nRANDOM EDGE SELECTION:")
    print("_____________________________")

    row, col = N, N
    adj_matrix = [[0 for x in range(row)] for y in range(col)]

    aaa, bbb = [], []
    for i in range(len(edgeList)):
        aaa.append(edgeList[i][0])
        bbb.append(edgeList[i][1])

    i = 0
    while i < len(aaa):
        adj_matrix[aaa[i] - 1][bbb[i] - 1] = 1
        adj_matrix[bbb[i] - 1][aaa[i] - 1] = 1
        i = i + 1

    i = 0
    df = []
    while i < len(adj_matrix):
        df.append(sum(adj_matrix[i]))
        i = i + 1

    ss = prob * N
    sample_size = round(ss)
    print("\nSample Size")
    print(sample_size)
    Label(window, text=sample_size, fg="black", bg="white", font="Comicsans 12", width=30).grid(row=16, column=2)

    DF = sorted(df)
    freq = {i: DF.count(i) for i in DF}
    print("\nDegree and Frequencies:")
    print(freq)
    print("\nRelative frequencies:")
    rf = [round((freq[i]) / len(adj_matrix), 4) for i in freq]
    print(rf)

    newlist1 = random.sample(edgeList, sample_size)
    print("\n\nRandom Edges Selection - Edges formed :")

    for i in range(len(newlist1)):
        print(newlist1[i])

    newlist2 = random.sample(adjacencyList.keys(), sample_size)
    newedges = []

    for i in range(len(newlist2)):
        for j in range(len(newlist2)):
            if ([newlist2[i], newlist2[j]]) or ([newlist2[j], newlist2[i]]) in edgeList:
                newedges.append([newlist2[i], newlist2[j]])

    for i in range(len(newedges)):
        print(newedges[i])

    wbkk = xlsxwriter.Workbook(xl)
    wkss = wbkk.add_worksheet("Sheet 1")

    for i in range(0, len(newlist1)):
        wkss.write(i, 0, newlist1[i][0])
        wkss.write(i, 1, newlist1[i][1])
    wbkk.close()

    messagebox.showinfo("Save settings ?", "Settings Saved")

Button(window, text="        Save file        ", font="Comicsans 12", command=save).grid(row=14, column=3)

Button(window, text="     Browse File     ", font="Comicsans 12", command=browsefunc).grid(row=10, column=3)
Label(window, text="", bg="sandy Brown", fg="black", font="Comicsans 12").grid(row=11, column=2)
Label(window, text="", bg="sandy Brown", fg="black", font="Comicsans 12").grid(row=13, column=2)

Label(window, text="     No. of Nodes", bg="sandy Brown", fg="black", font="Comicsans 12").grid(row=12, column=1)
Label(window, text="", fg="sandy Brown", bg="white", font="Comicsans 12", width=30).grid(row=12, column=2)

Button(window, text="          Reset          ", font="Comicsans 12", command=clear).grid(row=12, column=3)

window.mainloop()