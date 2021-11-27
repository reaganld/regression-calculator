from tkinter import *
import math as ma
import numpy as np
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from matplotlib import (rcParams, style, backend_bases)
import statistics

# Number of decimal places to round displayed values to
# Only affects display; calculations performed with maximum decimal places
ROUND_TO = 6

# Contains data entered into each list by user as strings
list1 = []
list2 = []

# Contains data for each list as floats
x_list = np.array([])
y_list = np.array([])

# List of residuals, or y-values minus respective x-value
residuals = []

# Size of the x variable and y variable lists
x_size = 0
y_size = 0

# Delimiter used to separate entered list values; set to a comma by default
delimiter1 = ","
delimiter2 = ","

# Used to check if command is linear or polynomial regression and assign degree of polynomial
polynomial_regressions = ('linear', 'quadratic', 'cubic', 'quartic', 'quintic')

# The coefficients in the previously calculated regression used to predict and graph values
reg_coefficients = []

# The last regression performed; used when predicting and graphing values
last_regression = None


# Converts a string of digits into superscript for exponents and list index labels
def superscript(exponent):
    sup = str.maketrans("0123456789.-", "⁰¹²³⁴⁵⁶⁷⁸⁹˙⁻")
    exp = exponent.translate(sup)
    return exp


# Sets the string used as a delimiter for values entered into list 1
def set_delimiter1():
    global delimiter1
    delimiter_entry = delimiterEntry1.get()
    if delimiter_entry != '':
        delimiter1 = delimiter_entry
        delimiterLabel1.config(text='List 1 delimiter: "' + delimiter_entry + '"')


# Sets the string used as a delimiter for values entered into list 2
def set_delimiter2():
    global delimiter2
    delimiter_entry = delimiterEntry2.get()
    if delimiter_entry != '':
        delimiter2 = delimiter_entry
        delimiterLabel2.config(text='List 2 delimiter: "' + delimiter_entry + '"')


# Sets the values entered into the list 1 entry by the user to a list of strings
def set_list1():
    global list1
    list1 = valuesEntry1.get().split(delimiter1)
    list1 = [e for e in list1 if e != '']
    list1Display.delete(0, END)
    for i in range(len(list1)):
        list1Display.insert(i + 1, superscript(str(i+1)) + "  " + list1[i])

    # Calculate and display 1-variable stats for list 1
    l1Stats.delete(0, END)
    try:
        npl1 = np.array(list(map(float, list1)))
        l1_stats = ['Σ: ' + str(round(np.sum(npl1), ROUND_TO)),
                    'μ: ' + str(round(np.average(npl1), ROUND_TO)),
                    'σ: ' + str(round(float(np.std(npl1)), ROUND_TO)),
                    'σ²: ' + str(round(float(np.var(npl1)), ROUND_TO)),
                    'MIN: ' + str(round(np.min(npl1), ROUND_TO)),
                    'Q1: ' + str(round(float(np.percentile(npl1, 25)), ROUND_TO)),
                    'MED: ' + str(round(float(np.median(npl1)), ROUND_TO)),
                    'Q3: ' + str(round(float(np.percentile(npl1, 75)), ROUND_TO)),
                    'MAX: ' + str(round(np.max(npl1), ROUND_TO)),
                    'IQR: ' + str(round(float(np.percentile(npl1, 75) - np.percentile(npl1, 25)), ROUND_TO)),
                    'RANGE: ' + str(round(np.max(npl1) - np.min(npl1), ROUND_TO)),
                    'MODE: ' + str(round(statistics.mode(npl1), ROUND_TO))]
        for i in range(len(l1_stats)):
            l1Stats.insert(i + 1, l1_stats[i])
    except ValueError:
        l1Stats.insert(1, "ERROR: Nonnumerical data in list 1")


