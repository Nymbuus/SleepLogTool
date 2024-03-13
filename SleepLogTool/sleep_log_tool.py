""" Imports. Numpy will be used. """
from os import environ
import csv
import tkinter as tk
import tkinter.filedialog as fd
import can
import matplotlib.pyplot as plt
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
    for _, file_var in enumerate(file_list_var):
        log = can.BLFReader(file_var)
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
    """ Suppresses warnings apering when starting .exe file. """
    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"


def csv_to_panda(saved_file):
    """ Read CSV file into a pandas DataFrame """
    chunks = []
    for chunk in pd.read_csv(saved_file, chunksize=500000):
        chunks.append(chunk)
    return pd.concat(chunks, ignore_index=True)


def remove_start_and_end(df):
    """ Loads pandas dataframe to a local variable.
        With this we remove the start and end elements provided in minutes 
        in the beginning of the program. If the if cases are'nt used the program will crash. """
    # 90000 is 15 min, 15 min is avarage sleep time
    remove_start = float(input("Insert minutes to remove from start and press enter:\n") * 6000)
    print(remove_start, "Minutes will be removed from the start of the log")
    remove_end = float(input("Insert minutes to remove from the end and press enter:\n") * 6000)
    print(remove_end, "Minutes will be removed from the end of the log")

    if remove_start != 0:
        df = df[remove_start:]
    if remove_end != 0:
        df = df[:-remove_end]
    return df


def calculating_statistics(df):
    """ Calculate statistics """
    average = df['Current'].mean()
    maximum = df['Current'].max()
    minimum = df['Current'].min()
    total_time = float(df['Time'].max() - df['Time'].min())
    ampere_hours = (total_time / 3600) * (average * 0.001)

    print(f"\nAverage Current: {average:.3f}mA")
    print(f"Max Current: {maximum} mA")
    print(f"Min Current: {minimum} mA")
    print(f"Total time: {(total_time / 3600):.3f} hours or {(total_time/60):.3f} minutes.")
    print(f"Ampere hours: {ampere_hours:.4f} Ah")


def plotting_graph(df):
    """ Plotting. """
    first_time = df["Time"].min()
    y = df.Current.to_numpy()
    x = df.Time.to_numpy()
    plt.plot((x - first_time) / 3600, y)
    plt.xlabel("Time(h)", fontsize=15)
    plt.ylabel("Current(mA)", fontsize=15)
    plt.title("Sleeplog analysis", fontsize=24)
    plt.subplots_adjust(left=0.05, bottom=0.06, right=0.97, top=0.955, wspace=None, hspace=None)
    plt.grid()
    manager = plt.get_current_fig_manager()
    manager.window.state('zoomed')
    plt.show()


def main():
    """ Main. """
    suppress_qt_warnings()

    # Open the file explorer to select files and save those files data into a csv file
    the_list = file_explorer()
    saved_file = save_file(the_list)

    df = csv_to_panda(saved_file)
    df = remove_start_and_end(df)
    calculating_statistics(df)
    plotting_graph(df)


if __name__ == '__main__':
    main()
