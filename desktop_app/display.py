import tkinter as tk

from typing import Dict, List
from threading import Timer
from matplotlib.animation import FuncAnimation

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib.backend_bases import MouseButton

import matplotlib.pyplot as plt
import numpy as np

REDRAW_FREQUENCY = 10
pause = False

class Display:
    # Helper functions
    def _root_init(self):
        self.root = tk.Tk()
        self.root.wm_title("iGEM uWaterloo 2021 Desktop App")
        self.root.attributes("-fullscreen", True)

        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.dpi = self.root.winfo_fpixels("1i")

    def _graph_init(self):
        self.graph = tk.Frame(master=self.root)
        self.graph.pack()

    def _info_readouts_init(self):
        self.info_readouts = tk.Frame(master=self.root)
        self.info_readouts.pack()

    def _controls_init(self):
        self.controls = tk.Frame(master=self.root)
        self.controls.pack()

    def _info_label_init(self):
        self.info_label = tk.Label(self.info_readouts, text="Hello World")
        self.info_label.pack()

    def _graph_figure_init(self):
        self.graph_figure = Figure(
            figsize=(
                self.screen_width / self.dpi,
                self.screen_height * 0.85 / self.dpi,
            ),
            dpi=self.dpi,
        )

    def plot(self):
        # TODO: Write a function to make the below nice
        # Plot by doing self.axis.plot() or if accessed externally:
        # d = Display()
        # d.axis.plot()

        x = np.arange(0, 25,0.1)
        self.graph_figure, (ax0, ax1) = plt.subplots(nrows=1, ncols=2, sharex=True, sharey=True)
        
        ax0.plot(np.cos(x))
        ax1.plot(np.sin(x))

        ax0.set_xlim([0, 200])
        ax0.set_ylim([-100, 100])

        ax0.set_ylabel('Concentration')
        ax0.set_xlabel('Time')
        ax1.set_xlabel('Time')

        self.graph_figure.canvas.mpl_connect('button_press_event', DisplayController.handle_graph_clicked)
        
        self.canvas = FigureCanvasTkAgg(self.graph_figure, master=self.graph)  # A tk.DrawingArea.
        # self.axis.cla() # clear axis before drawing
        self.canvas.draw()

    def _graph_toolbar_init(self):
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.graph, pack_toolbar=False)
        self.toolbar.update()

        self.toolbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def _buttons_init(self):
        # Add buttons with appropriate methods linked
        self.quit_button = tk.Button(master=self.controls, text="Quit", command=self.root.quit)
        self.quit_button.pack(side=tk.BOTTOM)

        # Below button needs to be assigned a command
        self.continue_button = tk.Button(master=self.controls, text="Continue Drawing")
        self.continue_button.pack(side=tk.BOTTOM)

    def __init__(self):

        self._root_init()

        # Set up frames to store the graph, info readout (text, data summaries, etc), and buttons for user input

        self._graph_init()
        self._info_readouts_init()
        self._controls_init()  # buttons

        # Set up text label for info window
        self._info_label_init()

        # Set up graph
        self._graph_figure_init()
        self.plot()
        self._graph_toolbar_init()

        self._buttons_init()

    @staticmethod
    def start_display():
        tk.mainloop()


class DisplayController:

    def __init__(self, display: Display):

        # Map graph titles to data
        self.graphs = dict()  # type: Dict[str, List[float]]

        # Which graphs we should draw
        self.graphs_to_draw = []  # type: List[str]

        # -- Pause and function for later
        self.display = display
        self.display.graph_figure.canvas.callbacks.connect('button_press_event', self.handle_graph_clicked)
        self.display.continue_button.configure(command=self.start_redraw_loop)

        self.do_redraw = False  # type: bool
        self.redraw_timer = None
        self.start_redraw_loop()

    def accept_data(self, graph_title: str, data: float):
        current_data = self.graphs.get(graph_title, [])
        current_data.append(data)
        self.graphs[graph_title] = current_data

    # -- Start here, redraw_loop() is called back 0.1 Hz
    def start_redraw_loop(self):
        self.do_redraw = True
        self.redraw_timer = Timer(1 / REDRAW_FREQUENCY, self._redraw_loop)
        self.redraw_timer.daemon = True  # Kill the timer when the program exits
        self.redraw_timer.start()

    def stop_redraw_loop(self):
        self.do_redraw = False
        if self.redraw_timer:
            self.redraw_timer.cancel()
            self.redraw_timer = None

    # -- Looped function
    def _redraw_loop(self):
        for graph_title in self.graphs_to_draw:
            graph = self.graphs[graph_title]
            # TODO: Draw each graph

            plt.cla()
            self.ax0.plot(graph)

        if self.do_redraw:
            self.redraw_timer = Timer(1 / REDRAW_FREQUENCY, self._redraw_loop)
            self.redraw_timer.daemon = True  # Kill the timer when the program exits
            self.redraw_timer.start()

    def handle_graph_clicked(self, event):
        # TODO: Pause drawing
        self.stop_redraw_loop()