# Sets the values entered into the list 2 entry by the user to a list of strings
def set_list2():
    global list2
    list2 = valuesEntry2.get().split(delimiter2)
    list2 = [e for e in list2 if e != '']
    list2Display.delete(0, END)
    for i in range(len(list2)):
        list2Display.insert(i + 1, superscript(str(i + 1)) + "  " + list2[i])

    # Calculate and display 1-variable stats for list 2
    l2Stats.delete(0, END)
    try:
        npl2 = np.array(list(map(float, list2)))
        l2_stats = ['Σ: ' + str(round(np.sum(npl2), ROUND_TO)),
                    'μ: ' + str(round(np.average(npl2), ROUND_TO)),
                    'σ: ' + str(round(float(np.std(npl2)), ROUND_TO)),
                    'σ²: ' + str(round(float(np.var(npl2)), ROUND_TO)),
                    'MIN: ' + str(round(np.min(npl2), ROUND_TO)),
                    'Q1: ' + str(round(float(np.percentile(npl2, 25)), ROUND_TO)),
                    'MED: ' + str(round(float(np.median(npl2)), ROUND_TO)),
                    'Q3: ' + str(round(float(np.percentile(npl2, 75)), ROUND_TO)),
                    'MAX: ' + str(round(np.max(npl2), ROUND_TO)),
                    'IQR: ' + str(round(float(np.percentile(npl2, 75) - np.percentile(npl2, 25)), ROUND_TO)),
                    'RANGE: ' + str(round(np.max(npl2) - np.min(npl2), ROUND_TO)),
                    'MODE: ' + str(round(statistics.mode(npl2), ROUND_TO))]
        for i in range(len(l2_stats)):
            l2Stats.insert(i + 1, l2_stats[i])
    except ValueError:
        l2Stats.insert(1, "ERROR: Nonnumerical data in list 2")


# Updates the residuals display to show whatever the current residuals are
def update_residuals():
    residualsDisplay.delete(0, END)
    for i in range(y_size):
        residuals[i] = str(residuals[i])
        # Replaces any incorrectly formatted 0 residuals with "0.0"
        if residuals[i] == "-0.0" or residuals[i] == "-0" or residuals[i] == "0":
            residuals[i] = "0.0"
        residualsDisplay.insert(i + 1, superscript(str(i+1)) + "  " + residuals[i])


# Performs a polynomial regression given the degree of the regression by the regression() method
def polynomial_regression(degree):
    display = []
    global reg_coefficients
    global last_regression
    reg_coefficients = []

    # Displays an error if the the lists are not big enough to perform the polynomial regression
    if x_size <= degree:
        error_message = "ERROR: At least " + str(degree+1) + " values are required for a " + \
                        polynomial_regressions[degree-1] + " regression."
        display.append(error_message)
        display.append(" ")
        display.append(" ")
        return display

    # Linear algebra to solve regression
    x_sums = []
    x_sums_matrix = []
    xy_sums_matrix = []
    for i in range(degree * 2 + 1):
        x_sums.append(sum([j**i for j in x_list]))
    for i in range(degree + 1):
        x_sums_matrix.append([x_sums[i]])
        xy_sums_matrix.append([sum([j**i * k for j, k in zip(x_list, y_list)])])
        for j in range(1, degree + 1):
            x_sums_matrix[i].append(x_sums[i+j])
    x_sums_matrix = np.array(x_sums_matrix)
    xy_sums_matrix = np.array(xy_sums_matrix)
    solution_matrix = np.matmul(np.linalg.inv(x_sums_matrix), xy_sums_matrix)
    for i in range(degree + 1):
        reg_coefficients.append(float(solution_matrix[i][0]))
    
    # Creates a reversed list of rounded string polynomial coefficients with the proper sign
    cs = []
    for i in range(degree):
        if reg_coefficients[i] < 0:
            cs.append(" - " + str(round(-1 * reg_coefficients[i], ROUND_TO)))
        else:
            cs.append(" + " + str(round(reg_coefficients[i], ROUND_TO)))
    cs.append(str(round(reg_coefficients[degree], ROUND_TO)))
    # Fixes any "-0.0" coefficient substrings by changing to "0.0"
    for i in range(degree + 1):
        if cs[i] == ' + -0.0' or ' - -0.0':
            cs[i] = cs[i].replace('-0', '0')

    # Builds a string for the regression formula using the coefficient strings
    result = cs[1] + 'x' + cs[0]
    if degree == 1:
        result = 'Least squares regression line:  y = ' + result
        last_regression = "linear"
    elif degree == 2:
        result = 'Quadratic regression curve:  y = ' + cs[2] + u'x\u00B2' + result
        last_regression = "quadratic"
    elif degree == 3:
        result = 'Cubic regression curve:  y = ' + cs[3] + u'x\u00B3' + cs[2] + u'x\u00B2' + result
        last_regression = "cubic"
    elif degree == 4:
        result = 'Quartic regression curve:  y = ' + cs[4] + u'x\u2074' + cs[3] + u'x\u00B3' + cs[2] + u'x\u00B2' \
                 + result
        last_regression = "quartic"
    elif degree == 5:
        result = 'Quintic regression curve:  y = ' + cs[5] + u'x\u2075' + cs[4] + u'x\u2074' + cs[3] + u'x\u00B3' \
              + cs[2] + u'x\u00B2' + result
        last_regression = "quintic"
    # Adds regression equation to the first line of the regression display
    display.append(result)

    # Finds correlation coefficient and coefficient of determination using a simple formula
    upper = []
    lower = []
    for i in range(x_size):
        temp = y_list[i]
        for j in range(degree + 1):
            temp -= x_list[i] ** j * reg_coefficients[j]
        upper.append(temp ** 2)
        lower.append((y_list[i] - np.average(y_list)) ** 2)
    r2 = 1 - sum(upper) / sum(lower)
    if r2 < 0:
        r = 'Correlation coefficient: r = ' + str(round(ma.sqrt(-1 * r2), ROUND_TO)) + ' ' * 5
    else:
        r = 'Correlation coefficient: r = ' + str(round(ma.sqrt(r2), ROUND_TO)) + ' ' * 5
    r2 = 'Coefficient of determination: r' + u'\u00B2 = ' + str(round(r2, ROUND_TO)) + ' ' * 5
    # Adds correlation coefficient and coefficient of determination to second and third lines of regression display
    display.append(r)
    display.append(r2)

    # Calculates and updates residuals by calculating each predicted y-value and subtracting from its actual y-value
    for i in range(x_size):
        temp = 0
        for j in range(degree + 1):
            temp += x_list[i] ** j * reg_coefficients[j]
        residuals.append(str(round(y_list[i] - temp, ROUND_TO)))
    update_residuals()

    # Returns display with the regression formula, r, and r2 to the main regression() method to be displayed to the GUI
    return display


