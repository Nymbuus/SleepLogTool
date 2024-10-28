import os
from tkinter import *
import tkinter.filedialog as fd
import can
import pandas as pd
import numpy as np


class FilesPreparation:
    """ Preps the files before displaying them. """

    def __init__(self, show_warning_func):
        """ Initialises the class. """
        self.show_warning = show_warning_func
        self.total_time_before = 0
        self.file_number = 1
        self.initalize_and_reset_bus_channel_indexes()
    

    def initalize_and_reset_bus_channel_indexes(self):
        self.index_body = 1
        self.index_front1 = 1
        self.index_front3 = 1
        self.index_mid1 = 1
        self.index_rear1 = 1
        self.index_LEM = 1
        self.index_unknown = 1


    def file_explorer(self, choice):
        """ Lets the user chose files to analyze. """
        # Checks what button the user pressed to act accordingly.
        match choice:
            # If Choose file(s) was chosen.
            case "file":
                # Will ask the user to chose file(s). If user cancel out it will stop.
                while True:
                    file_list = fd.askopenfilenames(title='Choose one or more blf/asc files')
                    if all(file.lower().endswith('.blf') or file.lower().endswith(".asc") for file in file_list):
                        if file_list == "":
                            return False
                        return file_list
                    else:
                        print("Files are not blf or asc file, try again.")

            # If Choose folder(s) was chosen.
            case "folder":
                # Will ask the user to chose folder(s). If user cancel out it will stop.
                while True:
                    folder_list = fd.askdirectory(title="Choose one or more folders with blf/asc files")
                    file_list = []
                    for root, dirs, files in os.walk(folder_list):
                        for file in files:
                            file_list.append(os.path.join(root,file))

                    if all(file.lower().endswith('.blf') for file in file_list):
                        return file_list
                    else:
                        print("File(s) in director(ies) are not blf/asc files, try again.")

            # If Extract LEM(s) was chosen.
            case "extract LEM":
                while True:
                    file_list = []
                    folder_list = []
                    folder_list.append(fd.askdirectory(title="Choose one or more folders with blf/asc files"))
                    # Takes the folder(s) chosen and loops through every folder until there is no more.
                    # Will only extract LEM files on it's way.
                    while True:
                        # Loops through folder(s) chosen by user.
                        for dir in folder_list:
                            # Loops through the folder and looks upp root path, directory (which I don't use here) and files.
                            for root, dirs, files in os.walk(dir):
                                root = root.replace("\\", "/")
                                # Loops through all files and creates search path to file.
                                for file in files:
                                    search_path = root + "/" + file
                                    if search_path.endswith(".blf") or search_path.endswith(".asc"):
                                        # Checks if the file is a LEM file and if so, adds it the the file list.
                                        with open(search_path, 'rb') as f:
                                            channel_get_blf = can.BLFReader(f)
                                            for msg in channel_get_blf:
                                                if msg.channel == 0 or 10 == msg.channel or 23 == msg.channel or 24 == msg.channel or 25 == msg.channel or 26 == msg.channel:
                                                    file_list.append(os.path.join(search_path))
                                                    break
                                                else:
                                                    break
                                        f.close()
                        return file_list
        

    def blf_to_df(self, file_list, LEM_graph, BL_graph):
        """ Write to df from blf. """
        """ file_list - The blf file(s) being read from. """
        
        # Checks if there's only blf/asc files in the list.
        if not all(file.lower().endswith('.blf') or file.lower().endswith(".asc") for file in file_list):
            raise TypeError("Only .blf & .asc files supported.")

        channel = None
        df = None
        dfs = []
        time_add = 0
        for index, file in enumerate(file_list):
            print(f"\nLoding File #{self.file_number}:",
                   "\n0%", end="\r")
            self.file_number += 1

            # Gets the can bus channel.
            mode = "rb" if file.endswith(".blf") else "r"
            with open(file, mode) as f:
                channel_get = can.BLFReader(f) if file.endswith(".blf") else can.ASCReader(f)
                for msg in channel_get:
                    channel = msg.channel
                    break

            # Checks what CANbus and calls corresponding function to prep it.
            # Also checks if LEM or BL-graph are selected in the settings.
            if ((channel == 0 or
                 channel == 1 or
                 channel == 10 or
                 channel == 23 or 
                 channel == 24 or 
                 channel == 25 or 
                 channel == 26)
                 and LEM_graph):
                blf_asc_datas = self.LEM_prep(file, mode, time_add)
            elif BL_graph:
                blf_asc_datas = self.BL_prep(file, mode)
            
            # Loads data into pandas dataframe.
            for j, blf_asc_data in enumerate(blf_asc_datas):
                data = blf_asc_data["Data"]

                temp = pd.DataFrame(data)
                if index == 0:
                    df = temp
                    df = {"df": df, "Info": blf_asc_data["Info"]}
                    dfs.append(df)
                else:
                    dfs[j]["df"] = pd.concat([dfs[j]["df"], temp], axis=0)
            time_add = dfs[0]["df"]["Time"].iloc[-1]
        return dfs
    

    def file_mode_chooser(self, file):
        if file.endswith(".blf"):
            return "rb"
        elif file.endswith(".asc"):
            return "r"


    def get_percent_and_data(self, file):
        name = file.name
        data_return = None
        percent = None
        if name.endswith(".blf"):
            data_return = can.BLFReader(file)
            percent = 100 / data_return.object_count
        elif name.endswith(".asc"):
            count = 0
            for line in file:
                if line.strip() and not line.startswith(';'):  # Ignore empty lines or comments
                    count += 1
            percent = 100 / count

            # ONLY TO SKIP FOR DEBUG!!!!!!!!!!!!!!!
            # count = 13998668

            file.seek(0)
            data_return = can.ASCReader(file)
        return percent, data_return
    

    def get_dec_value(self, data):
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
        return current_dec


    def create_new_directory_for_new_channel(self, channel, lem_or_bl, timestamps=None):
        if lem_or_bl == "lem":
            blf_asc_data = {"Data": {"Time": [], "Current": []},
                            "Info": {"Channel": channel}}
        elif lem_or_bl == "bl":
            blf_asc_data = {"Data": {"Time": timestamps, "Busload": [0]},
                            "Info": {"Channel": channel}}
        return blf_asc_data

    def LEM_prep(self, file, mode, time_add):
        """ If the file contains the LEM bus this will load in the data to the dataframe. """
        blf_asc_datas = []
        # Opens blf file to be read.

        with open(file, mode) as f:
            data_return = None
            percent = None
            progress = 0
            last_print = 0
            known_channels = []
            percent, data_return = self.get_percent_and_data(f)

            # Vill inte läsa filen av någon anledning!!!!!!!!!!!!!!!
            for msg in data_return:
                msg_channel = msg.channel

                if msg_channel not in known_channels:
                    blf_asc_datas.append(self.create_new_directory_for_new_channel(msg_channel, "lem"))
                    known_channels.append(msg_channel)

                progress += percent
                data = msg.data

                # Preps and reads out the current value.
                current_dec = self.get_dec_value(data)
                
                # Stores wanted data.
                for blf_asc_data in blf_asc_datas:
                    if blf_asc_data["Info"]["Channel"] == msg.channel:
                        blf_asc_data["Data"]["Time"].append(msg.timestamp+time_add)
                        blf_asc_data["Data"]["Current"].append(current_dec)

                # Prints the loading status in percentage.
                last_print = self.progress_print(progress, last_print)

            print("Done ✔")

        return blf_asc_datas
    

    def progress_print(self, progress, last_print):
        rounded_progress = round(progress)
        if rounded_progress != last_print and rounded_progress > last_print + 9:
            print(f"{rounded_progress}%", end="\r")
            last_print = rounded_progress
        return last_print


    def BL_prep(self, file, mode):
        """ If the file don't contain the LEM bus this will load in the data to the dataframe. """
        blf_asc_datas = []
        # Opens blf file to be read.
        with open(file, mode) as f:
            progress = 0
            last_print = 0
            count = 0
            sample_count = 1
            zeros = 0
            zero_event = 0
            known_channels = []
            percent, data_return = self.get_percent_and_data(f)

            total_time = round(data_return.stop_timestamp - data_return.start_timestamp)+1
            timestamps = np.arange(self.total_time_before, self.total_time_before + total_time)
            self.total_time_before += total_time-1

            for i, msg in enumerate(data_return):
                msg_channel = msg.channel

                if msg_channel not in known_channels:
                    blf_asc_datas.append(self.create_new_directory_for_new_channel(msg_channel, "bl", timestamps))
                    known_channels.append(msg_channel)
                progress += percent

                # Get the busload every second in percentage. It's not totaly accurate but the margin of error is around 1%.
                if msg.timestamp >= data_return.start_timestamp + sample_count:
                    # If there hasn't been a single message over a second then this part will fill in the data points up until the timestamp with zeros.
                    # Else it will add the datapoints every second with the busload percentage.
                    if msg.timestamp - (data_return.start_timestamp + sample_count) > 1:
                        zero_event += 1
                        zeros = round(msg.timestamp - data_return.start_timestamp) - (len(blf_asc_datas[0]["Data"]["Busload"])-1)
                        sample_count += zeros
                        for _ in range(zeros):
                            blf_asc_datas[0]["Data"]["Busload"].append(0)
                    else:
                        blf_asc_datas[0]["Data"]["Busload"].append((count/4219)*100)
                        sample_count += 1
                    count = 0
                count += 1

                # Prints the loading status in percentage.
                last_print = self.progress_print(progress, last_print)
            # Checks if it needs to add one more data point or not.
            if len(blf_asc_datas[0]["Data"]["Time"]) > len(blf_asc_datas[0]["Data"]["Busload"]):
                blf_asc_datas[0]["Data"]["Busload"].append((count/4219)*100)
            print("Done ✔")

        return blf_asc_datas


    def remove_time(self, df, remove_start_time, remove_end_time):
        """ Loads pandas dataframe to a local variable.
            With this we remove the start and end elements provided in minutes.
            If the if cases is'nt used the program will crash. """
        if not (isinstance(remove_start_time, int) or isinstance(remove_start_time, float)):
            raise TypeError("remove_start_time variable was not a integer or float!")
        if not (isinstance(remove_end_time, int) or isinstance(remove_end_time, float)):
            raise TypeError("remove_end_time variable was not a integer or float!")
        
        if remove_start_time != 0:
            df = df["df"][int(remove_start_time):]
        if remove_end_time != 0:
            df = df["df"][:-int(remove_end_time)]

        return df
    

    def analyze_data(self, get_graph_toggle_func, plot_line_frames):
        """ Takes the present filepaths and analyzes the data in the blf files. """
        self.dfs = []
        self.file_number = 1
        self.initalize_and_reset_bus_channel_indexes()
        LEM_graph, BL_graph = get_graph_toggle_func
        if LEM_graph == False and BL_graph == False:
            self.show_warning("Choose a graph in settings")
            return

        # Loops through every list of files in every line plot.
        for frame in plot_line_frames:
            blf_files = []
            for path in frame.file_path_array:
                blf_files.append(path.get())

            # Gets the dataframe and the channel of the dataframe.
            dfs = self.blf_to_df(blf_files, LEM_graph, BL_graph)
            dfs = self.check_name(dfs, frame)
            for df in dfs:
                self.dfs.append(df)
        
        for df in self.dfs:
            df["Info"]["First_df"] = False
            df["Info"]["Last_df"] = False
            df["Info"]["Skip"] = False
            df["Info"]["LEM_graph"] = LEM_graph
            df["Info"]["BL_graph"] = BL_graph
            df["Info"]["LEM_invert"] = frame.invert_LEM.get()

        # Checks if it's the first or/and last dataframe.
        self.dfs[0]["Info"]["First_df"] = True
        self.dfs[-1]["Info"]["Last_df"] = True
        return self.dfs


    def check_name(self, dfs, plot_line_frame):
        """ Checks if there was a name given and if there was none it get an automated one.
            Checks if the dataframe is a LEM file or BusLoad file. """
        for i, df in enumerate(dfs):
            plot_name = plot_line_frame.line_plot_name_entry.get()
            channel = df["Info"]["Channel"]
            if plot_name == "":
                match channel:
                    case 2:
                        df["Info"]["Name"] = f"Body #{self.index_body}"
                        self.index_body += 1
                    case 6:
                        df["Info"]["Name"] = f"Front1 #{self.index_front1}"
                        self.index_front1 += 1
                    case 7:
                        df["Info"]["Name"] = f"Front3 #{self.index_front3}"
                        self.index_front3 += 1
                    case 8:
                        df["Info"]["Name"] = f"Mid1 #{self.index_mid1}"
                        self.index_mid1 += 1
                    case 9:
                        df["Info"]["Name"] = f"Rear1 #{self.index_rear1}"
                        self.index_rear1 += 1
                    case 0:
                        df["Info"]["Name"] = f"LEM #{self.index_LEM}"
                        self.index_LEM += 1
                    case 1:
                        df["Info"]["Name"] = f"LEM #{self.index_LEM}"
                        self.index_LEM += 1
                    case 10:
                        df["Info"]["Name"] = f"LEM #{self.index_LEM}"
                        self.index_LEM += 1
                    case 23:
                        df["Info"]["Name"] = f"LEM #{self.index_LEM}"
                        self.index_LEM += 1
                    case 24:
                        df["Info"]["Name"] = f"LEM #{self.index_LEM}"
                        self.index_LEM += 1
                    case 25:
                        df["Info"]["Name"] = f"LEM #{self.index_LEM}"
                        self.index_LEM += 1
                    case 26:
                        df["Info"]["Name"] = f"LEM #{self.index_LEM}"
                        self.index_LEM += 1
                    case _:
                        df["Info"]["Name"] = f"Unknown Bus #{self.index_unknown}"
                        self.index_unknown += 1
            else:
                 df["Info"]["Name"] = plot_name

            if channel == 0 or channel == 1 or channel == 10 or channel == 23 or channel == 24 or channel == 25 or channel == 26:
                df["Info"]["isLEM"] = True
            else:
                df["Info"]["isLEM"] = False
            if channel == 2 or channel == 6 or channel == 7 or channel == 8 or channel == 9:
                df["Info"]["isBL"] = True
            else:
                df["Info"]["isBL"] = False

        return dfs