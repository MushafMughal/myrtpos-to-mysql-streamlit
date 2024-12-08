#import mysql.connector
import pymysql
import pandas as pd
import streamlit as st
import numpy as np
import time

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

# Preprocessing the data for database
def new_data_preprocessing(data1,data2,data3):

    #importing first data file
    override =   pd.read_excel(data1)
    override.columns = override.columns.str.lower().str.strip()

    #PREPROCESSING
    #for store id column
    override = override[~override['store name'].str.contains("Market:",na=False)]
    override['store id'] = override['store name'].where(override['store name'].str.contains("StoreID:", na=False))
    override['store id'] = override['store id'].fillna(method='ffill')
    override['store id'] = override['store id'].str.replace("StoreID: ", "", regex=False).str.strip()
    override = override.drop(columns=['store name'])  # Remove original column

    #for item# column
    condition_null = override['item #'].isnull()
    condition_in_list = override['item #'].isin(["ACT/QPAY DISCOUNT", "NC128TRIPLESIM"])
    override = override[~(condition_null | condition_in_list)]

    #for serial no. column
    override = override[override['serial no.'].isnull()]

    #for discount column
    override['discount'] = override['min price'] - override['price']
    override = override[override['discount'] >= 0]

    #**************************************************END***********************************************#

    #importing second data file
    disc_report = pd.read_excel(data2)
    disc_report.rename(columns={"Store ID": "Store_ID"}, inplace=True)

    #PREPROCESSING
    #for limit column
    if "limit" not in disc_report.columns:
        lst = ["NORTHWEST HWY", "704 JEFFERSON", "DUNCANVILLE", "COLORADO BLVD", "JACKSBORO"]
        disc_report["Store_Limit"] = np.where(
            disc_report["Store"].isin(lst),  # Condition: if 'Store' is in the list
            1500,                           # store limit 1500
            250                             # Else store limit 250
        )

    #for Override Disc
    override.rename(columns={"store id": "Store_ID"}, inplace=True)
    override_summed = override.groupby("Store_ID", as_index=False)["discount"].sum()
    disc_report = disc_report.merge(override_summed, how="left", left_on="Store_ID", right_on="Store_ID")
    disc_report.rename(columns={"discount": "Override_Disc"}, inplace=True)
    disc_report["Override_Disc"] = disc_report["Override_Disc"].fillna(0)

    #for Disc SKU
    salesbycategory = pd.read_excel(data3)
    salesbycategory.rename(columns={"custno": "Store_ID"}, inplace=True)
    salesbycategory_summed = salesbycategory.groupby("Store_ID", as_index=False)["price"].sum()
    disc_report = disc_report.merge(salesbycategory_summed, how="left", left_on="Store_ID", right_on="Store_ID")
    disc_report.rename(columns={"price": "Disc_SKU"}, inplace=True)
    disc_report["Disc_SKU"] = disc_report["Disc_SKU"].fillna(0)
    
    #for remaining columns
    required_columns = ['Market', 'Store', 'Store_ID', 'Store_Limit', 'Override_Disc',
                        'Disc_SKU', 'EOL', 'Aging', 'Cx_Survey', 'MD_approved', 'Comment']
    for column in required_columns:
        if column not in disc_report.columns:
            disc_report[column] = None

    return disc_report

# Function to update database with DataFrame
def update_or_insert_database(dataframe, connection, cursor):

    # Replace NaN with None for compatibility with MySQL
    columns_to_replace = ['EOL', 'Aging', 'Cx_Survey', 'MD_approved']
    dataframe[columns_to_replace] = dataframe[columns_to_replace].fillna(0)
    dataframe = dataframe.where(pd.notnull(dataframe), None)

    # Iterate through the rows of the dataframe
    for index, row in dataframe.iterrows():
        # Query to check if Store_ID exists
        check_query = "SELECT 1 FROM desc_report WHERE Store_ID = %s"
        cursor.execute(check_query, (row['Store_ID'],))
        result = cursor.fetchone()

        if result:  # If Store_ID exists, update the record
            update_query = """
                UPDATE desc_report
                SET 
                    Market = %s,
                    Store = %s,
                    Store_Limit = %s,
                    Override_Disc = %s,
                    Disc_SKU = %s,
                    EOL = %s,
                    Aging = %s,
                    Cx_Survey = %s,
                    MD_approved = %s,
                    Comment = %s
                WHERE Store_ID = %s
            """
            data_tuple = (
                row['Market'], row['Store'], row['Store_Limit'], row['Override_Disc'], row['Disc_SKU'], 
                row['EOL'], row['Aging'], row['Cx_Survey'], row['MD_approved'], row['Comment'], row['Store_ID']
            )
            cursor.execute(update_query, data_tuple)

        else:  # If Store_ID does not exist, insert the record
            insert_query = """
                INSERT INTO desc_report (
                    Market, Store, Store_ID, Store_Limit, Override_Disc, 
                    Disc_SKU, EOL, Aging, Cx_Survey, MD_approved, Comment
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            data_tuple = (
                row['Market'], row['Store'], row['Store_ID'], row['Store_Limit'], row['Override_Disc'], 
                row['Disc_SKU'], row['EOL'], row['Aging'], row['Cx_Survey'], row['MD_approved'], row['Comment']
            )
            cursor.execute(insert_query, data_tuple)
    
    # Commit the changes and close the connection
    connection.commit()

#*******************************************STREAMLIT APP**************************************************************#

st.title("Discount Report Page")
st.sidebar.title("Menu")

# Sidebar options
option = st.sidebar.radio("Choose an option:", ["Existing Discount Report", "Upload New Files"])

if option == "Existing Discount Report":
    file1 = st.sidebar.file_uploader("Upload Existing Discount Report", type=["xlsx", "xls"])

    if file1:
        final_df = pd.read_excel(file1)
        success_placeholder = st.empty()
        success_placeholder.success("Files uploaded successfully")
        time.sleep(1)
        success_placeholder.empty()
        st.dataframe(final_df,hide_index=True)

        if st.button("Update Database"):
            try:
                update_or_insert_database(final_df, mydb, mycursor)
                st.success("Database updated successfully.")
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please Upload Existing Discount Report")

if option == "Upload New Files":
    file1 = st.sidebar.file_uploader("Upload the Override Sales Report", type=["xlsx", "xls"])
    file2 = st.sidebar.file_uploader("Upload the Mapping File", type=["xlsx", "xls"])
    file3 = st.sidebar.file_uploader("Upload the Sales by Category Report", type=["xlsx", "xls"])

    if file3 and file1 and file2:
        success_placeholder = st.empty()
        success_placeholder.success("All three files uploaded successfully")
        time.sleep(1)
        success_placeholder.empty()
        final_df = new_data_preprocessing(file1,file2,file3)
        st.dataframe(final_df,hide_index=True)
        
        if st.button("Update Database"):
            try:
                update_or_insert_database(final_df, mydb, mycursor)
                st.success("Database updated successfully.")
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please Upload all three files")

