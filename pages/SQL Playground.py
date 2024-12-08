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
mycursor = mydb.cursor()

# Streamlit app code
st.title("SQL Playground")

lst =    [ "Market VARCHAR (255)", "Store VARCHAR(255)", "Store_ID VARCHAR(255) PRIMARY KEY", "Store_Limit INT",
          "Override_Disc FLOAT null", "Disc_SKU FLOAT null", "Total_Availed FLOAT null", "Remaining FLOAT null",
          "EOL FLOAT null", "Aging FLOAT null", "Cx_Survey FLOAT null", "MD_approved FLOAT null", "Comment VARCHAR(255)"
        ]

st.write("Database Column Info:", lst)

# Get user input (SQL query)
query = st.text_area(f'Enter your SQL queries for table "desc_report"')

# Execute the query and display the results
if st.button("Execute"):
    cursor = mydb.cursor()

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
    finally:
        cursor.close()
