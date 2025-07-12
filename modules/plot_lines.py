""" Tkinter widgets for GUI and can for handling can buses. """
from tkinter import LabelFrame, Label, Entry, BooleanVar, Checkbutton, Frame, Button
import can

BLF_LEM_CHANNELS = (10, 23, 24, 25, 26, 28)
ASC_LEM_CHANNELS = (0, 1)
BL_CHANNELS = (2, 6, 7, 8, 9)

class PlotLines(LabelFrame):
    """ Handles the graphic design and logic of the Plot line frames in the main menu. """


    def __init__(self, parent,
                 line_plot_frames,
                 analyze_button,
                 analyze_button_func,
                 show_warning_func):
        super().__init__(parent)

        self.line_plot_frames = line_plot_frames
        self.analyze_button = analyze_button
        self.file_path_array = []
        self.file_path_del_buttons = []
        self.analyze_button_func = analyze_button_func
        self.show_warning_func = show_warning_func
        self.toggling_frame = None
        self.toggle_button = None
        self.toggle_line = None
        self.path_frame = None
        self.decide_bus = None
        self.line_plot_frame_create()


    def line_plot_frame_create(self):
        """ Creates new line plot frame for storing parallel line in the graph. """

        # Gets correct line plot name and creates a line plot frame with it.
        len_line_plots = len(self.line_plot_frames)
        self.plot_line_name = f"Plot Line {len_line_plots+1}"
        self.config(text=self.plot_line_name, padx=10, pady=5)
        self.grid(row=len_line_plots+2, column=0, columnspan=6, pady=10, sticky="w")

        # Entry for specified line custom name.
        self.line_plot_name_label = Label(self, text="Plot line name:")
        self.line_plot_name_label.grid(row=0, column=0, sticky="w")
        self.line_plot_name_entry = Entry(self, width=25, borderwidth=5)
        self.line_plot_name_entry.grid(row=0, column=1)

        self.invert_lem = BooleanVar()
        self.line_plot_invert_cb = Checkbutton(self,
                                               text="Do you feel inverted? (Only inverts LEM)",
                                               variable=self.invert_lem,
                                               onvalue=True,
                                               offvalue=False)
        self.line_plot_invert_cb.grid(row=0, column=2, padx=(40, 340))

        self.toggling_frame_create()
        self.path_frame_create()
        self.text_to_set = self.plot_line_name


    def line_plot_del(self):
        """ Deletes the specified line_plot_frame.
            Deletes everything within it and updates all lists in it. """
        self.destroy()


    def toggling_frame_create(self):
        """ Create a button to toggle the frame """
        self.toggling_frame = Frame(self)
        self.toggling_frame.grid(row=1, column=0, columnspan=3, sticky="w")
        self.toggle_button = Button(self.toggling_frame,
                                    text="-",
                                    padx=1,
                                    command=self.toggle_frame)
        self.toggle_button.grid(row=0, column=0)
        self.toggle_line = Label(self.toggling_frame, text="_"*168)
        self.toggle_line.grid(row=0, column=1)


    def path_frame_create(self):
        """ Creates a frame for the paths that will be used in the plot. """
        self.path_frame = LabelFrame(self, text="Filepath(s)", padx=10, pady=5)
        self.path_frame.grid(row=2, column=0, columnspan=3, padx=(20, 0), sticky="w")


    def toggle_frame(self):
        """ Toggles the line plot content. """
        if self.path_frame and self.toggle_button.cget("text") == "-":
            self.path_frame.grid_forget()
            self.toggle_button.config(text="+", padx=0)
        else:
            self.toggle_button.config(text="-", padx=1)
            self.path_frame.grid(row=2, column=0, columnspan=3, padx=(20, 0), sticky="w")


    def yeild_message(self, file):
        """ Creates a file generator to yield the messages in it. """
        mode = "rb" if file.endswith(".blf") else "r"
        with open(file, mode) as f:
            open_file = can.BLFReader(f) if file.endswith(".blf") else can.ASCReader(f)
            yield from open_file


    def get_channel(self, search_path):
        """ Gets the channel from the file. """
        file_gen = self.yeild_message(search_path)
        for msg in file_gen:
            return msg.channel


    def check_bus(self, file):
        """ Checks if the file is of the same bus as the other(s) in the path_frame. """
        file_match = False

        channel = self.get_channel(file)

        if ((file.endswith(".blf") and channel in BLF_LEM_CHANNELS) or
            (file.endswith(".asc") and channel in ASC_LEM_CHANNELS)):
            file_match = self.bus_ok("LEM")
        else:
            file_match = self.bus_ok(channel)

        return file_match

    def bus_ok(self, channel):
        """ Prints ok bus or not depending channel and decide bus matches.
            Will also return True or False for the file loop in file_path_setup func. """
        if self.decide_bus == channel:
            print("same bus OK")
            return True
        print("Not same bus Not OK")
        self.show_warning_func("Not the same bus-type as in the line plot")
        return False


    def set_bus_plot_line(self, files):
        """ Takes the first file in self.files and get the channel from it
            and sets it as the decided bus for the plot line. """
        if files == None:
            self.decide_bus = None
            return
        elif isinstance(files, list):
            channel = self.get_channel(files[0])
        elif isinstance(files, str):
            channel = self.get_channel(files)
        
        if isinstance(files, list):
            if ((files[0].endswith(".blf") and channel in BLF_LEM_CHANNELS) or
                (files[0].endswith(".asc") and channel in ASC_LEM_CHANNELS)):
                self.decide_bus = "LEM"
            else:
                self.decide_bus = channel
        elif isinstance(files, str):
            if ((files.endswith(".blf") and channel in BLF_LEM_CHANNELS) or
                (files.endswith(".asc") and channel in ASC_LEM_CHANNELS)):
                self.decide_bus = "LEM"
            else:
                self.decide_bus = channel


    def file_path_setup(self, files):
        """ displayes the file paths in the main window. """
        if isinstance(files, str):
            files = [files]
        if files:
            # Gets the bus from the first file and that decides what buses goes into the frame
            # Have to iterate the messages because there is no other way to get the bus info.
            for file in files:
                if self.decide_bus:
                    file_match = self.check_bus(file)
                    if file_match is False:
                        return
                else:
                    self.set_bus_plot_line(file)
        else:
            return

        # Checks if there was any files selected.
        if files is not False:
            # Goes through every file and puts it in the frame.
            for file in files:
                current_row = len(self.file_path_array)

                # Entry with the file path.
                e = Entry(self.path_frame, width=117, borderwidth=5)
                e.grid(row=current_row, column=0, padx=(0, 10), pady=5, sticky="nw")
                e.insert(0, file)
                self.file_path_array.append(e)

                # Delete button for the file path.
                b = Button(self.path_frame, text="X", padx=5,
                           command=lambda x=len(self.file_path_array)-1:
                           self.del_path(self.file_path_array[x],
                                         self.file_path_del_buttons[x],
                                         x))
                b.grid(row=current_row, column=1)
                self.file_path_del_buttons.append(b)


    def del_path(self, entry, button, index):
        """ Deletes the specified file path and then updates everything associated with it. """
        entry.destroy()
        button.destroy()
        del self.file_path_array[index]
        del self.file_path_del_buttons[index]
        
        # When the last path is deleted,
        # it will destroy the frame and recreate it to get rid of visual frame.
        if len(self.file_path_array) == 0:
            self.path_frame.destroy()
            self.path_frame_create()
            self.set_bus_plot_line(files=None)

        for i in range(len(self.file_path_array)):
            self.file_path_del_buttons[i].config(command=lambda x=i:
                                                 self.del_path(self.file_path_array[x],
                                                               self.file_path_del_buttons[x],
                                                               x))
        self.analyze_button_func()

        # Reconfigure rows for the filepaths and delete buttons.
        for i, file_path in enumerate(self.file_path_array):
            file_path.grid_configure(row=i)
        for i, del_button in enumerate(self.file_path_del_buttons):
            del_button.grid_configure(row=i)
