import streamlit
import pandas as pd
import requests
import snowflake.connector
from irllib.error import URLError 

# get data from S3
my_fruit_list_s3_url = r"https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt"
my_fruit_list = pd.read_csv(my_fruit_list_s3_url)
my_fruit_list = my_fruit_list.set_index('Fruit')

# Start development of app
streamlit.title("My Parents New Healthy Dinner")

# First section - Menu
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

# Second Section - Smoothie
# Fruits list from S3 bucket
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), default=['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

# Third Section - Implement API call for fruit information
streamlit.header('Fruityvice Fruit Advice!')
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
  
  if not fruit_choice:
    stremlit.error('Please select a fruit to get information')
  else:
    fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{fruit_choice}")
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    streamlit.dataframe(fruityvice_normalized)

except URLError as e:
  streamlit.error()

# Fourth Section - get fruit list from snowflake db
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)

# list of tuples -> list of strings
my_cleaned_data = [elem[0] for elem in my_data_rows]
add_my_fruit = streamlit.multiselect('What fruit would you like to add?', my_cleaned_data, default = ['banana'])
streamlit.text(f"Thanks for adding {', '.join(add_my_fruit)}")




