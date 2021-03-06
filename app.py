# ScientificSW-Ex1-StockPricePrediction
#Homework exercise of Scientific Software course, a stock price prediction using linear regression.

from yahoo_finance import Share
from Tkinter import *
import tkMessageBox
import datetime #used for date to int conversion
import matplotlib.pyplot as plt
import numpy as np

#Global variables:
predicted_price = 0

stock_dates_list=[]
stock_close_prices_list=[]
stock_props_between_dates = []
number_of_prices = len(stock_dates_list)

stock_dates_as_int_list = []
regression_prices = []
slope = 0
intercept=0

def dateToInt(date_str):
    '''
    Function that converts dates to ints.
    :param date_str:  Date as a string in YYYY-MM-DD format.
    :return: Date an int variable
    '''
    year, month, day = map(int, date_str.split('-'))
    return (datetime.datetime(year, month, day) - datetime.datetime(1900, 1, 1)).days + 2

def allDatesToInts():
    '''
    Function that converts all stock dates to list of ints
    '''
    global stock_dates_as_int_list
    stock_dates_as_int_list = []
    for date in range(len(stock_dates_list)):
        stock_dates_as_int_list.append(dateToInt(stock_dates_list[date]))

def fromFormToVars(event):
    global stock_name,start_date,end_date,prediction_date
    plt.close()
    stock_name = stock_name_entry.get()
    start_date=start_date_entry.get()
    end_date=end_date_entry.get()
    prediction_date=prediction_date_entry.get()
    getDataFromYahoo()

def getDataFromYahoo():
    '''
    This function will get variables from GUI Form,
    Will get the required stock information from Yahoo servers.
    '''
    global stock_props_between_dates
    stock_name_from_yahoo = Share(stock_name)
    if(stock_name_from_yahoo.get_price()==None): tkMessageBox.showinfo("Error", "Stock Data Error!")
    stock_props_between_dates = stock_name_from_yahoo.get_historical(start_date, end_date)
    dataToLists()

def dataToLists():
    global stock_dates_list
    global stock_close_prices_list
    stock_dates_list = []
    stock_close_prices_list = []
    for i in reversed(range(len(stock_props_between_dates))):
        stock_dates_list.append(stock_props_between_dates[i]['Date'])
        stock_close_prices_list.append(float(stock_props_between_dates[i]['Close']))
    allDatesToInts()
    calcSlopeAndIntercept()

def calcSlopeAndIntercept():
    global slope,intercept,number_of_prices
    number_of_prices = len(stock_dates_list)
    # calculating the slope(m) of the linear regresion
    # step 1
    # collect all our points as (dates,prices) and we got the number_of_prices as number of points
    # step 2
    # Let a equal number_of_prices times the summation of all date-values multiplied by their corresponding price-values, so :
    sum_of_mults = 0
    for index in range(number_of_prices):
        sum_of_mults = sum_of_mults + stock_dates_as_int_list[index] * stock_close_prices_list[index]
    a = sum_of_mults * number_of_prices
    # step 3
    # Let b equal the sum of all date-values times the sum of all price-values, like so :
    sum_of_dates = 0
    for index in range(len(stock_dates_as_int_list)):
        sum_of_dates = sum_of_dates + stock_dates_as_int_list[index]

    sum_of_prices = 0
    for index in range(len(stock_close_prices_list)):
        sum_of_prices = sum_of_prices + stock_close_prices_list[index]
    b = sum_of_dates * sum_of_prices
    # step 4
    # Let c equal number_of_prices time the sum of all squared date-values , like so :
    squared_date = 0
    for index in range(len(stock_dates_as_int_list)):
        squared_date = squared_date + stock_dates_as_int_list[index] * stock_dates_as_int_list[index]
    c = number_of_prices * squared_date
    # step 5
    # Let d equal the squared sume of all date-values:
    d = sum_of_dates * sum_of_dates
    # step 6
    # plug the values that you calculated for a,b,c and d into equation to calculate the slope - m of the regression line
    slope = (a - b) / (c - d)
    # calculating the intercept
    # step 1
    # Let e equal the sum of all prices-values
    e = sum_of_prices
    # step 2
    # Let f equal the slope times the sum of all date-values:
    f = slope * sum_of_dates
    # step 3
    # Plug the values into intercept equalation
    intercept = (e - f) / number_of_prices
    # to calculate the prediction use :
    # predicted_price = slope*date+intercept  dateToInt(prediction_date)
    calculatePredictedPrice()
    plotDisplay(stock_close_prices_list,stock_dates_list)


