import os
from tkinter import *
import tkinter.filedialog as fd
import can
import pandas as pd
import numpy as np


class FilesPreparation:
    """ Preps the files before displaying them. """

    def __init__(self):
        """ Initialises the class. """
        self.total_time_before = 0
        self.file_number = 1
        self.plots = []
        self.dfs = None
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
        

    def blf_to_df(self, file_list, start_file_count, LEM_graph, BL_graph):
        """ Write to df from blf. """
        """ file_list - The blf file(s) being read from. """
        
        # Checks if there's only blf files in the list.
        if not all(file.lower().endswith('.blf') or file.lower().endswith(".asc") for file in file_list):
            raise TypeError("Only .blf & .asc files supported.")
        
        # Prints the file that is loading.
        if start_file_count:
            self.file_number = 1
        channel = None
        df = None
        dfs = []
        for index, file in enumerate(file_list):
            print(f"\nLoding File #{self.file_number}:",
                   "\n0%", end="\r")
            self.file_number += 1

            # Gets the channel on the CANbus.
            channel_get = None
            file_mode = None
            if file.endswith(".blf"):
                file_mode = "rb"
            elif file.endswith(".asc"):
                file_mode = "r"
            with open(file, file_mode) as f:
                if file.endswith(".blf"):
                    channel_get = can.BLFReader(f)
                elif file.endswith(".asc"):
                    channel_get = can.ASCReader(f)
                for msg in channel_get:
                    channel = msg.channel
                    break
            f.close()

            # Checks what CANbus and calls corresponding function to prep it.
            # Second layer of if-statements check if LEM or BL-graph are selected in the settings.
            if channel == 0 or channel == 1 or channel == 10 or channel == 23 or channel == 24 or channel == 25 or channel == 26:
                if LEM_graph:
                    blf_asc_datas = self.LEM_prep(file)
            else:
                if BL_graph:
                    blf_asc_datas, channel = self.BL_prep(file, index, channel)
            
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
        # HOPEFULLY THIS RETURNS MULTIPLE DFS WHEN IT'S ASCII. ASLO HOPE IT CONCATS TO CORRECT DF IN DFS!!!!!!!!    
        return dfs
    

    def file_mode_chooser(self, file):
        if file.endswith(".blf"):
            return "rb"
        elif file.endswith(".asc"):
            return "r"


    def get_percent_and_data(self, file):
        name = file.name
        if name.endswith(".blf"):
            data_return = can.BLFReader(file)
            percent = 100 / data_return.object_count
        elif name.endswith(".asc"):
            count = 0
            for line in file:
                if line.strip() and not line.startswith(';'):  # Ignore empty lines or comments
                    count += 1
            # ONLY TO SKIP FOR DEBUG!!!!!!!!!!!!!!!
            # count = 13998668
            percent = 100 / count
        return percent
    

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


    def create_new_directory_for_new_channel(self, channel):
        blf_asc_data = {"Data": {"Time": [], "Current": []},
                        "Info": {"Channel": channel}}
        return blf_asc_data

    def LEM_prep(self, file):
        """ If the file contains the LEM bus this will load in the data to the dataframe. """
        blf_asc_datas = []
        # Opens blf file to be read.
        file_mode = self.file_mode_chooser(file)

        with open(file, file_mode) as f:
            data_return = None
            percent = None
            progress = 0
            last_print = 0
            known_channels = []
            percent = self.get_percent_and_data(f)
            data_return = can.ASCReader(file)

            for i, msg in enumerate(data_return):
                msg_channel = msg.channel

                if msg_channel not in known_channels:
                    blf_asc_datas.append(self.create_new_directory_for_new_channel(msg_channel))
                    known_channels.append(msg_channel)

                progress += percent
                data = msg.data

                # Preps and reads out the current value.
                current_dec = self.get_dec_value(data)
                
                # Stores wanted data.
                blf_asc_datas[msg_channel]["Data"]["Time"].append(msg.timestamp)
                blf_asc_datas[msg_channel]["Data"]["Current"].append(current_dec)

                # Prints the loading status in percentage.
                last_print = self.progress_print(progress, last_print)

                # ONLY FOR DEBUGGING!!!!
                if i > 2000:
                    break

            print("Done ✔")

        return blf_asc_datas
    

    def progress_print(self, progress, last_print):
        rounded_progress = round(progress)
        if rounded_progress != last_print and rounded_progress > last_print + 9:
            print(f"{rounded_progress}%", end="\r")
            last_print = rounded_progress
        return last_print


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
                rounded_status = round(status)
                if rounded_status != last_print and rounded_status > last_print + 9:
                    print(f"{rounded_status}%")
                    last_print = rounded_status

        return blf_data, channel


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
        self.plots = []
        self.initalize_and_reset_bus_channel_indexes()
        LEM_graph, BL_graph = get_graph_toggle_func
        if LEM_graph == False and BL_graph == False:
            self.show_warning("Choose a graph in settings")
            return
        self.plot_line_name = None
        start_file_count = True
        # Loops through every list of files in every line plot.
        for i, frame in enumerate(plot_line_frames):
            blf_files = []
            for path in frame.file_path_array:
                blf_files.append(path.get())

            # Gets the name for the line plot.
            self.plot_line_name = frame.line_plot_name_entry.get()
            # Gets the dataframe and the channel of the dataframe.
            self.dfs = self.blf_to_df(blf_files, start_file_count, LEM_graph, BL_graph)
            start_file_count = False
            self.dfs = self.check_name(self.dfs, self.plot_line_name)
            
            for df in self.dfs:
                df["Info"]["First_df"] = False
                df["Info"]["Last_df"] = False
                df["Info"]["Skip"] = False
                df["Info"]["LEM_graph"] = LEM_graph
                df["Info"]["BL_graph"] = BL_graph
                df["Info"]["LEM_invert"] = frame.invert_LEM.get()

            # Checks if it's the first or/and last dataframe.
            # OSÄKER PÅ DEM HÄR!!!!
            if i == 0:
                self.dfs[0]["Info"]["First_df"] = True
            if len(plot_line_frames)-1 == i:
                self.dfs[-1]["Info"]["Last_df"] = True
            
            # Packs up the info about the dataframe and sends it for time removal.
            # plot_info = {"Dfs":dfs,
            #             "Name":self.plot_line_name,
            #             "First":first_dfs,
            #             "Last":last_dfs,
            #             "LEM":isLEM,
            #             "BL":isBL,
            #             "Skip":skip,
            #             "LEM_graph":LEM_graph,
            #             "BL_graph":BL_graph,
            #             "LEM_invert":LEM_invert}
            # self.plots.append(plot_info)
        return self.dfs


    def check_name(self, dfs, line_plot_name):
        """ Checks if there was a name given and if there was none it get an automated one.
            Checks if the dataframe is a LEM file or BusLoad file. """
        for df in dfs:
            channel = df["Info"]["Channel"]
            if line_plot_name == "":
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
                 df["Info"]["Name"] = line_plot_name

            if channel == 0 or channel == 10 or channel == 23 or channel == 24 or channel == 25 or channel == 26:
                df["Info"]["isLEM"] = True
            else:
                df["Info"]["isLEM"] = False
            if channel == 2 or channel == 6 or channel == 7 or channel == 8 or channel == 9:
                df["Info"]["isBL"] = True
            else:
                df["Info"]["isBL"] = False

        return dfs