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
                    file_list = fd.askopenfilenames(title='Choose one or multiple BLF files')
                    if all(file.lower().endswith('.blf') for file in file_list):
                        if file_list == "":
                            return False
                        return file_list
                    else:
                        print("One or more files is not a blf type file, try again.")

            # If Choose folder(s) was chosen.
            case "folder":
                # Will ask the user to chose folder(s). If user cancel out it will stop.
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

            # If Extract LEM(s) was chosen.
            case "extract LEM":
                while True:
                    file_list = []
                    folder_list = []
                    folder_list.append(fd.askdirectory(title="Choose one or more folders containing BLF files"))
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
                                    if search_path.endswith(".blf"):
                                        # Checks if the file is a LEM file and if so, adds it the the file list.
                                        with open(search_path, 'rb') as f:
                                            channel_get_blf = can.BLFReader(f)
                                            for msg in channel_get_blf:
                                                if 10 == msg.channel or 23 == msg.channel or 24 == msg.channel or 25 == msg.channel or 26 == msg.channel:
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
        if not all(file.lower().endswith('.blf') for file in file_list):
            raise TypeError("Only .blf files are supported to read from.")
        
        # Prints the file that is loading.
        if start_file_count:
            self.file_number = 1
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
            # Second layer of if-statements check if LEM or BL-graph are selected in the settings.
            if channel == 10 or channel == 23 or channel == 24 or channel == 25 or channel == 26:
                if LEM_graph:
                    blf_data, channel = self.LEM_prep(file, index, channel)
            else:
                if BL_graph:
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
                rounded_status = round(status)
                if rounded_status != last_print and rounded_status > last_print + 9:
                    print(f"{rounded_status}%")
                    last_print = rounded_status

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
    

    def analyze_data(self, get_graph_toggle_func, plot_line_frames):
        """ Takes the present filepaths and analyzes the data in the blf files. """
        self.plots = []
        self.initalize_and_reset_bus_channel_indexes()
        LEM_graph, BL_graph = get_graph_toggle_func
        if LEM_graph == False and BL_graph == False:
            self.show_warning("Choose a graph in settings")
            return
        last_dfs = False
        dfs = None
        self.plot_line_name = None
        start_file_count = True
        # Loops through every list of files in every line plot.
        for i, frame in enumerate(plot_line_frames):
            blf_files = []
            for path in frame.file_path_array:
                first_dfs = False
                skip = False
                isLEM = False
                isBL = False
                blf_files.append(path.get())

            # Gets the name for the line plot.
            self.plot_line_name = frame.line_plot_name_entry.get()
            # Gets the dataframe and the channel of the dataframe.
            dfs, channel = self.blf_to_df(blf_files, start_file_count, LEM_graph, BL_graph)
            start_file_count = False
            self.plot_line_name, isLEM, isBL = self.check_name(channel, self.plot_line_name)

            
            # Checks if it's the first or/and last dataframe.
            if i == 0: first_dfs = True
            if len(plot_line_frames)-1 == i: last_dfs = True

            #if len(frame.file_path_array)-1 == i: last_dfs = True

            LEM_invert = frame.invert_LEM.get()
            
            # Packs up the info about the dataframe and sends it for time removal.
            plot_info = {"Dfs":dfs,
                        "Name":self.plot_line_name,
                        "First":first_dfs,
                        "Last":last_dfs,
                        "LEM":isLEM,
                        "BL":isBL,
                        "Skip":skip,
                        "LEM_graph":LEM_graph,
                        "BL_graph":BL_graph,
                        "LEM_invert":LEM_invert}
            self.plots.append(plot_info)
        return self.plots


    def check_name(self, channel, line_plot_name):
        """ Checks if there was a name given and if there was none it get an automated one.
            Checks if the dataframe is a LEM file or BusLoad file. """
        isLEM = None
        isBL = None
        channel_name = None
        if line_plot_name == "":
            match channel:
                case 2:
                    channel_name = f"Body #{self.index_body}"
                    self.index_body += 1
                case 6:
                    channel_name = f"Front1 #{self.index_front1}"
                    self.index_front1 += 1
                case 7:
                    channel_name = f"Front3 #{self.index_front3}"
                    self.index_front3 += 1
                case 8:
                    channel_name = f"Mid1 #{self.index_mid1}"
                    self.index_mid1 += 1
                case 9:
                    channel_name = f"Rear1 #{self.index_rear1}"
                    self.index_rear1 += 1
                case 10:
                    channel_name = f"LEM #{self.index_LEM}"
                    self.index_LEM += 1
                case 23:
                    channel_name = f"LEM #{self.index_LEM}"
                    self.index_LEM += 1
                case 24:
                    channel_name = f"LEM #{self.index_LEM}"
                    self.index_LEM += 1
                case 25:
                    channel_name = f"LEM #{self.index_LEM}"
                    self.index_LEM += 1
                case 26:
                    channel_name = f"LEM #{self.index_LEM}"
                    self.index_LEM += 1
                case _:
                    channel_name = f"Unknown Bus #{self.index_unknown}"
                    self.index_unknown += 1
        else:
            channel_name = line_plot_name


        if channel == 10 or channel == 23 or channel == 24 or channel == 25 or channel == 26:
            isLEM = True
        if channel == 2 or channel == 6 or channel == 7 or channel == 8 or channel == 9:
            isBL = True

        return channel_name, isLEM, isBL