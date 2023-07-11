import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
import csv
import numpy as np
import torch

df = pd.read_csv('Dataset/20200118/310/summary.csv', nrows=2)

print(df.head(10))

x = []
y = []
Date = []
Acc = []
Eda = []
Temp = []
Mvmt = []
Step = []
Rest = []
On = []


with open('Dataset/20200118/310/summary.csv', 'r') as csvfile:
    lines = csv.reader(csvfile, delimiter=',')
    for row in lines:
        x.append(row[0])
        y.append(row[6])
        Date.append(row[0])
        Acc.append(row[3])
        Eda.append(row[4])
        Temp.append(row[5])
        Mvmt.append(row[6])
        Step.append(row[7])
        Rest.append(row[8])
        On.append(row[9])


def select_file():
    filetypes = (
        ('text files', '*.txt'),
        ('All files', '*.*')
    )
    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)
    # showinfo(
    #     title='Selected File',
    #     message=filename
    # )


class Graphy(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Graphy")
        self.frames = dict()

        container = LabelFrame(self, bg='blue', bd=2)
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

        frame = LabelFrame(self, padx=50, pady=50, bg="light blue")
        frame.grid(padx=10, pady=10, sticky="NSEW")

        def plot():
            fig = Figure(figsize=(5, 5), dpi=100)
            # adding the subplots
            plot1 = fig.add_subplot(111)
            # plotting the graph
            plot1.plot(x, y)
            # creating the Tkinter canvas
            # containing the Matplotlib figure
            canvas = FigureCanvasTkAgg(fig, frame)
            # canvas.draw()
            canvas.get_tk_widget().grid(row=1, sticky="EW")

            # !!!Not Working!!!
            # creating the Matplotlib toolbar
            # toolbar = NavigationToolbar2Tk(canvas, window)
            # toolbar.update()
            # canvas.get_tk_widget().pack()

        plot_button = Button(frame, text="Graph", command=plot, height=2, width=10)
        plot_button.grid(row=0, column=0)
        switch_page_button = Button(
            self,
            text="Switch to Chart",
            command=lambda: controller.show_frame(Chart)
        )
        switch_page_button.grid(column=0, row=1, columnspan=2, sticky="EW")


class Chart(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)

        frame = LabelFrame(self, padx=50, pady=50)
        frame.grid(padx=10, pady=10, sticky="NSEW")

        b = Button(frame, text="Chart")
        b.grid(row=0, column=0)
        switch_page_button = Button(
            self,
            text="Switch to Graph",
            command=lambda: controller.show_frame(Graph)
        )
        switch_page_button.grid(column=0, row=1, columnspan=2, sticky="EW")


root = Graphy()
root.geometry('800x800')
root.mainloop()
