from tkinter import *
import math as ma
import numpy as np
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from matplotlib import (rcParams, style, backend_bases)

# NOTE: Have central regression method for Calculate regression button that calls other specific regression
# methods depending on a global variable

# Prevents axes from being cut off in graph
rcParams.update({'figure.autolayout': True})

# Acceptable characters for list entries; used to check for list entry errors
acceptedCharacters = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-', '.'}

# Number of decimal places to round displayed values to
# Only affects display; calculations performed with maximum decimal places
roundTo = 10

# Converts a string of digits into superscript for exponents and list index labels
def superscript(exponent):
    sup = str.maketrans("0123456789.", "⁰¹²³⁴⁵⁶⁷⁸⁹˙")
    exp = exponent.translate(sup)
    return exp


# Begin setup for tkinter window
root = Tk()
root.title("Regression Calculator")
root.resizable(width=False, height=False)
root.geometry('750x695')
root.iconphoto(True, PhotoImage(file="reg_icon.png"))

# Frame used for list delimiter entry related widgets
delimiterFrame = Frame(root, width=800, height=100)
delimiterFrame.grid(row=0, column=0, columnspan=2, sticky=W, pady=(0, 8))

delimiterEntryLabel1 = Label(delimiterFrame, text="Enter character(s) separating values for list 1:  ")
delimiterEntryLabel1.grid(row=0, column=0, sticky=W, padx=2, pady=3)
delimiterEntryLabel2 = Label(delimiterFrame, text="Enter character(s) separating values for list 2:  ")
delimiterEntryLabel2.grid(row=1, column=0, sticky=W, padx=2, pady=3)

delimiterEntry1 = Entry(delimiterFrame, width=37)
delimiterEntry1.grid(row=0, column=1, padx=5, pady=3)
delimiterEntry2 = Entry(delimiterFrame, width=37)
delimiterEntry2.grid(row=1, column=1, padx=5, pady=3)

# TODO: Add command="" parameter to each button
delimiterButton1 = Button(delimiterFrame, text="Confirm")
delimiterButton1.grid(row=0, column=2, padx=5, pady=3)
delimiterButton2 = Button(delimiterFrame, text="Confirm")
delimiterButton2.grid(row=1, column=2, padx=5, pady=3)

delimiterLabel1 = Label(delimiterFrame, text="List 1 delimiter: Not set")
delimiterLabel1.grid(row=0, column=3, padx=2, pady=3)
delimiterLabel2 = Label(delimiterFrame, text="List 2 delimiter: Not set")
delimiterLabel2.grid(row=1, column=3, padx=2, pady=3)

# Frame used for list value entry related widgets
valuesFrame = Frame(root, width=800, height=100)
valuesFrame.grid(row=1, column=0, columnspan=2, sticky=W)

valuesLabel1 = Label(valuesFrame, text="Enter list 1 values separated by list 1 delimiter:")
valuesLabel1.grid(row=0, column=0, padx=2, pady=(3, 12))
valuesLabel2 = Label(valuesFrame, text="Enter list 2 values separated by list 2 delimiter:")
valuesLabel2.grid(row=1, column=0, padx=2, pady=(3, 12))

entryFrame1 = Frame(valuesFrame)
entryScroll1 = Scrollbar(entryFrame1, orient=HORIZONTAL, width=13)
valuesEntry1 = Entry(entryFrame1, width=65, xscrollcommand=entryScroll1.set)
entryScroll1.config(command=valuesEntry1.xview)
entryScroll1.pack(side=BOTTOM, fill=X)
valuesEntry1.pack()
entryFrame1.grid(row=0, column=1, padx=5, pady=3)
entryFrame2 = Frame(valuesFrame)
entryScroll2 = Scrollbar(entryFrame2, orient=HORIZONTAL, width=13)
valuesEntry2 = Entry(entryFrame2, width=65, xscrollcommand=entryScroll2.set)
entryScroll2.config(command=valuesEntry2.xview)
valuesEntry2.pack()
entryScroll2.pack(side=BOTTOM, fill=X)
entryFrame2.grid(row=1, column=1, padx=5, pady=3)

# TODO: Add command="" parameter to each button
valuesButton1 = Button(valuesFrame, text="Confirm")
valuesButton1.grid(row=0, column=2, padx=5, pady=(3, 12))
valuesButton2 = Button(valuesFrame, text="Confirm")
valuesButton2.grid(row=1, column=2, padx=5, pady=(3, 12))

