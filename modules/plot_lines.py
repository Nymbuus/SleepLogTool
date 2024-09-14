from tkinter import *
import can

class PlotLines(LabelFrame):
    """ Handles the graphic design and logic of the Plot line frames in the main menu. """


    def __init__(self, parent, line_plot_frames, plot_selected, analyze_button):
        super().__init__(parent)

        self.line_plot_frames = line_plot_frames
        self.plot_selected = plot_selected
        self.analyze_button = analyze_button
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
        line_plot_invert_cb.grid(row=0, column=2, padx=(40, 360))

        # Delete button for specified line plot.
        # Uses lambda function to store correct number at the time of defining the delete button.
        self.line_plot_del_button = Button(self, text="X",
                                           command=lambda x=len(self.line_plot_frames): self.line_plot_del(x))
        self.line_plot_del_button.grid(row=0, column=3)

        # Adds line plots to list to use later in functions below.
        # self.toggling_frame_create(len_line_plots)
        # self.path_frame_create(len_line_plots, append=True)
        self.toggling_frame_create()
        self.path_frame_create()

        # Checks if the dropdownbox does not have any line plots and if so destroys it to make a new one with Line plot 1 in it.
        if self.plot_selected == "-":
            self.drop_down_box.destroy()
        self.text_to_set = text


        # DON'T KNOW WHAT TO DO WITH THIS NOW!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        # Updates the dropdownbox with the new line plot.
        # self.optionsmenu_list.append(text)
        # self.drop_down_box = OptionMenu(self.browse_frame, self.line_plot_select, *self.optionsmenu_list)
        # self.drop_down_box.grid(row=1, column=5, padx=(0, 160), sticky=W)
    

    def toggling_frame_create(self):
        """ Create a button to toggle the frame """
        self.toggling_frame = Frame(self)
        self.toggling_frame.grid(row=1, column=0, columnspan=3, sticky=W)
        self.toggle_button = Button(self.toggling_frame, text="-",
                                    command=self.toggle_frame)
        self.toggle_button.grid(row=0, column=0)
        self.toggle_line = Label(self.toggling_frame, text="_"*175)
        self.toggle_line.grid(row=0, column=1)


    # def path_frame_create(self, frame_index, append):
    def path_frame_create(self):
        """ Creates a frame for the paths that will be used in the plot. """
        self.path_frame = LabelFrame(self, text="Filepath(s)", padx=10, pady=5)
        self.path_frame.grid(row=2, column=0, columnspan=3, padx=(20, 0), pady=5, sticky=W)


        # CHECK THIS IF PATH FRAMES FUCKS UP!!!!!!!!!!!!!!!!!!!

        # If it's the first path in the frame it will create a list otherwise append to it.
        # if append:
        #     self.path_frames.append(self.path_frame)
        # else:
        #     self.path_frames[frame_index] = self.path_frame
        

    def toggle_frame(self):
        """ Toggles the line plot info. """
        if self.path_frame.winfo_ismapped():
            self.path_frame.grid_forget()
            self.toggle_button.config(text="+")
        else:
            self.toggle_button.config(text="-")
            self.path_frame.grid(row=2, column=0, columnspan=2, padx=(20, 0), pady=5, sticky=W)


    def file_path_setup(self, files, frame_index, file_path_arrays, decide_bus, path_frames, del_buttons, add=None):
        """ displayes the file paths in the main window. """
        self.file_path_arrays = file_path_arrays
        self.decide_bus = decide_bus
        self.path_frames = path_frames
        self.file_path_del_buttons = del_buttons

        # Checks if there are any line plot frames to add file path to.
        if len(self.line_plot_frames) == 0:
            return
        
        self.files = []

        # Checks if it should add file from the browse entry.
        if add == None:
            # Calls function to get file(s) from the explorer.
            self.files = files
            if self.files:
                # If there are no file_paths in the frame, reset what bus can be add to it.
                if len(self.file_path_arrays[frame_index]) == 0:
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
                self.path_frame_create(frame_index, append=False)
            # Goes through every file and puts it in the frame.
            for file in self.files:
                current_row = len(self.file_path_arrays[frame_index])

                # Entry with the file path.
                e = Entry(self.path_frames[frame_index], width=130, borderwidth=5)
                e.grid(row=current_row, column=0, padx=(0, 28), pady=5, sticky=NW)
                e.insert(0, file)
                self.file_path_arrays[frame_index].append(e)

                # Delete button for the file path.
                b = Button(self.path_frames[frame_index], text="X", padx=5,
                           command=lambda x=len(self.file_path_arrays[frame_index])-1, y=frame_index:
                           self.del_path(self.file_path_arrays[y][x],
                                         self.file_path_del_buttons[y][x],
                                         x, y))
                b.grid(row=current_row, column=1, padx=(10, 0))
                self.file_path_del_buttons[frame_index].append(b)


    def del_path(self, entry, button, index, path_frame_index):
        """ Deletes the specified file path and then updates everything associated with it. """
        entry.destroy()
        button.destroy()
        del self.file_path_arrays[path_frame_index][index]
        del self.file_path_del_buttons[path_frame_index][index]
        if len(self.file_path_arrays[path_frame_index]) == 0:
            self.path_frames[path_frame_index].destroy()
            self.path_frames[path_frame_index] = []
            self.decide_bus[path_frame_index] = None

        for i in range(len(self.file_path_arrays[path_frame_index])):
            self.file_path_del_buttons[path_frame_index][i].config(command=lambda x=i, y=path_frame_index:
                                                 self.del_path(self.file_path_arrays[y][x],
                                                               self.file_path_del_buttons[y][x],
                                                               x, y))
        self.update_analyze_button()

    
    def update_analyze_button(self):
        """ Updates the analyze button """
        if all(isinstance(x, list) and not x for x in self.file_path_arrays):
            self.analyze_button["state"] = DISABLED
        else:
            self.analyze_button["state"] = NORMAL 


    def line_plot_del(self, x):
        """ Deletes the specified line_plot_frame. Deletes everything within it and updates all lists in it. """
        self.line_plot_frames[x].destroy()
        del self.line_plot_frames[x]
        del self.line_plot_del_buttons[x]
        del self.path_frames[x]
        del self.line_plot_name_entries[x]
        del self.file_path_arrays[x]
        del self.file_path_del_buttons[x]
        del self.decide_bus[x]
        del self.line_plot_invert_cbs[x]

        # Updates line_plot_frames text and row in it's grid.
        for i, frame in enumerate(self.line_plot_frames):
            text = f"Line Plot {i+1}"
            frame.config(text=text)
            frame.grid(row=i+1)
        
        # Updates line_plot_frames delete buttons.
        for i, button in enumerate(self.line_plot_del_buttons):
            button.config(command=lambda y=i: self.line_plot_del(y))
        
        # Updates file_paths delete buttons.
        for i in range(len(self.file_path_arrays)):
            for j in range(len(self.file_path_arrays[i])):
                self.file_path_del_buttons[i][j].config(command=lambda x=j, y=i:
                                                    self.del_path(self.file_path_arrays[y][x],
                                                                self.file_path_del_buttons[y][x],
                                                                x, y))

            # Updates the dropdownbox.
            self.drop_down_box.destroy()
            del self.optionsmenu_list[x]
            for i in range(0, len(self.optionsmenu_list)):
                self.optionsmenu_list[i] = f"Line Plot {i+1}"

            # Checks if the dropdownbox is empty and if it is then sets the symbol "-".
            # If there are plots in it, it will display Line Plot 1.
            if len(self.optionsmenu_list) == 0:
                self.drop_down_box = OptionMenu(self.browse_frame, self.line_plot_select, "")
                self.drop_down_box.grid(row=1, column=5, padx=(0, 210), sticky=W)
                self.line_plot_select.set("-")
            else:
                self.drop_down_box = OptionMenu(self.browse_frame, self.line_plot_select, *self.optionsmenu_list)
                self.drop_down_box.grid(row=1, column=5, padx=(0, 160), sticky=W)
                self.line_plot_select.set(f"Line Plot 1")