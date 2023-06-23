import tkinter as tk
#import pandas


window = tk.Tk()
window.title = 'Main Window'
# toplevel = tk.Toplevel(window)
# toplevel.title = 'Top Level'
message = tk.Label(window, text="Hello, World!")
message.pack()
window.mainloop()

print("Hello World") 