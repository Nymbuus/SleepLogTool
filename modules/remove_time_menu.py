from tkinter import *
from modules.files_preperation import FilesPreperation
from modules.plot_and_graph import PlotAndGraph

TENTH_SECOND = 6000

class RemoveTimeMenu:
    """ Menu for selecting how much time to remove from start and end of the blf file. """

    def __init__(self):
        """ Initializes the class. """
        self._fp = FilesPreperation()
        self._pag = PlotAndGraph()
        self.dfs = None
        self.filename = None
        self.root = None

    def time_menu(self, root):
        """ Design and functionality for time removal. """
        self.root = root

        self.time_removal_frame = LabelFrame(self.root, text="Time Removal")
        self.time_removal_frame.grid(row=0, rowspan=2, column=1, padx=(0, 30), pady=10, sticky=N)

        start_time_label = Label(self.time_removal_frame, text="Minutes to remove from start:")
        start_time_label.grid(row=0, column=0)
        self.start_time_entry = Entry(self.time_removal_frame, width=40, borderwidth=5)
        self.start_time_entry.grid(row=1, column=0, columnspan=2, padx=10)

        end_time_label = Label(self.time_removal_frame, text="Minutes to remove from end:")
        end_time_label.grid(row=2, column=0)
        self.end_time_entry = Entry(self.time_removal_frame, width=40, borderwidth=5)
        self.end_time_entry.grid(row=3, column=0, columnspan=2)

        sample_label = Label(self.time_removal_frame, text="Sample Rate:")
        sample_label.grid(row=4, column=0)
        self.sample_entry = Entry(self.time_removal_frame, width=40, borderwidth=5)
        self.sample_entry.grid(row=5, column=0, columnspan=2, pady=(0, 10))

    def warning(self, warning_text):
        """ Displays the warning text when you put in a wrong type of value. """
        warning_label = Label(self.time_removal_frame, text=warning_text)
        warning_label.grid(row=5, column=0)
    
    def set_df(self, dfs, filename, sample_rate):
        """ Removes time from start and end of graph. """
        self.dfs = dfs
        self.filename = filename
        if self.start_time_entry.get() == "":
            remove_start_time = 0
        else:
            remove_start_time = float(self.start_time_entry.get())
        if self.end_time_entry.get() == "":
            remove_end_time = 0
        else:
            remove_end_time = float(self.end_time_entry.get())

        try:
            remove_start_time = remove_start_time * (1/sample_rate) * TENTH_SECOND
            remove_end_time = remove_end_time * (1/sample_rate) * TENTH_SECOND
            if 0 <= remove_start_time < len(self.dfs)+12:
                if 0 <= remove_end_time < len(self.dfs)+12-remove_start_time:
                    self.dfs = self._fp.remove_time(self.dfs, remove_start_time, remove_end_time)
                    self.calculate_plot()
                elif remove_end_time < 0:
                    self.warning("End time too low value. Try again.")
                elif remove_start_time >= len(self.dfs)+12-remove_start_time:
                    self.warning("End time too high value. Try again.")
            elif remove_start_time < 0:
                self.warning("Start time too low value. Try again.")
            elif remove_start_time >= len(self.dfs)+12:
                self.warning("Start time too high value. Try again.")
        except ValueError as err:
            print(f"ValueError: {err}. Try again.")
    
    def get_df(self):
        return self.dfs

    def calculate_plot(self):
        self._pag.calculating_statistics(self.dfs)
        self._pag.plotting_graph(self.dfs, self.filename)

    def get_start_and_end_time(self):
        return self.start_time_entry.get(), self.end_time_entry.get()
    
    def get_sample_rate(self):
        if self.sample_entry.get() == "":
            return 0
        return int(self.sample_entry.get())