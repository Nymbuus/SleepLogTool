""" Handling of the Other settings menu. """
from tkinter import *

class OtherSettingsMenu:
    """ Handling of the Other settings menu. """

    
    def __init__(self, root):
        """ Initializes the class when called upon """
        self.root = root


    def frame(self):
        """ Creates the frame for the settings """
        self.settings_menu_frame = LabelFrame(self.root, text="Other settings", padx=10, pady=10)
        self.settings_menu_frame.grid(row=2, column=1, sticky=NW)

        self.choose_graph()


    def choose_graph(self):
        self.LEM_toggle = BooleanVar()
        self.LEM_toggle.set(True)
        self.LEM_checkbutton = Checkbutton(self.settings_menu_frame,
                                           text="LEM graph",
                                           variable=self.LEM_toggle,
                                           onvalue=True,
                                           offvalue=False)
        self.LEM_checkbutton.grid(row=0, column=0, sticky=W)
        self.BL_toggle = BooleanVar()
        self.BL_toggle.set(True)
        self.BL_checkbutton = Checkbutton(self.settings_menu_frame,
                                          text="BL graph",
                                          variable=self.BL_toggle,
                                          onvalue=True,
                                          offvalue=False)
        self.BL_checkbutton.grid(row=1, column=0, sticky=W)

        empty_space = Label(self.settings_menu_frame, text="")
        empty_space.grid(row=0, column=1, padx=(81, 80), sticky=E)
    

    def get_choose_graph(self):
        return self.LEM_toggle.get(), self.BL_toggle.get()