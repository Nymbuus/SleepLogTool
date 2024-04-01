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

    def write_to_df(self, file_list):
        """ Write to df from blf.\n\n
            file_list - The blf file(s) being read from. """
        if not all(file.lower().endswith('.blf') for file in file_list):
            raise TypeError("Only .blf files are supported to read from.")
        logs = []
        for file in file_list:
            logs.extend(list(can.BLFReader(file)))

        blf_time = []
        blf_current = []
        for msg in logs:
            msg = str(msg)
            msg = msg.strip()
            columns = msg.split()
            blf_time.append(float(columns[1]))
            upper_current_hexa = columns[9]
            lower_current_hexa = columns[10]
            current_hexa = upper_current_hexa + lower_current_hexa
            blf_current.append(int(current_hexa, 16))

        blf_data = {}
        blf_data["Time"] = blf_time
        blf_data["Current"] = blf_current
        return pd.DataFrame(blf_data)

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