import pymysql
import streamlit as st
import numpy as np
import pandas as pd

# Establish a connection to MySQL Server
def db():
    return pymysql.connect(   
    host='localhost',
    user='root',
    password='34&*^&AsXti2098as3#$><?',
    database='rtpos'
    )
mydb = db() 
cursor = mydb.cursor()

# Streamlit app code
st.title("SQL Playground")

with st.expander("Run Queries"):
    lst =    [ "Market VARCHAR (255)", "Store VARCHAR(255)", "Store_ID VARCHAR(255) PRIMARY KEY", "Store_Limit INT",
            "Override_Disc FLOAT null", "Disc_SKU FLOAT null", "Total_Availed FLOAT null", "Remaining FLOAT null",
            "EOL FLOAT null", "Aging FLOAT null", "Cx_Survey FLOAT null", "MD_approved FLOAT null", "Comment VARCHAR(255)"
            ]

    st.write("Database Column Info:", lst)

    # Get user input (SQL query)
    query = st.text_area(f'Enter your SQL queries for table "desc_report"')

    # Execute the query and display the results
    if st.button("Execute"):
        try:
            # Execute the query
            cursor.execute(query)
            # Determine the type of query and handle accordingly
            query_type = query.strip().split()[0].lower()

            if query_type == "insert":
                mydb.commit()
                st.success("Query executed successfully. Data inserted.")
            elif query_type == "update":
                mydb.commit()
                st.success("Query executed successfully. Data updated.")
            elif query_type == "delete":
                mydb.commit()
                st.success("Query executed successfully. Data deleted.")
            else:
                # For queries that return results (e.g., SELECT)
                results = cursor.fetchall()
                if results:
                    # Get column names
                    columns = [col[0] for col in cursor.description]
                    # Create a DataFrame from the results
                    df = pd.DataFrame(results, columns=columns)
                    st.dataframe(df)
                else:
                    st.info("No results found.")

        except pymysql.Error as err:
            st.error(f"Error: {err}")

# Write a query to fetch the data from the desc_report table
query = "SELECT * FROM desc_report"
cursor.execute(query)
result = cursor.fetchall()

# Get the column names
columns = [desc[0] for desc in cursor.description]
df = pd.DataFrame(result, columns=columns)

filtered_df = df
st.sidebar.header("Please Filter Here:")
# Sidebar - Filter by Market (with multiselect)
MARKET_options = sorted(df['Market'].unique().tolist())  # Add 'All' to MD options
selected_market = st.sidebar.multiselect('Select Market', MARKET_options,key="1")

# Filter MD only if 'All' is not selected
if len(selected_market) == 0:
    pass
else:
    filtered_df = df[df['Market'].isin(selected_market)]

# Ensure filtered_df is not empty before applying Store ID filter
if not filtered_df.empty:
    store_ids = filtered_df["Store_ID"].unique().tolist()
    selected_store_ids = st.sidebar.multiselect("Select Store ID", options=store_ids)
    
    # Filter MARKET only if True
    if len(selected_store_ids) > 0:
        filtered_df = filtered_df[filtered_df['Store_ID'].isin(selected_store_ids)]

if not filtered_df.empty:
    stores = filtered_df["Store"].unique().tolist()
    selected_store = st.sidebar.multiselect("Select Store", options=stores)
    
    # Filter MARKET only if True
    if len(selected_store) > 0:
        filtered_df = filtered_df[filtered_df['Store'].isin(selected_store)]

# Display the filtered DataFrame
st.dataframe(filtered_df,hide_index=True)