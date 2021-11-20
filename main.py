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
