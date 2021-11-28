# Regression Calculator

The code for this personal project was written independently and can be found in the main.py file.

Upon running the program, the following GUI opens:

![image](https://user-images.githubusercontent.com/88519278/143723755-9ef3bcca-1bac-4c42-b86b-021db1882318.png)

The purpose of this GUI program is to allow the user to enter two lists of data and perform regression analysis on them. After entering data, selecting a regression type, and choosing the independent and dependent lists, the program will calculate the regression formula that best fits the data and graph it using a matplotlib graph.

The first option the user has is entering a delimiter for each list, which simply specifies what character(s) will be used to separate data values when entering the list data. This is escpecially useful when copying data from another source in which the user has no control over the delimiter. Once a delimiter is specified, the user can then enter a list. Once entered, each list is displayed in a scrollable, indexed listbox. Additionally, 1 variable statistics such as mean, median, mode, sum, etc. are calculated and displayed below each list. This can be seen in the image below; a comma is used as the delimiter for both lists:

![image](https://user-images.githubusercontent.com/88519278/143723086-915b179d-5ce5-41ef-9eff-c150a7a9e934.png)

Next the user uses a dropdown to select which list will act as the independent variable and which will act as the dependent variable. Another dropdown allows the user to select which regression to perform. The included regressions are linear, quadratic, cubic, quartic, quintic, power, inverse, logarithmic, and exponential regressions. Each regression checks for invalid list values specific to that type of regression in addition to the basic error checking. Once the user is ready, clicking "Calculate regression" will calculate and display the specified regression formula as well as its correlation coefficiant and coefficient of determination (measures of how well the regression fits the data) in the large listbox in the middle of the GUI. An indexed list of residuals (the distance of each data point to the regression curve) is also filled next to the main lists. Additionally, a graph is displayed using matplotlib containing the plotted datapoints as well as the regression curve. The blue part of the curve represents the part within the domain of the dataset, while orange indicates extrapolation beyond the range of the data. An example of a completed quadratic regression is shown below:

![image](https://user-images.githubusercontent.com/88519278/143723411-f80eca7b-e145-4b2e-8834-fa528e693015.png)

The logic behind the inverse, power, logarithmic, and exponential regressions is similar. Each involved manipulating the lists and then applying statistical formulas to calculate the coefficients for the regression formula. The linear, quadratic, cubic, quartic, and quintic regressions are all considered polynomial regressions, each with a different degree, or highest exponent. This allows all polynomial regressions to be computed within one method by applying linear algebra utilizing the numpy library to matrices which sizes depend on the degree of the polynomial regression. The resulting matrix contains the regression's coefficients that simply need to be formatted into a readable formula.

The program also includes extensive error checking which catches user errors and displays custom messages in the listboxes which would otherwise display the results of the user's input. Here's an example of what happens when a regression is performed while there are invalid list values: 

![image](https://user-images.githubusercontent.com/88519278/143723166-52752f63-dd48-4c39-9c98-3e9491962598.png)

The last feature predicts a dependent y-value based on an indepedent x-value entered by the user. This simply enters the user's x-value into the previously calculated regression formula and displays the y-value that lies on the regression curve at the user-entered x-value, as shown below:

![image](https://user-images.githubusercontent.com/88519278/143723550-032a127c-aea1-464d-8d07-3b78cbb670a9.png)

The toolbar below the graph is provided by matplotlib automatically and provides features such as panning, zooming, and saving the graph as a png. Here's an example of the same graph above after zooming:

![image](https://user-images.githubusercontent.com/88519278/143723608-213eb93e-6f35-4385-9a3c-e33a8d3ce443.png)



