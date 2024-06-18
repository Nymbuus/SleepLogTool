from tkinter import *

class MyFrame:

    def __init__(self, frame=None, label=None, padx=0, pady=0, padxgrid=0, padygrid=0, row=0, column=0, direction=None):
        """ Creates a frame. """
        if label:
            the_frame = LabelFrame(frame=frame, text=label, padx=padx, pady=pady)
        else:
            the_frame = Frame(frame=frame, padx=padx, pady=pady)
        the_frame.grid(row=row, column=column, padx=padxgrid, pady=padygrid, sticky=direction)