# Checks for issues in lists for non-polynomial regressions and outputs an error message to the display if one is found
def error_check(reg_type):
    error = False
    if reg_type == "inverse":
        for i in range(x_size):
            if x_list[i] == 0:
                regressionDisplay.insert(1, "ERROR: Cannot perform inverse regression for x-value = 0 at index "
                                         + str(i+1))
                error = True
    if reg_type in {"power", "logarithmic"}:
        for i in range(x_size):
            if x_list[i] <= 0:
                regressionDisplay.insert(1, "ERROR: Cannot perform " + reg_type
                                         + " regression for x-value <= 0 at index " + str(i+1))
                error = True
    if not error and reg_type in {"power", "exponential", "e-exponential"}:
        for i in range(y_size):
            if y_list[i] <= 0:
                regressionDisplay.insert(1, "ERROR: Cannot perform " + reg_type
                                         + " regression for y-value <= 0 at index " + str(i+1))
                error = True
    return error


# Calculates the correlation coefficient r and the coefficient of determination r^2 for non-polynomial regressions
def calculate_goodness_of_fit(sxx, syy, sxy):
    r = sxy / (ma.sqrt(sxx) * ma.sqrt(syy))
    r2 = "Coefficient of determination: r" + u"\u00B2 = " + str(round(r**2, ROUND_TO))
    r = "Correlation coefficient: r = " + str(round(r, ROUND_TO))
    return r, r2


# Performs a power regression and returns the formula, r, & r2 to regression() method to be displayed to the GUI
def power_regression():
    global residuals
    display = []
    global reg_coefficients
    global last_regression
    reg_coefficients = []

    x_logs = np.array([ma.log10(i) for i in x_list])
    y_logs = np.array([ma.log10(i) for i in y_list])
    x_logs_mean = np.average(x_logs)
    y_logs_mean = np.average(y_logs)
    sxx = np.sum(np.array([(i - x_logs_mean)**2 for i in x_logs]))
    syy = np.sum(np.array([(j - y_logs_mean)**2 for j in y_logs]))
    sxy = np.sum(np.array([(i - x_logs_mean) * (j - y_logs_mean) for i, j in zip(x_logs, y_logs)]))
    reg_coefficients.append(sxy / sxx)
    reg_coefficients.append(10**(y_logs_mean - reg_coefficients[0] * x_logs_mean))
    a = str(round(reg_coefficients[1], ROUND_TO))
    b = str(round(reg_coefficients[0], ROUND_TO))
    if a == "-0.0":
        a = "0.0"
    if b == "-0.0":
        b = "0.0"
    display.append("Power regression curve: y = " + a + 'x' + superscript(b))

    residuals = [str(round(j - i**reg_coefficients[0] * reg_coefficients[1], ROUND_TO)) for i, j in zip(x_list, y_list)]
    update_residuals()

    goodness_of_fit_values = calculate_goodness_of_fit(sxx, syy, sxy)
    display.append(goodness_of_fit_values[0])
    display.append(goodness_of_fit_values[1])

    last_regression = "power"

    return display


