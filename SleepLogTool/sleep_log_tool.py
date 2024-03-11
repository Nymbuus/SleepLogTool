""" Imports. Numpy will be used. """
from os import environ
import csv
import tkinter as tk
import tkinter.filedialog as fd
import can
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

headers = ['Time', 'Current']
root = tk.Tk()
log_output = []


def file_explorer():
    """ Lets the user chose what files he wants to analyze. """
    filez = fd.askopenfilenames(parent=root, title='Choose one or multiple BLF files')
    file_list = list(filez)
    print("User choosed", len(file_list), "files to load")
    return file_list


def save_file(file_list_var):
    """ Chose where to save file and then save valuable data from the loaded files to CSV file. """
    my_file = fd.asksaveasfile(mode='w',defaultextension=".csv")
    out = ['Time']
    out.append('Current')
    with open(my_file.name,'w', encoding='UTF8', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=out)
        writer.writeheader()

    return write_to_csv(my_file.name, file_list_var)


def write_to_csv(file_name, file_list_var):
    """ Write to csv from blf. """
    g = open(file_name, mode='a', encoding="utf-8")
    for i in range(0, len(file_list_var)):
        log = can.BLFReader(file_list_var[i])
        log = list(log)

    for msg in log:
        print(msg)
        msg = str(msg)
        msg = msg.strip()
        columns = msg.split()
        time = columns[1]
        upper_current_hexa = columns[9]
        lower_current_hexa = columns[10]
        current_hexa = upper_current_hexa + lower_current_hexa
        current_value = str(int(current_hexa, 16))
        g.write('\n' + time + ',')
        g.write(current_value)
    g.close()

    return file_name


# Removes some environment warnings
def suppress_qt_warnings():
    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"


def main(savedFileName, removeStart, removeEnd):
    removeStart = int(removeStart * 6000)
    removeEnd = int(removeEnd * 6000)

    # Read CSV file into a pandas DataFrame
    chunk_size = 500    # Was 500000 before.
    chunks = []
    for chunk in pd.read_csv(savedFileName, chunksize=chunk_size):
        chunks.append(chunk)
    pandas_df = pd.concat(chunks, ignore_index=True)

    # Loads pandas dataframe to a local variable.
    # With this we remove the start and end elements provided in minutes in the beginning of the program.
    # If the if cases are'nt used the program will crash.
    df = pandas_df
    if removeStart != 0:
        df = df[removeStart:]
    if removeEnd != 0:
        df = df[:-removeEnd]

    # Calculate statistics
    average = df['Current'].mean()
    maximum = df['Current'].max()
    minimum = df['Current'].min()
    total_time = float(df['Time'].max() - df['Time'].min())
    ampere_hours = (total_time / 3600) * (average * 0.001)

    print('\nAverage Current:', "{:.3f}".format(average), "mA")
    print('Max Current:', maximum, "mA")
    print('Min Current:', minimum, "mA")
    print("Total measurement time:", "{:.3f}".format(total_time / 3600), "hours or", "{:.3f}".format(total_time/60), "minutes")
    print("Ampere hours:", "{:.4f}".format(ampere_hours), "Ah")

    # Plotting
    firstTime = pandas_df["Time"].min()
    y = df.Current.to_numpy()
    x = df.Time.to_numpy()
    plt.plot((x - firstTime) / 3600, y)
    plt.xlabel("Time(h)", fontsize=15)
    plt.ylabel("Current(mA)", fontsize=15)
    plt.title("Sleeplog analysis", fontsize=24)
    plt.subplots_adjust(left=0.05, bottom=0.06, right=0.97, top=0.955, wspace=None, hspace=None)
    plt.grid()
    manager = plt.get_current_fig_manager()
    manager.window.state('zoomed')
    plt.show()

# Start of programm    
if __name__ == '__main__':   
    suppress_qt_warnings()
    removeStart = float(input("Minutes to remove from the start: (Insert value and press enter)\n"))          # 90000 is 15 min, 15 min is avarage sleep time
    print(removeStart, "Minutes will be removed from the start of the log")
    removeEnd = float(input("Minutes to remove from the end: (Insert value and press enter\n"))               # 30000
    print(removeEnd, "Minutes will be removed from the end of the log")
    the_list = file_explorer()                                                                                  # Open the file explorer to select files and save those files data into a csv file
    savedFileName = save_file(the_list)
    main(savedFileName, removeStart, removeEnd)                                                               # Start plotfunction