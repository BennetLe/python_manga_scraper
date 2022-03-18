from tkinter import Tk
from tkinter.filedialog import askdirectory

Tk().withdraw()
filename = askdirectory()
filename = filename.strip().replace(filename[0:3], "")
print(filename)