""" Handles the design of the first pop-up menu. """
from tkinter import *
from modules.files_preperation import FilesPreperation
from modules.remove_time_menu import RemoveTimeMenu

class Menu:
    """ Handles the design of the first pop-up menu. """

    def __init__(self):
        """ Initializes the class. """
        self.root = Tk()
        self._fp = FilesPreperation()
        self._rtm = RemoveTimeMenu()
        self.browse_field = Entry()
        self.path_frame = LabelFrame()
        self.file_path_rows = []
        self.file_path_del_buttons = []
        self.x = 0
        self.path_frame_pady = 193


    def main_window(self):
        """ Menu for selecting files and adjust settings. """
        self.browse_frame_create()
        self.analyze_cancel_frame_create()
        self._rtm.time_menu(self.root)

        self.root.mainloop()


    def browse_frame_create(self):
        """ Creates the browse frame and all of it's contents. """
        self.browse_frame = LabelFrame(self.root, text="Choose blf file(s)", padx=10, pady=5)
        self.browse_frame.grid(row=0, column=0, padx=10, pady=(10, 180), sticky=S)
        self.browse_field = Entry(self.browse_frame, width=130, borderwidth=5)
        self.browse_field.grid(row=0, column=0, columnspan=2,padx=(0, 10), sticky=E)
        add_button = Button(self.browse_frame, text="Add", command=self.add_browse_field)
        add_button.grid(row=0, column=2, sticky=W)
        choose_file_button = Button(self.browse_frame, text="Choose file(s)", command=lambda:self.file_path_setup("file"))
        choose_file_button.grid(row=1, column=0, sticky=E, pady=10)
        choose_folder_button = Button(self.browse_frame, text="Choose folder(s)", command=lambda:self.file_path_setup("folder"))
        choose_folder_button.grid(row=1, column=1, sticky=W, padx=(10, 610), pady=10)


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


    def file_path_setup(self, choice):
        """ displayes the file paths in the main window. """
        self.files = self.get_file_explorer(choice)
        if self.files != False:
            # Frame for path files if beginning of the program or if just deleted.
            if len(self.file_path_rows) == 0:
                self.browse_frame.grid(pady=(10, 0))
                self.path_frame = LabelFrame(self.root, text="Filepath(s)", padx=10, pady=5)
                self.path_frame.grid(row=1, rowspan=2, column=0, padx=10, pady=(5, self.path_frame_pady), sticky=N)
            for file in self.files:
                current_row = len(self.file_path_rows)
                e = Entry(self.path_frame, width=131, borderwidth=5)
                e.grid(row=current_row, column=0, pady=5, sticky=NW)
                e.insert(0, file)
                self.file_path_rows.append(e)
                b = Button(self.path_frame, text="X", padx=5,
                        command=lambda x=len(self.file_path_rows)-1:
                        self.del_path(self.file_path_rows[x],
                                        self.file_path_del_buttons[x],
                                        x))
                b.grid(row=current_row, column=1, padx=(10, 0))
                self.file_path_del_buttons.append(b)
                if self.path_frame_pady > 37:
                    self.path_frame_pady -= 37
                else:
                    self.path_frame_pady = 10
                self.path_frame.grid(pady=(5, self.path_frame_pady))
        self.update_analyze_button()


    def del_path(self, entry, button, index):
        """ Deletes the specified row and then updates the command for delete buttons. """
        entry.destroy()
        button.destroy()
        del self.file_path_rows[index]
        del self.file_path_del_buttons[index]
        for i in range(len(self.file_path_rows)):
            self.file_path_del_buttons[i].config(command=lambda x=i:
                                                 self.del_path(self.file_path_rows[x],
                                                               self.file_path_del_buttons[x],
                                                               x))
        self.update_analyze_button()

        if len(self.file_path_rows) == 0:
            self.browse_frame.grid(pady=(10, 180))
        self.path_frame_pady += 37
        self.path_frame.grid(pady=(5, self.path_frame_pady))

        # Deletes the path_frame if there isn't any path files left.
        if not self.file_path_rows:
            self.path_frame.destroy()
    

    def add_browse_field(self):
        """ Adds path given in browse field to Filepath(s) frame. """
        file = self.browse_field.get()
        if file:
            self.file_path_setup(file)


    def update_analyze_button(self):
        """ Updates the analyze button """
        if self.file_path_rows:
            self.analyze_button["state"] = NORMAL
        else:
            self.analyze_button["state"] = DISABLED


    def analyze_data(self):
        """ Takes the present filepaths and analyzes the data in the blf files. """
        # start_time_value, end_time_value = self._rtm.get_start_and_end_time()
        # if start_time_value and end_time_value:
        blf_files = []
        for file in self.file_path_rows:
            blf_files.append(file.get())
        
        self.sample_rate = self._rtm.get_sample_rate()
        dfs, filename = self.get_write_to_df(blf_files)
        self._rtm.set_df(dfs, filename, self.sample_rate)


    def get_file_explorer(self, choice):
        """ Gets the list of file paths. """
        return self._fp.file_explorer(choice)


    def get_write_to_df(self, blf_files):
        """ returns the blf_to_df function. """
        return self._fp.blf_to_df(blf_files, self.sample_rate)


    def get_remove_time(self, df):
        """ returns the remove_time function. """
        return self._fp.remove_time(df)