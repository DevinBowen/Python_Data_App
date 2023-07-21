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

filepath = 'Dataset/20200118/310/summary.csv'

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# Date = []
# Acc = []
# Eda = []
# Temp = []
# Mvmt = []
# Step = []
# Rest = []
# On = []
#
#
# with open('Dataset/20200118/310/summary.csv', 'r') as csvfile:
#     lines = csv.reader(csvfile, delimiter=',')
#     next(lines)
#     for row in lines:
#         Date.append(row[0])
#         Acc.append(row[3])
#         Eda.append(row[4])
#         Temp.append(row[5])
#         Mvmt.append(row[6])
#         Step.append(row[7])
#         Rest.append(row[8])
#         On.append(row[9])


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

        def select_file():
            filetypes = (
                ('CSV files', '*.csv'),
                ('All files', '*.*')
            )
            global filepath
            filepath = fd.askopenfilename(
                title='Open a file',
                # initialdir='/',
                filetypes=filetypes)
            # showinfo(
            #     title='Selected File',
            #     message=filename
            # )
            print(filepath)

        change = Button(
            frame,
            text="Change File",
            command=select_file
        )
        change.grid(column=0, row=3, pady=5, columnspan=1, sticky="EW")

        def ex():
            root.quit()

        qu = Button(
            frame,
            text="EXIT",
            command=ex
        )
        qu.grid(column=0, row=4, pady=5, columnspan=1, sticky="EW")


class Graph(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)

        frame_left = Frame(self, padx=50, pady=50, bg="light blue")
        frame_left.grid(row=0, column=0, padx=10, pady=10, sticky="NSEW")

        frame_right = Frame(self, padx=50, pady=50, bg="light blue")
        frame_right.grid(row=0, column=1, padx=10, pady=10, sticky="NSEW")

        df = pd.read_csv(filepath[filepath.find('Dataset'):])
        df['Range'] = pd.to_datetime(df['Datetime (UTC)'], format='%Y-%m-%dT%Xz')

        def plot():
            df = pd.read_csv(filepath[filepath.find('Dataset'):])

            # df["Datetime (UTC)"].head(5)

            df['Date'] = pd.to_datetime(df['Datetime (UTC)'], format='%Y-%m-%dT%Xz')
            # offset = int(df['Timezone (minutes)'][0])
            df['Time'] = df['Date'].dt.time
            df['datetime'] = pd.to_datetime(df['Unix Timestamp (UTC)'], unit='ms')
            df['datetime_UTC'] = df['datetime'].dt.tz_localize('UTC')
            # df['datetime (Local)'] = df['datetime'] + pd.DateOffset(minutes=offset)
            df['datetime (Local)'] = df['datetime'] + pd.DateOffset(hours=5)
            df['Month'] = df['Date'].dt.month
            df['Time'] = df['Time'].astype(str)
            df['Date'] = df['Date'].astype(str)
            df['datetime (Local)'] = df['datetime (Local)'].astype(str)

            df['Time Local'] = df['Time']
            df['Time UTC'] = df['datetime (Local)']
            x_local = df['Time Local']
            x_utc = df['Time UTC']
            # y = df['Eda avg']

            fig = Figure(figsize=(12, 6), dpi=200)
            
            # adding the subplot
            fig, axes = plt.subplots(1, 1, figsize=(6.55, 4.3)) #add_subplots(111)
            axes.clear()  # Clears graph so there will be no overlapping.

            fig.autofmt_xdate()  # Formats the datetime

            # Aggregation
            if combo.get() == 'Local Time':
                print(combo.get())
                print(value_inside_start)
                # df_subset = df['Time Local'].between(value_inside_start.get(), value_inside_end.get())
                # df_subset = df[('Time Local' >= value_inside_start.get()) & ('Time Local' <= value_inside_end.get())]
                # print(df_subset)
                df.groupby(x_local).max()['Temp avg'].plot()  # df.groupby('Time').max()['Temp avg'].plot()
            else:
                print(combo.get())
                df.groupby(x_utc).max()['Temp avg'].plot()

            # filter 0 values.
            # df[df['Steps count'] > 0].groupby('Time').count()['Steps count'].step()

            # plotting the graph
            plt.setp(axes.get_xticklabels(), rotation=30, horizontalalignment='right')  # Set the alignment
            fig.tight_layout()  # Add spacing for x axis.

            # creating the Tkinter canvas
            # containing the Matplotlib figure
            canvas = FigureCanvasTkAgg(fig, frame_right)
            canvas.draw()
            canvas.get_tk_widget().grid(row=1, sticky="EW")

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

        # print(df['Range'][0])

        value_inside_start = StringVar()
        value_inside_end = StringVar()
        value_inside_start.set(df['Range'][0])
        value_inside_end.set(df['Range'][20])
        drop = OptionMenu(frame_left, value_inside_start, *df['Range'])
        drop.grid(row=2, column=0, sticky="NEW")
        drop2 = OptionMenu(frame_left, value_inside_end, *df['Range'])
        drop2.grid(row=3, column=0, pady=1, sticky="NEW")

        print(df['Range'][0])
        print(value_inside_start.get())

        # COMBO BOX FOR UTC/LOCAL TIMEZONES
        time_values = ('UTC', 'Local Time')
        time_string = tk.StringVar()
        combo = ttk.Combobox(frame_left, textvariable=time_string, state='readonly')
        combo['values'] = time_values
        combo.current(0)
        combo.grid(row=4, column=0)

        def option_selected(event):
            selected_option = combo.get()
            print("You selected:", selected_option)
            if selected_option == 'UTC':
                print()
                # x = df['Time']
                # print(x)
            if selected_option == 'Local Time':
                print()
                # x = df['datetime (Local)']
                # print(x)

        combo.bind("<<ComboboxSelected>>", option_selected)

        plot_button = Button(frame_left, text="Graph", command=plot, height=2, width=10)
        plot_button.grid(row=5, column=0, pady=5, sticky="NEW")

        # print(max(df['Time']))


