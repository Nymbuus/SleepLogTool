from tkinter import *

class MyCheckbutton:

    def __init__(self,
                 frame,
                 text="",
                 variable=False,
                 padx=0,
                 pady=0,
                 row=0,
                 column=0,
                 padxgrid=0,
                 padygrid=0,
                 direction=W):
        """ Creates a TKinter checkbutton. """
        checkbutton = Checkbutton(frame, text=text, variable=variable, padx=padx, pady=pady)
        checkbutton.grid(row=row, column=column, padx=padxgrid, pady=padygrid, sticky=direction)