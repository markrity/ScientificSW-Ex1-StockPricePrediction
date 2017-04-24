# ScientificSW-Ex1-StockPricePrediction
#Homework exercise of Scientific Software course, a stock price prediction using linear regression.

from yahoo_finance import Share
from Tkinter import *
import tkMessageBox

#Global variables:
predicted_price = None
stock_dates_list=[]
stock_close_prices_list=[]
stock_props_between_dates = []


def fromFormToVars(event):
    global stock_name,start_date,end_date,prediction_date
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
    for i in reversed(range(len(stock_props_between_dates))):
        stock_dates_list.append(stock_props_between_dates[i]['Date'])
        stock_close_prices_list.append(stock_props_between_dates[i]['Close'])

def createForm():
    global root
    global stock_name_entry,start_date_entry,end_date_entry,prediction_date_entry

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
    make_label(root, 133, 170, 25, 143, text=predicted_price, background=None)

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

