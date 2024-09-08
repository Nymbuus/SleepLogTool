from tkinter import *
from tkinter import messagebox
from modules.files_preperation import FilesPreparation
from modules.time_menu import TimeMenu
from modules.other_settings_menu import OtherSettingsMenu
from modules.browse_field import BrowseField
from modules.plot_lines import PlotLines

class Menu(Tk):
    """ Handles the design and functionality of the menu. """

    def __init__(self):
        super().__init__()
        """ Initializes the class. """
        self.initialize_vars()
        self._fp = FilesPreparation()
        self._rtm = TimeMenu(self, self.line_plot_frames)
        self._osm = OtherSettingsMenu(self)
        self.browse_field = BrowseField(self, self.line_plot_frames)
        plot_selected = self.browse_field.line_plot_select.get()
        self.first_plot_line = PlotLines(self, self.line_plot_frames, plot_selected)
        self.line_plot_frames.append(self.first_plot_line)
        self.path_frames.append(self.first_plot_line.path_frame)

        # DON'T KNOW ABOUT THIS ONE!!!!!!!!!!!!!!
        # self.browse_field.line_plot_select.set(self.first_plot_line.text_to_set)


        # Prepares the frame with lists to be filled.
        self.file_path_arrays.append([])
        self.file_path_del_buttons.append([])
        self.decide_bus.append(None)


    def main_window(self):
        """ Menu for selecting files and adjust settings. """
        self.left_section_frames_create()
        self.analyze_cancel_frame_create()

        self.mainloop()


    def initialize_vars(self):
        self.toggle_buttons = []
        self.file_path_arrays = []
        self.file_path_del_buttons = []
        self.x = 0
        self.line_plot_frames = []
        self.optionsmenu_list = []
        self.line_plot_del_buttons = []
        self.line_plot_name_entries = []
        self.decide_bus = []
        self.line_plot_invert_cbs = []
        self.path_frames = []
        self.toggling_frames = []


    def left_section_frames_create(self):
        """ Holds all frames in the left section of the window. """
        self.left_section_frames = LabelFrame(self, text="Left Section Frames", padx=10)
        self.left_section_frames.grid(row=0, rowspan=4, column=0, padx=10, pady=10, sticky=N)


    def analyze_cancel_frame_create(self):
        """ Creates the analyze/cancel frame and all of it's contents. """
        analyze_cancel_frame = Frame(self)
        analyze_cancel_frame.grid(row=3, column=1, padx=5, sticky=SE)
        self.analyze_button = Button(analyze_cancel_frame,
                                     text="Analyze",
                                     state=DISABLED,
                                     command=self.analyze_data,
                                     padx=15)
        self.analyze_button.grid(row=0, column=0, pady=10)
        self.cancel_button = Button(analyze_cancel_frame,
                                    text="Cancel",
                                    command=self.quit,
                                    padx=15)
        self.cancel_button.grid(row=0,column=1, padx=15, pady=10)


    def update_analyze_button(self):
        """ Updates the analyze button """
        if all(isinstance(x, list) and not x for x in self.file_path_arrays):
            self.analyze_button["state"] = DISABLED
        else:
            self.analyze_button["state"] = NORMAL 


    def show_warning(self, warning_text):
        messagebox.showwarning("warning", warning_text)