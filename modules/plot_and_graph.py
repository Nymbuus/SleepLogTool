""" Imports. Numpy will be used. """
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.widgets import Slider


class PlotAndGraph():
    """ Calculates the statistics that will be shown i graph and the plots it. """

    def __init__(self):
        """ Initializes the class. """
        self.index = 1


    def plotting_graph(self, dfs, filename, stats, first_dfs, last_dfs):
        """ Plotting. """
        # Will only execute when the the first dfs comes in.
        if first_dfs:
            self.fig, self.ax = plt.subplots()

        first_time = dfs["Time"].min()
        y = dfs.Current.to_numpy()
        x = dfs.Time.to_numpy()
        # CAN_channel = filename[0][-7:-4]             This is used if the name of the file isn't modified.
        CAN_channel = f"LEM{self.index}"
        self.index += 1
        self.ax.plot((x - first_time), y,
                label=f"{CAN_channel}  "+
                    f" Avg: {dfs['Current'].mean():.2f} mA,"+
                    f" Max: {dfs['Current'].max():.2f} mA,"+
                    f" Min: {dfs['Current'].min():.2f} mA\n"+
                    f" Avg: {stats[0].mean():.2f} mA,"+
                    f" Max: {stats[1].max():.2f} mA,"+
                    f" Min: {stats[2].min():.2f} mA")

        # Will execute if all lines are plotted.
        if last_dfs:
            plt.xlabel("Time(s)", fontsize=15)
            plt.ylabel("Current(mA)", fontsize=15)
            plt.title("Sleeplog analysis", fontsize=24)
            plt.subplots_adjust(left=0.25, bottom=0.05, right=0.97, top=0.955, wspace=None, hspace=None)
            self.ax.grid(which = "major", linewidth = 1)
            self.ax.grid(which = "minor", linewidth = 0.4)
            self.ax.minorticks_on()
            self.ax.tick_params(which = "minor", bottom = False, left = False)
            manager = plt.get_current_fig_manager()
            manager.window.state('zoomed')
            self.fig.legend(loc="upper left")

        return

        # point, = ax.plot(0, 0, 'ro')
        # text = ax.text(0, 0, '', va='bottom')
        # x_time_min = min(x)

        # def update_point(event):
        #     if event.inaxes == ax:
        #         x_mouse = event.xdata

        #         # np.argmin() takes the smallest value and returns the index.
        #         plus_x_mouse = x_time_min + x_mouse
        #         idx = np.argmin(np.abs(x - plus_x_mouse))

        #         # Update the position of the draggable point
        #         point.set_xdata(x[idx] - x_time_min)
        #         point.set_ydata(y[idx])

        #         # Update the text annotation with coordinates
        #         text.set_text(f'({x[idx] - x_time_min:.2f}s, {y[idx]:.2f}mA)')
        #         text.set_position((x[idx] - x_time_min, y[idx]))

        #         fig.canvas.draw_idle()

        # fig.canvas.mpl_connect('motion_notify_event', update_point)