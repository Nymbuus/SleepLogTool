from tkinter import *
from sleep_log_tool_repo.sleep_log_tool import SleepLogTool

class Menu:
    """ Handles the design of the first pop-up menu. """

    def __init__(self):
        """ Initializes the class. """
        self.root = Tk()
        self._slt = SleepLogTool()
        self.browse_field = Entry(self.root, width=150, borderwidth=5)

    def selection_window(self):
        """ Menu for selecting files and adjust settings. """
        my_label = Label(self.root, text="Choose .blf file(s)")
        my_label.grid(row=0, column=0)

        browse_button = Button(self.root, text="Browse", command=self.get_file_explorer)
        browse_button.grid(row=1, column=1)
        analyze_button = Button(self.root, text="Analyze")
        analyze_button.grid(row=2, column=0)
        cancel_button = Button(self.root, text="Cancel", command=self.root.quit)
        cancel_button.grid(row=3, column=1)

        self.browse_field.grid(row=1, column=0)

        self.root.mainloop()
        exit()

    def get_file_explorer(self):
        file_explorer_return = self._slt.file_explorer()
        self.browse_field.insert(0, file_explorer_return[0] + "\nhejhejhej")
