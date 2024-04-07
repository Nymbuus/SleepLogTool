""" Imports. Numpy will be used. """
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider


class PlotAndGraph():
    """ Calculates the statistics that will be shown i graph and the plots it. """

    def __init__(self):
        """ Initializes the class. """

    def calculating_statistics(self, df):
        """ Calculate statistics """
        average = df['Current'].mean()
        maximum = df['Current'].max()
        minimum = df['Current'].min()
        total_time = float(df['Time'].max() - df['Time'].min())
        ampere_hours = (total_time / 3600) * (average * 0.001)

        print(f"\nAverage Current: {average:.3f}mA")
        print(f"Max Current: {maximum} mA")
        print(f"Min Current: {minimum} mA")
        print(f"Total time: {(total_time / 3600):.3f} hours or {(total_time / 60):.1f} minutes.")
        print(f"Ampere hours: {ampere_hours:.4f} Ah")

    def plotting_graph(self, df):
        """ Plotting. """
        first_time = df["Time"].min()
        y = df.Current.to_numpy()
        x = df.Time.to_numpy()
        fig, ax = plt.subplots()
        ax.plot((x - first_time), y, label="LEM")
        #plt.axis([-10, 30, -1000, 71000])
        plt.xlabel("Time(s)", fontsize=15)
        plt.ylabel("Current(mA)", fontsize=15)
        plt.title("Sleeplog analysis", fontsize=24)
        plt.subplots_adjust(left=0.05, bottom=0.25, right=0.97, top=0.955, wspace=None, hspace=None)
        plt.grid()
        axpos = plt.axes([0.2, 0.1, 0.65, 0.03], facecolor='lightgoldenrodyellow')

        spos = Slider(axpos, 'Pos', 0.1, 90.0)

        def update(val):
            pos = spos.val
            print(f"\npos: {pos}\n")
            ax.axis([pos,pos+10,-5.5,120.5])
            fig.canvas.draw_idle()

        spos.on_changed(update)

        manager = plt.get_current_fig_manager()
        manager.window.state('zoomed')

        fig.legend(loc="upper left")

        point, = ax.plot(0, 0, 'ro')
        text = ax.text(0, 0, '', va='bottom')
        x_time_min = min(x)

        def update_point(event):
            if event.inaxes == ax:
                x_mouse = event.xdata

                # np.argmin() takes the smallest value and returns the index.
                plus_x_mouse = x_time_min + x_mouse
                idx = np.argmin(np.abs(x - plus_x_mouse))

                # Update the position of the draggable point
                point.set_xdata(x[idx] - x_time_min)
                point.set_ydata(y[idx])

                # Update the text annotation with coordinates
                text.set_text(f'({x[idx] - x_time_min:.2f}, {y[idx]:.2f})')
                text.set_position((x[idx] - x_time_min, y[idx]))

                fig.canvas.draw_idle()

        fig.canvas.mpl_connect('motion_notify_event', update_point)