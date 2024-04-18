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

    def main_window(self):
        """ Menu for selecting files and adjust settings. """
        browse_frame = LabelFrame(self.root, text="Choose blf file(s)", padx=10, pady=5)
        browse_frame.grid(row=0, column=0, padx=10, pady=10, sticky=N)
        self.browse_field = Entry(browse_frame, width=150, borderwidth=5)
        self.browse_field.grid(row=0, column=0, columnspan=3)
        choose_file_button = Button(browse_frame, text="Choose file(s)", command=lambda:self.file_path_setup("file"))
        choose_file_button.grid(row=1, column=0, sticky=E, pady=10)
        choose_folder_button = Button(browse_frame, text="Choose folder(s)", command=lambda:self.file_path_setup("folder"))
        choose_folder_button.grid(row=1, column=1, sticky=W, padx=(10, 723), pady=10)
        

        analyze_cancel_frame = Frame(self.root)
        analyze_cancel_frame.grid(row=2, column=1, padx=5, sticky=E)
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

        self._rtm.time_menu(self.root)

        self.root.mainloop()

    def file_path_setup(self, choice):
        """ displayes the file paths in the main window. """
        self.files = self.get_file_explorer(choice)
        # Frame for path files if beginning of the program or if just deleted.
        if len(self.file_path_rows) == 0:
            self.path_frame = LabelFrame(self.root, text="Filepath(s)", padx=10, pady=5)
            self.path_frame.grid(row=1, column=0, padx=10, sticky=W)
        for file in self.files:
            current_row = len(self.file_path_rows)
            e = Entry(self.path_frame, width=145, borderwidth=5)
            e.grid(row=current_row, column=0, pady=5, sticky=W)
            e.insert(0, file)
            self.file_path_rows.append(e)
            b = Button(self.path_frame, text="X", padx=5,
                       command=lambda x=len(self.file_path_rows)-1:
                       self.del_path(self.file_path_rows[x],
                                     self.file_path_del_buttons[x],
                                     x))
            b.grid(row=current_row, column=1, padx=(10, 0))
            self.file_path_del_buttons.append(b)
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
        # Deletes the path_frame if there isn't any path files left.
        if not self.file_path_rows:
            self.path_frame.destroy()

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