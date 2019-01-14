from tkinter import *
from tkinter import filedialog

from src.driveSinus import getSQD, getMeanAmp, wrtePlot

resSQD = []
resMA = []
loadedFilename = ""

window = Tk()
window.title("Sinus Drive App")
window.geometry('150x80')

lbl = Label(window, text="Press load csv file")
lbl.grid(column=0, columnspan=2, row=0)

def load():
    global resSQD
    global resMA
    global loadedFilename


    filename = filedialog.askopenfilename(initialdir=".", title="Select file",
                                            filetypes=(("csv", "*.csv"), ("all files", "*.*")))

    lbl.configure(text="Calculation in work... wait")
    lbl.update()
    loadedFilename = filename.split('/')[-1]

    resSQD = getSQD(filename)
    resMA = getMeanAmp(filename)
    lbl.configure(text="Calculation ready")
    lbl.update()

def save():
    savefolder = filedialog.askdirectory(initialdir=".", title="Select folder")
    print(savefolder)
    wrtePlot(resMA[0], resMA[1], resMA[2], savefolder +"/mean_amplitude_"+ loadedFilename.split('.')[0] + '.png', "mean_amplitude_" + loadedFilename.split('.')[0])
    wrtePlot(resSQD[0], resSQD[1], resSQD[2], savefolder +"/sqd_"+ loadedFilename.split('.')[0] + '.png', "sqd_" + loadedFilename.split('.')[0])

    lbl.configure(text="images are saved")

btn = Button(window, text="Load", command=load)
btn.grid(column=0, row=1)

btn = Button(window, text="Save", command=save)
btn.grid(column=1, row=1)

window.mainloop()