from tkinter import *

CAN_BUSES = ("Body", "Front1", "Front3", "Mid1", "Rear1", "Lem")

class BusSelectionMenu(Toplevel):
    """ Creates the Bus selection window for selecting the buses that the user wants to extract. """

    def __init__(self, parent, add_file_path_func):
        super().__init__(parent)
        self.title("Bus Selection")
        self.bus_cbs = []
        self.cbs_checked = []
        self.buses_checked = []
        self.add_file_path = add_file_path_func
        self.menu_setup()


    def menu_setup(self):
        self.bus_checkbuttons()
        self.navi_buttons()


    def bus_checkbuttons(self):
        checkbuttons_frame = Frame(self)
        checkbuttons_frame.grid(row=0, column=0, pady=10)
        top_text_label = Label(checkbuttons_frame, text="Choose buses to extract")
        top_text_label.grid(row=0, column=0, columnspan=2, pady=(0, 15))

        can_bus_counter = 0
        for i in range(1,4):
            for j in range(2):
                cb_checked = BooleanVar()
                bus_cb = Checkbutton(checkbuttons_frame,
                                    text=CAN_BUSES[can_bus_counter],
                                    variable=cb_checked,
                                    onvalue=True,
                                    offvalue=False)
                bus_cb.grid(row=i, column=j, padx=5, sticky="w")
                self.cbs_checked.append(cb_checked)
                self.bus_cbs.append(bus_cb)
                can_bus_counter += 1


    def navi_buttons(self):
        navi_buttons_frame = Frame(self)
        navi_buttons_frame.grid(row=1, column=0, padx=10, pady=10)
        add_busses_button = Button(navi_buttons_frame,
                                   text="Extract Busses",
                                   command=self.add_buses)
        add_busses_button.grid(row=0, column=0, sticky="e")
        cancel_button = Button(navi_buttons_frame,
                               text="Cancel",
                               command=self.destroy)
        cancel_button.grid(row=0, column=1, padx=(10,0))


    def add_buses(self):
        for i, cb_checked in enumerate(self.cbs_checked):
            bus_checked = cb_checked.get()
            if bus_checked:
                bus = CAN_BUSES[i]
                self.buses_checked.append(bus)
        
        self.add_file_path("extract bus", self.buses_checked)
        self.destroy()