# Performs an inverse regression and returns the formula, r, & r2 to regression() method to be displayed to the GUI
def inverse_regression():
    global residuals
    display = []
    global reg_coefficients
    global last_regression
    reg_coefficients = []

    x_inverse = np.array([1 / i for i in x_list])
    x_inverse_mean = np.average(sum(x_inverse))
    y_mean = np.average(y_list)
    sxx = np.sum(np.array([(i - x_inverse_mean)**2 for i in x_inverse]))
    syy = np.sum(np.array([(j - y_mean)**2 for j in y_list]))
    sxy = np.sum(np.array([(i - x_inverse_mean) * (j - y_mean) for i, j in zip(x_inverse, y_list)]))
    reg_coefficients.append(sxy / sxx)
    reg_coefficients.append(y_mean - reg_coefficients[0] * x_inverse_mean)
    a = str(round(reg_coefficients[1], ROUND_TO))
    if reg_coefficients[0] < 0:
        b = " - " + str(round(-1 * reg_coefficients[0], ROUND_TO))
    else:
        b = " + " + str(round(reg_coefficients[0], ROUND_TO))
    if a == "-0.0":
        a = "0.0"
    if b == " + -0.0" or " - -0.0":
        b = b.replace("-0", "0")
    display.append("Inverse regression curve: y = " + a + b + "/x")

    residuals = [str(round(j - (reg_coefficients[0] / i + reg_coefficients[1]), ROUND_TO)) for i, j
                 in zip(x_list, y_list)]
    update_residuals()

    goodness_of_fit_values = calculate_goodness_of_fit(sxx, syy, sxy)
    display.append(goodness_of_fit_values[0])
    display.append(goodness_of_fit_values[1])

    last_regression = "inverse"

    return display


# Performs a logarithmic regression and returns the formula, r, & r2 to regression() method to be displayed to the GUI
def logarithmic_regression():
    global residuals
    display = []
    global reg_coefficients
    global last_regression
    reg_coefficients = []

    x_logs = np.array([ma.log(i) for i in x_list])
    x_logs_mean = np.average(x_logs)
    y_mean = np.average(y_list)
    sxx = np.sum(np.array([(i - x_logs_mean)**2 for i in x_logs]))
    syy = np.sum(np.array([(j - y_mean)**2 for j in y_list]))
    sxy = np.sum(np.array([(i - x_logs_mean) * (j - y_mean) for i, j in zip(x_logs, y_list)]))
    reg_coefficients.append(sxy / sxx)
    reg_coefficients.append(y_mean - reg_coefficients[0] * x_logs_mean)
    a = str(round(reg_coefficients[1], ROUND_TO))
    if reg_coefficients[0] < 0:
        b = " - " + str(round(-1 * reg_coefficients[0], ROUND_TO))
    else:
        b = " + " + str(round(reg_coefficients[0], ROUND_TO))
    if a == "-0.0":
        a = "0.0"
    if b == " + -0.0" or " - -0.0":
        b = b.replace("-0", "0")
    display.append("Logarithmic regression curve: y = " + a + b + "ln(x)")

    residuals = [str(round(j - (reg_coefficients[0] * ma.log(i) + reg_coefficients[1], ROUND_TO)) for i, j
                 in zip(x_list, y_list))]
    update_residuals()

    goodness_of_fit_values = calculate_goodness_of_fit(sxx, syy, sxy)
    display.append(goodness_of_fit_values[0])
    display.append(goodness_of_fit_values[1])

    last_regression = "logarithmic"

    return display


