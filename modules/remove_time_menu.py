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
        self.warning_label = None


    def time_menu(self, root):
        """ Design and functionality for time removal. """
        self.root = root

        self.time_removal_frame = LabelFrame(self.root, text="Time Removal", padx=10, pady=10)
        self.time_removal_frame.grid(row=0, rowspan=2, column=1, padx=(0, 20), pady=10, sticky=N)

        start_time_label = Label(self.time_removal_frame, text="Minutes to remove from start:")
        start_time_label.grid(row=0, column=0, sticky=W)
        self.start_time_entry = Entry(self.time_removal_frame, width=40, borderwidth=5)
        self.start_time_entry.grid(row=1, column=0, columnspan=2)

        end_time_label = Label(self.time_removal_frame, text="Minutes to remove from end:")
        end_time_label.grid(row=2, column=0, sticky=W)
        self.end_time_entry = Entry(self.time_removal_frame, width=40, borderwidth=5)
        self.end_time_entry.grid(row=3, column=0, columnspan=2)

        sample_label = Label(self.time_removal_frame, justify="left", text="Sample Rate:\n"+
                                                                           "Low number = More detailed info\n"+
                                                                           "High number = Smoother graph\n"+
                                                                           "1 = Sample every 0.01s\n"+
                                                                           "1000 = Sample every 10s\n"+
                                                                           "6000 = Sample every 1min\n"+
                                                                           "360000 = Sample every 1h")
        sample_label.grid(row=4, column=0, sticky=W)
        self.sample_entry = Entry(self.time_removal_frame, width=40, borderwidth=5)
        self.sample_entry.grid(row=5, column=0, columnspan=2)


    def warning(self, warning_text):
        """ Displays the warning text when you put in a wrong type of value. """
        self.warning_label = Label(self.time_removal_frame, text=warning_text)
        self.warning_label.grid(row=6, column=0, pady=(0, 10))

    
    def set_df(self, dfs, filename, stats, sample_rate, last_dfs):
        """ Removes time from start and end of graph. """
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
            if 0 <= remove_start_time < len(dfs)+12:
                if 0 <= remove_end_time < len(dfs)+12-remove_start_time:
                    if self.warning_label: self.warning_label.destroy()
                    dfs = self._fp.remove_time(dfs, remove_start_time, remove_end_time)
                    self._pag.plotting_graph(dfs, filename, stats, last_dfs)
                    return
                elif remove_end_time < 0:
                    self.warning("End time too low value. Try again.")
                elif remove_start_time >= len(dfs)+12-remove_start_time:
                    self.warning("End time too high value. Try again.")
            elif remove_start_time < 0:
                self.warning("Start time too low value. Try again.")
            elif remove_start_time >= len(dfs)+12:
                self.warning("Start time too high value. Try again.")
        except ValueError as err:
            print(f"ValueError: {err}. Try again.")


    def get_start_and_end_time(self):
        return self.start_time_entry.get(), self.end_time_entry.get()

    
    def get_sample_rate(self):
        if self.sample_entry.get() == "":
            return 1
        return int(self.sample_entry.get())