def calculatePredictedPrice():
    global predicted_price
    predicted_price =slope*dateToInt(prediction_date)+intercept
    predicted_price=round(predicted_price,5)
    pricted_price_label.set(predicted_price)

# Makes an array that represents the regression line.
def makeRegressionArray():
    global regression_prices
    regression_prices = []
    # Calculating the regression prices.
    for index in range(len(stock_dates_as_int_list)):
        regression_prices.append(slope * (stock_dates_as_int_list[index]) + intercept)

    first_price = regression_prices[0]
    last_price = regression_prices[len(regression_prices) -1]

    new_array = []
    new_array.append(first_price)

    diff = (last_price - first_price)/(len(regression_prices)-1)

    for i in range(len(regression_prices) -1):
        n = new_array[i] + diff
        new_array.append(n)

    return new_array

def plotDisplay(price, date):

    length = len(date)
    x = range(len(date))
    plt.xticks([0, length/2, length-1], (date[0], date[length/2], date[length-1]))
    plt.plot(x, price, "g")

    plt.xlabel('Dates')
    plt.ylabel('Stock Closing Price')
    plt.title('Stock Graph')

    fit = np.polyfit(stock_dates_as_int_list, price, 1)
    fit_fn = np.poly1d(fit)

    regression = makeRegressionArray()
    plt.plot(regression, '--k')

    plt.get_current_fig_manager().window.wm_geometry("+400+135")  # move the window
    plt.gcf().canvas.set_window_title("ScientificSW-Ex1-StockPricePrediction")

    plt.show()
    plt.clf()
    plt.cla()
    plt.close()


def createForm():
    global root
    global stock_name_entry,start_date_entry,end_date_entry,prediction_date_entry,pricted_price_label

    root = Tk()
    root.title("ScientificSW-Ex1-StockPricePrediction")
    root.geometry("682x225")
    root.resizable(0, 0)

    #Labels:
    def make_label(master, x, y, h, w, *args, **kwargs):
        f = Frame(master, height=h, width=w)
        f.pack_propagate(0)  # don't shrink
        f.place(x=x, y=y)
        label = Label(f, font=("Helvetica", 12) ,*args, **kwargs )
        label.pack(fill=BOTH, expand=1)
        return label

    make_label(root, 36, 32, 25, 119, text='Stock Name', background=None)
    make_label(root, 206, 32, 25, 99, text='Start Date', background=None)
    make_label(root, 374, 32, 25, 93, text='End Date', background=None)
    make_label(root, 513, 32, 25, 144, text='Prediction Date', background=None)
    make_label(root, 32, 170, 25, 104, text='Prediction:', background=None)
    pricted_price_label = StringVar()
    make_label(root, 133, 170, 25, 143, textvariable=pricted_price_label, background=None)

    #Entries
    stock_name_entry = Entry(root,font=("Helvetica", 12))
    stock_name_entry.place(x=37,y=61,width=114)
    start_date_entry = Entry(root,font=("Helvetica", 12))
    start_date_entry.place(x=200, y=61,width=114)
    end_date_entry = Entry(root,font=("Helvetica", 12))
    end_date_entry.place(x=363, y=61,width=114)
    prediction_date_entry = Entry(root,font=("Helvetica", 12))
    prediction_date_entry.place(x=526, y=61,width=114)

    #Button
    find_button = Button(root, text="Find Regression",font=("Helvetica", 12))
    find_button.bind("<ButtonRelease-1>", fromFormToVars)
    find_button.place(x=37, y=112, width=163, height=38)
    root.mainloop()

createForm()

