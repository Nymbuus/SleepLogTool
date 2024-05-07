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
                    if file_list == "":
                        return False
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
        
        df = None
        channel = None
        for index, file in enumerate(file_list):
            blf_data = {"Time": [], "Current": []}
            with open(file, 'rb') as f:
                channel_get_blf = can.BLFReader(f)
                for msg in channel_get_blf:
                    channel = msg.channel
                    break
            f.close()

            with open(file, 'rb') as e:
                blf_return = can.BLFReader(e)
                percent = 100 / blf_return.object_count
                status = 0
                last_print = 0
                for i, msg in enumerate(blf_return):
                    status += percent
                    data = msg.data
                    hex1 = hex(data[1])[2:]
                    if len(hex1) == 1:
                        hex1 = "0"+hex1
                    hex2 = hex(data[2])[2:]
                    if len(hex2) == 1:
                        hex2 = "0"+hex2
                    hex3 = hex(data[3])[2:]
                    if len(hex3) == 1:
                        hex3 = "0"+hex3
                    current_dec = int(hex1+hex2+hex3,16)
                    # If byte 0 is less then 128, the number is negative.
                    if data[0] < 128:
                        current_dec -= 16777216
                    blf_data["Time"].append(msg.timestamp)
                    blf_data["Current"].append(current_dec)
                    if round(status) != last_print:
                        print(f"{round(status)}%")
                        last_print = round(status)
            
            temp = pd.DataFrame(blf_data)
            if index == 0:
                df = temp
            else:
                df = pd.concat([df, temp], axis=0)

        return df, channel


    def remove_time(self, dfs, remove_start_time, remove_end_time):
        """ Loads pandas dataframe to a local variable.
            With this we remove the start and end elements provided in minutes.
            If the if cases is'nt used the program will crash. """
        if not (isinstance(remove_start_time, int) or isinstance(remove_start_time, float)):
            raise TypeError("remove_start_time variable was not a integer or float!")
        if not (isinstance(remove_end_time, int) or isinstance(remove_end_time, float)):
            raise TypeError("remove_end_time variable was not a integer or float!")
        
        if remove_start_time != 0:
            dfs = dfs[int(remove_start_time):]
        if remove_end_time != 0:
            dfs = dfs[:-int(remove_end_time)]

        return dfs