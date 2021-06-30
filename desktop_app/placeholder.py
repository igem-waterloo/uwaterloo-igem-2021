import tkinter as tk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib.backend_bases import MouseButton

import numpy as np
from threading import Timer


root = tk.Tk()
root.wm_title("iGEM uWaterloo 2021 Desktop App")
root.attributes("-fullscreen", True)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
dpi = root.winfo_fpixels('1i')

# True if we are updating the graph
do_redraw = True

# Frames to store the graph, info readout (text, data summaries, etc), and buttons for user input
graph = tk.Frame(root)
info_window = tk.Frame(root)
controls = tk.Frame(root)

graph.pack()
info_window.pack()
controls.pack()

# Text label for info window
info = tk.Label(info_window, text="Hello World")
info.pack()

# Almost fullscreen figure for graph
fig = Figure(figsize=(screen_width / dpi,  screen_height * 0.85 / dpi), dpi=dpi)
t = np.arange(0, 3, .01)
axis = fig.add_subplot()
axis.plot(t, 2 * np.sin(2 * np.pi * t))

canvas = FigureCanvasTkAgg(fig, master=graph)  # A tk.DrawingArea.
canvas.draw()


def clicku(event):
    """
    To be triggered whenever the graph is clicked. Pauses graph updates while the user manipulates the graph.
    :param event: Data about a click event on the graph
    :return: Nothing
    """
    global do_redraw, info

    if event.button in [MouseButton.LEFT, MouseButton.RIGHT] and do_redraw:
        info.configure(text="User interrupt. Pausing graph updates...")
        do_redraw = False


def continue_drawing():
    """
    Starts to update the graph again if it wasn't being updated before
    :return: Nothing
    """
    global do_redraw, info
    if do_redraw:
        info.configure(text="Already updating graph.")
    else:
        info.configure(text="Continuing graph updates...")
        do_redraw = True


# Stop graph updates when graph is clicked
fig.canvas.callbacks.connect('button_press_event', clicku)


def update_graph(ax, shtuff):
    """
    Computes data for the graph and displays it to axis ax. Shtuff is an X offset for the generated date.
    This function will call itself every 0.1 seconds until the program ends.
    :param ax: Axis to update
    :param shtuff: X offset for data generation
    :return: Nothing
    """
    g = np.arange(shtuff - 3, shtuff, .01)

    if do_redraw:
        ax.cla()
        ax.plot(g, 2 * np.sin(2 * np.pi * g) + g / 10)
        canvas.draw()

    tim = Timer(0.1, update_graph, [ax, shtuff + 0.1])
    tim.daemon = True
    tim.start()


# Start graph update loop
update_graph(axis, 3)

# Add toolbar to graph
toolbar = NavigationToolbar2Tk(canvas, graph, pack_toolbar=False)
toolbar.update()

toolbar.pack(side=tk.BOTTOM, fill=tk.X)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Add buttons with appropriate methods linked
tk.Button(master=controls, text="Quit", command=root.quit).pack(side=tk.BOTTOM)
tk.Button(master=controls, text="Continue Drawing", command=continue_drawing).pack(side=tk.BOTTOM)

# Start the GUI
tk.mainloop()
