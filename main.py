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
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
from datetime import datetime
import time
import datetime


pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

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

        df = pd.read_csv('Dataset/20200118/310/summary.csv')
        del df['Timezone (minutes)']
        del df['Unix Timestamp (UTC)']

        df["Datetime (UTC)"].head(5)

        df['Date'] = pd.to_datetime(df['Datetime (UTC)'], format='%Y-%m-%dT%Xz')
        df['Date'].dt.time
        df['Time'] = df['Date'].dt.time
        df['Month'] = df['Date'].dt.month
        df['Time'] = df['Time'].astype(str)
        x = df['Date']
        y = df['Eda avg']

        # def plot():
        #     # print(value_inside_start.get())

        #     # df_subset = df[("Datetime (UTC)" >= value_inside_start.get()) & ("Datetime (UTC)" <= value_inside_end.get())]
        #     # print(df_subset)

        #     fig = Figure(figsize=(4, 3.87), dpi=100)
        #     plot1 = fig.add_subplot(111)
        #     plot1.plot(Date, Mvmt)
        #     # loc = plticker.LogLocator(base=2)
        #     # plot1.yaxis.set_major_locator(loc)
        #     # --** Here is where I am trying to filter based on date **--
        #     # plot1.set_xlim(Mvmt[0], Mvmt[20])
        #     canvas = FigureCanvasTkAgg(fig, frame_right)
        #     canvas.get_tk_widget().grid(row=1, column=1, rowspan=1, columnspan=1)

        def plot():
            #pylab.rcParams['xtick.major.pad']= '25'
            
            fig = Figure(figsize = (12, 6), dpi = 200)

            #plt.rc_context({'xtick.major.pad':10})
            
            # adding the subplot
            fig,axes = plt.subplots(1,1, figsize=(6.55, 4.3)) #add_subplots(111)
            axes.clear()
            
            #axes.tick_params(axis='x', which='major', pad=50)
            
            #axes.plot(x,y)
            
            fig.autofmt_xdate()
            #axes.plot(x,y)
            df.groupby('Time').max()['Steps count'].plot()
            plt.tight_layout()
            
            # plotting the graph
            plt.setp(axes.get_xticklabels(), rotation=30, horizontalalignment='right')
            #axes.xaxis.set_tick_params(padx=100)
            fig.tight_layout()

            #fig = sns.lineplot(df, x=X, y=Y)


            # creating the Tkinter canvas
            # containing the Matplotlib figure

            canvas = FigureCanvasTkAgg(fig, frame_right)  
            canvas.draw()
            canvas.get_tk_widget().grid(row=1, sticky="EW")

            # !!!Not Working!!!
            # creating the Matplotlib toolbar
            # toolbar = NavigationToolbar2Tk(canvas, frame_right, pack_toolbar=False)
            # toolbar.update()
            # toolbar.pack(anchor="w", fill=tk.X)
            # canvas.get_tk_widget().pack()

        home_button = Button(
            frame_left,
            text="Main Menu",
            command=lambda: controller.show_frame(Front),
            width=21
        )
        home_button.grid(column=0, row=0, columnspan=1, sticky="EW")

        switch_page_button = Button(
            frame_left,
            text="Switch to Chart",
            command=lambda: controller.show_frame(Chart)
        )
        switch_page_button.grid(column=0, row=1, columnspan=1, pady=5, sticky="NEW")

        value_inside_start = StringVar(frame_left)
        value_inside_end = StringVar(frame_left)
        value_inside_start.set(Date[0])
        value_inside_end.set(Date[20])
        drop = OptionMenu(frame_left, value_inside_start, *Date)
        drop.grid(row=2, column=0, sticky="NEW")
        drop2 = OptionMenu(frame_left, value_inside_end, *Date)
        drop2.grid(row=3, column=0, pady=1, sticky="NEW")

        plot_button = Button(frame_left, text="Graph", command=plot, height=2, width=10)
        plot_button.grid(row=4, column=0, pady=5, sticky="NEW")

        print(max(df['Time']))

class Chart(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)

        frame_left = Frame(self, padx=50, pady=50, bg="light blue")
        frame_left.grid(row=0, column=0, padx=10, pady=10, sticky="NSEW")

        frame_right = Frame(self, padx=50, pady=50, bg="light blue")
        frame_right.grid(row=0, column=1, padx=10, pady=10, sticky="NSEW")

        df = pd.read_csv('Dataset/20200118/310/summary.csv', index_col=0)
        del df['Timezone (minutes)']
        del df['Unix Timestamp (UTC)']
        df['Temp avg'] = df['Temp avg']
        df['Movement intensity'] = df['Movement intensity']
        df['Steps count'] = df['Steps count']

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
            command=lambda: controller.show_frame(Front),
            width=21
        )
        home_button.grid(column=0, row=0, columnspan=1, sticky="EW")

        switch_page_button = Button(
            frame_left,
            text="Switch to Graph",
            command=lambda: controller.show_frame(Graph)
        )
        switch_page_button.grid(column=0, row=1, columnspan=1, pady=5, sticky="EW")

        # value_inside_start = StringVar(frame_left)
        # value_inside_end = StringVar(frame_left)
        # value_inside_start.set(Date[0])
        # value_inside_end.set(Date[20])
        # drop = OptionMenu(frame_left, value_inside_start, *Date)
        # drop.grid(row=2, column=0)
        # drop2 = OptionMenu(frame_left, value_inside_end, *Date)
        # drop2.grid(row=3, column=0)

        row_label = Label(frame_left, text="Number of Rows")
        row_label.grid(row=2, column=0, padx=5, pady=1, sticky="NSEW")
        row_input = Entry(frame_left, justify='center')
        row_input.grid(row=3, column=0)

        b = Button(frame_left, command=chart, height=2, text="Chart")
        b.grid(row=4, column=0, pady=5, sticky="EW")

        fun = Label(frame_left, text="Functions")
        fun.grid(row=5, column=0, padx=0, pady=1, sticky="EW")

        cBox = ttk.Combobox(frame_left, justify=CENTER)
        cBox['values'] = (
            'Temp avg',
            'Movement intensity',
            'Steps count'
            )
        cBox.grid(column=0, row=6, columnspan=1, pady=1, sticky="EW")
        cBox.current(0)

        m=np.around(max(df['Temp avg']), 3)
        maxx = Label(frame_left, text=("Max",m))
        maxx.grid(row=7, column=0, padx=0, pady=5, sticky="EW")

        mead=np.around(np.median(df['Temp avg']), 3)
        meadian = Label(frame_left, text=("Meadian",mead))
        meadian.grid(row=8, column=0, padx=0, pady=5, sticky="EW")

        mean=np.around(np.mean(df['Temp avg']), 3)
        meann = Label(frame_left, text=("Mean",mean))
        meann.grid(row=9, column=0, padx=0, pady=5, sticky="EW")
        

root = Graphy()
root.mainloop()
