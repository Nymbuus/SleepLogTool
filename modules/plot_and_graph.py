from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import tkinter as tk


class PlotAndGraph():
    """ Plotting the graphs window. """

    def __init__(self):
        """ Initializes the class. """
        self.legend = {"LEM": False, "BL": False}
        self.window = None

    def plotting_graph(self, dfs, time_unit):
        """ Plotting dataframes time and current/busload in one graph for current and one for busload. """
        for df in dfs:
            if df["Info"]["Skip"]:
                if df["Info"]["First_df"]:
                    self.chosen_graphs(df)
                if df["Info"]["Last_df"]:
                    self.plot_window(dfs, time_unit)
                return
            
            self.name = df["Info"]["Name"]

            if df["Info"]["First_df"]:
                self.chosen_graphs(df)

            if df["Info"]["isLEM"]:
                self.x_data, self.y_data = self.LEM_plot(df, time_unit)
                self.legend["LEM"] = True
            elif df["Info"]["isBL"]:
                self.BL_plot(df, time_unit)
                self.legend["BL"] = True
            else:
                print("Couldn't find LEM or BL to plot.")

            if df["Info"]["Last_df"]:
                self.plot_window(dfs, time_unit)

                # Embed the figure in Tkinter using FigureCanvasTkAgg
                self.canvas = FigureCanvasTkAgg(self.fig, master=self.window)
                self.canvas.draw()
                self.canvas.get_tk_widget().grid(row=0, column=0)

                # Bind hover event to on_hover function
                self.canvas.mpl_connect("motion_notify_event", self.on_hover)

    def on_hover(self, event):
        print(self.x_data[0], self.y_data[0])
        if event.inaxes:  # Check if hovering over an axis
            x, y = event.xdata, event.ydata
            if x is not None and y is not None:  # Ensure x, y are within plot bounds
                    print(f"Hovering at ({x:.2f}, {y})")  # Display rounded coordinates

    def LEM_plot(self, df, time_unit):
        """ Plots one line for LEM """
        first_time = df["df"]["Time"].min()
        data = df["df"]
        y = data.Current.to_numpy()
        x = data.Time.to_numpy()

        x = (x - first_time) / time_unit
        if df["Info"]["LEM_invert"]:
            y = y * -1

        self.axLEM.plot(x, y,
                        label=f"{self.name}  " +
                              f" Avg: {y.mean():.1f} mA," +
                              f" Max: {y.max():.1f} mA," +
                              f" Min: {y.min():.1f} mA")
        
        return x, y

    def BL_plot(self, df, time_unit):
        """ Plots one line for BusLoad """
        first_time = df["df"]["Time"].min()
        data = df["df"]
        y = data.Busload.to_numpy()
        x = data.Time.to_numpy()

        x = (x - first_time) / time_unit

        self.axBL.plot(x, y,
                       label=f"{self.name}  " +
                             f" Avg: {y.mean():.2f} %," +
                             f" Max: {y.max():.2f} %," +
                             f" Min: {y.min():.2f} %")

    def plot_window(self, dfs, time_unit):
        """ Plots the graph window. """
        time_unit_character = {1: "s", 60: "m", 3600: "h"}.get(time_unit, "s")

        plt.xlabel(f"Time[{time_unit_character}]", fontsize=15)
        if dfs[0]["Info"]["LEM_graph"]:
            self.axLEM.set_ylabel("Current[mA]", fontsize=15)
            self.axLEM.set_title("CAN Bus Analysis", fontsize=24)
        if dfs[0]["Info"]["BL_graph"]:
            self.axBL.set_ylabel("BusLoad[%]", fontsize=15)
            if not dfs[0]["Info"]["LEM_graph"]:
                self.axBL.set_title("CAN Bus Analysis", fontsize=24)

        plt.subplots_adjust(left=0.33, bottom=0.05, right=0.97, top=0.955,
                            wspace=None, hspace=0.1 if dfs[0]["Info"]["LEM_graph"] and dfs[0]["Info"]["BL_graph"] else None)

        if dfs[0]["Info"]["LEM_graph"]:
            self.axLEM.grid(which="major", linewidth=1)
            self.axLEM.grid(which="minor", linewidth=0.4)
            self.axLEM.minorticks_on()
            self.axLEM.tick_params(which="minor", bottom=False, left=False)
        if dfs[0]["Info"]["BL_graph"]:
            self.axBL.grid(which="major", linewidth=1)
            self.axBL.grid(which="minor", linewidth=0.4)
            self.axBL.minorticks_on()
            self.axBL.tick_params(which="minor", bottom=False, left=False)

        manager = plt.get_current_fig_manager()
        manager.window.state('zoomed')

        if self.legend["LEM"] and dfs[0]["Info"]["LEM_graph"]:
            self.axLEM.legend(bbox_to_anchor=(-0.51, 1), loc="upper left")
        if self.legend["BL"] and dfs[0]["Info"]["BL_graph"]:
            self.axBL.legend(bbox_to_anchor=(-0.51, 1), loc="upper left")
        self.legend = {"LEM": False, "BL": False}

    def chosen_graphs(self, df):
        """ Decides which graphs are used. """
        
        if df["Info"]["LEM_graph"] and df["Info"]["BL_graph"]:
            self.fig, (self.axLEM, self.axBL) = plt.subplots(2, 1)
        elif df["Info"]["LEM_graph"]:
            self.fig, self.axLEM = plt.subplots()
        elif df["Info"]["BL_graph"]:
            self.fig, self.axBL = plt.subplots()
        else:
            raise NameError
