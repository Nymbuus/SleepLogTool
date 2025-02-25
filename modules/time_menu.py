""" For GUI """
from tkinter import LabelFrame, Label, Entry, IntVar, Radiobutton

TENTH_SECOND = 6000
SECOND = 60

class TimeMenu(LabelFrame):
    """ Menu for time settings.
        How much time to remove from start and end of the file.
        What time unit to choose (seconds, minutes, hours). """

    def __init__(self, parent, show_warning_func):
        super().__init__(parent)
        self.show_warning = show_warning_func
        self.dfs = None
        self.filename = None
        self.warning_label = None
        self.time_unit = None
        self.time_menu()


    def time_menu(self):
        """ Design and functionality for time settings frame. """
        self.config(text="Time Settings", padx=10, pady=10)
        self.grid(row=0, column=0, padx=(0, 20), pady=(10, 5))

        # Remove time from start part.
        start_time_label = Label(self, text="Minutes to remove from start:")
        start_time_label.grid(row=0, column=0, columnspan=3, sticky="w")
        self.start_time_entry = Entry(self, width=40, borderwidth=5)
        self.start_time_entry.grid(row=1, column=0, columnspan=3)

        # Remove time from end part.
        end_time_label = Label(self, text="Minutes to remove from end:")
        end_time_label.grid(row=2, column=0, columnspan=3, sticky="w")
        self.end_time_entry = Entry(self, width=40, borderwidth=5)
        self.end_time_entry.grid(row=3, column=0, columnspan=3)

        # Selection of time unit part.
        self.time_unit_selected = IntVar(value=60)
        self.time_unit_label = Label(self, text="Choose time unit for graph:")
        self.time_unit_label.grid(row=4, column=0, columnspan=3, sticky="w")
        self.time_unit_radiobutton1 = Radiobutton(self,
                                                  text="Seconds",
                                                  variable=self.time_unit_selected, value=1)
        self.time_unit_radiobutton1.grid(row=5, column=0)
        self.time_unit_radiobutton2 = Radiobutton(self,
                                                  text="Minutes",
                                                  variable=self.time_unit_selected, value=60)
        self.time_unit_radiobutton2.grid(row=5, column=1)
        self.time_unit_radiobutton3 = Radiobutton(self,
                                                  text="Hours",
                                                  variable=self.time_unit_selected, value=3600)
        self.time_unit_radiobutton3.grid(row=5, column=2)


    def set_df(self, df):
        """ Removes time from start and end of graph.
            This will not remove time from every file in the graph,
            just the ones in the start and end. """
        # If either remove start or end time entry is empty,
        # remove time is set to 0 for that variable.
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
            if df["Info"]["isLEM"]:
                remove_start_time = remove_start_time * TENTH_SECOND
                remove_end_time = remove_end_time  * TENTH_SECOND
            elif df["Info"]["isBL"]:
                remove_start_time = remove_start_time * SECOND
                remove_end_time = remove_end_time  * SECOND

            # Checks if the numbers given in the time entries are too small (negative)
            # or too big compared to the dataframe time.
            if 0 <= remove_start_time < len(df["df"])+12:
                if 0 <= remove_end_time < len(df["df"])+12-remove_start_time:

                    # If the number is accepted the warning label is deleted if one was displayed.
                    if self.warning_label:
                        self.warning_label.destroy()
                    return remove_start_time, remove_end_time
                if remove_end_time < 0:
                    self.show_warning("End time too low value. Try again.")
                if remove_start_time >= len(df["df"])+12-remove_start_time:
                    self.show_warning("End time too high value. Try again.")
            if remove_start_time < 0:
                self.show_warning("Start time too low value. Try again.")
            if remove_start_time >= len(df["df"])+12:
                self.show_warning("Start time too high value. Try again.")
        except ValueError as err:
            print(f"ValueError: {err}. Try again.")
        return None, None
