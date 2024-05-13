""" Handles the design of the first pop-up menu. """
from tkinter import *
import can
from modules.files_preperation import FilesPreperation
from modules.time_menu import TimeMenu

class Menu:
    """ Handles the design of the first pop-up menu. """

    def __init__(self):
        """ Initializes the class. """
        self.root = Tk()
        self._fp = FilesPreperation()
        self._rtm = TimeMenu()
        self.browse_field = Entry()
        self.path_frame = LabelFrame()
        self.path_frames = []
        self.toggling_frames = []
        self.toggle_buttons = []
        self.file_path_arrays = []
        self.file_path_del_buttons = []
        self.x = 0
        self.line_plot_frames = []
        self.optionsmenu_list = []
        self.line_plot_select = StringVar()
        self.line_plot_del_buttons = []
        self.index_body = 1
        self.index_front1 = 1
        self.index_front3 = 1
        self.index_mid1 = 1
        self.index_rear1 = 1
        self.index_LEM = 1
        self.index_unknown = 1
        self.line_plot_name_entries = []
        self.decide_bus = []


    def main_window(self):
        """ Menu for selecting files and adjust settings. """
        self.left_section_frames_create()
        #self.parallel_line_plot_settings_frame_create()
        self.browse_frame_create()
        self.line_plot_frame_create()
        self.analyze_cancel_frame_create()
        self._rtm.time_menu(self.root)

        self.root.mainloop()


    def left_section_frames_create(self):
        """ Holds all frames in the left section of the window. """
        self.left_section_frames = LabelFrame(self.root, text="Left Section Frames", padx=10)
        self.left_section_frames.grid(row=0, rowspan=3, column=0, padx=10, pady=10, sticky=N)


    def browse_frame_create(self):
        """ Creates the browse frame and all of it's contents. """
        self.browse_frame = LabelFrame(self.left_section_frames, text="Choose blf file(s)", padx=10, pady=5)
        self.browse_frame.grid(row=0, column=0, pady=10, sticky=W)
        self.browse_field = Entry(self.browse_frame, width=140, borderwidth=5)
        self.browse_field.grid(row=0, column=0, columnspan=6, padx=(0, 10), pady=(0, 10))
        add_button = Button(self.browse_frame, text="Add File", command=self.add_browse_field)
        add_button.grid(row=0, column=6, padx=(2, 3), sticky=N)
        choose_file_button = Button(self.browse_frame, text="Choose file(s)", command=lambda:self.file_path_setup("file"))
        choose_file_button.grid(row=1, column=0, sticky=W)
        choose_folder_button = Button(self.browse_frame, text="Choose folder(s)", command=lambda:self.file_path_setup("folder"))
        choose_folder_button.grid(row=1, column=1, padx=10)
        extract_LEM_button = Button(self.browse_frame, text="Extract LEM(s)", command=lambda:self.file_path_setup("extract LEM"))
        extract_LEM_button.grid(row=1, column=2,)
        add_plot_line_button = Button(self.browse_frame, text="Add Plot Line", command=self.line_plot_frame_create)
        add_plot_line_button.grid(row=1, column=3, padx=(10, 30))
        drop_down_box_text = Label(self.browse_frame, text="Select Line Plot to add files to:")
        drop_down_box_text.grid(row=1, column=4, sticky=E)


    def line_plot_frame_create(self):
        """ Creates new line plot frame to plot a parallel line in the graph. """
        len_line_plots = len(self.line_plot_frames)
        text = f"Line Plot {len_line_plots+1}"
        self.line_plot_frame = LabelFrame(self.left_section_frames, text=text, padx=10, pady=5)
        self.line_plot_frame.grid(row=len_line_plots+1, column=0, pady=10)

        self.line_plot_name_label = Label(self.line_plot_frame, text="Line plot name:")
        self.line_plot_name_label.grid(row=0, column=0, sticky=W)
        self.line_plot_name_entry = Entry(self.line_plot_frame, width=25, borderwidth=5)
        self.line_plot_name_entry.grid(row=0, column=1, padx=(0, 640))
        self.line_plot_name_entries.append(self.line_plot_name_entry)

        self.line_plot_del_button = Button(self.line_plot_frame, text="X",
                                           command=lambda x=len(self.line_plot_frames): self.line_plot_del(x))
        self.line_plot_del_button.grid(row=0, column=2)
        self.line_plot_del_buttons.append(self.line_plot_del_button)

        self.line_plot_frames.append(self.line_plot_frame)
        self.toggling_frame_create(len_line_plots)
        self.path_frame_create(len_line_plots, append=True)
        self.optionsmenu_list.append(text)
        if self.line_plot_select.get() == "-":
            self.drop_down_box.destroy()
        self.line_plot_select.set(text)
        self.drop_down_box = OptionMenu(self.browse_frame, self.line_plot_select, *self.optionsmenu_list)
        self.drop_down_box.grid(row=1, column=5, padx=(0, 160), sticky=W)
        self.file_path_arrays.append([])
        self.file_path_del_buttons.append([])
        self.decide_bus.append(None)
    

    def line_plot_del(self, x):
        """ Deletes the specified line_plot_frame, deletes everything else within it and updates all lists associated with it. """
        self.line_plot_frames[x].destroy()
        del self.line_plot_frames[x]
        del self.line_plot_del_buttons[x]
        del self.path_frames[x]
        del self.line_plot_name_entries[x]
        del self.file_path_arrays[x]
        del self.file_path_del_buttons[x]
        del self.decide_bus[x]

        # Update line_plot_frames text and row in it's grid.
        for i, frame in enumerate(self.line_plot_frames):
            text = f"Line Plot {i+1}"
            frame.config(text=text)
            frame.grid(row=i+1)
        
        # Update line_plot_frames delete buttons.
        for i, button in enumerate(self.line_plot_del_buttons):
            button.config(command=lambda y=i: self.line_plot_del(y))
        
        # Update file_paths delete buttons.
        for i in range(len(self.file_path_arrays)):
            for j in range(len(self.file_path_arrays[i])):
                self.file_path_del_buttons[i][j].config(command=lambda x=j, y=i:
                                                    self.del_path(self.file_path_arrays[y][x],
                                                                self.file_path_del_buttons[y][x],
                                                                x, y))

        self.drop_down_box.destroy()
        del self.optionsmenu_list[x]
        for i in range(0, len(self.optionsmenu_list)):
            self.optionsmenu_list[i] = f"Line Plot {i+1}"

        if len(self.optionsmenu_list) == 0:
            self.drop_down_box = OptionMenu(self.browse_frame, self.line_plot_select, "")
            self.drop_down_box.grid(row=1, column=5, padx=(0, 210), sticky=W)
            self.line_plot_select.set("-")
        else:
            self.drop_down_box = OptionMenu(self.browse_frame, self.line_plot_select, *self.optionsmenu_list)
            self.drop_down_box.grid(row=1, column=5, padx=(0, 160), sticky=W)
            self.line_plot_select.set(f"Line Plot 1")


    def toggling_frame_create(self, frame_index):
        """ Create a button to toggle the frame """
        toggling_frame = Frame(self.line_plot_frames[frame_index])
        toggling_frame.grid(row=1, column=0, columnspan=2, sticky=W)
        toggle_button = Button(toggling_frame, text="-",
                               command=lambda index=len(self.toggling_frames): self.toggle_frames(index))
        toggle_button.grid(row=0, column=0)
        toggle_line = Label(toggling_frame, text="_"*175)
        toggle_line.grid(row=0, column=1)
        self.toggling_frames.append(toggling_frame)
        self.toggle_buttons.append(toggle_button)


    def path_frame_create(self, frame_index, append):
        """ Creates a frame for the paths that will be used in the plot. """
        path_frame = LabelFrame(self.line_plot_frames[frame_index], text="Filepath(s)", padx=10, pady=5)
        path_frame.grid(row=2, column=0, columnspan=2, padx=(20, 0), pady=5, sticky=W)

        if append:
            self.path_frames.append(path_frame)
        else:
            self.path_frames[frame_index] = path_frame
    

    def toggle_frames(self, index):
        """ Toggles the line plot info. """
        if self.path_frames[index].winfo_ismapped():
            self.path_frames[index].grid_forget()
            self.toggle_buttons[index].config(text="+")
        else:
            self.toggle_buttons[index].config(text="-")
            self.path_frames[index].grid(row=2, column=0, columnspan=2, padx=(20, 0), pady=5, sticky=W)


    def analyze_cancel_frame_create(self):
        """ Creates the analyze/cancel frame and all of it's contents. """
        analyze_cancel_frame = Frame(self.root)
        analyze_cancel_frame.grid(row=2, column=1, padx=5, sticky=SE)
        self.analyze_button = Button(analyze_cancel_frame,
                                     text="Analyze",
                                     state=DISABLED,
                                     command=self.analyze_data,
                                     padx=15)
        self.analyze_button.grid(row=0, column=0, pady=10)
        self.cancel_button = Button(analyze_cancel_frame,
                                    text="Cancel",
                                    command=self.root.quit,
                                    padx=15)
        self.cancel_button.grid(row=0,column=1, padx=15, pady=10)


    def file_path_setup(self, choice, add=None):
        """ displayes the file paths in the main window. """
        if len(self.line_plot_frames) == 0:
            return
        self.files = []

        if add == None:
            self.files = self._fp.file_explorer(choice)
            if self.files:
                frame_index = int(self.line_plot_select.get()[-1:])-1
                if len(self.file_path_arrays[frame_index]) == 0:
                    self.decide_bus[frame_index] = None
                for file in self.files:
                    if self.decide_bus[frame_index] != None:
                        with open(file, 'rb') as f:
                            channel_get_blf = can.BLFReader(f)
                            for msg in channel_get_blf:
                                if self.decide_bus[frame_index] == msg.channel:
                                    print("same bus OK")
                                    self.wrong_bus_warning(wrong=False)
                                    break
                                else:
                                    print("Not same bus Not OK")
                                    self.wrong_bus_warning(wrong=True)
                                    return
                        f.close()
                    else:
                        with open(self.files[0], 'rb') as f:
                            channel_get_blf = can.BLFReader(f)
                            for msg in channel_get_blf:
                                self.decide_bus[frame_index] = msg.channel
                                break
                        f.close()
            else:
                return
        elif add == "add":
            self.files.append(choice)

        if self.files != False:
            # Frame for path files if beginning of the program or if just deleted.
            # Gets what path_frame it should put the files in.
            path_frame_index = int(self.line_plot_select.get()[-1:])-1

            if self.path_frames[path_frame_index] == []:
                self.path_frame_create(path_frame_index, append=False)
            for file in self.files:
                current_row = len(self.file_path_arrays[path_frame_index])

                e = Entry(self.path_frames[path_frame_index], width=130, borderwidth=5)
                e.grid(row=current_row, column=0, padx=(0, 28), pady=5, sticky=NW)
                e.insert(0, file)
                self.file_path_arrays[path_frame_index].append(e)

                b = Button(self.path_frames[path_frame_index], text="X", padx=5,
                           command=lambda x=len(self.file_path_arrays[path_frame_index])-1, y=path_frame_index:
                           self.del_path(self.file_path_arrays[y][x],
                                         self.file_path_del_buttons[y][x],
                                         x, y))
                b.grid(row=current_row, column=1, padx=(10, 0))
                self.file_path_del_buttons[path_frame_index].append(b)

        self.update_analyze_button()


    def del_path(self, entry, button, index, path_frame_index):
        """ Deletes the specified row and then updates the command for delete buttons. """
        entry.destroy()
        button.destroy()
        
        del self.file_path_arrays[path_frame_index][index]
        del self.file_path_del_buttons[path_frame_index][index]
        if len(self.file_path_arrays[path_frame_index]) == 0:
            self.path_frames[path_frame_index].destroy()
            self.path_frames[path_frame_index] = []
            self.wrong_bus_warning(wrong=False)
            self.decide_bus[path_frame_index] = None

        for i in range(len(self.file_path_arrays[path_frame_index])):
            self.file_path_del_buttons[path_frame_index][i].config(command=lambda x=i, y=path_frame_index:
                                                 self.del_path(self.file_path_arrays[y][x],
                                                               self.file_path_del_buttons[y][x],
                                                               x, y))
        self.update_analyze_button()


    def wrong_bus_warning(self, wrong):
        if wrong:
            self.bus_warning_label = Label(self.browse_frame, text="Chosen file(s) don't match bus in this line plot!\n"+
                                                                   "Choose correct bus.")
            self.bus_warning_label.grid(row=2, column=0, columnspan=5, sticky=W)
        else:
            try:
                self.bus_warning_label.destroy()
            except:
                _ = None


    def add_browse_field(self):
        """ Adds path given in browse field to Filepath(s) frame. """
        file = self.browse_field.get()
        if file:
            self.file_path_setup(file, "add")


    def update_analyze_button(self):
        """ Updates the analyze button """
        if all(isinstance(x, list) and not x for x in self.file_path_arrays):
            self.analyze_button["state"] = DISABLED
        else:
            self.analyze_button["state"] = NORMAL


    def analyze_data(self):
        """ Takes the present filepaths and analyzes the data in the blf files. """
        self.index_LEM = 1
        self.indexBL = 1
        last_dfs = False
        dfs = None
        line_plot_name = None
        isLEM = None
        isBL = None
        for i, array in enumerate(self.file_path_arrays):
            first_dfs = False
            skip = False
            if len(array) != 0:
                blf_files = []
                isLEM = False
                isBL = False
                for file in array:
                    blf_files.append(file.get())

                line_plot_name = self.line_plot_name_entries[i].get()
                dfs, channel = self._fp.blf_to_df(blf_files)
                if line_plot_name == "":
                    match channel:
                        case 2:
                            line_plot_name = f"Body #{self.index_body}"
                            self.index_body += 1
                        case 6:
                            line_plot_name = f"Front1 #{self.index_front1}"
                            self.index_front1 += 1
                        case 7:
                            line_plot_name = f"Front3 #{self.index_front3}"
                            self.index_front3 += 1
                        case 8:
                            line_plot_name = f"Mid1 #{self.index_mid1}"
                            self.index_mid1 += 1
                        case 9:
                            line_plot_name = f"Rear1 #{self.index_rear1}"
                            self.index_rear1 += 1
                        case 10:
                            line_plot_name = f"LEM #{self.index_LEM}"
                            self.index_LEM += 1
                        case _:
                            line_plot_name = f"Unknown Bus #{self.index_unknown}"
                            self.index_unknown += 1
                if channel == 10:
                    isLEM = True
                else:
                    isBL = True
            else:
                skip = True
            if i == 0: first_dfs = True
            if len(self.file_path_arrays)-1 == i: last_dfs = True
            
            plot_info = {"Dfs":dfs, "Name":line_plot_name, "First":first_dfs, "Last":last_dfs, "LEM":isLEM, "BL":isBL, "Skip":skip}
            self._rtm.set_df(plot_info)