# Performs an exponential regression and returns the formula, r, & r2 to regression() method to be displayed to the GUI
def exponential_regression():
    global residuals
    display = []
    global reg_coefficients
    global last_regression
    reg_coefficients = []

    x_mean = np.average(x_list)
    y_logs = np.array([ma.log10(i) for i in y_list])
    y_logs_mean = np.average(y_logs)
    sxx = np.sum(np.array([(i - x_mean)**2 for i in x_list]))
    syy = np.sum(np.array([(j - y_logs_mean)**2 for j in y_logs]))
    sxy = np.sum(np.array([(i - x_mean) * (j - y_logs_mean) for i, j in zip(x_list, y_logs)]))
    reg_coefficients.append(10**(sxy / sxx))
    reg_coefficients.append(10**(y_logs_mean - x_mean * ma.log10(reg_coefficients[0])))
    a = str(round(reg_coefficients[1], ROUND_TO))
    b = str(round(reg_coefficients[0], ROUND_TO))
    if a == "-0.0":
        a = "0.0"
    if b == "-0.0":
        b = "0.0"
    display.append("Exponential regression curve: y = " + a + "(" + b + ")ˣ")

    residuals = [str(round(j - reg_coefficients[0]**i * reg_coefficients[1], ROUND_TO)) for i, j in zip(x_list, y_list)]
    update_residuals()

    goodness_of_fit_values = calculate_goodness_of_fit(sxx, syy, sxy)
    display.append(goodness_of_fit_values[0])
    display.append(goodness_of_fit_values[1])

    last_regression = "exponential"

    return display


# Main method called by the "Calculate regression" button to calculate a regression given the user's input
def regression():
    global x_list
    global y_list
    global x_size
    global y_size
    global residuals
    display = ""
    regressionDisplay.delete(0, END)
    residuals = []

    # Displays an error if the lists are too small or unequal in size
    if len(list1) != len(list2):
        display = "ERROR: Lists must be of equal size to perform regression"
    elif len(list1) < 2:
        display = "ERROR: List 1 has less than 2 values"
    elif len(list2) < 2:
        display = "ERROR: List 2 has less than 2 values"
    if "ERROR:" in display:
        regressionDisplay.insert(1, display)
        return

    # Displays an error if any values entered by the user are invalid
    for i in range(len(list1)):
        current_list = 1
        try:
            list1[i] = float(list1[i])
            current_list = 2
            list2[i] = float(list2[i])
        except ValueError:
            display = "ERROR: Invalid value at index " + str(i + 1) + " in list " + str(current_list)
            regressionDisplay.insert(1, display)
            return

    # Assigns list 1 and 2 to either x_list or y_list depending on the user's choice
    if variablesSelected.get() == "x = list 1  |  y = list 2":
        x_list = np.array(list1)
        y_list = np.array(list2)
    else:
        x_list = np.array(list2)
        y_list = np.array(list1)
    x_size = np.size(x_list)
    y_size = np.size(y_list)

    # Calls a method to finish the regression depending on which regression is selected by the user
    reg_type = regressionSelected.get()
    if reg_type in polynomial_regressions:
        degree = polynomial_regressions.index(reg_type) + 1
        display = polynomial_regression(degree)
    else:
        # Checks for errors in list values specific to the type of regression
        if error_check(reg_type):
            print("error")
            return
        if reg_type == "power":
            display = power_regression()
        elif reg_type == "inverse":
            display = inverse_regression()
        elif reg_type == "logarithmic":
            display = logarithmic_regression()
        elif reg_type == "exponential":
            display = exponential_regression()

    # The display list returned by whichever regression method was called is displayed to the GUI
    regressionDisplay.insert(1, display[0])
    regressionDisplay.insert(2, display[1])
    regressionDisplay.insert(3, display[2])

    create_graph()


# Takes an x-value entered by the user and uses the last regression to predict its y-value
def predict():
    # Uses last regression to determine what formula to use to predict y
    global last_regression
    x = predictionEntry.get()
    yValueDisplay.delete(0, END)
    # Checks for any errors
    if last_regression is None:
        y = "ERROR: No regression completed"
    elif x == "":
        y = "ERROR: No x-value entered"
    else:
        # Uses a formula based on the last regression performed to compute the predicted y-value
        try:
            x = float(x)
            y = 0
            degree = 0
            if last_regression in polynomial_regressions:
                for i in range(5):
                    if polynomial_regressions[i] == last_regression:
                        degree = i + 1
                        break
            if degree > 0:
                for j in range(degree + 1):
                    y += x ** j * reg_coefficients[j]
            elif last_regression == "power":
                y = x ** reg_coefficients[0] * reg_coefficients[1]
            elif last_regression == "inverse":
                y = reg_coefficients[0] / x + reg_coefficients[1]
            elif last_regression == "logarithmic":
                y = reg_coefficients[0] * ma.log(x) + reg_coefficients[1]
            elif last_regression == "exponential":
                y = reg_coefficients[0] ** x * reg_coefficients[1]
            y = str(round(y, ROUND_TO))
        # Catches any errors caused by an invalid x value entered by the user
        except ValueError:
            y = "ERROR: Invalid x-value"
    yValueDisplay.insert(1, y)