class Chart(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)

        frame_left = Frame(self, padx=50, pady=50, bg="light blue")
        frame_left.grid(row=0, column=0, padx=10, pady=10, sticky="NSEW")

        frame_right = Frame(self, padx=50, pady=50, bg="light blue")
        frame_right.grid(row=0, column=1, padx=10, pady=10, sticky="NSEW")

        def chart():
            print(filepath)

            df = pd.read_csv(filepath[filepath.find('Dataset'):], index_col=0)
            del df['Timezone (minutes)']
            del df['Unix Timestamp (UTC)']
            df['Temp avg'] = df['Temp avg']
            df['Movement intensity'] = df['Movement intensity']
            df['Steps count'] = df['Steps count']

            num_rows = int(row_input.get())
            # print(num_rows)

            scroll = Scrollbar(frame_right, orient="vertical")
            scroll.grid(row=0, column=1, rowspan=1, sticky="NS")
            scroll_h = Scrollbar(frame_right, orient="horizontal")
            scroll_h.grid(row=1, column=0, rowspan=1, sticky="EW")

            table = Text(frame_right, wrap="none")
            table.insert(END, str(df.head(num_rows).to_string()))
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

        def modified(label, text_value):
            print(filepath)

            df = pd.read_csv(filepath[filepath.find('Dataset'):], index_col=0)
            del df['Timezone (minutes)']
            del df['Unix Timestamp (UTC)']
            df['Temp avg'] = df['Temp avg']
            df['Movement intensity'] = df['Movement intensity']
            df['Steps count'] = df['Steps count']

            # maxx.configure(text=("Max",m))
            maxx.configure(text=("Max", np.around(max(df[text_value]),3)))
            median.configure(text=("Median", np.around(np.median(df[text_value]),3)))
            meann.configure(text=("Mean", np.around(np.mean(df[text_value]),3)))
            print(cbox.get())

        box = StringVar()
        cbox = ttk.Combobox(frame_left, textvariable=box, justify=CENTER, state='readonly')
        cbox['values'] = (
            'Steps count',
            'Temp avg',
            'Movement intensity'
            )
        cbox.grid(column=0, row=6, columnspan=1, pady=1, sticky="EW")
        # cbox.current(0)

        # m = np.around(max(df[cbox.get()]), 3)
        maxx = Label(frame_left, text=("Max"))
        maxx.grid(row=7, column=0, padx=0, pady=5, sticky="EW")

        # mead = np.around(np.median(df[cbox.get()]), 3)
        median = Label(frame_left, text=("Median"))
        median.grid(row=8, column=0, padx=0, pady=5, sticky="EW")

        # mean = np.around(np.mean(df[cbox.get()]), 3)
        meann = Label(frame_left, text=("Mean"))
        meann.grid(row=9, column=0, padx=0, pady=5, sticky="EW")

        cbox.bind('<<ComboboxSelected>>', lambda event: modified(maxx, box.get()))
        

root = Graphy()
root.mainloop()
