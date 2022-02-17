from pyparsing import null_debug_action
from sqlalchemy import null
import streamlit as st #imports streamlit and changes its reference to st
from datetime import date
import pandas as pd # imports panda library and changes its reference to pd



st.write("""
# CS 460 Stock Analysis Web App
# Hello *Bozo!*
##### "Enter a description of the app here"
# """)
###
import yfinance as yf
#from prophet import Prophet
#from prophet.plot import plot_plotly
from plotly import graph_objs as go

START = "2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

st.title("Stock Analyzer")

st.sidebar.write("Example sidebar text") #st.sidebar puts widgets and texts in a sidebar on your page


#stocks = ("APRE","AAPL", "GOOG", "MSFT", "GME")
selected_stocks = st.text_input("Input stock")
if selected_stocks == "": #displays info box when no ticker is entered
    st.info("Enter your ticker in the box above")

@st.cache #caches the data, doesnt need to run this code again if stock has been cached
def load_data(ticker):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace=True)
    return data


data_load_state = st.text("Load data...")
if selected_stocks == "":
    data = load_data("AAPL")
    st.warning("Currently showing data for AAPL. Try inputing your own ticker!")
else:
    data = load_data(selected_stocks)

while True: #Catchs invalid tickers and produces an error message
    try: 
        testingbox = data.at[0,"Date"] #checks to see if there is any "date" data
        break
    except KeyError: 
        st.error("Please enter a valid ticker")
        break

data_load_state.text("Loading data...done!")

st.write()
DateRange = st.selectbox("How far would you like to look back?", ["1 week", "1 month", "3 months", "1 year", "All Time"])
if DateRange == "1 week":
    DateRange = 7
elif DateRange == "1 month":
    DateRange = 31
elif DateRange == "3 months":
    DateRange = 93
elif DateRange == "1 year":
    DateRange = 365


st.subheader('Raw data')
if DateRange == "All Time":
    st.write(data)
else:
    with st.expander("Click to expand"):
        st.write(data.tail(DateRange)) 
    #creates a table with data entries from yahoo finance
    # tail cuts off the last entries determined by the DateRange

def plot_raw_data(): #configures and creates plot.ly graph, could also look into matplotlib graph
    fig = go.Figure()
    fig.add_trace(go.Scatter(x= data['Date'], y=data['Open'], name='stock_open'))
    fig.add_trace(go.Scatter(x= data['Date'], y=data['Close'], name='stock_close'))
    fig.layout.update(title_text="Time Series Data", xaxis_rangeslider_visible=True)
    st.plotly_chart(fig) #creates the plotly graph integrated with streamlit

plot_raw_data()