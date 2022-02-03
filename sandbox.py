import streamlit as st
import numpy as np
import pandas as pd

st.title("Streamlit Testing Sandbox")
st.write("") #blank space


#example dataframe (table) with random numbers
st.write("Dataframe")
dataframe = np.random.randn(10, 20)
st.dataframe(dataframe)

#example dataframe that uses a Pandas Styler object to highlight elements in the table
st.write("Dataframe with Highlight Styler")
dataframe = pd.DataFrame(
    np.random.randn(10, 20),
    columns=('col %d' % i for i in range(20)))

st.dataframe(dataframe.style.highlight_max(axis=0))

#static dataframe
st.write("Static Table")
dataframe = pd.DataFrame(
    np.random.randn(10, 20),
    columns=('col %d' % i for i in range(20)))
st.table(dataframe)

#line chart
st.write("line chart")
chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['a', 'b', 'c'])

st.line_chart(chart_data)

#map with scatter points on it, should use a mapbox.com token to customize map
st.write("map")
map_data = pd.DataFrame(
    np.random.randn(100, 2) / [10, 10] + [42.727, -92.467],
    columns=['lat', 'lon'])

st.map(map_data)

#widgets, can think of like variables 

#slider
st.write("Slider")
x = st.slider('x')  # 👈 this is a widget
st.write(x, 'squared is', x * x)

#checkboxes to show/hide data
st.write("Checkboxes")
if st.checkbox('Show dataframe'):
    chart_data = pd.DataFrame(
       np.random.randn(20, 3),
       columns=['a', 'b', 'c'])

    chart_data

#selectbox for choosing options form a series
st.write("selectbox")
df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
    })

option = st.selectbox(
    'Which number do you like best?',
     df['first column'])

'You selected: ', option

#layout

#Sidebar with selectbox and slider

# Add a selectbox to the sidebar:
add_selectbox = st.sidebar.selectbox(
    'How would you like to be contacted?',
    ('Email', 'Home phone', 'Mobile phone')
)

# Add a slider to the sidebar:
add_slider = st.sidebar.slider(
    'Select a range of values',
    0.0, 100.0, (25.0, 75.0)
)

#Columns (place widgets side by side) and expander (hides large elements)
left_column, right_column = st.columns(2)
# You can use a column just like st.sidebar:
left_column.button('Press me!')

# Or even better, call Streamlit functions inside a "with" block:
with right_column:
    chosen = st.radio(
        'Sorting hat',
        ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
    st.write(f"You are in {chosen} house!")