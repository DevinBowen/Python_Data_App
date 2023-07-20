import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backend_tools import ToolBase, ToolToggleBase
import csv
import numpy as np
#import torch
import matplotlib.ticker as plticker

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
df = pd.read_csv('Dataset/20200118/310/summary.csv', index_col=0)
del df['Timezone (minutes)']
del df['Unix Timestamp (UTC)']

print(df.head())

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
    next(lines)
    for row in lines:
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
        # self.geometry("600x800")
        # self.minsize(800, 500)
        self.frames = dict()

        container = LabelFrame(self, bg='light grey')
        container.grid(padx=0, pady=0, sticky="EW")

        for FrameClass in (Front, Graph, Chart):
            frame = FrameClass(container, self)
            self.frames[FrameClass] = frame
            frame.grid(row=0, column=0, sticky="NSEW")

        self.show_frame(Front)

    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()


class Front(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)

        frame = Frame(self, padx=70, pady=78, bg="light blue")
        frame.grid(padx=10, pady=10, sticky="NSEW")

        title = Label(frame, text="GRAPHY MENU", pady=10, padx=10)
        title.grid(column=0, row=0, padx=5, pady=5, sticky="EW")

        g_button = Button(
            frame,
            text="Switch to Graph",
            command=lambda: controller.show_frame(Graph)
        )
        g_button.grid(column=0, row=1, columnspan=1, sticky="EW")

        c_button = Button(
            frame,
            text="Switch to Chart",
            command=lambda: controller.show_frame(Chart)
        )
        c_button.grid(column=0, row=2, columnspan=1, sticky="EW")


class Graph(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)

        frame_left = Frame(self, padx=50, pady=50, bg="light blue")
        frame_left.grid(row=0, column=0, padx=10, pady=10, sticky="NSEW")

        frame_right = Frame(self, padx=50, pady=50, bg="light blue")
        frame_right.grid(row=0, column=1, padx=10, pady=10, sticky="NSEW")

        def plot():
            print(value_inside_start.get())
            fig = Figure(figsize=(4, 3.87), dpi=100)
            plot1 = fig.add_subplot(111)
            plot1.plot(Date, Mvmt)
            # loc = plticker.LogLocator(base=2)
            # plot1.yaxis.set_major_locator(loc)
            # --** Here is where I am trying to filter based on date **--
            # plot1.set_xlim(Mvmt[0], Mvmt[20])
            canvas = FigureCanvasTkAgg(fig, frame_right)
            canvas.get_tk_widget().grid(row=1, column=1, rowspan=1, columnspan=1)

        home_button = Button(
            frame_left,
            text="Main Menu",
            command=lambda: controller.show_frame(Front)
        )
        home_button.grid(column=0, row=0, columnspan=1, sticky="EW")

        switch_page_button = Button(
            frame_left,
            text="Switch to Chart",
            command=lambda: controller.show_frame(Chart)
        )
        switch_page_button.grid(column=0, row=1, columnspan=1, sticky="NEW")

        value_inside_start = StringVar(frame_left)
        value_inside_end = StringVar(frame_left)
        value_inside_start.set(Date[0])
        value_inside_end.set(Date[20])
        drop = OptionMenu(frame_left, value_inside_start, *Date)
        drop.grid(row=2, column=0, sticky="NEW")
        drop2 = OptionMenu(frame_left, value_inside_end, *Date)
        drop2.grid(row=3, column=0, sticky="NEW")

        plot_button = Button(frame_left, text="Graph", command=plot, height=2, width=10)
        plot_button.grid(row=4, column=0, sticky="NEW")


class Chart(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)

        frame_left = Frame(self, padx=50, pady=50, bg="light blue")
        frame_left.grid(row=0, column=0, padx=10, pady=10, sticky="NSEW")

        frame_right = Frame(self, padx=50, pady=50, bg="light blue")
        frame_right.grid(row=0, column=1, padx=10, pady=10, sticky="NSEW")

        def chart():
            num_rows = int(row_input.get())
            print(num_rows)

            scroll = Scrollbar(frame_right, orient="vertical")
            scroll.grid(row=0, column=1, rowspan=1, sticky="NS")
            scroll_h = Scrollbar(frame_right, orient="horizontal")
            scroll_h.grid(row=1, column=0, rowspan=1, sticky="EW")

            table = Text(frame_right, wrap="none")
            table.insert(END, str(df.head(num_rows)))
            # with open('Dataset/20200118/310/summary.csv', "r") as f:
            #     data = f.read()
            #     table.insert("1.0", data)
            table.configure(state=DISABLED, yscrollcommand=scroll.set, xscrollcommand=scroll_h.set)
            scroll.config(command=table.yview)
            scroll_h.config(command=table.xview)
            table.grid(row=0, column=0, rowspan=1, columnspan=1)

        home_button = Button(
            frame_left,
            text="Main Menu",
            command=lambda: controller.show_frame(Front)
        )
        home_button.grid(column=0, row=0, columnspan=1, sticky="EW")

        switch_page_button = Button(
            frame_left,
            text="Switch to Graph",
            command=lambda: controller.show_frame(Graph)
        )
        switch_page_button.grid(column=0, row=1, columnspan=1, sticky="EW")

        # value_inside_start = StringVar(frame_left)
        # value_inside_end = StringVar(frame_left)
        # value_inside_start.set(Date[0])
        # value_inside_end.set(Date[20])
        # drop = OptionMenu(frame_left, value_inside_start, *Date)
        # drop.grid(row=2, column=0)
        # drop2 = OptionMenu(frame_left, value_inside_end, *Date)
        # drop2.grid(row=3, column=0)

        row_label = Label(frame_left, text="Number of Rows")
        row_label.grid(row=2, column=0, sticky="NSEW")
        row_input = Entry(frame_left, justify='center')
        row_input.grid(row=3, column=0)

        b = Button(frame_left, command=chart, height=2, width=10, text="Chart")
        b.grid(row=4, column=0)


root = Graphy()
root.mainloop()
