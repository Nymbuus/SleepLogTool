""" Tkinter is used to sturcture up the menu graphically and functionally. 
    The other files are for handeling logic for different parts of the menu
    and also the graph window. """

from tkinter import Tk, messagebox, Label, LabelFrame, Entry, Button, OptionMenu, Frame, StringVar
import tkinter as tk
from modules.files_preperation import FilesPreparation
from modules.time_menu import TimeMenu
from modules.other_settings_menu import OtherSettingsMenu
from modules.plot_lines import PlotLines
from modules.plot_and_graph import PlotAndGraph
from modules.bus_selection_menu import BusSelectionMenu

class MainMenu(Tk):
    """ Handles the design and functionality of the menu. """

    def __init__(self):
        """ Initializes the class. """
        super().__init__()
        self.call("tk", "scaling", 1.51)
        self.toggle_buttons = []
        self.file_path_del_buttons = []
        self.x = 0
        self.plot_line_frames = []
        self.optionsmenu_list = ["-"]
        self.plot_line_del_buttons = []
        self.line_plot_name_entries = []
        self.decide_bus = []
        self.toggling_frames = []
        self.browse_entry = Entry()
        self.plot_line_select = StringVar()
        self.skip_optionsmenu_list_update = True

        self.settings_frame = Frame(self)
        self.settings_frame.grid(row=0, column=1, sticky=tk.N)
        self.rtm = TimeMenu(self.settings_frame, self.show_warning)
        self.osm = OtherSettingsMenu(self.settings_frame)
        self.pag = PlotAndGraph()
        self.browse_frame_create()
        self.analyze_cancel_frame_create()
        self.plot_line_create()
        self.fp = FilesPreparation(self.show_warning, self.plot_line_frames)
        self.resizable(width=False, height=False)


    def main_window(self):
        """ Mainloop keeps the program running until exit. """
        self.mainloop()


    def browse_frame_create(self):
        """ Creates the browse frame and adds all of it's contents. """
        self.browse_frame = LabelFrame(self, text="Choose blf/asc file(s)", padx=10, pady=5)
        self.browse_frame.grid(row=0, rowspan=2, column=0, pady=10, padx=10, sticky="n")

        # Entry and button to add a file manually by entering path to it.
        self.browse_entry = Entry(self.browse_frame, width=130, borderwidth=5)
        self.browse_entry.grid(row=0, column=0, columnspan=6, padx=(0, 10), pady=(0, 10), sticky="w")
        add_button = Button(self.browse_frame, text="Add File", command=self.add_browse_field)
        add_button.grid(row=0, column=6, columnspan=2, padx=(2, 3), sticky="n")

        # Buttons to add files in different ways with the file_path_setup function.
        choose_file_button = Button(self.browse_frame,
                                    text="Choose file(s)",
                                    command=lambda:self.add_file_path("file"))
        choose_file_button.grid(row=1, column=0, sticky="w")
        extract_bus_button = Button(self.browse_frame,
                                    text="Extract Bus",
                                    command=self.bus_selection)
        extract_bus_button.grid(row=1, column=1, sticky="w")

        # Button to add a parallel plot line and a drop down box to select wanted plot line.
        add_plot_line_button = Button(self.browse_frame,
                                      text="Add Plot Line",
                                      command=self.plot_line_create)
        add_plot_line_button.grid(row=1, column=2, sticky="w")

        # Updates the dropdownbox with the new line plot.
        drop_down_box_text = Label(self.browse_frame, text="Select Line Plot to add files to:")
        drop_down_box_text.grid(row=1, column=3, sticky="e")
        self.drop_down_box = OptionMenu(self.browse_frame,
                                        self.plot_line_select,
                                        *self.optionsmenu_list)
        self.drop_down_box.grid(row=1, column=4, sticky="w")


    def bus_selection(self):
        self.bsm = BusSelectionMenu(self, self.add_file_path)


    def add_file_path(self, choice, chosen_busses=None):
        """ Adds a filepath to the plot line. """
        if choice == "file":
            selected_plot_line = self.get_selected_plotline()
            if selected_plot_line == None:
                return
            else:
                files = self.fp.file_explorer(choice)
                self.plot_line_frames[selected_plot_line].file_path_setup(files)
        elif choice == "extract bus":
            busses = self.fp.file_explorer(choice, chosen_busses)
            frame_counter = 0
            for files in busses.values():
                if files:
                    while True:
                        try:
                            if self.plot_line_frames[frame_counter].file_path_array == []:
                                self.plot_line_frames[frame_counter].file_path_setup(files)
                                break
                            else:
                                frame_counter += 1
                        except:
                            self.plot_line_create()

        self.update_analyze_button()
    

    def get_selected_plotline(self):
        try:
            selected_plot_line = int(self.plot_line_select.get()[-1]) - 1
        except:
            self.show_warning("No plot line present, please add one")
            return
        return selected_plot_line


    def plot_line_create(self):
        """ Adds a new plot line in main window. """
        plot_line_frame = PlotLines(self.browse_frame,
                                    self.plot_line_frames,
                                    self.analyze_button,
                                    self.update_analyze_button,
                                    self.show_warning)
        self.plot_line_frames.append(plot_line_frame)

        self.update_optionmenu(plot_line_frame, choice="add")

        # Delete button for specified line plot.
        # Uses lambda function to store correct number at the time of defining the delete button.
        plot_line_del_b=Button(self.browse_frame,
                               text="X",
                               command=lambda i=len(self.plot_line_frames)-1:self.line_plot_del(i))
        plot_line_del_b.grid(row=len(self.plot_line_frames)+1,
                                  column=6,
                                  padx=(10, 0),
                                  pady=20,
                                  sticky="nw")
        self.plot_line_del_buttons.append(plot_line_del_b)


    def update_optionmenu(self, plot_line_frame, choice):
        """ Updates the optionsmenu for chosing plot. """
        menu = self.drop_down_box["menu"]
        menu.delete(0, "end")
        text_to_set = None
        if choice == "delete":
            del self.optionsmenu_list[-1]
            text_to_set = "Plot Line 1"
        elif self.optionsmenu_list == ["-"]:
            self.optionsmenu_list = ["Plot Line 1"]
            text_to_set = plot_line_frame.text_to_set
        else:
            self.optionsmenu_list.append(plot_line_frame.text_to_set)
            text_to_set = plot_line_frame.text_to_set
        for string in self.optionsmenu_list:
            menu.add_command(label=string,
                            command=lambda value=string: self.plot_line_select.set(value))
        self.plot_line_select.set(text_to_set)
        self.update_drop_down_box()


    def line_plot_del(self, index):
        """ Deletes selected plot line. """
        self.update_optionmenu(plot_line_frame=self.plot_line_frames[index], choice="delete")
        self.plot_line_frames[index].line_plot_del()
        del self.plot_line_frames[index]
        self.plot_line_del_buttons[index].destroy()
        del self.plot_line_del_buttons[index]
        self.update_drop_down_box()
        self.update_plot_line_frames()
        self.update_plot_line_del_buttons()


    def update_drop_down_box(self):
        """ Updates the drop down box containing the plot lines. """
        if self.plot_line_frames:
            self.drop_down_box.grid_configure(padx=(0, 240))
        else:
            self.plot_line_select.set("-")
            self.drop_down_box.grid_configure(padx=(0, 290))


    def update_plot_line_frames(self):
        """ Updates the rows for the plot lines. """
        for i, frame in enumerate(self.plot_line_frames):
            frame.config(text=f"Plot Line {i+1}")
            frame.grid_configure(row=i+2)


    def update_plot_line_del_buttons(self):
        """ Update the rows for the plot line delete buttons. """
        for i, button in enumerate(self.plot_line_del_buttons):
            button.grid_configure(row=i+2)
            button.config(command=lambda x=i: self.line_plot_del(x))


    def add_browse_field(self):
        """ Adds path given in browse field to specified line plot frame. """
        file = self.browse_entry.get()
        selected_plot_line = self.get_selected_plotline()
        if selected_plot_line == None:
            return
        else:
            if file:
                self.plot_line_frames[selected_plot_line].file_path_setup(file)

        self.update_analyze_button()


    def analyze_cancel_frame_create(self):
        """ Creates the analyze/cancel frame and all of it's contents. """
        analyze_cancel_frame = Frame(self)
        analyze_cancel_frame.grid(row=2, column=1, padx=5, sticky=tk.SE)
        self.analyze_button = Button(analyze_cancel_frame,
                                     text="Analyze",
                                     state=tk.DISABLED,
                                     command=self.analyze_data,
                                     padx=15)
        self.analyze_button.grid(row=0, column=0, pady=10)
        self.cancel_button = Button(analyze_cancel_frame,
                                    text="Cancel",
                                    command=self.quit,
                                    padx=15)
        self.cancel_button.grid(row=0,column=1, padx=15, pady=10)


    def analyze_data(self):
        """ Connected to the analyze button and start the analyze process of all the files. """
        dfs = self.fp.analyze_data(self.osm.get_choose_graph(),
                             self.plot_line_frames)

        # Will skip set_df function if true and go to plotting directly.
        for df in dfs:
            if df["Info"]["Skip"]:
                # MÅSTE FIXA PLOTTING_GRAPH, PLOTS HAR BYTTS MOT DFS!!!!
                self.pag.plotting_graph(dfs, self.rtm.time_unit_selected.get())
                return
            remove_start_time, remove_end_time = self.rtm.set_df(df)
            if remove_start_time is None and remove_end_time is None:
                return

            # Takes the dataframe and calls the function to remove the specified time,
            # then plots the graph.
            df = self.fp.remove_time(df, remove_start_time, remove_end_time)
        self.tk.call("tk", "scaling", 1.3)
        self.pag.plotting_graph(dfs, self.rtm.time_unit_selected.get())


    def update_analyze_button(self):
        """ Updates the analyze button """
        for array in self.plot_line_frames:
            if array.file_path_array:
                self.analyze_button["state"] = tk.NORMAL
                return
        self.analyze_button["state"] = tk.DISABLED


    def show_warning(self, warning_text):
        """ Shows warning with a provided pop-up message. """
        messagebox.showwarning("warning", warning_text)
