from tkinter import *

class MyLabel:

    def __init__(self, frame=None, text="", padx=0, pady=0, padxgrid=0, padygrid=0, row=0, column=0, direction=None):
        """ Creates a TKinter label. """

        label = Label(frame, text=text, padx=padx, pady=pady)
        label.grid(row=row, column=column, padx=padxgrid, pady=padygrid, sticky=direction)