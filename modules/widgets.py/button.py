from tkinter import *

class MyButton:

    def __init__(self, frame, text="", padx=0, pady=0, padxgrid=0, padygrid=0, command=None, row=0, column=0, direction=None):
        """ Creates a TKinter button """
        button = Button(frame, text=text, padx=padx, pady=pady, command=command)
        button.grid(row=row, column=column, padx=padxgrid, pady=padygrid, sticky=direction)