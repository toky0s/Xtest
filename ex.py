import tkinter as tk
from tkinter.messagebox import askokcancel
def ask_quit():
    if askokcancel("Quit", "You want to quit now? *sniff*"):
        root.destroy()
root = tk.Tk()
root.protocol("WM_DELETE_WINDOW", ask_quit)
root.mainloop()