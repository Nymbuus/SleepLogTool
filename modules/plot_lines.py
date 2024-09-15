from tkinter import *
import can

class PlotLines(LabelFrame):
    """ Handles the graphic design and logic of the Plot line frames in the main menu. """


    def __init__(self, parent, line_plot_frames, plot_selected, analyze_button, analyze_button_func):
        super().__init__(parent)

        self.line_plot_frames = line_plot_frames
        self.plot_selected = plot_selected
        self.analyze_button = analyze_button
        self.file_path_array = []
        self.file_path_del_buttons = []
        self.analyze_button_func = analyze_button_func
        self.line_plot_frame_create()


    def line_plot_frame_create(self):
        """ Creates new line plot frame for storing parallel line in the graph. """

        # Gets correct line plot name and creates a line plot frame with it.
        len_line_plots = len(self.line_plot_frames)
        text = f"Plot Line {len_line_plots+1}"
        self.config(text=text, padx=10, pady=5)
        self.grid(row=len_line_plots+2, column=0, columnspan=7, pady=10)

        # Entry for specified line custom name.
        self.line_plot_name_label = Label(self, text="Plot line name:")
        self.line_plot_name_label.grid(row=0, column=0, sticky=W)
        self.line_plot_name_entry = Entry(self, width=25, borderwidth=5)
        self.line_plot_name_entry.grid(row=0, column=1)

        invert_LEM = BooleanVar()
        line_plot_invert_cb = Checkbutton(self,
                                          text="Do you feel inverted? (Only inverts LEM)",
                                          variable=invert_LEM,
                                          onvalue=True,
                                          offvalue=False)
        line_plot_invert_cb.grid(row=0, column=2, padx=(40, 340))

        self.toggling_frame_create()
        self.path_frame_create()
        self.text_to_set = text
    

    def line_plot_del(self):
        """ Deletes the specified line_plot_frame. Deletes everything within it and updates all lists in it. """
        self.destroy()
    

    def toggling_frame_create(self):
        """ Create a button to toggle the frame """
        self.toggling_frame = Frame(self)
        self.toggling_frame.grid(row=1, column=0, columnspan=3, sticky=W)
        self.toggle_button = Button(self.toggling_frame,
                                    text="-",
                                    padx=1,
                                    command=self.toggle_frame)
        self.toggle_button.grid(row=0, column=0)
        self.toggle_line = Label(self.toggling_frame, text="_"*168)
        self.toggle_line.grid(row=0, column=1)


    # def path_frame_create(self, frame_index, append):
    def path_frame_create(self, append=True):
        """ Creates a frame for the paths that will be used in the plot. """
        self.path_frame = LabelFrame(self, text="Filepath(s)", padx=10, pady=5)
        self.path_frame.grid(row=2, column=0, columnspan=3, padx=(20, 0), sticky=W)
        

    def toggle_frame(self):
        """ Toggles the line plot content. """
        if self.path_frame and self.toggle_button.cget("text") == "-":
            self.path_frame.grid_forget()
            self.toggle_button.config(text="+", padx=0)
        else:
            self.toggle_button.config(text="-", padx=1)
            self.path_frame.grid(row=2, column=0, columnspan=3, padx=(20, 0), sticky=W)


    def file_path_setup(self, files, frame_index, decide_bus, path_frames, add=None):
        """ displayes the file paths in the main window. """
        self.decide_bus = decide_bus
        self.path_frames = path_frames
        self.files = files

        # Checks if there are any line plot frames to add file path to.
        if len(self.line_plot_frames) == 0:
            return

        # Checks if it should add file from the browse entry.
        if add == None:
            # Calls function to get file(s) from the explorer.
            self.files = files
            if self.files:
                # If there are no file_paths in the frame, reset what bus can be add to it.
                if len(self.file_path_array) == 0:
                    self.decide_bus[frame_index] = None
                # Gets the bus from the first file and that decides what buses goes into the frame
                # Have to iterate the messages because there is no other way to get the bus info.
                for file in self.files:
                    if self.decide_bus[frame_index] != None:
                        with open(file, 'rb') as f:
                            channel_get_blf = can.BLFReader(f)
                            for msg in channel_get_blf:
                                if msg.channel == 10 or msg.channel == 23 or msg.channel == 24 or msg.channel == 25 or msg.channel == 26:
                                    if self.decide_bus[frame_index] == "LEM":
                                        print("same bus OK")
                                        break
                                    else:
                                        print("Not same bus Not OK")
                                        self.show_warning("Not the same bus-type as in the line plot")
                                        return
                                if self.decide_bus[frame_index] == msg.channel:
                                    print("same bus OK")
                                    break
                                else:
                                    print("Not same bus Not OK")
                                    self.show_warning("Not the same bus-type as in the line plot")
                                    return
                        f.close()
                    else:
                        with open(self.files[0], 'rb') as f:
                            channel_get_blf = can.BLFReader(f)
                            for msg in channel_get_blf:
                                if msg.channel == 10 or msg.channel == 23 or msg.channel == 24 or msg.channel == 25 or msg.channel == 26:
                                    self.decide_bus[frame_index] = "LEM"
                                else:
                                    self.decide_bus[frame_index] = msg.channel
                                break
                        f.close()
            else:
                return
        elif add == "add":
            self.files.append(self.files)

        # Checks if there was any files selected.
        if self.files != False:
            # Creates new path frame in the line plot frame if there is none.
            if self.path_frames[frame_index] == []:
                self.path_frame_create(append=False)
            # Goes through every file and puts it in the frame.
            for file in self.files:
                current_row = len(self.file_path_array)

                # Entry with the file path.
                e = Entry(self.path_frames[frame_index], width=128, borderwidth=5)
                e.grid(row=current_row, column=0, padx=(0, 10), pady=5, sticky=NW)
                e.insert(0, file)
                self.file_path_array.append(e)

                # Delete button for the file path.
                b = Button(self.path_frames[frame_index], text="X", padx=5,
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
        if len(self.file_path_array) == 0:
            self.path_frame.destroy()
            self.path_frame = []
            self.decide_bus = None

        for i in range(len(self.file_path_array)):
            self.file_path_del_buttons[i].config(command=lambda x=i:
                                                 self.del_path(self.file_path_array[x],
                                                               self.file_path_del_buttons[x],
                                                               x))
        self.analyze_button_func()
