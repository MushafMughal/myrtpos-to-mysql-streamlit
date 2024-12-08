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
mydb = db()
mycursor = mydb.cursor()

# Write a query to fetch the data from the desc_report table
query = "SELECT * FROM desc_report"
mycursor.execute(query)
result = mycursor.fetchall()

# Get the column names
columns = [desc[0] for desc in mycursor.description]

df = pd.DataFrame(result, columns=columns)

# Display the DataFrame in the Streamlit app
st.title("Final Discount Report Data")

selected = option_menu(menu_title=None,options=["Data Record", "Data Updation"],orientation='horizontal',
                    styles={
                        "nav-link": {"--hover-color": "#a42bad4b"},
                        "nav-link-selected": {"background-color": "#832a80"}
                        },key="0")

if selected == "Data Record":
    
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

    # Display the filtered DataFrame
    st.dataframe(filtered_df,hide_index=True)

if selected == "Data Updation":
    option = st.sidebar.selectbox('Select an Operation',('Update', 'Create','Delete'))

    if option == 'Update':
        
        st.subheader('Update a Record')
        store_id = st.text_input('Enter Store ID to update')
        st.button("Enter")
        # Fetch the current record for the given Doctor ID
        select_sql = 'SELECT * FROM desc_report WHERE Store_ID = %s'
        select_val = (store_id,)
        mycursor.execute(select_sql, select_val)
        result = mycursor.fetchone()

        if result is None:
            st.warning('No record found with the provided Store ID')
        else:
            # Get the column names dynamically from the table
            desc_sql = 'DESCRIBE desc_report'
            mycursor.execute(desc_sql)
            columns = [column[0] for column in mycursor.fetchall()]

            current_data = list(result)

            updated_data = []
            for column in columns[1:]:
                updated_value = st.text_input(f'Enter updated {column}', value=current_data[columns.index(column)])
                updated_data.append(updated_value)

            if st.button("Update"):
                # Create the SQL update query dynamically
                update_sql = f"UPDATE desc_report SET {', '.join([f'{column} = %s' for column in columns[1:]])} WHERE Store_ID = %s"
                
                # Append the primary key (Store_ID) as the last parameter
                update_values = updated_data + [store_id]

                try:
                    # Execute the update query
                    mycursor.execute(update_sql, update_values)
                    mydb.commit()  # Commit changes to the database
                    st.success("Record updated successfully!")
                except Exception as e:
                    mydb.rollback()  # Rollback in case of an error
                    st.error(f"An error occurred while updating: {e}")

    elif option == 'Create':
        st.subheader('Create a Store Record')

        # Input fields for the new table
        market = st.text_input('Enter Market')
        store = st.text_input('Enter Store')
        store_id = st.text_input('Enter Store ID')  # Primary Key
        store_limit = st.number_input('Enter Store Limit', min_value=0, step=1)
        override_disc = st.number_input('Enter Override Discount', format="%.2f")
        disc_sku = st.number_input('Enter Discount SKU', format="%.2f")
        total_availed = st.number_input('Enter Total Availed', format="%.2f")
        remaining = st.number_input('Enter Remaining', format="%.2f")
        eol = st.number_input('Enter EOL', format="%.2f")
        aging = st.number_input('Enter Aging', format="%.2f")
        cx_survey = st.number_input('Enter CX Survey', format="%.2f")
        md_approved = st.number_input('Enter MD Approved', format="%.2f")
        comment = st.text_input('Enter Comment')

        if st.button("Create Record"):
            sql = '''
                INSERT INTO desc_report (
                    Market, Store, Store_ID, Store_Limit, Override_Disc, Disc_SKU, 
                    Total_Availed, Remaining, EOL, Aging, Cx_Survey, MD_approved, Comment
                ) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''
            val = (
                market, store, store_id, store_limit, override_disc, disc_sku, 
                total_availed, remaining, eol, aging, cx_survey, md_approved, comment
            )
            try:
                mycursor.execute(sql, val)
                mydb.commit()
                st.success('Record Created Successfully')
            except pymysql.IntegrityError as e:
                st.error('Error: Duplicate entry for primary key. Please provide a unique Store ID.')
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

    elif option == 'Delete':
        st.subheader("Delete a Record")
        store_id = st.text_input("Enter Store ID")
        if st.button("Delete"):
            try:
                sql = "DELETE FROM desc_report WHERE Store_ID = %s"
                val = (store_id,)
                mycursor.execute(sql, val)
                mydb.commit()
                if mycursor.rowcount > 0:
                    st.success("Record Deleted Successfully!")
                else:
                    st.warning("No record found with the provided Store ID")
            except pymysql.IntegrityError as e:
                error_code = e.args[0]
                st.error(f"IntegrityError: {error_code}")





