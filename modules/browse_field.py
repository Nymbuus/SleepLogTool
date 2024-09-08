from tkinter import *
from plot_lines import PlotLines

class BrowseField(LabelFrame):
    """ Handles the graphic design and logic of the browse field frame in the main menu. """


    def __init__(self, parent, line_plot_frames):
        super().__init__(parent)

        self.browse_field = Entry()
        self.line_plot_select = StringVar()
        self.line_plot_frames = line_plot_frames
        self.browse_frame_create()
    

    def browse_frame_create(self):
        """ Creates the browse frame and adds all of it's contents. """
        self.config(text="Choose blf file(s)", padx=10, pady=5)
        self.grid(row=0, column=0, pady=10, sticky=W)

        # Entry and button to add a file manually by entering path to it.
        self.browse_field = Entry(self, width=140, borderwidth=5)
        self.browse_field.grid(row=0, column=0, columnspan=6, padx=(0, 10), pady=(0, 10))
        add_button = Button(self, text="Add File", command=self.add_browse_field)
        add_button.grid(row=0, column=6, padx=(2, 3), sticky=N)

        # Buttons to add files in different ways with the file_path_setup function.
        choose_file_button = Button(self, text="Choose file(s)", command=lambda:self.file_path_setup("file"))
        choose_file_button.grid(row=1, column=0, sticky=W)
        choose_folder_button = Button(self, text="Choose folder(s)", command=lambda:self.file_path_setup("folder"))
        choose_folder_button.grid(row=1, column=1, padx=10)
        extract_LEM_button = Button(self, text="Extract LEM(s)", command=lambda:self.file_path_setup("extract LEM"))
        extract_LEM_button.grid(row=1, column=2,)

        # Button to add a parallel plot line and a drop down box to select wanted plot line.
        add_plot_line_button = Button(self, text="Add Plot Line", command=self.plot_line_create)
        add_plot_line_button.grid(row=1, column=3, padx=(10, 30))
        drop_down_box_text = Label(self, text="Select Line Plot to add files to:")
        drop_down_box_text.grid(row=1, column=4, sticky=E)

    
    def plot_line_create(self):
        plot_selected = self.line_plot_select.get()
        # IS self INCORRECT HERE?!?!?!?!!?
        PlotLines(self, self.line_plot_frames, plot_selected)


    def add_browse_field(self):
        """ Adds path given in browse field to specified line plot frame. """
        file = self.browse_field.get()
        if file:
            self.file_path_setup(file, "add")
    