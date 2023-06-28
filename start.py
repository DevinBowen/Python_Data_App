import tkinter as tk
import pandas as pd
import matplotlib as plt
import csv

df = pd.read_csv('Dataset/20200118/310/summary.csv')

print(df.head(10))

x = []
y = []

with open('Dataset/20200118/310/summary.csv','r') as csvfile:
    lines = csv.reader(csvfile, delimiter=',')
    for row in lines:
        x.append(row[0])
        y.append(int(row[2]))

plt.plot(x, y, color = 'g', width = 0.72, label = "data")
plt.legend()
plt.show()

window = tk.Tk()
window.title = 'Main Window'
# toplevel = tk.Toplevel(window)
# toplevel.title = 'Top Level'
message = tk.Label(window, text="Hello, World!")
message.pack()
window.mainloop()

print("Hello World") 
print(pd.__version__)
print(plt.__version__)

###test###