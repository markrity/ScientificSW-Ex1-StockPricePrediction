# ScientificSW-Ex1-StockPricePrediction
#Homework exercise of Scientific Software course, a stock price prediction using linear regression.

from yahoo_finance import Share

#Global variables:
predicted_price = None
stock_dates_list=[]
stock_close_prices_list=[]
stock_props_between_dates = []


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


