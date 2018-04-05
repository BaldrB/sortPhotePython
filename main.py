# !/usr/bin/python
# -*- coding: utf-8 -*-
# Vladislav Popko vpopko@gmail.com

import os
import shutil
import pickle
from tkinter import filedialog
from tkinter import *
import datetime
import time
import piexif



def sortfile(pathfilesout, pathfilesin):
    """Поиск даты в exif"""

    cou_folder = 0
    cou_files = 0

    cou = 0
    cou_f = 0
    pathall = []

    for path, dirs, files in os.walk(pathfilesout):
        pathall.append(path)
        cou_folder = len(pathall)
    for pathfile in pathall:
        faile = os.listdir(pathfile)
        faile = list(filter(lambda x: x.endswith('.jpg') or x.endswith('.jpg'), faile))
        cou_files = len(faile)
        cou_f += 1
        cou = 0
        
        for i in faile:
            gm = None
            exif_dict = piexif.load(os.path.join(pathfile, i))
            for ifd in ("0th", "Exif", "GPS", "1st"):
                for tag in exif_dict[ifd]:
                    if ((piexif.TAGS[ifd][tag]["name"] == "DateTime") or (piexif.TAGS[ifd][tag]["name"] == "DateTimeOriginal")):  
                        gm = exif_dict[ifd][tag]
                # f = os.stat(os.path.join(pathfile, i)).st_ctime
            print(os.path.join(pathfile, i))  
            if(gm == None):
                gm = "0000.00"
            else:
                gm = gm.decode("utf-8")
                gm = gm.replace(':', '.')
                gm = gm[0:7]

            cou += 1
            labelLoad.config(text="Папка: {} из {}".format(cou_f, cou_folder))
            labelg.config(width=int((cou_f * 100 / cou_folder)* 50 / 100))
            labelLoad1.config(text="Файл номер: {} из {}".format(cou, cou_files))
            labelg1.config(width=int((cou * 100 / cou_files)* 50 / 100))
            root.update()
            if(os.path.exists(os.path.join(pathfilesin, gm))):
                shutil.copy(os.path.join(pathfile,i), os.path.join(pathfilesin,gm))
            else:
                os.mkdir(os.path.join(pathfilesin, gm))
                shutil.copy(os.path.join(pathfile,i), os.path.join(pathfilesin,gm))
    labelLoad.config(text="Готово!")
    labelLoad1.config(text="Готово!")

def click_button():
    sortfile(pathout.get(), pathout1.get())

def LoadFile(): 
    dir_path = filedialog.askdirectory()
    pathout.set(dir_path)

def LoadFile1(): 
    dir_path = filedialog.askdirectory()
    pathout1.set(dir_path)
    


root = Tk()
panelFrame = Frame(root, height = 60, bg = 'gray')
root.title("Перемещалка")
root.geometry("600x400")

pathout = StringVar()
npathout_file = Entry(textvariable=pathout)
npathout_file.place(x=170, y=170, width=350)

pathout1 = StringVar()
npathout_file1 = Entry(textvariable=pathout1)
npathout_file1.place(x=170, y=220, width=350)

labelLoad = Label(text="0", fg="#000", height=1, width=50)
labelLoad.place(x=150, y= 10)
labelg = Label(fg="#000", bg="#00ff00", height=1, width=0)
labelg.place(x=150, y= 35)

labelLoad1 = Label(text="0", fg="#000", height=1, width=50)
labelLoad1.place(x=150, y= 60)
labelg1 = Label(fg="#000", bg="#00ff00", height=1, width=0)
labelg1.place(x=150, y= 85)

btn = Button(text="начать сортировку", background="#555", foreground="#ccc",
             padx="20", pady="8", font="16", command=click_button)
btn.place(x=10, y=70, height=40, width=140)

buttonLoadDirectoryOut = Button(text="Выберите папку", background="#555", foreground="#ccc",
             padx="20", pady="8", font="16", command=LoadFile)
buttonLoadDirectoryOut.place(x=10, y=160, height=40, width=140)

buttonLoadDirectoryIn = Button(text="Расортировать в", background="#555", foreground="#ccc",
             padx="20", pady="8", font="16", command=LoadFile1)
buttonLoadDirectoryIn.place(x=10, y=210, height=40, width=140)
 
root.mainloop()
