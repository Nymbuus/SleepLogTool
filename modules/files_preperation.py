""" Tkinter for GUI, Can for handeling can bus singals.
    Pandas and Numpy for handeling data in an efficient way. """
import os
import tkinter.filedialog as fd
import can
import pandas as pd
import numpy as np

BLF_LEM_CHANNELS = (10, 23, 24, 25, 26, 28)
ASC_LEM_CHANNELS = (0, 1)
BLF_BL_CHANNELS = (2, 6, 7, 8, 9)
ALL_BLF_CHANNELS = BLF_LEM_CHANNELS + BLF_BL_CHANNELS

class FilesPreparation:
    """ Preps the files before displaying them. """

    def __init__(self, show_warning_func, plot_line_frames):
        """ Initialises the class. """
        self.show_warning = show_warning_func
        self.plot_line_frames = plot_line_frames
        self.total_time_before = 0
        self.file_number = 1
        self.dfs = []
        self.data_count = 0
        self.no_neg_values = False
        self.initalize_and_reset_bus_channel_indexes()


    def initalize_and_reset_bus_channel_indexes(self):
        """ Initializes the indexes for the bus names number. """
        self.index_body = 1
        self.index_front1 = 1
        self.index_front3 = 1
        self.index_mid1 = 1
        self.index_rear1 = 1
        self.index_lem = 1
        self.index_unknown = 1


    def file_explorer(self, choice, buses=None):
        """ Lets the user chose files to analyze. """
        # Checks what button the user pressed to act accordingly.
        file_list = None
        while True:
            if choice == "file":
                # Will ask the user to chose file(s). If user cancel out it will stop.
                file_list = self.open_file_source("Choose one or more blf/asc files")

            # If Extract Bus was chosen.
            elif choice == "extract bus":
                file_list = self.open_file_source("Choose folder(s) with blf/asc files", buses)

            if file_list == None:
                return
            elif file_list:
                return file_list


    def open_file_source(self, text, buses=None):
        if text == "Choose one or more blf/asc files":
            file_list = fd.askopenfilenames(title=text)
            if file_list == "":
                print("No files were selected.")
                return
            elif self.check_accepted_files(file_list):
                return file_list
            else:
                return False
        elif text == "Choose folder(s) with blf/asc files":
            dir_list = []
            dir_list.append(fd.askdirectory(title=text))
            if dir_list == "":
                print("No folders were selected.")
                return
            file_list = self.get_files(dir_list)
            if self.check_accepted_files(file_list):
                file_list = self.bus_sorter(file_list, buses)
                return file_list
            else:
                return False


    def check_accepted_files(self, file_list):
        if all(file.lower().endswith((".blf", ".asc")) and
               ("Front2" not in file and "Backbone" not in file)
               for file in file_list):
            return file_list
        elif all("Front2" in file or "Backbone" in file
                 for file in file_list):
            self.show_warning("Not accepted bus (Front2 or Backbone)")
            return False
        else:
            self.show_warning("Files not blf/asc, try again")
            return False                


    def get_files(self, dir_list):
        file_list = []
        for dir_ in list(dir_list):
            # Loops through the folder and looks up root path and files.
            for root, _, files in os.walk(dir_):
                root = root.replace("\\", "/")
                # Loops through all files and creates search path to file.
                for file in files:
                    file = root + "/" + file
                    if (file.lower().endswith((".blf", ".asc")) and
                       ("Front2" not in file and "Backbone" not in file)):
                        file_list.append(file)
        return file_list


    def bus_sorter(self, file_list, buses):
        # Takes the folder(s) chosen and loops through every folder.
        # Will extract chosen bus files on it's way.
        # Loops through folder(s) chosen by user.
        bus_sort_list = {"Lem":[],
                         "Body":[],
                         "Front1":[],
                         "Front3":[],
                         "Mid1":[],
                         "Rear1":[],
                         "Multi":[]}

        for file in file_list:
            # Checks if it's a LEM file and adds it to the file list.
            file_gen = self.yield_message(file)
            known_channels = []
            for msg in file_gen:
                if msg.channel not in known_channels:
                    known_channels.append(msg.channel)
            if len(known_channels) > 1:
                if (file.endswith(".blf") and
                    all(channel in ALL_BLF_CHANNELS for channel in known_channels)):
                    if "Multi" in buses:
                        bus_sort_list["Multi"].append(os.path.join(file))
                    continue

            # Checks if Lem is chosen in extract buses.
            # Also checks if it's asc or blf.
            # Depending on which one, it compares to LEM channels in that type of file.
            if ((file.endswith(".blf") and known_channels[0] in BLF_LEM_CHANNELS) or
                (file.endswith(".asc") and known_channels[0] in ASC_LEM_CHANNELS)):
                if "Lem" in buses:
                    bus_sort_list["Lem"].append(os.path.join(file))
                else:
                    continue
            # If not Lem it will check the other buses.
            else:
                match known_channels[0]:
                    case 2:
                        if "Body" in buses:
                            bus_sort_list["Body"].append(os.path.join(file))
                    case 6:
                        if "Front1" in buses:
                            bus_sort_list["Front1"].append(os.path.join(file))
                    case 7:
                        if "Front3" in buses:
                            bus_sort_list["Front3"].append(os.path.join(file))
                    case 8:
                        if "Mid1" in buses:
                            bus_sort_list["Mid1"].append(os.path.join(file))
                    case 9:
                        if "Rear1" in buses:
                            bus_sort_list["Rear1"].append(os.path.join(file))
                    case _:
                        print("Unknown bus")
        return bus_sort_list


    def yield_message(self, file):
        """ Creates a file generator to yield the messages in it. """
        mode = "rb" if file.endswith(".blf") else "r"
        with open(file, mode) as f:
            open_file = can.BLFReader(f) if file.endswith(".blf") else can.ASCReader(f)
            yield from open_file


    def get_attribute(self, file, attribute):
        """ Gets the specified attributed asked for. """
        mode = "rb" if file.endswith(".blf") else "r"
        with open(file, mode) as f:
            open_file = can.BLFReader(f) if file.endswith(".blf") else can.ASCReader(f)
            return getattr(open_file, attribute)


    def convert_to_df(self, file_list, lem_graph, bl_graph, invert_lem):
        """ Write to df from blf/asc.
            file_list - The blf/asc file(s) being read from. """

        # Checks if there's only blf/asc files in the list.
        if self.check_accepted_files(file_list):
            msg_channel = None
            df = None
            dfs = []
            time_add = 0
            for index, file in enumerate(file_list):
                blf_asc_datas = []
                known_channels = []
                known_arbitration_ids = []
                print(f"\nLoding File #{self.file_number}:",
                    "\n0%", end="\r")
                self.file_number += 1
                start_time = self.get_attribute(file, "start_timestamp")
                stop_time = self.get_attribute(file, "stop_timestamp")
                total_time = round(stop_time - start_time+1)

                file_gen = self.yield_message(file)
                for msg in file_gen:
                    msg_channel = msg.channel
                    if msg_channel not in known_channels:
                        arbitration_id = msg.arbitration_id
                        if file.endswith(".blf"):
                            if msg_channel in BLF_BL_CHANNELS:
                                timestamps = np.arange(self.total_time_before,
                                                       self.total_time_before + total_time)
                                blf_asc_datas.append(self.create_new_directory_for_new_channel(channel=msg_channel,
                                                                                               lem_or_bl="bl",
                                                                                               file_type=".blf",
                                                                                               timestamps=timestamps))
                            elif msg_channel in BLF_LEM_CHANNELS:
                                blf_asc_datas.append(self.create_new_directory_for_new_channel(channel=msg_channel,
                                                                                               lem_or_bl="lem",
                                                                                               file_type=".blf"))
                        elif file.endswith(".asc"):
                            # Checks what graph is selected by the user.
                            if msg_channel in ASC_LEM_CHANNELS:
                                if arbitration_id not in known_arbitration_ids:
                                    blf_asc_datas.append(self.create_new_directory_for_new_channel(channel=msg_channel,
                                                                                                   lem_or_bl="lem",
                                                                                                   file_type=".asc",
                                                                                                   arbitration_id=arbitration_id))
                                    known_arbitration_ids.append(arbitration_id)
                        known_channels.append(msg_channel)

                    for blf_asc_data in blf_asc_datas:
                        if blf_asc_data["Info"]["Channel"] == msg_channel:
                            if blf_asc_data["Info"]["arbitration_id"]:
                                if blf_asc_data["Info"]["arbitration_id"] == arbitration_id:
                                    blf_asc_data["Msgs"].append(msg)
                            else:
                                blf_asc_data["Msgs"].append(msg)



                # Checks file and calls corresponding function to prep it.
                # Checks if file is .blf or .asc.
                # Checks what graph is selected by the user.
                for blf_asc_data in blf_asc_datas:
                    if blf_asc_data["Info"]["File_type"] == ".blf":
                        if ((blf_asc_data["Info"]["Bus_type"] == "lem") and lem_graph):
                            blf_asc_data = self.lem_prep(blf_asc_data, time_add, invert_lem)
                        elif ((blf_asc_data["Info"]["Bus_type"] == "bl") and bl_graph):
                            blf_asc_data = self.bl_prep(blf_asc_data, start_time, total_time)
                        else:
                            raise ValueError("Neither LEM or BL graph was selected. Please select one!")

                    elif blf_asc_data["Info"]["File_type"] == ".asc":
                        if ((blf_asc_data["Info"]["Bus_type"] == "lem") and lem_graph):
                            blf_asc_data = self.lem_prep(blf_asc_data, time_add, invert_lem)
                        else:
                            raise ValueError("LEM graph wasn't selected. Please select it!")
                    else:
                        raise ValueError(f"Expexted a .blf or .asc file, got {file!r}")


                # Loads data into pandas dataframe.
                # It's a loop since asc files can have multiple channels.
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
        else:
            return


    def get_percent(self, msgs_count):
        """ Gets how many percentage units the progress
            variable in the prep functions should increase with. """
        percent = 100 / msgs_count
        return percent


    def get_dec_value(self, data, invert_lem):
        """ Converts the hex value in the message to decimal. """
        current_dec = 0
        hex1 = hex(data[1])[2:]
        if len(hex1) == 1:
            hex1 = "0"+hex1
        hex2 = hex(data[2])[2:]
        if len(hex2) == 1:
            hex2 = "0"+hex2
        hex3 = hex(data[3])[2:]
        if len(hex3) == 1:
            hex3 = "0"+hex3
        current_dec = int(hex1+hex2+hex3, 16)

        # If byte 0 is less then 128, the number is negative.
        if data[0] < 128:
            current_dec -= 16777216

        # Invert LEM graph if the box is checked.
        if invert_lem:
            current_dec = -current_dec

        # Removes negative values if the box is checked.
        if current_dec < 0 and self.no_neg_values:
            current_dec = 0

        return current_dec


    def create_new_directory_for_new_channel(self,
                                             channel,
                                             lem_or_bl,
                                             file_type,
                                             arbitration_id = None,
                                             timestamps=None):
        """ Creates a new directory for the a new channel, either if it's lem or bl.
            Arbitration is only for LEM. """
        blf_asc_data = None
        if lem_or_bl == "lem":
            blf_asc_data = {"Data": {"Time": [],
                                     "Current": []},
                            "Info": {"Channel": channel,
                                     "Bus_type": lem_or_bl,
                                     "File_type": file_type,
                                     "arbitration_id": arbitration_id},
                            "Msgs": []}
        elif lem_or_bl == "bl":
            blf_asc_data = {"Data": {"Time": timestamps,
                                     "Busload": [0]},
                            "Info": {"Channel": channel,
                                     "Bus_type": lem_or_bl,
                                     "File_type": file_type,
                                     "arbitration_id": arbitration_id},
                            "Msgs": []}
        return blf_asc_data


    def lem_prep(self, blf_asc_data, time_add, invert_lem):
        """ Loads in the data to the dataframe. """
        progress = 0
        last_print = 0
        percent = self.get_percent(len(blf_asc_data["Msgs"]))

        for msg in blf_asc_data["Msgs"]:
            progress += percent
            data = msg.data
            # Preps and reads out the current value.
            current_dec = self.get_dec_value(data, invert_lem)
            # Stores wanted data.
            # Only need time_add for asc files.
            if blf_asc_data["Info"]["File_type"] == ".blf":
                blf_asc_data["Data"]["Time"].append(msg.timestamp)
            elif blf_asc_data["Info"]["File_type"] == ".asc":
                blf_asc_data["Data"]["Time"].append(msg.timestamp+time_add)
            blf_asc_data["Data"]["Current"].append(current_dec)
            # Prints the loading status in percentage.
            last_print = self.progress_print(progress, last_print)
        print("Done ✔")

        return blf_asc_data


    def progress_print(self, progress, last_print):
        """ Checks what percentage was last printed out in console if the progres is 10% more.
            If it is then it's printed to the console. """
        rounded_progress = round(progress)
        if rounded_progress != last_print and rounded_progress > last_print + 9:
            print(f"{rounded_progress}%", end="\r")
            last_print = rounded_progress
        return last_print


    def bl_prep(self, blf_asc_data, start_time, total_time):
        """ Loads in the data to the dataframe. """
        progress = 0
        last_print = 0
        percent = self.get_percent(len(blf_asc_data["Msgs"]))
        self.total_time_before += total_time-1

        # Actually process the messages.
        sample_count = 1
        count = 0
        zeros = 0

        for msg in blf_asc_data["Msgs"]:
            msg_timestamp = msg.timestamp

            progress += percent

            # Gets the busload every second in percentage.
            # It's not totaly accurate but the margin of error is around 1%.
            if msg_timestamp >= start_time + sample_count:
                # If there hasn't been a single message over a second then this part will
                # fill in the data points up until the timestamp with zeros.
                # Else it will add the datapoints every second with the busload percentage.
                if msg_timestamp - (start_time + sample_count) > 1:
                    time_passed = round(msg_timestamp - start_time)
                    len_busload = len(blf_asc_data["Data"]["Busload"])-1
                    zeros = time_passed - len_busload
                    sample_count += zeros
                    for _ in range(zeros):
                        blf_asc_data["Data"]["Busload"].append(0)
                else:
                    blf_asc_data["Data"]["Busload"].append((count/4219)*100)
                    sample_count += 1
                count = 0
            count += 1

            # Prints the loading status in percentage.
            last_print = self.progress_print(progress, last_print)

        # Checks if it needs to add more data points in the end.
        if len(blf_asc_data["Data"]["Time"]) > len(blf_asc_data["Data"]["Busload"]):
            blf_asc_data["Data"]["Busload"].append((count/4219)*100)
            len_busload = len(blf_asc_data["Data"]["Busload"])-1
            zeros = (total_time - 1) - len_busload
            for _ in range(zeros):
                blf_asc_data["Data"]["Busload"].append(0)
        print("Done ✔")

        return blf_asc_data


    def remove_time(self, df, remove_start_time, remove_end_time):
        """ Loads pandas dataframe to a local variable.
            With this we remove the start and end elements provided in minutes.
            If the if cases is'nt used the program will crash. """
        if not (isinstance(remove_start_time, int) or isinstance(remove_start_time, float)):
            raise TypeError("remove_start_time variable was not a integer or float!")
        if not (isinstance(remove_end_time, int) or isinstance(remove_end_time, float)):
            raise TypeError("remove_end_time variable was not a integer or float!")

        if remove_start_time != 0:
            df["df"] = df["df"][int(remove_start_time):]
        if remove_end_time != 0:
            df["df"] = df["df"][:-int(remove_end_time)]

        return df


    def analyze_data(self, get_graph_toggle_func, plot_line_frames):
        """ Takes the present filepaths and analyzes the data in the files. """
        lem_graph, bl_graph, self.no_neg_values = get_graph_toggle_func
        if lem_graph is False and bl_graph is False:
            self.show_warning("Choose a graph in settings")
            return False

        lem_present = False
        bl_present = False
        for frame in plot_line_frames:
            if frame.decide_bus == "LEM":
                lem_present = True
            elif frame.decide_bus != "LEM" and frame.decide_bus is not None:
                bl_present = True

        # Checks if only one of the graph options are selected and if there's matching files for it.
        if lem_present is False and lem_graph is True and bl_graph is False:
            self.show_warning("No LEM files in plotlines. Only LEM graph selected")
            return False
        elif bl_present is False and bl_graph is True and lem_graph is False:
            self.show_warning("No BusLoad files in plotlines. Only BusLoad graph selected")
            return False

        self.dfs = []
        self.file_number = 1
        self.initalize_and_reset_bus_channel_indexes()

        # Loops through every list of files in every line plot.
        for frame in plot_line_frames:
            blf_asc_files = []
            if frame.file_path_array:
                for path in frame.file_path_array:
                    blf_asc_files.append(path.get())

                # Gets the dataframe and the channel of the dataframe.
                invert_lem = frame.invert_lem.get()
                dfs = self.convert_to_df(blf_asc_files, lem_graph, bl_graph, invert_lem)
                dfs = self.check_name(dfs, frame)
                for df in dfs:
                    df["Info"]["First_df"] = False
                    df["Info"]["Last_df"] = False
                    df["Info"]["Skip"] = False
                    df["Info"]["LEM_graph"] = lem_graph
                    df["Info"]["BL_graph"] = bl_graph
                    self.dfs.append(df)

        # Checks if it's the first or/and last dataframe.
        self.dfs[0]["Info"]["First_df"] = True
        self.dfs[-1]["Info"]["Last_df"] = True
        return self.dfs


    def check_name(self, dfs, plot_line_frame):
        """ Checks if there was a name given and if there was none it get an automated one.
            Checks if the dataframe is a LEM file or BusLoad file. """
        for df in dfs:
            plot_name = plot_line_frame.line_plot_name_entry.get()
            channel = df["Info"]["Channel"]
            if plot_name == "":
                if ((df["Info"]["File_type"] == ".blf" and channel in BLF_LEM_CHANNELS) or
                    (df["Info"]["File_type"] == ".asc" and channel in ASC_LEM_CHANNELS)):
                    df["Info"]["Name"] = f"LEM #{self.index_lem}"
                    self.index_lem += 1
                else:
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
                        case _:
                            df["Info"]["Name"] = f"Unknown Bus #{self.index_unknown}"
                            self.index_unknown += 1
            else:
                df["Info"]["Name"] = plot_name

            if ((df["Info"]["File_type"] == ".blf" and channel in BLF_LEM_CHANNELS) or
                (df["Info"]["File_type"] == ".asc" and channel in ASC_LEM_CHANNELS)):
                df["Info"]["isLEM"] = True
            else:
                df["Info"]["isLEM"] = False
            if channel in BLF_BL_CHANNELS:
                df["Info"]["isBL"] = True
            else:
                df["Info"]["isBL"] = False

        return dfs
