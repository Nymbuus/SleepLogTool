""" Imports. Numpy will be used. """
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.widgets import Slider


class PlotAndGraph():
    """ Calculates the statistics that will be shown i graph and the plots it. """

    def __init__(self):
        """ Initializes the class. """


    def plotting_graph(self, plotinfo):
        """ Plotting. """
        self.dfs = plotinfo["Dfs"]
        self.name = plotinfo["Name"]

        # Will only execute when the the first dfs comes in.
        if plotinfo["First"]:
            # axLEM is graph for the LEM files, axBL is for the BusLoad files.
            self.fig, (self.axLEM, self.axBL) = plt.subplots(2, 1)

        # Plots a line in the LEM or BL graph window.
        if plotinfo["LEM"]:
            self.LEM_plot()
        elif plotinfo["BL"]:
            self.BL_plot()
        else:
            print("Couldn't find LEM or BL to plot.")

        # Will execute if all lines are plotted.
        if plotinfo["Last"]:
            self.plot_window()
    
    def LEM_plot(self):
        """ Plots one line for LEM """
        first_time = self.dfs["Time"].min()
        y = self.dfs.Current.to_numpy()
        x = self.dfs.Time.to_numpy()
        self.axLEM.plot((x - first_time), y,
                label=f"{self.name}  "+
                    f" Avg: {self.dfs['Current'].mean():.2f} mA,"+
                    f" Max: {self.dfs['Current'].max():.2f} mA,"+
                    f" Min: {self.dfs['Current'].min():.2f} mA")

    def BL_plot(self):
        """ Plots one line for BusLoad """
        first_time = self.dfs["Time"].min()
        y = self.dfs.Busload.to_numpy()
        x = self.dfs.Time.to_numpy()
        self.axBL.plot((x - first_time), y,
                label=f"{self.name}  "+
                    f" Avg: {self.dfs['Busload'].mean():.2f} %,"+
                    f" Max: {self.dfs['Busload'].max():.2f} %,"+
                    f" Min: {self.dfs['Busload'].min():.2f} %")

    def plot_window(self):
        """ Plots the graphwindow. """
        plt.xlabel("Time[s]", fontsize=15)
        self.axLEM.set_ylabel("Current[mA]", fontsize=15)
        self.axBL.set_ylabel("BusLoad[%]", fontsize=15)
        plt.title("CAN Bus Analysis", fontsize=24)
        plt.subplots_adjust(left=0.25, bottom=0.05, right=0.97, top=0.955, wspace=None, hspace=0.2)

        self.axLEM.grid(which = "major", linewidth = 1)
        self.axLEM.grid(which = "minor", linewidth = 0.4)
        self.axLEM.minorticks_on()
        self.axLEM.tick_params(which = "minor", bottom = False, left = False)
        manager = plt.get_current_fig_manager()
        manager.window.state('zoomed')
        self.fig.legend(loc="upper left")