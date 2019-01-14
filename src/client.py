from tkinter import *
from tkinter import filedialog

from src.driveSinus import getSQD, getMeanAmp, wrtePlot

resSQD = []
resMA = []
loadedFilename = ""

window = Tk()
window.title("Sinus Drive App")
window.geometry('300x150')

lbl = Label(window, text="Press load csv file")
lbl.grid(column=0, columnspan=2, row=0)

var = IntVar()

c = Checkbutton(window, text="Range", variable=var)
c.grid(column=0, columnspan=2, row=2)



sl = Label(window, text="Start")
sl.grid(column=0, row=3)

fl = Label(window, text="Finish")
fl.grid(column=1, row=3)

start = Entry(window)
start.grid(column=0, row=4)

start.delete(0, END)
start.insert(0, "0")

end = Entry(window)
end.grid(column=1, row=4)

end.delete(0, END)
end.insert(0, "100000")


def load():
    global resSQD
    global resMA
    global loadedFilename
    global var

    filename = filedialog.askopenfilename(initialdir=".", title="Select file",
                                          filetypes=(("csv", "*.csv"), ("all files", "*.*")))

    lbl.configure(text="Calculation in work... wait")
    lbl.update()
    loadedFilename = filename.split('/')[-1]

    if var:
        print(int(start.get()), int(end.get()))
        resMA = getMeanAmp(filename, int(start.get()), int(end.get()))
        resSQD = getSQD(filename, int(start.get()), int(end.get()))
    else:
        resMA = getMeanAmp(filename)
        resSQD = getSQD(filename)

    print("calculations ready")
    lbl.configure(text="Calculation ready")
    lbl.update()


def save():
    savefolder = filedialog.askdirectory(initialdir=".", title="Select folder")
    print(savefolder)
    wrtePlot(resMA[0], resMA[1], resMA[2], savefolder + "/mean_amplitude_" + loadedFilename.split('.')[0] + '.png',
             "mean_amplitude_" + loadedFilename.split('.')[0])
    wrtePlot(resSQD[0], resSQD[1], resSQD[2], savefolder + "/sqd_" + loadedFilename.split('.')[0] + '.png',
             "sqd_" + loadedFilename.split('.')[0])

    lbl.configure(text="images are saved")


btn = Button(window, text="Load", command=load)
btn.grid(column=0, row=1)

btn = Button(window, text="Save", command=save)
btn.grid(column=1, row=1)

window.mainloop()
