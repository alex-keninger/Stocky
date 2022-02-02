import streamlit as st #imports streamlit and changes its reference to st
from datetime import date
import pandas as pd # imports panda library and changes its reference to pd



st.write("""
# CS 460 Stock Analysis Web App
# Hello *Bozo!*
# """)
###
import yfinance as yf
#from prophet import Prophet
#from prophet.plot import plot_plotly
from plotly import graph_objs as go

START = "2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

st.title("Stock Prediction App")

st.sidebar.write("Example sidebar text") #st.sidebar puts widgets and texts in a sidebar on your page




stocks = ("APRE","AAPL", "GOOG", "MSFT", "GME")
selected_stocks = st.selectbox("Select dataset for prediction", stocks)

#n_years = st.slider("Years of prediction:", 1, 4)
#period = n_years * 365

@st.cache #caches the data, doesnt need to run this code again if stock has been cached
def load_data(ticker):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace=True)
    return data

data_load_state = st.text("Load data...")
data = load_data(selected_stocks)
data_load_state.text("Loading data...done!")


st.subheader('Raw data')
st.write(data.tail()) 
    #creates a table with data entries from yahoo finance
    # tail cuts off the last entries (default of 5)
    #this is also already a pandas dataframe so stremlit can handle it

def plot_raw_data(): #configures and creates plot.ly graph, could also look into matplotlib graph
    fig = go.Figure()
    fig.add_trace(go.Scatter(x= data['Date'], y=data['Open'], name='stock_open'))
    fig.add_trace(go.Scatter(x= data['Date'], y=data['Close'], name='stock_close'))
    fig.layout.update(title_text="Time Series Data", xaxis_rangeslider_visible=True)
    st.plotly_chart(fig) #creates the plotly graph integrated with streamlit

plot_raw_data()