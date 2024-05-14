""" Imports. Numpy will be used. """
import matplotlib.pyplot as plt


class PlotAndGraph():
    """ Calculates the statistics that will be shown i graph and the plots it. """

    def __init__(self):
        """ Initializes the class. """
        self.legend = {"LEM":False, "BL":False}


    def plotting_graph(self, plotinfo, time_unit):
        """ Plotting dataframes time and current/busload in one graph for current and one for busload. """
        # Skips ploting a new line but will still check if it's the first or last time this function is called.
        if plotinfo["Skip"] == True:
            if plotinfo["First"] == True:
                self.fig, (self.axLEM, self.axBL) = plt.subplots(2, 1)
            if plotinfo["Last"]:
                self.plot_window(time_unit)
            return
        
        self.dfs = plotinfo["Dfs"]
        self.name = plotinfo["Name"]

        # Will only execute when the the first dfs comes in.
        if plotinfo["First"]:
            # axLEM is graph for the LEM files, axBL is for the BusLoad files.
            self.fig, (self.axLEM, self.axBL) = plt.subplots(2, 1)

        # Plots a line in the LEM or BL graph window.
        if plotinfo["LEM"]:
            self.LEM_plot(time_unit)
            self.legend["LEM"] = True
        elif plotinfo["BL"]:
            self.BL_plot(time_unit)
            self.legend["BL"] = True
        else:
            print("Couldn't find LEM or BL to plot.")

        # Will execute if all lines are plotted.
        if plotinfo["Last"]:
            self.plot_window(time_unit)
    
    def LEM_plot(self, time_unit):
        """ Plots one line for LEM """
        first_time = self.dfs["Time"].min()
        y = self.dfs.Current.to_numpy()
        x = self.dfs.Time.to_numpy()
        self.axLEM.plot(((x - first_time))/time_unit, y,
                         label=f"{self.name}  "+
                             f" Avg: {self.dfs['Current'].mean():.2f} mA,"+
                             f" Max: {self.dfs['Current'].max():.2f} mA,"+
                             f" Min: {self.dfs['Current'].min():.2f} mA")

    def BL_plot(self, time_unit):
        """ Plots one line for BusLoad """
        first_time = self.dfs["Time"].min()
        y = self.dfs.Busload.to_numpy()
        x = self.dfs.Time.to_numpy()
        self.axBL.plot(((x - first_time))/time_unit, y,
                        label=f"{self.name}  "+
                              f" Avg: {self.dfs['Busload'].mean():.2f} %,"+
                              f" Max: {self.dfs['Busload'].max():.2f} %,"+
                              f" Min: {self.dfs['Busload'].min():.2f} %")


    def plot_window(self, time_unit):
        """ Plots the graphwindow. """
        time_unit_character = None

        # Checks what time unit to put in x-axis.
        match time_unit:
            case 1:
                time_unit_character = "s"
            case 60:
                time_unit_character = "m"
            case 3600:
                time_unit_character = "h"
        
        # Plots all labels in graph.
        plt.xlabel(f"Time[{time_unit_character}]", fontsize=15)
        self.axLEM.set_ylabel("Current[mA]", fontsize=15)
        self.axBL.set_ylabel("BusLoad[%]", fontsize=15)
        self.axLEM.set_title("CAN Bus Analysis", fontsize=24)

        # Adjusts the graph frames.
        plt.subplots_adjust(left=0.25, bottom=0.05, right=0.97, top=0.955, wspace=None, hspace=0.1)

        # Adds the grid to both graphs.
        self.axLEM.grid(which = "major", linewidth = 1)
        self.axLEM.grid(which = "minor", linewidth = 0.4)
        self.axLEM.minorticks_on()
        self.axLEM.tick_params(which = "minor", bottom = False, left = False)
        self.axBL.grid(which = "major", linewidth = 1)
        self.axBL.grid(which = "minor", linewidth = 0.4)
        self.axBL.minorticks_on()
        self.axBL.tick_params(which = "minor", bottom = False, left = False)

        # Sets window in fullscreen.
        manager = plt.get_current_fig_manager()
        manager.window.state('zoomed')

        # Checks if there's LEM and BusLoad file in the plots to display their legend.
        if self.legend["LEM"]:
            self.axLEM.legend(bbox_to_anchor=(-0.34, 1), loc="upper left")
        if self.legend["BL"]:
            self.axBL.legend(bbox_to_anchor=(-0.34, 1), loc="upper left")
        self.legend = {"LEM":False, "BL":False}
        