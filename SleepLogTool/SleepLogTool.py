import can
import csv
import os
from re import M
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from statistics import mean
from os.path import dirname
from pathlib import Path
from matplotlib.widgets import Slider
import tkinter as tk
import tkinter.filedialog as fd
import vaex as vx
from os import environ



headers = ['Time', 'Current']
root = tk.Tk()
log_output = []
global removeStart
global removeEnd



def fileExplorer():
    #Lets the user chose what files he wants to analyze
    filez = fd.askopenfilenames(parent=root, title='Choose one or multiple BLF files')
    fileList = list(filez)
    print("User choosed", len(fileList), "files to load")
    return fileList



def saveFile(fileListVar):
    #Chose where to save the file and then save the valuabe data from the loaded files into this new CSV file
    myFile = fd.asksaveasfile(mode='w',defaultextension=".csv")
    out = ['Time']
    out.append('Current')
    with open(myFile.name,'w', encoding='UTF8', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=out)
        writer.writeheader()

    fileName = myFile.name
    g = open(fileName, 'a')
    for i in range(0,len(fileListVar)):
        print ("Reading values from:  ", fileListVar[i])
        log = can.BLFReader(fileListVar[i])
        log = list(log)

        for msg in log:
            msg = str(msg)
            msg = msg.strip()
            columns = msg.split()
            time = columns[1]
            negVar = str(int(columns[7], 16))
            name1 = columns[8]
            name2 = columns[9]
            name3 = columns[10]
            name4 = name2 + name3
            name5 = str(int(name4, 16))
            g.write('\n' + time + ',')
            g.write(name5)
    g.close()
    return fileName


def suppress_qt_warnings():
    #Removes some environment warnings
    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"


def main(savedFileName, removeStart, removeEnd):
    removeStart = removeStart*6000
    removeEnd = removeEnd*6000

    #This part creates a hdf5 file for faster usage and plots a graph using matplotlib
    vaex_df = vx.from_csv(savedFileName, convert = True, chunk_size =5_00_000)
    type(vaex_df)
    df = vx.open(savedFileName+'.hdf5')
    firstTime = df["Time"].min()                                                                    #Should the plot start from 0?
    df = df[:-removeEnd]
    df = df[removeStart:]
    avarage = df['Current'].mean()                                                                  #calculates the mean value from the csv file
    max = df['Current'].max()                                                                       #calculates the max value from the csv file
    min = df['Current'].min()                                                                       #calculates the min value from the csv file
    totalTime = float(df['Time'].max() - df['Time'].min())
    print('\nAvarage Current:', "{:.3f}".format(avarage), "mA")                                     #prints the avarage
    print('Max Current:', max, "mA")                                                                #prints the max
    print('Min Current:', min, "mA")                                                                #prints the min
    print("Total measurement time:", "{:.3f}".format(totalTime/3600), "hours")                      #prints the Total measurent time
    print("Ampere hours:", "{:.4f}".format((totalTime/3600)*(avarage*0.001)), "Ah")                 #prints the Ampere Hours
    y=df.Current.to_numpy()
    x=df.Time.to_numpy()
    plt.scatter((x-firstTime)/3600, (y), s=2)                                                       #
    plt.xlabel("Time(h)", fontsize=15)
    plt.ylabel("Current(mA)", fontsize=15)
    plt.title("Sleeplog analysis", fontsize=24)
    plt.subplots_adjust(left=0.05, bottom=0.06, right=0.97, top=0.955, wspace=None, hspace=None)
    plt.grid()
    manager = plt.get_current_fig_manager()
    manager.window.state('zoomed')
    plt.show()
    
    

if __name__ == '__main__':   
    suppress_qt_warnings()
    removeStart = int(input("Minutes to remove from the start: (Insert value and press enter)\n"))          #90000 is 15 min, 15 min is avarage sleep time
    print(removeStart, "Minutes will be removed from the start of the log")
    removeEnd = int(input("Minutes to remove from the end: (Insert value and press enter\n"))               #30000
    print(removeEnd, "Minutes will be removed from the end of the log")
    theList = fileExplorer()                                                                                #Open the file explorer to select files and save those files data into a csv file
    savedFileName = saveFile(theList)
    main(savedFileName, removeStart, removeEnd)                                                             #Start plotfunction
        
