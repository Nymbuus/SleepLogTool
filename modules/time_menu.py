from tkinter import *
from modules.files_preperation import FilesPreparation
from modules.plot_and_graph import PlotAndGraph

TENTH_SECOND = 6000
SECOND = 60

class TimeMenu(LabelFrame):
    """ Menu for time settings. """
    """ How much time to remove from start and end of the blf file. """
    """ What time unit to choose (seconds, minutes, hours). """

    def __init__(self, parent):
        super().__init__(parent)
        """ Initializes the class. """
        self._fp = FilesPreparation()
        self._pag = PlotAndGraph()
        self.dfs = None
        self.filename = None
        self.warning_label = None
        self.time_unit = None


    def time_menu(self):
        """ Design and functionality for time settings frame. """
        self.config(text="Time Settings", padx=10, pady=10)
        self.grid(row=0, rowspan=2, column=1, padx=(0, 20), pady=(10, 0), sticky=N)

        # Remove time from start part.
        start_time_label = Label(self, text="Minutes to remove from start:")
        start_time_label.grid(row=0, column=0, columnspan=3, sticky=W)
        self.start_time_entry = Entry(self, width=40, borderwidth=5)
        self.start_time_entry.grid(row=1, column=0, columnspan=3)

        # Remove time from end part.
        end_time_label = Label(self, text="Minutes to remove from end:")
        end_time_label.grid(row=2, column=0, columnspan=3, sticky=W)
        self.end_time_entry = Entry(self, width=40, borderwidth=5)
        self.end_time_entry.grid(row=3, column=0, columnspan=3)

        # Selection of time unit part.
        self.time_unit_selected = IntVar(value=60)
        self.time_unit_label = Label(self, text="Choose time unit for graph:")
        self.time_unit_label.grid(row=4, column=0, columnspan=3, sticky=W)
        self.time_unit_radiobutton1 = Radiobutton(self, text="Seconds", variable=self.time_unit_selected, value=1)
        self.time_unit_radiobutton1.grid(row=5, column=0)
        self.time_unit_radiobutton2 = Radiobutton(self, text="Minutes", variable=self.time_unit_selected, value=60)
        self.time_unit_radiobutton2.grid(row=5, column=1)
        self.time_unit_radiobutton3 = Radiobutton(self, text="Hours", variable=self.time_unit_selected, value=3600)
        self.time_unit_radiobutton3.grid(row=5, column=2)


    def warning(self, warning_text):
        """ Displays the warning text when you put in wrong type of value. """
        self.warning_label = Label(self, text=warning_text)
        self.warning_label.grid(row=6, column=0, pady=(0, 10))

    
    def set_df(self, plotinfo):
        """ Removes time from start and end of graph. """
        """ This will not remove time from every file in the graph, just the ones in the start and end. """
        # Will skip set_df function if true and go to plotting directly.
        if plotinfo["Skip"] == True:
            self._pag.plotting_graph(plotinfo, self.time_unit_selected.get())
            return

        # If either remove start or end time entry is empty, remove time is set to 0 for that variable.
        if self.start_time_entry.get() == "":
            remove_start_time = 0
        else:
            remove_start_time = float(self.start_time_entry.get())
        if self.end_time_entry.get() == "":
            remove_end_time = 0
        else:
            remove_end_time = float(self.end_time_entry.get())

        try:
            # Will convert time given in minutes to correct time unit depending on the file.
            if plotinfo["LEM"]:
                remove_start_time = remove_start_time * TENTH_SECOND
                remove_end_time = remove_end_time  * TENTH_SECOND
            elif plotinfo["BL"]:
                remove_start_time = remove_start_time * SECOND
                remove_end_time = remove_end_time  * SECOND

            # Checks if the numbers given in the time entries are too small (negative) or too big compared to the dataframe time.
            if 0 <= remove_start_time < len(plotinfo["Dfs"])+12:
                if 0 <= remove_end_time < len(plotinfo["Dfs"])+12-remove_start_time:

                    # If the number are accected the warning label is deleted if there was one displayed.
                    if self.warning_label:
                        self.warning_label.destroy()
                    
                    # Takes the dataframe and calls the function to remove the specified time, then plots the graph.
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