# Graphs the data points and regression curve
def create_graph():
    # Calculates values needed for graphing depending on the regression performed
    x_min = np.min(x_list)
    x_max = np.max(x_list)
    rangex = x_max - x_min
    x = np.linspace(x_min, x_max, 80)
    # Space beyond the domain of the dataset
    x_plus = np.linspace(x_max, x_max + rangex / 2, 80)
    # Space before the domain of the dataset
    x_minus = np.linspace(x_min - rangex / 5, x_min, 80)
    if last_regression in polynomial_regressions:
        degree = polynomial_regressions.index(last_regression) + 1
        temp = 0
        for j in range(degree + 1):
            temp += x ** j * reg_coefficients[j]
        y = temp
        temp = 0
        for j in range(degree + 1):
            temp += x_plus ** j * reg_coefficients[j]
        y_plus = temp
        temp = 0
        for j in range(degree + 1):
            temp += x_minus ** j * reg_coefficients[j]
        y_minus = temp
    elif last_regression == "power":
        y = x ** reg_coefficients[0] * reg_coefficients[1]
        y_plus = x_plus ** reg_coefficients[0] * reg_coefficients[1]
        y_minus = x_minus ** reg_coefficients[0] * reg_coefficients[1]
    elif last_regression == "inverse":
        y = reg_coefficients[0] / x + reg_coefficients[1]
        y_plus = reg_coefficients[0] / x_plus + reg_coefficients[1]
        y_minus = reg_coefficients[0] / x_minus + reg_coefficients[1]
    elif last_regression == "logarithmic":
        # Uses very accurate approximation to avoid errors
        y = reg_coefficients[0] * (9999 * ((x ** (1 / 9999)) - 1)) + reg_coefficients[1]
        y_plus = reg_coefficients[0] * (9999 * ((x_plus ** (1 / 9999)) - 1)) + reg_coefficients[1]
        y_minus = reg_coefficients[0] * (9999 * ((x_minus ** (1 / 9999)) - 1)) + reg_coefficients[1]
    elif last_regression == "exponential":
        y = reg_coefficients[0] ** x * reg_coefficients[1]
        y_plus = reg_coefficients[0] ** x_plus * reg_coefficients[1]
        y_minus = reg_coefficients[0] ** x_minus * reg_coefficients[1]

    # Uses graph created in GUI code section to plot data points and regression curve
    graph.clear()
    graph.plot(x_list, y_list, ".", color="dimgray")
    graph.plot(x_plus, y_plus, color="orangered", linewidth=2)
    graph.plot(x_minus, y_minus, color="orangered", linewidth=2)
    graph.plot(x, y, color="b", linewidth=2)
    fig.canvas.draw()


# Prevents axes from being cut off in graph
rcParams.update({'figure.autolayout': True})

# Begin setup for tkinter window
root = Tk()
root.title("Regression Calculator")
root.resizable(width=True, height=True)
root.geometry('765x695')
root.iconphoto(True, PhotoImage(file="reg_icon.png"))

# Frame used for list delimiter entry related widgets
delimiterFrame = Frame(root, width=800, height=100)
delimiterFrame.grid(row=0, column=0, columnspan=2, sticky=W, pady=(0, 8))

delimiterEntryLabel1 = Label(delimiterFrame, text="Enter character(s) separating values for list 1:  ")
delimiterEntryLabel1.grid(row=0, column=0, sticky=W, padx=2, pady=3)

delimiterEntryLabel2 = Label(delimiterFrame, text="Enter character(s) separating values for list 2:  ")
delimiterEntryLabel2.grid(row=1, column=0, sticky=W, padx=2, pady=3)

delimiterEntry1 = Entry(delimiterFrame, width=40)
delimiterEntry1.grid(row=0, column=1, padx=5, pady=3)
delimiterEntry2 = Entry(delimiterFrame, width=40)
delimiterEntry2.grid(row=1, column=1, padx=5, pady=3)

delimiterLabel1 = Label(delimiterFrame, text='List 1 delimiter: ","')
delimiterLabel1.grid(row=0, column=3, sticky=W, padx=2, pady=3)
delimiterLabel2 = Label(delimiterFrame, text='List 2 delimiter: ","')
delimiterLabel2.grid(row=1, column=3, sticky=W, padx=2, pady=3)

delimiterButton1 = Button(delimiterFrame, text="Confirm", command=set_delimiter1)
delimiterButton1.grid(row=0, column=2, padx=5, pady=3)
delimiterButton2 = Button(delimiterFrame, text="Confirm", command=set_delimiter2)
delimiterButton2.grid(row=1, column=2, padx=5, pady=3)


