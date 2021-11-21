from tkinter import *
import math as ma
import numpy as np
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from matplotlib import (rcParams, style, backend_bases)

# Prevents axes from being cut off in graph
rcParams.update({'figure.autolayout': True})

# Acceptable characters for list entries; used in regression function to check for list entry errors
acceptedCharacters = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-', '.'}


# Converts a string of digits into superscript for exponents and list index labels
def superscript(exponent):
    sup = str.maketrans("0123456789.", "⁰¹²³⁴⁵⁶⁷⁸⁹˙")
    exp = exponent.translate(sup)
    return exp


root = Tk()
root.title("Regression Calculator")
root.resizable(width=False, height=False)
root.geometry('800x700')
root.iconphoto(True, PhotoImage(file="icon/reg_icon.png"))

delimiterFrame = Frame(root, highlightbackground="black", highlightthickness=1, width=800, height=100)
delimiterFrame.grid(row=0, column=0, columnspan=2)

valuesFrame = Frame(root, highlightbackground="black", highlightthickness=1, width=800, height=100)
valuesFrame.grid(row=1, column=0, columnspan=2)

regressionFrame = Frame(root, highlightbackground="black", highlightthickness=1, width=800, height=100)
regressionFrame.grid(row=2, column=0, columnspan=2)

predictionFrame = Frame(root, highlightbackground="black", highlightthickness=1, width=800, height=50)
predictionFrame.grid(row=3, column=0, columnspan=2)

listsFrame = Frame(root, highlightbackground="black", highlightthickness=1, width=350, height=350)
listsFrame.grid(row=4, column=0)

graphFrame = Frame(root, highlightbackground="black", highlightthickness=1, width=450, height=350)
graphFrame.grid(row=4, column=1)

root.mainloop()
