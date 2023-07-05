import tkinter as tk
from tkinter import ttk
from tkinter import *
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
import csv

df = pd.read_csv('Dataset/20200118/310/summary.csv')

print(df.head(10))

x = []
y = []

with open('Dataset/20200118/310/summary.csv','r') as csvfile:
    lines = csv.reader(csvfile, delimiter=',')
    for row in lines:
        x.append(row[0])
        y.append((row[6]))


class Graphy(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Graphy")
        self.frames = dict()

        container = ttk.Frame(self)
        container.grid(padx=60, pady=30, sticky="EW")

        for FrameClass in (Graph, Chart):
            frame = FrameClass(container, self)
            self.frames[FrameClass] = frame
            frame.grid(row=0, column=0, sticky="NSEW")

        self.show_frame(Graph)

    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()

    


class Graph(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)

        frame = LabelFrame(self, padx=50, pady=50)
        frame.pack(padx=10, pady=10)

        def plot():
            fig = Figure(figsize = (5, 5), dpi = 100)
            # adding the subplot
            plot1 = fig.add_subplot(111)
            # plotting the graph
            plot1.plot(x,y)
  
            # creating the Tkinter canvas
            # containing the Matplotlib figure
            canvas = FigureCanvasTkAgg(fig, frame)  
            canvas.draw()
            canvas.get_tk_widget().grid(row=1, sticky="EW")

  
            # !!!Not Working!!!
            # creating the Matplotlib toolbar
            # toolbar = NavigationToolbar2Tk(canvas, window)
            # toolbar.update()
            # canvas.get_tk_widget().pack()

        plot_button = Button(frame, text="Graph", command = plot, height = 2, width = 10)
        plot_button.grid(row=0, column=0)
        swap_button = Button(frame, text="Swap", height=2, width=10,
                             command=lambda: controller.show_frame("Chart"))
        swap_button.grid(row=0, column=1)


class Chart(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)

        frame = LabelFrame(self, padx=50, pady=50)
        frame.pack(padx=10, pady=10)

        b = Button(frame, text="Chart")
        b.grid(row=0, column=0)


root = Graphy()
root.mainloop()
