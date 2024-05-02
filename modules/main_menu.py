""" Handles the design of the first pop-up menu. """
from tkinter import *
from modules.files_preperation import FilesPreperation
from modules.remove_time_menu import RemoveTimeMenu

class Menu:
    """ Handles the design of the first pop-up menu. """

    def __init__(self):
        """ Initializes the class. """
        self.root = Tk()
        self.root.geometry("1250x350")
        self._fp = FilesPreperation()
        self._rtm = RemoveTimeMenu()
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
        self.left_section_frames.grid(row=0, column=0, padx=10, pady=10, sticky=N)


    def browse_frame_create(self):
        """ Creates the browse frame and all of it's contents. """
        self.browse_frame = LabelFrame(self.left_section_frames, text="Choose blf file(s)", padx=10, pady=5)
        self.browse_frame.grid(row=0, column=0, pady=(10, 0), sticky=W)
        self.browse_field = Entry(self.browse_frame, width=136, borderwidth=5)
        self.browse_field.grid(row=0, column=0, columnspan=5, padx=(0, 10), pady=(0, 10))
        add_button = Button(self.browse_frame, text="Add File", command=self.add_browse_field)
        add_button.grid(row=0, column=5, padx=(2, 3), sticky=N)
        choose_file_button = Button(self.browse_frame, text="Choose file(s)", command=lambda:self.file_path_setup("file"))
        choose_file_button.grid(row=1, column=0, sticky=W)
        choose_folder_button = Button(self.browse_frame, text="Choose folder(s)", command=lambda:self.file_path_setup("folder"))
        choose_folder_button.grid(row=1, column=1, padx=10)
        add_plot_line_button = Button(self.browse_frame, text="Add Plot Line", command=self.line_plot_frame_create)
        add_plot_line_button.grid(row=1, column=2, padx=(0, 30))
        drop_down_box_text = Label(self.browse_frame, text="Select Line Plot to add files to:")
        drop_down_box_text.grid(row=1, column=3, sticky=E)


    def line_plot_frame_create(self):
        """ Creates new line plot frame to plot a parallel line in the graph. """
        len_line_plots = len(self.line_plot_frames)
        text = f"Line Plot {len_line_plots+1}"
        line_plot_frame = LabelFrame(self.left_section_frames, text=text, padx=10)
        line_plot_frame.grid(row=len_line_plots+1, column=0, pady=10)
        self.line_plot_frames.append(line_plot_frame)
        self.toggling_frame_create(len_line_plots)
        self.path_frame_create(len_line_plots)
        self.optionsmenu_list.append(text)
        self.line_plot_select.set(text)
        self.drop_down_box = OptionMenu(self.browse_frame, self.line_plot_select, *self.optionsmenu_list)
        self.drop_down_box.grid(row=1, column=4, padx=(0, 260), sticky=W)
        # Adds a empty list to the 2D list.
        self.file_path_arrays.append([])


    def toggling_frame_create(self, frame_index):
        """ Create a button to toggle the frame """
        toggling_frame = Frame(self.line_plot_frames[frame_index])
        toggling_frame.grid(row=0, column=0, columnspan=2, pady=(10, 0), sticky=W)
        toggle_button = Button(toggling_frame, text="-",
                               command=lambda index=len(self.toggling_frames): self.toggle_frames(index))
        toggle_button.grid(row=0, column=0)
        toggle_line = Label(toggling_frame, text="_"*175)
        toggle_line.grid(row=0, column=1)
        self.toggling_frames.append(toggling_frame)
        self.toggle_buttons.append(toggle_button)


    def path_frame_create(self, frame_index):
        """ Creates a frame for the paths that will be used in the plot. """
        path_frame = LabelFrame(self.line_plot_frames[frame_index], text="Filepath(s)", padx=10, pady=5)
        path_frame.grid(row=2, rowspan=2, column=1, pady=5, sticky=E)
        self.path_frames.append(path_frame)
    

    def toggle_frames(self, index):
        """ Toggles the line plot info. """
        if self.path_frames[index].winfo_ismapped():
            self.path_frames[index].grid_forget()
            self.toggling_frames[index].grid(pady=10)
            self.toggle_buttons[index].config(text="+")
        else:
            self.toggling_frames[index].grid(pady=(10, 0))
            self.toggle_buttons[index].config(text="-")
            self.path_frames[index].grid(row=2, rowspan=2, column=1, pady=5, sticky=E)


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
        self.files = []
        if add == None:
            self.files = self.get_file_explorer(choice)
        elif add == "add":
            self.files.append(choice)
        if self.files != False:
            # Frame for path files if beginning of the program or if just deleted.
            # Gets what path_frame it should put the files in.
            path_frame_index = int(self.line_plot_select.get()[-1:])-1
            for file in self.files:
                current_row = len(self.file_path_arrays[path_frame_index])
                e = Entry(self.path_frames[path_frame_index], width=130, borderwidth=5)
                e.grid(row=current_row, column=0, padx=(0, 28), pady=5, sticky=NW)
                e.insert(0, file)
                self.file_path_arrays[path_frame_index].append(e)
                b = Button(self.path_frames[path_frame_index], text="X", padx=5,
                        command=lambda x=len(self.file_path_arrays[path_frame_index])-1:
                        self.del_path(self.file_path_arrays[path_frame_index][x],
                                        self.file_path_del_buttons[path_frame_index][x],
                                        x, path_frame_index))
                b.grid(row=current_row, column=1, padx=(10, 0))
                self.file_path_del_buttons[path_frame_index].append(b)
                # Append funkar inte på del_buttons men på file_path_arrays

        self.update_analyze_button()


    def del_path(self, entry, button, index, path_frame_index):
        """ Deletes the specified row and then updates the command for delete buttons. """
        entry.destroy()
        button.destroy()
        del self.file_path_arrays[path_frame_index][index]
        del self.file_path_del_buttons[path_frame_index][index]
        for i in range(len(self.file_path_arrays[path_frame_index])):
            self.file_path_del_buttons[path_frame_index][i].config(command=lambda x=i:
                                                 self.del_path(self.file_path_arrays[path_frame_index][x],
                                                               self.file_path_del_buttons[path_frame_index][x],
                                                               x))
        self.update_analyze_button()


    def add_browse_field(self):
        """ Adds path given in browse field to Filepath(s) frame. """
        file = self.browse_field.get()
        if file:
            self.file_path_setup(file, "add")


    def update_analyze_button(self):
        """ Updates the analyze button """
        if self.file_path_arrays:
            self.analyze_button["state"] = NORMAL
        else:
            self.analyze_button["state"] = DISABLED


    def analyze_data(self):
        """ Takes the present filepaths and analyzes the data in the blf files. """
        blf_files = []
        self.sample_rate = self._rtm.get_sample_rate()
        last_dfs = False
        for i, array in enumerate(self.file_path_arrays):
            for file in array:
                blf_files.append(file.get())
        
            dfs, filename = self._fp.blf_to_df(blf_files, self.sample_rate)
            if len(self.file_path_arrays)-1 == i:
                last_dfs = True
            self._rtm.set_df(dfs, filename, self.sample_rate, last_dfs)


    def get_file_explorer(self, choice):
        """ Gets the list of file paths. """
        return self._fp.file_explorer(choice)


    def get_remove_time(self, df):
        """ returns the remove_time function. """
        return self._fp.remove_time(df)