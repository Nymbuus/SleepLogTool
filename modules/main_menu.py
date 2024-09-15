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
        self.settings_frame = Frame(self)
        self.settings_frame.grid(row=0, column=1, sticky=N)
        self.rtm = TimeMenu(self.settings_frame)
        self.osm = OtherSettingsMenu(self.settings_frame)
        self.pag = PlotAndGraph()
        self.browse_frame_create()
        self.analyze_cancel_frame_create()
        self.plot_line_create()
        

        # Prepares the frame with lists to be filled.
        self.decide_bus.append(None)


    def main_window(self):
        """ Mainloop keeps the program running until exit. """
        self.mainloop()


    def initialize_vars(self):
        self.toggle_buttons = []
        self.file_path_del_buttons = []
        self.x = 0
        self.plot_line_frames = []
        self.optionsmenu_list = ["Plot Line 1"]
        self.plot_line_del_buttons = []
        self.line_plot_name_entries = []
        self.decide_bus = []
        self.line_plot_invert_cbs = []
        self.path_frames = []
        self.toggling_frames = []
        self.browse_field = Entry()
        self.plot_line_select = StringVar()
        self.plot_lines = []
        self.skip_optionsmenu_list_update = True


    def browse_frame_create(self):
        """ Creates the browse frame and adds all of it's contents. """
        self.browse_frame = LabelFrame(self, text="Choose blf file(s)", padx=10, pady=5)
        self.browse_frame.grid(row=0, rowspan=2, column=0, pady=10, padx=10, sticky=N)

        # Entry and button to add a file manually by entering path to it.
        self.browse_field = Entry(self.browse_frame, width=140, borderwidth=5)
        self.browse_field.grid(row=0, column=0, columnspan=6, padx=(0, 10), pady=(0, 10))
        add_button = Button(self.browse_frame, text="Add File", command=self.add_browse_field)
        add_button.grid(row=0, column=6, columnspan=2, padx=(2, 3), sticky=N)

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

        # Updates the dropdownbox with the new line plot.
        drop_down_box_text = Label(self.browse_frame, text="Select Line Plot to add files to:")
        drop_down_box_text.grid(row=1, column=4, sticky=E)
        self.drop_down_box = OptionMenu(self.browse_frame, self.plot_line_select, *self.optionsmenu_list)
        self.drop_down_box.grid(row=1, column=5, padx=(0, 160), sticky=W)

    
    def add_file_path(self, choice):
        selected_plot_line = int(self.plot_line_select.get()[-1]) - 1

        files = self.fp.file_explorer(choice)

        self.plot_line_frames[selected_plot_line].file_path_setup(files,
                                                                  selected_plot_line,
                                                                  self.decide_bus,
                                                                  self.path_frames,
                                                                  self.file_path_del_buttons)
        
        self.update_analyze_button()

    
    def plot_line_create(self):
        plot_line_frame = PlotLines(self.browse_frame,
                                    self.plot_line_frames,
                                    self.analyze_button,
                                    self.update_analyze_button)
        self.plot_line_frames.append(plot_line_frame)
        self.path_frames.append(plot_line_frame.path_frame)

        menu = self.drop_down_box["menu"]
        menu.delete(0, "end")
        if plot_line_frame.text_to_set != "Plot Line 1":
            self.optionsmenu_list.append(plot_line_frame.text_to_set)
        for string in self.optionsmenu_list:
            menu.add_command(label=string,
                            command=lambda value=string: self.plot_line_select.set(value))

        self.plot_line_select.set(plot_line_frame.text_to_set)

        # Delete button for specified line plot.
        # Uses lambda function to store correct number at the time of defining the delete button.
        plot_line_del_button = Button(self.browse_frame,
                                           text="X",
                                           command=lambda i=len(self.plot_line_frames)-1: self.line_plot_del(i))
        plot_line_del_button.grid(row=len(self.plot_line_frames)+1, column=7, padx=(10, 0), pady=20, sticky=NW)
        self.plot_line_del_buttons.append(plot_line_del_button)


    def line_plot_del(self, index):
        self.plot_line_frames[index].line_plot_del()
        del self.plot_line_frames[index]
        self.plot_line_del_buttons[index].destroy()
        del self.plot_line_del_buttons[index]
        self.update_drop_down_box()
        self.update_plot_line_frames()
        self.update_plot_line_del_buttons()


    def update_drop_down_box(self):
        if self. plot_line_frames:
            self.plot_line_select.set("Plot Line 1")
        else:
            self.plot_line_select.set("-")


    def update_plot_line_frames(self):
        for i, frame in enumerate(self.plot_line_frames):
            frame.config(text=f"Plot Line {i+1}")
            frame.grid_configure(row=i+2)
    

    def update_plot_line_del_buttons(self):
        for i, button in enumerate(self.plot_line_del_buttons):
            button.grid_configure(row=i+2)
            button.config(command=lambda: self.line_plot_del(i-1))


    def add_browse_field(self):
        """ Adds path given in browse field to specified line plot frame. """
        file = self.browse_field.get()
        selected_plot_line = int(self.plot_line_select.get()[-1]) - 1
        if file:
            self.plot_line_frames[selected_plot_line].file_path_setup(file, selected_plot_line, self.decide_bus, self.path_frames, self.file_path_del_buttons, add="add")

        self.update_analyze_button()


    def analyze_cancel_frame_create(self):
        """ Creates the analyze/cancel frame and all of it's contents. """
        analyze_cancel_frame = Frame(self)
        analyze_cancel_frame.grid(row=2, column=1, padx=5, sticky=SE)
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
        for array in self.plot_line_frames:
            if array.file_path_array:
                self.analyze_button["state"] = NORMAL
                return
        self.analyze_button["state"] = DISABLED


    def show_warning(self, warning_text):
        messagebox.showwarning("warning", warning_text)