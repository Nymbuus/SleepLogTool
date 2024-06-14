from tkinter import *

class MyCheckbutton:

    def __init__(self, frame, text, int_variable):
        """ Creates a TKinter checkbutton. """
        if int_variable == True:

        checkbutton = Checkbutton(frame, text=text, variable=variable)