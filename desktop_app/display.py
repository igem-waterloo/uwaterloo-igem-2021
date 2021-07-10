import tkinter as tk

from typing import Dict, List
from threading import Timer

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib.backend_bases import MouseButton

REDRAW_FREQUENCY = 10


class Display:

    def __init__(self):

        # TODO: Separate this into several functions?

        self.root = tk.Tk()
        self.root.wm_title("iGEM uWaterloo 2021 Desktop App")
        self.root.attributes("-fullscreen", True)

        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.dpi = self.root.winfo_fpixels('1i')

        # Frames to store the graph, info readout (text, data summaries, etc), and buttons for user input
        self.graph = tk.Frame(self.root)
        self.info_window = tk.Frame(self.root)  # meant info readouts
        self.controls = tk.Frame(self.root)  # buttons

        self.graph.pack()
        self.info_window.pack()
        self.controls.pack()

        # Text label for info window
        self.info_label = tk.Label(self.info_window, text="Hello World")
        self.info_label.pack()

        self.graph_figure = Figure(
            figsize=(self.screen_width / self.dpi, self.screen_height * 0.85 / self.dpi),
            dpi=self.dpi
        )

        # TODO: Write a function to make the below nice
        # Plot by doing self.axis.plot() or if accessed externally:
        # d = Display()
        # d.axis.plot()
        self.axis = self.graph_figure.add_subplot()

        self.canvas = FigureCanvasTkAgg(self.graph_figure, master=self.graph)  # A tk.DrawingArea.
        self.canvas.draw()

        # Add toolbar to graph
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.graph, pack_toolbar=False)
        self.toolbar.update()

        self.toolbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Add buttons with appropriate methods linked
        self.quit_button = tk.Button(master=self.controls, text="Quit", command=self.root.quit)
        self.quit_button.pack(side=tk.BOTTOM)

        # Below button needs to be assigned a command
        self.continue_button = tk.Button(
            master=self.controls,
            text="Continue Drawing",
        )
        self.continue_button.pack(side=tk.BOTTOM)

    @staticmethod
    def start_display():
        tk.mainloop()


class DisplayController:

    def __init__(self, display: Display):

        # Map graph titles to data
        self.graphs = dict()  # type: Dict[str, List[float]]

        # Which graphs we should draw
        self.graphs_to_draw = []  # type: List[str]

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

    def _redraw_loop(self):
        for graph_title in self.graphs_to_draw:
            graph = self.graphs[graph_title]
            # TODO: Draw each graph

        if self.do_redraw:
            self.redraw_timer = Timer(1 / REDRAW_FREQUENCY, self._redraw_loop)
            self.redraw_timer.daemon = True  # Kill the timer when the program exits
            self.redraw_timer.start()

    def handle_graph_clicked(self, event):
        # TODO: Pause drawing
        pass
