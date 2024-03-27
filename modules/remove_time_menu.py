from tkinter import *
from modules.files_preperation import FilesPreperation

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

        analyze_button = Button(self.root, text="Analyze",
                                command=lambda: self.set_df(callback))
        analyze_button.grid(row=4, column=0)

        self.cancel_button = Button(self.root, text="Cancel", command=self.root.destroy)
        self.cancel_button.grid(row=5, column=1)

        self.root.mainloop()
    
    def warning(self, warning_text):
        warning_label = Label(self.root, textvariable=warning_text)
        warning_label.grid(row=5, column=0)
        self.cancel_button.grid(row=6, column=1)
    
    def set_df(self, callback):
        self.df = self._fp.remove_time(self.df, self.start_time_entry.get(), self.end_time_entry.get())
        self.root.destroy()
        callback(self.df)
    
    def get_df(self):
        return self.df
