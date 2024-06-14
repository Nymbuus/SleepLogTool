from tkinter import *

class MyLabel:

    def __init__(self, frame=None, text="", padxgrid=0, padygrid=0, row=0, column=0, sticky=None):
        """ Creates a TKinter label. """

        label = Label(frame, text=text)
        label.grid(row=row, column=column, padx=padxgrid, pady=padygrid, sticky=sticky)