# Frame used for regression related widgets
regressionFrame = Frame(root, width=800, height=100)
regressionFrame.grid(row=2, column=0, columnspan=2, sticky=W)

variablesLabel = Label(regressionFrame, text="Set independent(x) and dependent(y) variables:")
variablesLabel.grid(row=0, column=0, padx=2, pady=3)
varList = ('x = list 1  |  y = list 2', 'x = list 2  |  y = list 1')
defaultRegression = StringVar()
defaultRegression.set('x = list 1  |  y = list 2')
variablesOptions = OptionMenu(regressionFrame, defaultRegression, *varList)
variablesOptions.grid(row=0, column=1, padx=(3, 8), pady=3)

selectionLabel = Label(regressionFrame, text="Select regression:")
selectionLabel.grid(row=0, column=2, padx=2, pady=3)
regList = ('linear', 'quadratic', 'cubic', 'quartic', 'quintic', 'power', 'inverse', 'logarithmic', 'exponential')
defaultRegression = StringVar()
defaultRegression.set('linear')
regressionOptions = OptionMenu(regressionFrame, defaultRegression, *regList)
regressionOptions.grid(row=0, column=3, padx=3, pady=3)

calculateButton = Button(regressionFrame, text="Calculate regression")
calculateButton.grid(row=0, column=4, padx=9, pady=3)

regDisplayFrame = Frame(regressionFrame)
regressionScroll = Scrollbar(regDisplayFrame, orient=HORIZONTAL, width=13)
regressionDisplay = Listbox(regDisplayFrame, width=117, height=3, xscrollcommand=regressionScroll)
regressionScroll.config(command=regressionDisplay.xview)
regressionScroll.pack(side=BOTTOM, fill=X)
regressionDisplay.pack()
regDisplayFrame.grid(row=1, column=0, columnspan=5, sticky=W, padx=8, pady=3)

# Frame used for value prediction related widgets
predictionFrame = Frame(root, width=800, height=50)
predictionFrame.grid(row=3, column=0, columnspan=2, sticky=W)

predictionLabelX = Label(predictionFrame, text="Enter x-value:")
predictionLabelX.grid(row=0, column=0, padx=2, pady=3)

predictionEntry = Entry(predictionFrame, width=20)
predictionEntry.grid(row=0, column=1, padx=5, pady=3)

# TODO: Add command="" parameter to button
predictionButton = Button(predictionFrame, text="Predict y-value")
predictionButton.grid(row=0, column=2, padx=5, pady=3)

# TODO: Add code to display current regression being used to predict y-value; can display error if no data/reg set
predictionLabelY = Label(predictionFrame, text="Predicted y-value with regression: ")
predictionLabelY.grid(row=0, column=3, padx=(4, 2), pady=3)

yValueDisplay = Listbox(predictionFrame, width=33, height=1)
yValueDisplay.grid(row=0, column=4, padx=2, pady=3)

# Frame used for list display related widgets
listsFrame = Frame(root, width=350, height=350)
listsFrame.grid(row=4, column=0, sticky=NW)

listLabel1 = Label(listsFrame, text="List 1:")
listLabel1.grid(row=0, column=0, sticky=W,  padx=7, pady=(8, 0))
listLabel2 = Label(listsFrame, text="List 2:")
listLabel2.grid(row=0, column=1, sticky=W, padx=7, pady=(8, 0))
residualsLabel = Label(listsFrame, text="Residuals:")
residualsLabel.grid(row=0, column=2, sticky=W, padx=7, pady=(8, 0))

list1Frame = Frame(listsFrame)
list1Scroll = Scrollbar(list1Frame, orient=VERTICAL, width=13)
list1ScrollX = Scrollbar(list1Frame, orient=HORIZONTAL, width=13)
list1Display = Listbox(list1Frame, width=10, height=13, yscrollcommand=list1Scroll, xscrollcommand=list1ScrollX)
list1Scroll.config(command=list1Display.yview)
list1ScrollX.config(command=list1Display.xview)
list1Scroll.pack(side=RIGHT, fill=Y)
list1ScrollX.pack(side=BOTTOM, fill=X)
list1Display.pack()
list1Frame.grid(row=1, column=0, sticky=NW, padx=(8, 6), pady=3)