# Frame used for list value entry related widgets
valuesFrame = Frame(root, width=800, height=100)
valuesFrame.grid(row=1, column=0, columnspan=2, sticky=W)

valuesLabel1 = Label(valuesFrame, text="Enter list 1 values separated by list 1 delimiter:")
valuesLabel1.grid(row=0, column=0, padx=2, pady=(3, 12))
valuesLabel2 = Label(valuesFrame, text="Enter list 2 values separated by list 2 delimiter:")
valuesLabel2.grid(row=1, column=0, padx=2, pady=(3, 12))

entryFrame1 = Frame(valuesFrame)
entryScroll1 = Scrollbar(entryFrame1, orient=HORIZONTAL, width=13)
valuesEntry1 = Entry(entryFrame1, width=70, xscrollcommand=entryScroll1.set)
entryScroll1.config(command=valuesEntry1.xview)
entryScroll1.pack(side=BOTTOM, fill=X)
valuesEntry1.pack()
entryFrame1.grid(row=0, column=1, padx=5, pady=3)
entryFrame2 = Frame(valuesFrame)
entryScroll2 = Scrollbar(entryFrame2, orient=HORIZONTAL, width=13)
valuesEntry2 = Entry(entryFrame2, width=70, xscrollcommand=entryScroll2.set)
entryScroll2.config(command=valuesEntry2.xview)
valuesEntry2.pack()
entryScroll2.pack(side=BOTTOM, fill=X)
entryFrame2.grid(row=1, column=1, padx=5, pady=3)

valuesButton1 = Button(valuesFrame, text="Confirm", command=set_list1)
valuesButton1.grid(row=0, column=2, padx=5, pady=(3, 12))
valuesButton2 = Button(valuesFrame, text="Confirm", command=set_list2)
valuesButton2.grid(row=1, column=2, padx=5, pady=(3, 12))

# Frame used for regression related widgets
regressionFrame = Frame(root, width=800, height=100)
regressionFrame.grid(row=2, column=0, columnspan=2, sticky=W)

variablesLabel = Label(regressionFrame, text="Set independent(x) and dependent(y) variables:")
variablesLabel.grid(row=0, column=0, padx=2, pady=3)
varList = ('x = list 1  |  y = list 2', 'x = list 2  |  y = list 1')
variablesSelected = StringVar()
variablesSelected.set('x = list 1  |  y = list 2')
variablesOptions = OptionMenu(regressionFrame, variablesSelected, *varList)
variablesOptions.grid(row=0, column=1, padx=(3, 8), pady=3)

selectionLabel = Label(regressionFrame, text="Select regression:")
selectionLabel.grid(row=0, column=2, padx=2, pady=3)
regList = ('linear', 'quadratic', 'cubic', 'quartic', 'quintic', 'power', 'inverse',
           'logarithmic', 'exponential')
regressionSelected = StringVar()
regressionSelected.set('linear')
regressionOptions = OptionMenu(regressionFrame, regressionSelected, *regList)
regressionOptions.grid(row=0, column=3, padx=3, pady=3)

calculateButton = Button(regressionFrame, text="Calculate regression", command=regression)
calculateButton.grid(row=0, column=4, padx=9, pady=3)

regDisplayFrame = Frame(regressionFrame)
regressionScroll = Scrollbar(regDisplayFrame, orient=HORIZONTAL, width=13)
regressionDisplay = Listbox(regDisplayFrame, width=123, height=3, xscrollcommand=regressionScroll.set)
regressionScroll.config(command=regressionDisplay.xview)
regressionScroll.pack(side=BOTTOM, fill=X)
regressionDisplay.pack()
regDisplayFrame.grid(row=1, column=0, columnspan=5, sticky=W, padx=8, pady=3)

# Frame used for value prediction related widgets
predictionFrame = Frame(root, width=800, height=50)
predictionFrame.grid(row=3, column=0, columnspan=2, sticky=W)

predictionLabelX = Label(predictionFrame, text="Enter x-value:")
predictionLabelX.grid(row=0, column=0, padx=2, pady=3)

predictionEntry = Entry(predictionFrame, width=22)
predictionEntry.grid(row=0, column=1, padx=5, pady=3)

predictionButton = Button(predictionFrame, text="Predict y-value", command=predict)
predictionButton.grid(row=0, column=2, padx=5, pady=3)

