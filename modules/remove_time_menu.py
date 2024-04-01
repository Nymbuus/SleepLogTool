from tkinter import *
from modules.files_preperation import FilesPreperation

MINUTE_TO_10MS = 6000

class RemoveTimeMenu:
    """ Menu for selecting how much time to remove from start and end of the blf file. """

    def __init__(self):
        """ Initializes the class. """
        self._fp = FilesPreperation()

    def time_menu(self, df, callback):
        """ Design and functionality for time removal. """
        self.root = Tk()
        self.df = df
        start_time_label = Label(self.root, text="Time to remove from start:")
        start_time_label.grid(row=0, column=0)
        self.start_time_entry = Entry(self.root, width=40, borderwidth=5)
        self.start_time_entry.grid(row=1, column=0, columnspan=2)

        end_time_label = Label(self.root, text="Time to remove from end:")
        end_time_label.grid(row=2, column=0)
        self.end_time_entry = Entry(self.root, width=40, borderwidth=5)
        self.end_time_entry.grid(row=3, column=0, columnspan=2)

        analyze_button = Button(self.root, text="Analyze", command=lambda: self.set_df(callback))
        analyze_button.grid(row=4, column=0)

        self.cancel_button = Button(self.root, text="Cancel", command=self.root.destroy)
        self.cancel_button.grid(row=5, column=1)

        self.root.mainloop()
    
    def warning(self, warning_text):
        warning_label = Label(self.root, text=warning_text)
        self.cancel_button.grid(row=6, column=1)
        warning_label.grid(row=5, column=0)
    
    def set_df(self, callback):
        remove_start_time = float(self.start_time_entry.get())
        remove_end_time = float(self.end_time_entry.get())

        try:
            remove_start_time = remove_start_time * MINUTE_TO_10MS
            remove_end_time = remove_end_time * MINUTE_TO_10MS
            if 0 <= remove_start_time < len(self.df)+12:
                if 0 <= remove_end_time < len(self.df)+12-remove_start_time:
                    self.df = self._fp.remove_time(self.df, remove_start_time, remove_end_time)
                    self.root.destroy()
                    callback(self.df)
                elif remove_end_time < 0:
                    self.warning("End time too low value. Try again.")
                elif remove_start_time >= len(self.df)+12-remove_start_time:
                    self.warning("End time too high value. Try again.")
            elif remove_start_time < 0:
                self.warning("Start time too low value. Try again.")
            elif remove_start_time >= len(self.df)+12:
                self.warning("Start time too high value. Try again.")
        except ValueError as err:
            print(f"ValueError: {err}. Try again.")
    
    def get_df(self):
        return self.df