xStatsFrame = Frame(listsFrame)
xStatsScroll = Scrollbar(xStatsFrame, orient=VERTICAL, width=13)
xStatsScrollX = Scrollbar(xStatsFrame, orient=HORIZONTAL, width=13)
xStatsDisplay = Listbox(xStatsFrame, width=10, height=6, yscrollcommand=xStatsScroll, xscrollcommand=xStatsScrollX)
xStatsScroll.config(command=xStatsDisplay.yview)
xStatsScrollX.config(command=xStatsDisplay.xview)
xStatsScroll.pack(side=RIGHT, fill=Y)
xStatsScrollX.pack(side=BOTTOM, fill=X)
xStatsDisplay.pack()
xStatsFrame.grid(row=2, column=0, sticky=NW, padx=(8, 6), pady=11)

list2Frame = Frame(listsFrame)
list2Scroll = Scrollbar(list2Frame, orient=VERTICAL, width=13)
list2ScrollX = Scrollbar(list2Frame, orient=HORIZONTAL, width=13)
list2Display = Listbox(list2Frame, width=10, height=13, yscrollcommand=list2Scroll, xscrollcommand=list2ScrollX)
list2Scroll.config(command=list2Display.yview)
list2ScrollX.config(command=list2Display.xview)
list2Scroll.pack(side=RIGHT, fill=Y)
list2ScrollX.pack(side=BOTTOM, fill=X)
list2Display.pack()
list2Frame.grid(row=1, column=1, sticky=NW, padx=6, pady=2)

yStatsFrame = Frame(listsFrame)
yStatsScroll = Scrollbar(yStatsFrame, orient=VERTICAL, width=13)
yStatsScrollX = Scrollbar(yStatsFrame, orient=HORIZONTAL, width=13)
yStatsDisplay = Listbox(yStatsFrame, width=10, height=6, yscrollcommand=yStatsScroll, xscrollcommand=yStatsScrollX)
yStatsScroll.config(command=yStatsDisplay.yview)
yStatsScrollX.config(command=yStatsDisplay.xview)
yStatsScroll.pack(side=RIGHT, fill=Y)
yStatsScrollX.pack(side=BOTTOM, fill=X)
yStatsDisplay.pack()
yStatsFrame.grid(row=2, column=1, sticky=NW, padx=(8, 6), pady=11)

residualsFrame = Frame(listsFrame)
residualsScroll = Scrollbar(residualsFrame, orient=VERTICAL, width=13)
residualsScrollX = Scrollbar(residualsFrame, orient=HORIZONTAL, width=13)
residualsDisplay = Listbox(residualsFrame, width=10, height=21,
                           yscrollcommand=residualsScroll, xscrollcommand=residualsScrollX)
residualsScroll.config(command=residualsDisplay.yview)
residualsScrollX.config(command=residualsDisplay.xview)
residualsScroll.pack(side=RIGHT, fill=Y)
residualsScrollX.pack(side=BOTTOM, fill=X)
residualsDisplay.pack()
residualsFrame.grid(row=1, column=2, sticky=NW, rowspan=2, padx=6, pady=2)

# Frame used for the matplotlib graph
graphFrame = Frame(root, highlightbackground="black", highlightthickness=1, width=450, height=350)
graphFrame.grid(row=4, column=1, sticky=SW, padx=2, pady=6)

fig = Figure(figsize=(5.45, 4.2), dpi=80)
ax = fig.add_subplot(111)
ax.set_xlabel('x-values', fontsize=12)
ax.tick_params(axis='x', labelsize=10, labelrotation=30)
ax.set_ylabel('y-values', fontsize=12)
ax.tick_params(axis='y', labelsize=10, labelrotation=30)
canvas = FigureCanvasTkAgg(fig, master=graphFrame)
# Removes unnecessary button from toolbar
backend_bases.NavigationToolbar2.toolitems = (
    ('Home', 'Reset original view', 'home', 'home'),
    ('Back', 'Back to  previous view', 'back', 'back'),
    ('Forward', 'Forward to next view', 'forward', 'forward'),
    (None, None, None, None),
    ('Pan', 'Pan axes with left mouse, zoom with right', 'move', 'pan'),
    ('Zoom', 'Zoom to rectangle', 'zoom_to_rect', 'zoom'),
    (None, None, None, None),
    ('Save', 'Save the figure', 'filesave', 'save_figure'),
)
toolbar = NavigationToolbar2Tk(canvas, graphFrame)
toolbar.update()
canvas.get_tk_widget().pack(side=TOP, expand=1)

root.mainloop()
