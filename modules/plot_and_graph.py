""" Imports. Numpy will be used. """
import matplotlib.pyplot as plt
import numpy as np


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
        ax.plot((x - first_time) / 3600, y)
        plt.axis([-0.000001, 0.000025, -1000, 71000])
        plt.xlabel("Time(h)", fontsize=15)
        plt.ylabel("Current(mA)", fontsize=15)
        plt.title("Sleeplog analysis", fontsize=24)
        plt.subplots_adjust(left=0.05, bottom=0.06, right=0.97, top=0.955, wspace=None, hspace=None)
        plt.grid()
        manager = plt.get_current_fig_manager()
        manager.window.state('zoomed')

        # Create a draggable point
        point, = ax.plot(0, np.sin(0), 'ro')  # Starting point at x=3

        # Create a text annotation for displaying coordinates
        text = ax.text(0, 0, 'hej', va='bottom')

        def update_point(event):
            if event.inaxes == ax:
                x_mouse = event.xdata

                # First x_mouse value is subtracted from all x elements.
                # Then np.abs() makes converts all results to absolutes.
                # Then np.argmin() takes the smallest value and returns the index.
                # This index is then used to get the the value from the x and y arrays.
                npabs = np.abs(x - x_mouse)
                idx = np.argmin(np.abs(x - x_mouse))
                print(idx)
                print(x[6])
                x_closest = x[idx]
                y_closest = y[idx]

                # Update the position of the draggable point
                point.set_xdata(x_closest)
                point.set_ydata(y_closest)

                # Update the text annotation with coordinates
                text.set_text(f'({x_closest:.2f}, {y_closest:.2f})')
                text.set_position((x_closest, y_closest))
                text.set_va('bottom')

                fig.canvas.draw_idle()

        fig.canvas.mpl_connect('motion_notify_event', update_point)

        plt.show()
