import matplotlib.pyplot as plt


class PlotAndGraph():
    """ Plotting the graphs window. """

    def __init__(self):
        """ Initializes the class. """
        self.legend = {"LEM":False, "BL":False}


    def plotting_graph(self, plotinfo, time_unit):
        """ Plotting dataframes time and current/busload in one graph for current and one for busload. """

        self.plotinfo = plotinfo

        # Skips ploting a new line but will still check if it's the first or last time this function is called.
        if plotinfo["Skip"]:
            if plotinfo["First"]:
                self.chosen_graphs()
            if plotinfo["Last"]:
                self.plot_window(time_unit)
            return
        
        self.dfs = plotinfo["Dfs"]
        self.name = plotinfo["Name"]

        # Will only execute when the the first dfs comes in.
        if plotinfo["First"]:
            self.chosen_graphs()

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

        # preps x and y for plotting.
        x = x - first_time
        x = x / time_unit
        if self.plotinfo["LEM_invert"]:
            y = y * (-1)

        self.axLEM.plot(x, y,
                        label=f"{self.name}  "+
                              f" Avg: {y.mean():.1f} mA,"+
                              f" Max: {y.max():.1f} mA,"+
                              f" Min: {y.min():.1f} mA")

    def BL_plot(self, time_unit):
        """ Plots one line for BusLoad """
        first_time = self.dfs["Time"].min()
        y = self.dfs.Busload.to_numpy()
        x = self.dfs.Time.to_numpy()

        # preps x for plotting.
        x = x - first_time
        x = x / time_unit

        self.axBL.plot(x, y,
                       label=f"{self.name}  "+
                             f" Avg: {y.mean():.2f} %,"+
                             f" Max: {y.max():.2f} %,"+
                             f" Min: {y.min():.2f} %")


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
        if (self.plotinfo["LEM_graph"] and self.plotinfo["BL_graph"]) or self.plotinfo["LEM_graph"]:
            self.axLEM.set_ylabel("Current[mA]", fontsize=15)
            self.axLEM.set_title("CAN Bus Analysis", fontsize=24)
        else:
            self.axBL.set_ylabel("BusLoad[%]", fontsize=15)
            self.axBL.set_title("CAN Bus Analysis", fontsize=24)

        # Adjusts the graph frames.
        if self.plotinfo["LEM_graph"] and self.plotinfo["BL_graph"]:
            plt.subplots_adjust(left=0.33, bottom=0.05, right=0.97, top=0.955, wspace=None, hspace=0.1)
        else:
            plt.subplots_adjust(left=0.33, bottom=0.05, right=0.97, top=0.955)

        # Adds the grid to both graphs.
        if self.plotinfo["LEM_graph"]:
            self.axLEM.grid(which = "major", linewidth = 1)
            self.axLEM.grid(which = "minor", linewidth = 0.4)
            self.axLEM.minorticks_on()
            self.axLEM.tick_params(which = "minor", bottom = False, left = False)
        if self.plotinfo["BL_graph"]:
            self.axBL.grid(which = "major", linewidth = 1)
            self.axBL.grid(which = "minor", linewidth = 0.4)
            self.axBL.minorticks_on()
            self.axBL.tick_params(which = "minor", bottom = False, left = False)

        # Sets window in fullscreen.
        manager = plt.get_current_fig_manager()
        manager.window.state('zoomed')

        # Checks if there's LEM and BusLoad file in the plots to display their legend.
        if self.legend["LEM"] and self.plotinfo["LEM_graph"]:
            self.axLEM.legend(bbox_to_anchor=(-0.51, 1), loc="upper left")
        if self.legend["BL"] and self.plotinfo["BL_graph"]:
            self.axBL.legend(bbox_to_anchor=(-0.51, 1), loc="upper left")
        self.legend = {"LEM":False, "BL":False}
        

    def chosen_graphs(self):
        """ Decides which graphs are used. """
        
        # axLEM is graph for the LEM files, axBL is for the BusLoad files.
        if self.plotinfo["LEM_graph"] and self.plotinfo["BL_graph"]:
            self.fig, (self.axLEM, self.axBL) = plt.subplots(2, 1)
        elif self.plotinfo["LEM_graph"]:
            self.fig, self.axLEM = plt.subplots()
        elif self.plotinfo["BL_graph"]:
            self.fig, self.axBL = plt.subplots()
        else:
            raise NameError