import tkinter as tk
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

plt.plot(x, y, color = 'g', label = "data")
plt.legend()
# plt.show()


def plot():
    # the figure that will contain the plot
    fig = Figure(figsize = (5, 5),
                 dpi = 100)
  
    # list of squares
    y = [i**2 for i in range(101)]
  
    # adding the subplot
    plot1 = fig.add_subplot(111)
  
    # plotting the graph
    plot1.plot(y)
  
    # creating the Tkinter canvas
    # containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig,
                               master = window)  
    canvas.draw()
  
    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().pack()
  
    # creating the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas,
                                   window)
    toolbar.update()
  
    # placing the toolbar on the Tkinter window
    canvas.get_tk_widget().pack()


window = tk.Tk()
window.title = 'Charts'
window.geometry('500x500')
# toplevel = tk.Toplevel(window)
# toplevel.title = 'Top Level'
plot_button = tk.Button(master = window, command = plot, height = 2, width = 10, text = 'plot')
plot_button.pack()


window.mainloop()

print("Hello World") 
print(pd.__version__)
# print(plt.__version__)

###test###