# TODO: Add code to display current regression being used to predict y-value; can display error if no data/reg set
predictionLabelY = Label(predictionFrame, text="Predicted y-value with regression: ")
predictionLabelY.grid(row=0, column=3, padx=(4, 2), pady=3)

yValueDisplay = Listbox(predictionFrame, width=36, height=1)
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
list1Display = Listbox(list1Frame, width=10, height=13, yscrollcommand=list1Scroll.set, xscrollcommand=list1ScrollX.set)
list1Scroll.config(command=list1Display.yview)
list1ScrollX.config(command=list1Display.xview)
list1Scroll.pack(side=RIGHT, fill=Y)
list1ScrollX.pack(side=BOTTOM, fill=X)
list1Display.pack()
list1Frame.grid(row=1, column=0, sticky=NW, padx=(8, 6), pady=3)

l1StatsFrame = Frame(listsFrame)
l1StatsScroll = Scrollbar(l1StatsFrame, orient=VERTICAL, width=13)
l1StatsScrollX = Scrollbar(l1StatsFrame, orient=HORIZONTAL, width=13)
l1Stats = Listbox(l1StatsFrame, width=10, height=6, yscrollcommand=l1StatsScroll.set, xscrollcommand=l1StatsScrollX.set)
l1StatsScroll.config(command=l1Stats.yview)
l1StatsScrollX.config(command=l1Stats.xview)
l1StatsScroll.pack(side=RIGHT, fill=Y)
l1StatsScrollX.pack(side=BOTTOM, fill=X)
l1Stats.pack()
l1StatsFrame.grid(row=2, column=0, sticky=NW, padx=(8, 6), pady=11)

list2Frame = Frame(listsFrame)
list2Scroll = Scrollbar(list2Frame, orient=VERTICAL, width=13)
list2ScrollX = Scrollbar(list2Frame, orient=HORIZONTAL, width=13)
list2Display = Listbox(list2Frame, width=10, height=13, yscrollcommand=list2Scroll.set, xscrollcommand=list2ScrollX.set)
list2Scroll.config(command=list2Display.yview)
list2ScrollX.config(command=list2Display.xview)
list2Scroll.pack(side=RIGHT, fill=Y)
list2ScrollX.pack(side=BOTTOM, fill=X)
list2Display.pack()
list2Frame.grid(row=1, column=1, sticky=NW, padx=6, pady=2)

l2StatsFrame = Frame(listsFrame)
l2StatsScroll = Scrollbar(l2StatsFrame, orient=VERTICAL, width=13)
l2StatsScrollX = Scrollbar(l2StatsFrame, orient=HORIZONTAL, width=13)
l2Stats = Listbox(l2StatsFrame, width=10, height=6, yscrollcommand=l2StatsScroll.set, xscrollcommand=l2StatsScrollX.set)
l2StatsScroll.config(command=l2Stats.yview)
l2StatsScrollX.config(command=l2Stats.xview)
l2StatsScroll.pack(side=RIGHT, fill=Y)
l2StatsScrollX.pack(side=BOTTOM, fill=X)
l2Stats.pack()
l2StatsFrame.grid(row=2, column=1, sticky=NW, padx=(8, 6), pady=11)

residualsFrame = Frame(listsFrame)
residualsScroll = Scrollbar(residualsFrame, orient=VERTICAL, width=13)
residualsScrollX = Scrollbar(residualsFrame, orient=HORIZONTAL, width=13)
residualsDisplay = Listbox(residualsFrame, width=10, height=21,
                           yscrollcommand=residualsScroll.set, xscrollcommand=residualsScrollX.set)
residualsScroll.config(command=residualsDisplay.yview)
residualsScrollX.config(command=residualsDisplay.xview)
residualsScroll.pack(side=RIGHT, fill=Y)
residualsScrollX.pack(side=BOTTOM, fill=X)
residualsDisplay.pack()
residualsFrame.grid(row=1, column=2, sticky=NW, rowspan=2, padx=6, pady=2)

# Frame used for the matplotlib graph
graphFrame = Frame(root, highlightbackground="gray", highlightthickness=1, width=480, height=350)
graphFrame.grid(row=4, column=0, sticky=SW, padx=(285, 0), pady=6)

fig = Figure(figsize=(5.7, 4.2), dpi=80)
graph = fig.add_subplot(111)
graph.set_xlabel('x-values', fontsize=12)
graph.tick_params(axis='x', labelsize=10, labelrotation=30)
graph.set_ylabel('y-values', fontsize=12)
graph.tick_params(axis='y', labelsize=10, labelrotation=30)
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
