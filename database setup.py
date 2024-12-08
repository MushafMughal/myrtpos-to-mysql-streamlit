import pymysql
import pandas as pd
import numpy as np

# ***********************************OVERRIDE REPORT**************************************************#
#importing data
override =   pd.read_excel("Override Sales Report.xlsx")
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

# ***********************************MAIN DISCOUNT REPORT**********************************************#
#importing data
disc_report = pd.read_excel("map.xlsx")
disc_report.rename(columns={"Store ID": "Store_ID"}, inplace=True)

#PREPROCESSING
#for limit column
if "limit" not in disc_report.columns:
    lst = ["NORTHWEST HWY", "704 JEFFERSON", "DUNCANVILLE", "COLORADO BLVD", "JACKSBORO"]
    disc_report["Store_Limit"] = np.where(
        disc_report["Store"].isin(lst),  # Condition: if 'Store' is in the list
        1500,                           # Value if condition is True
        250                             # Value if condition is False
    )
#for Override Disc column
override.rename(columns={"store id": "Store_ID"}, inplace=True)
override_summed = override.groupby("Store_ID", as_index=False)["discount"].sum()
disc_report = disc_report.merge(override_summed, how="left", left_on="Store_ID", right_on="Store_ID")
disc_report.rename(columns={"discount": "Override_Disc"}, inplace=True)
disc_report["Override_Disc"] = disc_report["Override_Disc"].fillna(0)

#for Disc SKU column
salesbycategory = pd.read_excel("SalesbyCategory.xls")
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

# *************************Insert the data first time into the database*******************************#

# Establish a connection to MySQL Server using pymysql
mydb = pymysql.connect(   
    host='localhost',
    user='root',
    password='34&*^&AsXti2098as3#$><?',
    database='rtpos'
)

mycursor = mydb.cursor()

for _, row in disc_report.iterrows():
    sql = """
    INSERT INTO desc_report (
        Market, Store, Store_ID, Store_Limit, Override_Disc, Disc_SKU, EOL, Aging, Cx_Survey, MD_approved, Comment) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = tuple(row[col] for col in required_columns)
    mycursor.execute(sql, values)

# Commit the transaction and close the connection
mydb.commit()
mycursor.close()
mydb.close()