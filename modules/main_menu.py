from tkinter import *
from tkinter import messagebox
from modules.files_preperation import FilesPreparation
from modules.time_menu import TimeMenu
from modules.other_settings_menu import OtherSettingsMenu
from modules.plot_lines import PlotLines
from modules.plot_and_graph import PlotAndGraph

class Menu(Tk):
    """ Handles the design and functionality of the menu. """

    def __init__(self):
        super().__init__()
        """ Initializes the class. """
        self.initialize_vars()
        self.fp = FilesPreparation()
        self.rtm = TimeMenu(self)
        self.osm = OtherSettingsMenu(self)
        self.pag = PlotAndGraph()
        self.left_section_frames_create()
        self.browse_frame_create()
        self.analyze_cancel_frame_create()
        plot_selected = self.plot_line_select.get()
        plot_line = PlotLines(self.left_section_frame, self.plot_line_frames, plot_selected, self.analyze_button)
        self.plot_line_frames.append(plot_line)
        self.path_frames.append(plot_line.path_frame)
        self.plot_line_select.set(plot_line.text_to_set)

        # Prepares the frame with lists to be filled.
        self.file_path_arrays.append([])
        self.file_path_del_buttons.append([])
        self.decide_bus.append(None)


    def main_window(self):
        """ Mainloop keeps the program running until exit. """
        self.mainloop()


    def initialize_vars(self):
        self.toggle_buttons = []
        self.file_path_arrays = []
        self.file_path_del_buttons = []
        self.x = 0
        self.plot_line_frames = []
        self.optionsmenu_list = ["Plot Line 1"]
        self.line_plot_del_buttons = []
        self.line_plot_name_entries = []
        self.decide_bus = []
        self.line_plot_invert_cbs = []
        self.path_frames = []
        self.toggling_frames = []
        self.browse_field = Entry()
        self.plot_line_select = StringVar()
        self.plot_lines = []


    def browse_frame_create(self):
        """ Creates the browse frame and adds all of it's contents. """
        self.browse_frame = LabelFrame(self.left_section_frame, text="Choose blf file(s)", padx=10, pady=5)
        self.browse_frame.grid(row=0, column=0, pady=10, sticky=W)

        # Entry and button to add a file manually by entering path to it.
        self.browse_field = Entry(self.browse_frame, width=140, borderwidth=5)
        self.browse_field.grid(row=0, column=0, columnspan=6, padx=(0, 10), pady=(0, 10))
        add_button = Button(self.browse_frame, text="Add File", command=self.add_browse_field)
        add_button.grid(row=0, column=6, padx=(2, 3), sticky=N)

        # Buttons to add files in different ways with the file_path_setup function.
        choose_file_button = Button(self.browse_frame, text="Choose file(s)", command=lambda:self.add_file_path("file"))
        choose_file_button.grid(row=1, column=0, sticky=W)
        choose_folder_button = Button(self.browse_frame, text="Choose folder(s)", command=lambda:self.add_file_path("folder"))
        choose_folder_button.grid(row=1, column=1, padx=10)
        extract_LEM_button = Button(self.browse_frame, text="Extract LEM(s)", command=lambda:self.add_file_path("extract LEM"))
        extract_LEM_button.grid(row=1, column=2,)

        # Button to add a parallel plot line and a drop down box to select wanted plot line.
        add_plot_line_button = Button(self.browse_frame, text="Add Plot Line", command=self.plot_line_create)
        add_plot_line_button.grid(row=1, column=3, padx=(10, 30))
        drop_down_box_text = Label(self.browse_frame, text="Select Line Plot to add files to:")
        drop_down_box_text.grid(row=1, column=4, sticky=E)

        # Updates the dropdownbox with the new line plot.
        self.drop_down_box = OptionMenu(self.browse_frame, self.plot_line_select, *self.optionsmenu_list)
        self.drop_down_box.grid(row=1, column=5, padx=(0, 160), sticky=W)

    
    def add_file_path(self, choice):
        selected_plot_line = int(self.plot_line_select.get()[-1]) - 1

        files = self.fp.file_explorer(choice)

        self.plot_line_frames[selected_plot_line].file_path_setup(files, selected_plot_line, self.file_path_arrays, self.decide_bus, self.path_frames, self.file_path_del_buttons)
        
        self.update_analyze_button()

    
    def plot_line_create(self):
        plot_selected = self.plot_line_select.get()
        # IS self INCORRECT HERE?!?!?!?!!?
        plot_line = PlotLines(self.left_section_frame, self.plot_line_frames, plot_selected)
        self.plot_lines.append(plot_line)


    def add_browse_field(self):
        """ Adds path given in browse field to specified line plot frame. """
        file = self.browse_field.get()
        selected_plot_line = int(self.plot_line_select.get()[-1]) - 1
        if file:
            self.plot_line_frames[selected_plot_line].file_path_setup(file, selected_plot_line, self.file_path_arrays, self.decide_bus, self.path_frames, self.file_path_del_buttons, add="add")

        self.update_analyze_button()


    def left_section_frames_create(self):
        """ Holds all frames in the left section of the window. """
        self.left_section_frame = Frame(self, padx=10)
        self.left_section_frame.grid(row=0, rowspan=4, column=0, padx=10, pady=10, sticky=N)


    def analyze_cancel_frame_create(self):
        """ Creates the analyze/cancel frame and all of it's contents. """
        analyze_cancel_frame = Frame(self)
        analyze_cancel_frame.grid(row=3, column=1, padx=5, sticky=SE)
        self.analyze_button = Button(analyze_cancel_frame,
                                     text="Analyze",
                                     state=DISABLED,
                                     command=self.fp.analyze_data,
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