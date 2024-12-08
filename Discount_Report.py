import pymysql
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu 


def db():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='34&*^&AsXti2098as3#$><?',
        database='rtpos'
    )

# Establish a connection to the database
mydb = db()

# Create a cursor to interact with the database
mycursor = mydb.cursor()

# Write a query to fetch the data from the desc_report table
query = "SELECT * FROM desc_report"

# Execute the query
mycursor.execute(query)

# Fetch all rows from the executed query
result = mycursor.fetchall()

# Get the column names
columns = [desc[0] for desc in mycursor.description]

# Load the result into a pandas DataFrame
df = pd.DataFrame(result, columns=columns)

# Close the cursor and connection
mycursor.close()
mydb.close()

# Display the DataFrame in the Streamlit app
st.title("Final Discount Report Data")

selected = option_menu(menu_title=None,options=["Data Record", "Data Updation"],orientation='horizontal',
                    styles={
                        "nav-link": {"--hover-color": "#a42bad4b"},
                        "nav-link-selected": {"background-color": "#832a80"}
                        },key="0")

if selected == "Data Record":
    
    filtered_df = df

    # Sidebar filter for Store_ID
    store_ids = df["Store_ID"].unique().tolist()
    selected_store_ids = st.sidebar.multiselect("Filter by Store ID", options=store_ids)

    # Filter the DataFrame
    if len(selected_store_ids) == 0:
        pass
    else:
        filtered_df = df[df["Store_ID"].isin(selected_store_ids)]

    # Display the filtered DataFrame
    st.dataframe(filtered_df,hide_index=True)

    


