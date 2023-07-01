import tkinter as tk
from tkinter import *
from tkinter import ttk
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

# plt.plot(x, y, color = 'g', label = "data")
# plt.legend()
# plt.show()


def plot():
    fig = Figure(figsize = (5, 5), dpi = 100)
    # adding the subplot
    plot1 = fig.add_subplot(111)
    # plotting the graph
    plot1.plot(x,y)
  
    # creating the Tkinter canvas
    # containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig, master = window)  
    canvas.draw()
    canvas.get_tk_widget().pack()
  
    # !!!Not Working!!!
    # creating the Matplotlib toolbar
    # toolbar = NavigationToolbar2Tk(canvas, window)
    # toolbar.update()
    # canvas.get_tk_widget().pack()

def chart():
    canvas = Canvas(master = window)
    canvas.create_text(500, 250, text=df, fill="black", font=('Helvetica 15 bold'))
    canvas.pack()

# Tkinter Window
window = tk.Tk()
window.title = 'Charts'
window.geometry('1250x1000')

# Plot Graph Button
plot_button = tk.Button(master = window, command = plot, height = 2, width = 10, text = 'plot')
plot_button.pack()

# Plot Chart Button
chart_button = tk.Button(master = window, command = chart, height = 2, width = 10, text = 'chart')
chart_button.pack()

# Open tkinter window
window.mainloop()


# Test prints
print("Hello World") 
print(pd.__version__)
# print(plt.__version__)