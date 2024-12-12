# MYRTPOS Data Sync and Reporting System 🌟

A streamlined application for syncing MYRTPOS data with MySQL and creating a customizable reporting interface using **Streamlit** for easy data visualization and management. This project provides real-time updates to the database and a SQL playground for advanced operations. 

## Features 🔧

### 1. **Data Sync Options** 

- **Create from Scratch**: Upload three input files (Override Sales Report, Mapping File, and Sales by Category Report) to generate and populate the database.
- **Use Existing Data**: Upload a pre-processed Discount Report to update or modify the database in real time.
![image](https://github.com/user-attachments/assets/aedc7716-a7f9-4230-ab86-449893e796ca)

### 2. **Real-Time Database Updates** 

- All changes made via the main application are reflected in the MySQL database instantly.
![image](https://github.com/user-attachments/assets/02782d3c-375d-40fa-b600-78967d3a6a0b)

### 3. **SQL Playground** 

- Execute bulk SQL operations or custom queries on the database.
- View query results or update the database directly.
![image](https://github.com/user-attachments/assets/c7096a82-0daa-4769-a913-62962211041f)
![image](https://github.com/user-attachments/assets/8eae8f4f-fa72-46dc-b6e4-c99f65f1b699)

### 4. **Customizable Reporting Interface** 

- Interactive filtering options for markets, store IDs, and stores.
- View filtered data with user-friendly visualization through Streamlit.

### 5. **Error Handling** 

- Comprehensive error messages for database operations and file uploads.

---

## Installation 📦

### Prerequisites 

1. **Python 3.8+**
2. **MySQL Server**
3. Required Python Libraries:
   ```bash
   pip install pandas numpy pymysql streamlit openpyxl
   ```

### Database Setup 

1. Create a MySQL database named `rtpos`.
2. Use the following table structure for the `desc_report` table:
   ```sql
   CREATE TABLE desc_report (
       Market VARCHAR(255),
       Store VARCHAR(255),
       Store_ID VARCHAR(255) PRIMARY KEY,
       Store_Limit INT,
       Override_Disc FLOAT,
       Disc_SKU FLOAT,
       EOL FLOAT,
       Aging FLOAT,
       Cx_Survey FLOAT,
       MD_approved FLOAT,
       Comment VARCHAR(255)
   );
   ```

---

## Usage 👨‍💻📊

### Step 1: Run the Application 

Start the Streamlit application:

```bash
streamlit run app.py
```

### Step 2: Upload Data 

#### Option 1: Existing Discount Report 

1. Upload a pre-processed Discount Report.
2. Review the data and click **Update Database** to sync changes.

#### Option 2: Generate from Scratch 

1. Upload the following three files:
   - **Override Sales Report**
   - **Mapping File**
   - **Sales by Category Report**
2. Review the generated report.
3. Click **Update Database** to populate the database.

### Step 3: Filter and View Reports 

1. Use the sidebar to filter by market, store ID, and store.
2. View filtered results in the main interface.

### Step 4: SQL Playground 

1. Open the **SQL Playground** tab.
2. Enter your SQL query in the text area.
3. Execute the query to view or modify the database.

---

## Examples 📚

### Input Files 

- **Override Sales Report**: Contains details about sales overrides.
- **Mapping File**: Maps store IDs to markets and stores.
- **Sales by Category Report**: Sales data categorized by store IDs.

### Generated Discount Report 

A combined report with the following calculated fields:

- **Override Discount**
- **Discount SKU**
- **Store Limit**

---

## Contribution 🤝👨‍💻

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a feature branch.
3. Submit a pull request. ✨

---

