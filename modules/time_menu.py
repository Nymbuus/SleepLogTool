from tkinter import *
from modules.files_preperation import FilesPreperation
from modules.plot_and_graph import PlotAndGraph

TENTH_SECOND = 6000
SECOND = 60

class TimeMenu:
    """ Menu for time settings. """
    """ How much time to remove from start and end of the blf file. """
    """ What time unit to choose (seconds, minutes, hours). """

    def __init__(self):
        """ Initializes the class. """
        self._fp = FilesPreperation()
        self._pag = PlotAndGraph()
        self.dfs = None
        self.filename = None
        self.root = None
        self.warning_label = None
        self.time_unit = None


    def time_menu(self, root):
        """ Design and functionality for time removal. """
        self.root = root

        self.time_frame = LabelFrame(self.root, text="Time Settings", padx=10, pady=10)
        self.time_frame.grid(row=0, rowspan=2, column=1, padx=(0, 20), pady=10, sticky=N)

        start_time_label = Label(self.time_frame, text="Minutes to remove from start:")
        start_time_label.grid(row=0, column=0, columnspan=3, sticky=W)
        self.start_time_entry = Entry(self.time_frame, width=40, borderwidth=5)
        self.start_time_entry.grid(row=1, column=0, columnspan=3)

        end_time_label = Label(self.time_frame, text="Minutes to remove from end:")
        end_time_label.grid(row=2, column=0, columnspan=3, sticky=W)
        self.end_time_entry = Entry(self.time_frame, width=40, borderwidth=5)
        self.end_time_entry.grid(row=3, column=0, columnspan=3)

        self.time_unit_selected = IntVar(value=60)
        self.time_unit_label = Label(self.time_frame, text="Choose time unit for graph:")
        self.time_unit_label.grid(row=4, column=0, columnspan=3, sticky=W)
        self.time_unit_radiobutton1 = Radiobutton(self.time_frame, text="Seconds", variable=self.time_unit_selected, value=1)
        self.time_unit_radiobutton1.grid(row=5, column=0)
        self.time_unit_radiobutton2 = Radiobutton(self.time_frame, text="Minutes", variable=self.time_unit_selected, value=60)
        self.time_unit_radiobutton2.grid(row=5, column=1)
        self.time_unit_radiobutton3 = Radiobutton(self.time_frame, text="Hours", variable=self.time_unit_selected, value=3600)
        self.time_unit_radiobutton3.grid(row=5, column=2)


    def warning(self, warning_text):
        """ Displays the warning text when you put in a wrong type of value. """
        self.warning_label = Label(self.time_frame, text=warning_text)
        self.warning_label.grid(row=6, column=0, pady=(0, 10))

    
    def set_df(self, plotinfo):
        """ Removes time from start and end of graph. """
        if plotinfo["Skip"] == True:
            self._pag.plotting_graph(plotinfo, self.time_unit_selected.get())
            return

        if self.start_time_entry.get() == "":
            remove_start_time = 0
        else:
            remove_start_time = float(self.start_time_entry.get())
        if self.end_time_entry.get() == "":
            remove_end_time = 0
        else:
            remove_end_time = float(self.end_time_entry.get())

        try:
            if plotinfo["LEM"]:
                remove_start_time = remove_start_time * TENTH_SECOND
                remove_end_time = remove_end_time  * TENTH_SECOND
            elif plotinfo["BL"]:
                remove_start_time = remove_start_time * SECOND
                remove_end_time = remove_end_time  * SECOND
            if 0 <= remove_start_time < len(plotinfo["Dfs"])+12:
                if 0 <= remove_end_time < len(plotinfo["Dfs"])+12-remove_start_time:
                    if self.warning_label: self.warning_label.destroy()
                    plotinfo["Dfs"] = self._fp.remove_time(plotinfo["Dfs"], remove_start_time, remove_end_time)
                    self._pag.plotting_graph(plotinfo, self.time_unit_selected.get())
                    return
                elif remove_end_time < 0:
                    self.warning("End time too low value. Try again.")
                elif remove_start_time >= len(plotinfo["Dfs"])+12-remove_start_time:
                    self.warning("End time too high value. Try again.")
            elif remove_start_time < 0:
                self.warning("Start time too low value. Try again.")
            elif remove_start_time >= len(plotinfo["Dfs"])+12:
                self.warning("Start time too high value. Try again.")
        except ValueError as err:
            print(f"ValueError: {err}. Try again.")
