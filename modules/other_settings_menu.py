""" Handling of the Other settings menu. """
from tkinter import LabelFrame, BooleanVar, Checkbutton

class OtherSettingsMenu(LabelFrame):
    """ Handling of the Other settings menu. """

    def __init__(self, parent):
        super().__init__(parent)
        self.lem_toggle = BooleanVar()
        self.bl_toggle = BooleanVar()
        self.no_negative_values_toggle = BooleanVar()
        self.lem_checkbutton = None
        self.bl_checkbutton = None
        self.no_negative_valuesbutton = None
        self.frame()


    def frame(self):
        """ Creates the frame for the settings """
        self.config(text="Other settings", pady=10)
        self.grid(row=1, column=0, padx=(0, 10), sticky="nw")

        self.choose_graph()


    def choose_graph(self):
        """ Choose what graph will be used. """
        self.lem_toggle.set(True)
        self.lem_checkbutton = Checkbutton(self,
                                           text="LEM graph [mA]",
                                           variable=self.lem_toggle,
                                           onvalue=True,
                                           offvalue=False,
                                           padx=10)
        self.lem_checkbutton.grid(row=0, column=0, sticky="w")
        self.bl_toggle.set(True)
        self.bl_checkbutton = Checkbutton(self,
                                          text="BusLoad graph [%]",
                                          variable=self.bl_toggle,
                                          onvalue=True,
                                          offvalue=False,
                                          padx=10)
        self.bl_checkbutton.grid(row=1, column=0, padx=(0, 190), sticky="w")
        self.no_negative_values_toggle.set(False)
        self.no_negative_valuesbutton = Checkbutton(self,
                                                    text="No negative value",
                                                    variable=self.no_negative_values_toggle,
                                                    onvalue=True,
                                                    offvalue=False,
                                                    padx=10)
        self.no_negative_valuesbutton.grid(row=2, column=0, sticky="w")


    def get_choose_graph(self):
        """ Gets the chosen graph. """
        return self.lem_toggle.get(), self.bl_toggle.get(), self.no_negative_values_toggle.get()
