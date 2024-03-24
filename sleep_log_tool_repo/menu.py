from tkinter import *
from sleep_log_tool_repo.sleep_log_tool import SleepLogTool

class Menu:
    """ Handles the design of the first pop-up menu. """

    def __init__(self):
        """ Initializes the class. """
        self.root = Tk()
        self._slt = SleepLogTool()
        self.browse_field = Entry(self.root, width=150, borderwidth=5)
        self.file_path_rows = []
        self.file_path_del_buttons = []
        self.x = 0

    def selection_window(self):
        """ Menu for selecting files and adjust settings. """
        my_label = Label(self.root, text="Choose .blf file(s)")
        my_label.grid(row=0, column=0)

        browse_button = Button(self.root, text="Browse", command=self.get_file_explorer)
        browse_button.grid(row=1, column=1)
        self.analyze_button = Button(self.root, text="Analyze", state=DISABLED)
        self.analyze_button.grid(row=2, column=0)
        self.cancel_button = Button(self.root, text="Cancel", command=self.root.quit)
        self.cancel_button.grid(row=3, column=1)

        self.browse_field.grid(row=1, column=0)

        self.root.mainloop()
        exit()

    # Kanske inte behövs!
    def get_file_explorer(self):
        file_explorer_return = self._slt.file_explorer()
        for i, file in enumerate(file_explorer_return):
            current_row = self.root.grid_size()[1]-1
            self.cancel_button.grid(row=current_row+1, column=1)
            e = Entry(self.root, width=150, borderwidth=5)
            e.grid(row=current_row, column=0)
            e.insert(0, file)
            self.file_path_rows.append(e)
            b = Button(self.root, text="X", padx=5,
                       command=lambda x=len(self.file_path_rows)-1: self.del_path(self.file_path_rows[x], self.file_path_del_buttons[x], x))
            b.grid(row=current_row, column=1)
            self.file_path_del_buttons.append(b)
        if self.file_path_rows:
            self.analyze_button["state"] = NORMAL
        else:
            self.analyze_button["state"] = DISABLED

    def del_path(self, entry, button, index):
        """ Deletes the specified row and then updates the command for delete buttons. """
        entry.destroy()
        button.destroy()
        del self.file_path_rows[index]
        del self.file_path_del_buttons[index]
        for i in range(len(self.file_path_rows)):
            self.file_path_del_buttons[i].config(command=lambda x=i: self.del_path(self.file_path_rows[x], self.file_path_del_buttons[x], x))