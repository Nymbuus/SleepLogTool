import os
import tkinter.filedialog as fd
import can
import pandas as pd

MINUTE_TO_10MS = 6000

class FilesPreperation:
    """ Preps the files before displaying them. """

    def __init__(self):
        """ Initialises the class. """

    def file_explorer(self, choice):
        """ Lets the user chose files to analyze. """
        if choice == "file":
            while True:
                file_list = fd.askopenfilenames(title='Choose one or multiple BLF files')
                if all(file.lower().endswith('.blf') for file in file_list):
                    print("User choosed", len(file_list), "files to load")
                    return file_list
                else:
                    print("One or more files is not a blf type file, try again.")
        elif choice == "folder":
            while True:
                folder_list = fd.askdirectory(title="Choose one or more folders containing BLF files")
                file_list = []
                for root, dirs, files in os.walk(folder_list):
                    for file in files:
                        file_list.append(os.path.join(root,file))

                if all(file.lower().endswith('.blf') for file in file_list):
                    print("User choosed", len(file_list), "files to load")
                    return file_list
                else:
                    print("One or more files in directory is not blf file type, try again.")

    def blf_to_df(self, file_list):
        """ Write to df from blf.\n\n
            file_list - The blf file(s) being read from. """
        if not all(file.lower().endswith('.blf') for file in file_list):
            raise TypeError("Only .blf files are supported to read from.")
        
        list_dfs = []
        for file in file_list:
            blf_data = {"Time": [], "Current": []}
            with open(file, 'rb') as f:
                blf_return = can.BLFReader(f)
                percent = 100 / blf_return.object_count
                status = 0
                last_print = 0
                for i, msg in enumerate(blf_return):
                    status += percent
                    if i % 10 == 0:
                        columns = str(msg).strip().split()
                        blf_data["Time"].append(float(columns[1]))
                        current_dec = int(columns[10] + columns[11], 16)
                        if current_dec > 40000:
                            current_dec -= 72769
                        blf_data["Current"].append(current_dec)
                        if int(status) != last_print:
                            print(f"{status:.0f}%")
                            last_print = int(status)

            df = pd.DataFrame(blf_data)
            list_dfs.append(df)

        return list_dfs, file_list


    def remove_time(self, df, remove_start_time, remove_end_time):
        """ Loads pandas dataframe to a local variable.
            With this we remove the start and end elements provided in minutes.
            If the if cases is'nt used the program will crash. """
        if not (isinstance(remove_start_time, int) or isinstance(remove_start_time, float)):
            raise TypeError("remove_start_time variable was not a integer or float!")
        if not (isinstance(remove_end_time, int) or isinstance(remove_end_time, float)):
            raise TypeError("remove_end_time variable was not a integer or float!")
        
        if remove_start_time != 0:
            df = df[int(remove_start_time):]
        if remove_end_time != 0:
            df = df[:-int(remove_end_time)]

        return df