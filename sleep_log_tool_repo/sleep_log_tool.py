""" Imports. Numpy will be used. """
from os import environ
import csv
from tkinter import *
import tkinter.filedialog as fd
import can
import matplotlib.pyplot as plt
import pandas as pd
import numpy


MINUTE_TO_10MS = 6000

class SleepLogTool():
    """ SleepLogTool """

    def __init__(self):
        """ Initializes the class. """

    def file_explorer(self):
        """ Lets the user chose files to analyze. """
        while True:
            file_list = fd.askopenfilenames(title='Choose one or multiple BLF files')
            if all(file.lower().endswith('.blf') for file in file_list):
                print("User choosed", len(file_list), "files to load")
                return file_list
            else:
                print("Wrong file type, try again.")

    def save_file(self):
        """ Chose where to save file and then save valuable data from the loaded files to CSV file. """
        my_file = fd.asksaveasfile(mode='w', defaultextension=".csv")
        if my_file == None:
            exit("Program canceled.")
        out = ["Time", "Current"]
        with open(my_file.name, 'w', encoding='UTF8', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=out)
            writer.writeheader()

        return my_file.name

    def write_to_csv(self, file_name, file_list):
        """ Write to csv from blf. """
        if not file_name.endswith(".csv"):
            raise TypeError("Only .csv files are supported to save to.")
        if not all(file.lower().endswith('.blf') for file in file_list):
            raise TypeError("Only .blf files are supported to read from.")
        logs = []
        for _, file in enumerate(file_list):
            logs.extend(list(can.BLFReader(file)))

        with open(file_name, mode='a', encoding="utf-8") as file:
            for msg in logs:
                msg = str(msg)
                msg = msg.strip()
                columns = msg.split()
                time = columns[1]
                upper_current_hexa = columns[9]
                lower_current_hexa = columns[10]
                current_hexa = upper_current_hexa + lower_current_hexa
                current_value = str(int(current_hexa, 16))
                file.write('\n' + time + ',')
                file.write(current_value)
            file.close()

        return file_name

    def csv_to_panda(self, saved_file):
        """ Read CSV file into a pandas DataFrame """
        if not saved_file.endswith(".csv"):
            raise TypeError("Only .csv files are supported.")
        chunks = []
        for chunk in pd.read_csv(saved_file, chunksize=500000):
            chunks.append(chunk)
        return pd.concat(chunks, ignore_index=True)
    
    def remove_time_get_input(self, input_text, len_left_df):
        """ Returns the value from user input. """
        while True:
            try:
                remove_start_value = float(input(input_text))
                if 0 < ((remove_start_value * MINUTE_TO_10MS) + 12) < len_left_df:
                    return remove_start_value
                elif ((remove_start_value * MINUTE_TO_10MS) + 12) >= len_left_df:
                    print("Too high value. Try again.")
                elif ((remove_start_value * MINUTE_TO_10MS) + 12) < 0:
                    print("Too small value. Try again.")
            except ValueError as err:
                print(f"ValueError: {err}. Try again.")

    def remove_time(self, df):
        """ Loads pandas dataframe to a local variable.
            With this we remove the start and end elements provided in minutes 
            in the beginning of the program. If the if cases are'nt used the program will crash. """
        # 90000 is 15 min, 15 min is avarage sleep time
        remove_start = int(self.remove_time_get_input("Insert minutes to remove from start and press enter:\n", len(df)) * MINUTE_TO_10MS)
        print(f"{remove_start / MINUTE_TO_10MS} minutes will be removed from the start of the log")
        remove_end = int(self.remove_time_get_input("Insert minutes to remove from end and press enter:\n", len(df) - remove_start) * MINUTE_TO_10MS)
        print(f"{remove_end / MINUTE_TO_10MS} minutes will be removed from the end of the log")

        if remove_start != 0:
            df = df[remove_start:]
        if remove_end != 0:
            df = df[:-remove_end]

        return df

    def calculating_statistics(self, df):
        """ Calculate statistics """
        average = df['Current'].mean()
        maximum = df['Current'].max()
        minimum = df['Current'].min()
        total_time = float(df['Time'].max() - df['Time'].min())
        print(f"\n\navarage: {average}\n\n")
        ampere_hours = (total_time / 3600) * (average * 0.001)

        print(f"\nAverage Current: {average:.3f}mA")
        print(f"Max Current: {maximum} mA")
        print(f"Min Current: {minimum} mA")
        print(f"Total time: {(total_time / 3600):.3f} hours or {(total_time / 60):.1f} minutes.")
        print(f"Ampere hours: {ampere_hours:.4f} Ah")

    def plotting_graph(self, df):
        """ Plotting. """
        first_time = df["Time"].min()
        y = df.Current.to_numpy()
        x = df.Time.to_numpy()
        # print(f"\n\nfirst_time: {first_time}\n\n")
        # print(f"\n\nfirst_time x: {x - first_time}\n\n")
        plt.plot((x - first_time) / 3600, y)
        plt.xlabel("Time(h)", fontsize=15)
        plt.ylabel("Current(mA)", fontsize=15)
        plt.title("Sleeplog analysis", fontsize=24)
        plt.subplots_adjust(left=0.05, bottom=0.06, right=0.97, top=0.955, wspace=None, hspace=None)
        plt.grid()
        manager = plt.get_current_fig_manager()
        manager.window.state('zoomed')
        plt.show()
        root.mainloop()
