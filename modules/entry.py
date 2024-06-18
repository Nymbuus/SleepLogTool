from tkinter import *

class MyEntry:

    def __init__(self, frame, width, borderwidth, padxgrid=0, padygrid=0, row=0, column=0, direction=None):
        """ Creates an TKinter entry. """
        entry = Entry(frame, width=width, borderwidth=borderwidth)
        entry.grid(row=row, column=column, padx=padxgrid, pady=padygrid, sticky=direction)