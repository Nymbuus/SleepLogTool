import os
import tkinter.filedialog as fd
import can
import pandas as pd
import numpy as np


class FilesPreperation:
    """ Preps the files before displaying them. """

    def __init__(self):
        """ Initialises the class. """
        self.total_time_before = 0
        self.file_number = 1

    def file_explorer(self, choice):
        """ Lets the user chose files to analyze. """
        match choice:
            case "file":
                while True:
                    file_list = fd.askopenfilenames(title='Choose one or multiple BLF files')
                    if all(file.lower().endswith('.blf') for file in file_list):
                        if file_list == "":
                            return False
                        return file_list
                    else:
                        print("One or more files is not a blf type file, try again.")

            case "folder":
                while True:
                    folder_list = fd.askdirectory(title="Choose one or more folders containing BLF files")
                    file_list = []
                    for root, dirs, files in os.walk(folder_list):
                        for file in files:
                            file_list.append(os.path.join(root,file))

                    if all(file.lower().endswith('.blf') for file in file_list):
                        return file_list
                    else:
                        print("One or more files in directory is not blf file type, try again.")

            case "extract LEM":
                while True:
                    folder_list = []
                    folder_list.append(fd.askdirectory(title="Choose one or more folders containing BLF files"))
                    file_list = []
                    while True:
                        for dir in folder_list:
                            for root, dirs, files in os.walk(dir):
                                root = root.replace("\\", "/")
                                for file in files:
                                    search_path = root + "/" + file
                                    if search_path.endswith(".blf"):
                                        with open(search_path, 'rb') as f:
                                            channel_get_blf = can.BLFReader(f)
                                            for msg in channel_get_blf:
                                                if 10 == msg.channel:
                                                    file_list.append(os.path.join(search_path))
                                                    break
                                                else:
                                                    break
                                        f.close()
                        return file_list
        

    def blf_to_df(self, file_list):
        """ Write to df from blf.\n\n
            file_list - The blf file(s) being read from. """
        
        # Checks if there's only blf files in the list.
        if not all(file.lower().endswith('.blf') for file in file_list):
            raise TypeError("Only .blf files are supported to read from.")
        
        channel = None
        df = None
        for index, file in enumerate(file_list):
            print(f"\nFile #{self.file_number}:")
            self.file_number += 1

            # Gets the channel on the CANbus.
            with open(file, 'rb') as f:
                channel_get_blf = can.BLFReader(f)
                for msg in channel_get_blf:
                    channel = msg.channel
                    break
            f.close()

            # Checks what CANbus and calls corresponding function to prep it.
            if channel == 10:
                blf_data, channel = self.LEM_prep(file, index, channel)
            else:
                blf_data, channel = self.BL_prep(file, index, channel)
            
            # Loads data into pandas dataframe.
            temp = pd.DataFrame(blf_data)
            if index == 0:
                df = temp
            else:
                df = pd.concat([df, temp], axis=0)
            
        return df, channel
    

    def LEM_prep(self, file, index, channel):
        """ If the file contains the LEM bus this will load in the data to the dataframe. """
        blf_data = {"Time": [], "Current": []}
        # Opens blf file to be read.
        with open(file, 'rb') as e:
            blf_return = can.BLFReader(e)
            percent = 100 / blf_return.object_count
            status = 0
            last_print = 0
            for i, msg in enumerate(blf_return):
                status += percent
                data = msg.data

                # Preps and reads out the current value.
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
                
                # Stores wanted data.
                blf_data["Time"].append(msg.timestamp)
                blf_data["Current"].append(current_dec)

                # Prints the loading status in percentage.
                rounded_status = round(status)
                if rounded_status != last_print and rounded_status > last_print + 9:
                    print(f"{rounded_status}%")
                    last_print = rounded_status

        return blf_data, channel


    def BL_prep(self, file, index, channel):
        """ If the file don't contain the LEM bus this will load in the data to the dataframe. """
        blf_data = {"Time": [], "Busload": []}
        # Opens blf file to be read.
        with open(file, 'rb') as e:
            blf_return = can.BLFReader(e)

            blf_data["Busload"].append(0)

            total_time = round(blf_return.stop_timestamp - blf_return.start_timestamp)+1
            blf_data["Time"] = np.arange(self.total_time_before, self.total_time_before + total_time)
            self.total_time_before += total_time-1

            percent = 100 / blf_return.object_count
            status = 0
            last_print = 0
            count = 0
            sample_count = 1

            for i, msg in enumerate(blf_return):
                status += percent

                # Get the busload every second in percentage. It's not totaly accurate but the margin of error is about 1%.
                if msg.timestamp >= blf_return.start_timestamp + sample_count or i == blf_return.object_count-1:
                    blf_data["Busload"].append((count/4219)*100)
                    count = 0
                    sample_count += 1
                count += 1

                # Prints the loading status in percentage.
                if round(status) != last_print:
                    print(f"{round(status)}%")
                    last_print = round(status)

        return blf_data, channel


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