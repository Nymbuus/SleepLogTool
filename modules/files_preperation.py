import csv
import tkinter.filedialog as fd
import can
import pandas as pd

MINUTE_TO_10MS = 6000

class FilesPreperation:
    """ Preps the files before displaying them. """

    def __init__(self):
        """ Initialises the class. """

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
        """ Write to csv from blf.\n
            file_name - The csv file being written to.\n
            file_list - The blf file(s) being read from. """
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

    def remove_time(self, df, remove_start_time, remove_end_time):
        """ Loads pandas dataframe to a local variable.
            With this we remove the start and end elements provided in minutes.
            If the if cases is'nt used the program will crash. """
        start_time_bool = True
        end_time_bool = True
        while start_time_bool and end_time_bool:
            try:
                remove_start_time = float(remove_start_time) * MINUTE_TO_10MS
                remove_end_time = float(remove_end_time) * MINUTE_TO_10MS
                if 0 <= remove_start_time < len(df)+12:
                    start_time_bool = False
                    if 0 <= remove_end_time < len(df)+12-remove_start_time:
                        start_time_bool = False
                    elif remove_end_time < 0:
                        self._rtm.warning("End time too low value. Try again.")
                    elif remove_start_time >= len(df)+12-remove_start_time:
                        self._rtm.warning("End time too high value. Try again.")
                elif remove_start_time < 0:
                    self._rtm.warning("Start time too low value. Try again.")
                elif remove_start_time >= len(df)+12:
                    self._rtm.warning("Start time too high value. Try again.")
            except ValueError as err:
                print(f"ValueError: {err}. Try again.")
        
        if remove_start_time != 0:
            df = df[int(remove_start_time):]
        if remove_end_time != 0:
            df = df[:-int(remove_end_time)]

        return df