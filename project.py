
from io import StringIO
import streamlit as st #imports streamlit and changes its reference to st
from datetime import date
import pandas as pd # imports panda library and changes its reference to pd
import yfinance as yf
from plotly import graph_objs as go

START = "2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

watchlist_stocks = []

if 'watchlist_stocks' not in st.session_state:  #initializes the session state for saving watchlist variables
    st.session_state.watchlist_stocks = []
if 'selected_stock' not in st.session_state:
    st.session_state.selected_stock = ''

page_names = ["Home", "Watchlist", "Analysis"]
page = st.sidebar.radio('Navigation', page_names)



try:
    if page == "Home":
        
        st.write("""
        # CS 460 Stock Analysis Web App
        # Hello!
        ##### Welcome to STOCKY! 
        This is a free-to-use web application that allows you to
        view real, up-to-date financial information in one convinient location. See raw data, view charts, creates watchlists,
        and more! 

        Created by Alex Keninger and Michael Hoelzer.""")
        
        st.title("Stock Analyzer Test")

        input = st.text_input("Input stock")
        search_stock = st.checkbox("Check to search for stock")
        if search_stock:
            st.session_state.selected_stock = input
            st.warning("If you are done searching for this stock, make sure to uncheck the box above")
        
        if st.session_state.selected_stock == "": #displays info box when no ticker is entered
            st.info("Enter your ticker in the box above")

        @st.cache #caches the data, doesnt need to run this code again if stock has been cached
        def load_data(ticker):
            data = yf.download(ticker, START, TODAY)
            data.reset_index(inplace=True)
            return data

        if st.session_state.selected_stock == '':
            data = load_data("AAPL")
            st.warning("Currently showing data for AAPL. Try inputing your own ticker!")
        else:
            data = load_data(st.session_state.selected_stock)

        while True: #Catchs invalid tickers and produces an error message
            try: 
                testingbox = data.at[0,"Date"] #checks to see if there is any "date" data
                break
            except KeyError: 
                st.error("Please enter a valid ticker")
                break


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

        if st.session_state.selected_stock == "": #title that shows the current stock
            st.title("Currently viewing data for...")
            st.title("AAPL")
        else:
            st.title("Currently viewing data for...")
            st.title(st.session_state.selected_stock)

        def plot_raw_data(): #configures and creates plot.ly graph, could also look into matplotlib graph
            fig = go.Figure()
            fig.add_trace(go.Scatter(x= data['Date'], y=data['Open'], name='stock_open'))
            fig.add_trace(go.Scatter(x= data['Date'], y=data['Close'], name='stock_close'))
            fig.layout.update(title_text="Time Series Data", xaxis_rangeslider_visible=True)
            st.plotly_chart(fig) #creates the plotly graph integrated with streamlit
        
        plot_raw_data() #plots the graph

    elif page == "Watchlist":
        
        st.title("Watchlist") #st.sidebar puts widgets and texts in a sidebar on your page

        #Adds stocks to the watchlist and saves them to session state
        watchstock = st.text_input("Enter a stock to add to watchlist")
        add_stock = st.checkbox("Check to add stock")
        if add_stock:
            st.session_state.watchlist_stocks.append(watchstock)
            st.warning("If you are done adding your stock, make sure to uncheck the box above")

        selected_watch_stock = st.selectbox("Current Watchlist", st.session_state.watchlist_stocks) 


        #A button when clicked that clears the watchlist
        ###Problem here probably has to do with the 'keys' session state not being defined
        st.title("")
        result = st.button("Click to clear your watchlist")
        if result:
            for key in st.session_state.keys(): #deletes all the keys saved in session_state
                    del st.session_state[key]


        #Downloads watchlist to a text file
        st.title("")
        st.download_button('Download your watchlist', str(st.session_state.watchlist_stocks))
        
        #Uploads a previously downloaded watchlist
        st.title("")
        uploaded_file = st.file_uploader("Upload a previous watchlist")
        if uploaded_file is not None:
            # To read file as bytes:
            bytes_data = uploaded_file.getvalue()
            #st.write(bytes_data)

            # To convert to a string based IO:
            stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
            #st.write(stringio)

            # To read file as string:
            string_data = stringio.read()
            #st.write(string_data)

            # Can be used wherever a "file-like" object is accepted:
            uploaded_watchlist = pd.read_csv(uploaded_file)
            for i in uploaded_watchlist:
                i = ''.join(filter(str.isalnum, i)) #ensures only the letters for the ticker are used
                st.session_state.watchlist_stocks.append(i)
            st.warning("""While this feature does upload an existing watchlist, a certain bug
                            may cause the app to freeze. 
                            
                            If this occurs, please refresh the page. """)
            
            
            

    elif page == "Analysis":
        
        st.warning("This page is currently under construction")  
        st.write("""While this page is incompete, once finished this page
        will allow the user to generate a reccomendation for whether 
        an inputted stock is a good or bad buy based off of our created
        algorithm. The incomplete code which showcases the details
        of our algorithm is listed below. 
        
        #Condition 1: Current Price > 150 SMA and > 200 SMA
		if(currentClose>moving_average_150>moving_average_200):
			cond_1=True
		else:
			cond_1=False
		
        #Condition 2: 150 SMA and > 200 SMA
		if(moving_average_150>moving_average_200):
			cond_2=True
		else:
			cond_2=False
		
        #Condition 3: 200 SMA trending up for at least 1 month (ideally 4-5 months)
		if(moving_average_200>moving_average_200_20):
			cond_3=True
		else:
			cond_3=False
		
        #Condition 4: 50 SMA> 150 SMA and 50 SMA> 200 SMA
		if(moving_average_50>moving_average_150>moving_average_200):
			#print("Condition 4 met")
			cond_4=True
		else:
			#print("Condition 4 not met")
			cond_4=False
		
        #Condition 5: Current Price > 50 SMA
		if(currentClose>moving_average_50):
			cond_5=True
		else:
			cond_5=False
		
        #Condition 6: Current Price is at least 30% above 52 week low (Many of the best are up 100-300% before coming out of consolidation)
		if(currentClose>=(1.3*low_of_52week)):
			cond_6=True
		else:
			cond_6=False
		
        #Condition 7: Current Price is within 25% of 52 week high
		if(currentClose>=(.75*high_of_52week)):
			cond_7=True
		else:
			cond_7=False
		
        #Condition 8: IBD RS rating >70 and the higher the better
		if(RS_Rating>70):
			cond_8=True
		else:
			cond_8=False""")  


    watchstockview = st.sidebar.selectbox("Current watchlist", st.session_state.watchlist_stocks)
    search = st.sidebar.button("Click to search for selected stock")  

    if search:
        st.session_state.selected_stock = watchstockview
        st.sidebar.text("(May need to click button twice)") 
        
except AttributeError:
    st.warning("You are about to clear your watchlist. Click the button below to confirm.")
    st.button("Confirm?")



    
    




