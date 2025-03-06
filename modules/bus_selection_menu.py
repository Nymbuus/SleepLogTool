from tkinter import *

CAN_BUSES = ("Body", "Front1", "Front3", "Mid1", "Rear1", "Lem")

class BusSelectionMenu(Toplevel):
    """ Creates the Bus selection window for selecting the buses that the user wants to extract. """

    def __init__(self, parent):
        super().__init__(parent)
        self.title("Bus Selection")
        self.geometry("200x200")
        self.bus_cbs = []
        self.cbs_checked = []
        self.bus_checkbuttons()

    def bus_checkbuttons(self):
        for i in range(6):
            cb_checked = BooleanVar()
            bus_cb = Checkbutton(self,
                                 text=CAN_BUSES[i],
                                 variable=cb_checked,
                                 onvalue=True,
                                 offvalue=False)
            bus_cb.grid(row=i, column=0)
            self.cbs_checked.append(cb_checked)
            self.bus_cbs.append(bus_cb)