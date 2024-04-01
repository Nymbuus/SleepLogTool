""" Handles the design of the first pop-up menu. """
from tkinter import *
from modules.plot_and_graph import PlotAndGraph
from modules.files_preperation import FilesPreperation
from modules.remove_time_menu import RemoveTimeMenu

class Menu:
    """ Handles the design of the first pop-up menu. """

    def __init__(self):
        """ Initializes the class. """
        self.root = Tk()
        self._pag = PlotAndGraph()
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
        browse_frame.grid(row=0, column=0, padx=10, pady=10, sticky=W)
        self.browse_field = Entry(browse_frame, width=150, borderwidth=5)
        self.browse_field.grid(row=0, column=0)
        browse_button = Button(browse_frame, text="Browse", command=self.file_path_setup)
        browse_button.grid(row=0, column=1)

        analyze_cancel_frame = Frame(self.root)
        analyze_cancel_frame.grid(row=2, column=0, padx=5, sticky=E)
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

        self.root.mainloop()

    def file_path_setup(self):
        """ displayes the file paths in the main window. """
        self.files = self.get_file_explorer()
        # Frame for path files if beginning of the program or if just deleted.
        if len(self.file_path_rows) == 0:
            self.path_frame = Frame(self.root, padx=20, pady=5)
            self.path_frame.grid(row=1, column=0, sticky=W)
        for file in self.files:
            current_row = len(self.file_path_rows)
            e = Entry(self.path_frame, width=150, borderwidth=5)
            e.grid(row=current_row, column=0, padx=5, pady=5, sticky=W)
            e.insert(0, file)
            self.file_path_rows.append(e)
            b = Button(self.path_frame, text="X", padx=5,
                       command=lambda x=len(self.file_path_rows)-1:
                       self.del_path(self.file_path_rows[x],
                                     self.file_path_del_buttons[x],
                                     x))
            b.grid(row=current_row, column=1)
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
        blf_files = []
        for file in self.file_path_rows:
            blf_files.append(file.get())

        # Deletes the main window because it's not needed anymore.
        self.root.destroy()

        df = self.get_write_to_df(blf_files)

        def continuation(df):
            self.calculate_plot(df)

        self._rtm.time_menu(df, continuation)
        
    def calculate_plot(self, df):
        self._pag.calculating_statistics(df)
        self._pag.plotting_graph(df)
    
    def get_file_explorer(self):
        """ Gets the list of file paths. """
        return self._fp.file_explorer()
    
    def get_write_to_df(self, blf_files):
        """ returns the blf_to_df function. """
        return self._fp.blf_to_df( blf_files)
    
    def get_remove_time(self, df):
        """ returns the remove_time function. """
        return self._fp.remove_time(df)