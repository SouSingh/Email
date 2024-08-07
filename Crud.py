import streamlit as st
import mysql.connector
from datetime import time
import pandas as pd
import requests
from PIL import Image, ImageDraw, ImageOps


def add_logo(logo_path, width, height, radius):
    """Read, resize, and return a logo with rounded edges."""
    logo = Image.open(logo_path)
    logo = logo.resize((width, height))
    
    # Create a mask for rounded corners
    mask = Image.new('L', (width, height), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), (width, height)], radius=radius, fill=255)

    # Apply the mask to the logo
    rounded_logo = ImageOps.fit(logo, (width, height), centering=(0.5, 0.5))
    rounded_logo.putalpha(mask)

    return rounded_logo

db = mysql.connector.connect(
    host="mariadb.cjw8mm0ymwaz.us-east-1.rds.amazonaws.com",
    user="easework",
    password="easework12345",
    database="easework"
)
st.set_page_config(
    page_title="Automation Admin",
    page_icon="🗃️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
with open("style.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
# Get a cursor

def call_fastapi_endpoints(base_url, time_string, days_before):
    print(time_string)
    try:
        response = requests.post(base_url, json={"time_string": time_string,"days_before": days_before })
        return response.json()
    except Exception as e:
        print("Error Response", e)

# st.sidebar.image(add_logo(logo_path="logo.png", width=190, height=60, radius=15))
st.sidebar.markdown("# Automation Admin Portal")
st.sidebar.subheader("Select Day & Interval Time")

days_before = st.sidebar.number_input("Choose # of days for delivery due to send document reminder", min_value=1, value=1, step=1)
# Get the user's time input
hour = st.sidebar.slider("Hour", 0, 23, 12)
minute = st.sidebar.slider("Minute", 0, 59, 0)
second = st.sidebar.slider("Second", 0, 59, 0)



# Create a time object from the user's input
user_time = time(hour, minute, second)
if st.sidebar.button("Save Configuration"):
    pas = user_time.strftime('%H:%M:%S')
    base_url = "http://34.118.169.177:8000/time/"
    response = call_fastapi_endpoints(base_url, pas,days_before)


cursor = db.cursor()

# Get a list of tables
cursor.execute("SHOW TABLES")
from itertools import chain

#tables = [table[0] for table in cursor.fetchall()]
#tables_name = [table[0] for table in cursor.fetchall()]
#Streamlit app
#st.sidebar.title("Select Table")
#selected_table = st.sidebar.selectbox("Table", [name.replace("_", " ").title() for name in tables_name])

tables = [table[0] for table in cursor.fetchall()]
table_names = [name.replace("_", " ").title() for name in tables]
temp = []
for gone in table_names:
    if gone == 'Documents Received Tobuyer Bysupplier':
        gone = "Documents Received from Supplier"
    if gone == 'Documents Received Tosupplier Bybuyer':
        gone = "Documents Received from Buyer"
    if gone == 'Incharge':
        gone = "Document Reviewer"
    if gone == "Requestor Supplier":
        gone = "PO Change Automation"
    temp.append(gone)
# Streamlit app
st.sidebar.title("Maintain Configuration")
selected_table = st.sidebar.selectbox("Table", temp)
if selected_table == "Documents Received from Supplier":
    selected_table = 'Documents Received Tobuyer Bysupplier'
if selected_table == "Documents Received from Buyer":
    selected_table ='Documents Received Tosupplier Bybuyer' 
if selected_table == "Document Reviewer":
    selected_table ='Incharge' 
if selected_table ==  "PO Change Automation":
    selected_table ="Requestor Supplier"
selected_table = selected_table.replace(" ", "_").lower()

# CRUD operations based on the selected table
if selected_table:
    gone  = ' '.join(word.capitalize() for word in selected_table.split('_'))
    if gone == 'Documents Received Tobuyer Bysupplier':
        gone = "Documents Received from Supplier"
    if gone == 'Documents Received Tosupplier Bybuyer':
        gone = "Documents Received from Buyer"
    if gone == 'Incharge':
        gone = "Document Reviewer"
    if gone == "Requestor Supplier":
        gone = "PO Change Automation"
    st.title(gone)
    

    # Read
    # st.subheader("Read Data")
    cursor.execute(f"SELECT * FROM {selected_table}")
    data = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]  # Get column names

# Dictionary to map column names
    column_mapping = {
    'BOL': "Bill of Ladding",
    'PFI': "Pro Forma Invoice",
    'Drawings': "Drawings and Design",
    'MQIC': "Material Quality Inspection Certificate",
    'LOC': "Letter of Credits"}

# Dictionary to map data values
    data_mapping = {1: "Received", 0: "Not Received"}

# Replace column names and data values
    columns = [column_mapping.get(col, col) for col in columns]
    data = [[data_mapping.get(val, val) for val in row] for row in data]

# Display the table
    #st.table(pd.DataFrame(data, columns=columns))
    df = pd.DataFrame(data, columns=columns)
    df.index = df.index + 1 
    #df.set_index('S.No', inplace=True)
    df.index.name = "S.No"
    st.table(df)

    # Create
    st.subheader("Create Data")
    cols = [desc[0] for desc in cursor.description]

    tempcols = cols.copy()
    # tempcols = ["Bill of Ladding","Pro Forma Invoice", "Drawings and Design",  "Material Quality Inspection Certificate"]
    new_data = {}
    for i,col in enumerate(cols):
        if col == 'BOL':
            tempcols[i] = "Bill of Ladding"
        if col == 'PFI':
            tempcols[i] = "Pro Forma Invoice"
        if col == 'Drawings':
            tempcols[i] = "Drawings and Design"
        if col == 'MQIC':
            tempcols[i] = "Material Quality Inspection Certificate"
        if col == 'LOC':
            tempcols[i] = "Letter of Credits"
        new_data[col] = st.text_input(f"{tempcols[i]}:", "")

    if st.button("Insert"):
        query = f"INSERT INTO {selected_table} ({', '.join(new_data.keys())}) VALUES ({', '.join(['%s'] * len(cols))})"
        values = tuple(new_data.values())
        cursor.execute(query, values)
        db.commit()
        st.success("Data inserted successfully!")

    # Update
    st.subheader("Update Data")
    cursor.execute(f"SELECT * FROM {selected_table}")
    data = cursor.fetchall()
    selected_row = st.selectbox("Select a row to update", data, format_func=lambda x: str(x))
    if selected_row:
        update_data = {}
        for i, col in enumerate(cols):
            # if col == 'BOL':
            #     tempcols[i] = "Bill of Ladding"
            # if col == 'PFI':
            #     tempcols[i] = "Pro Forma Invoice"
            # if col == 'Drawings':
            #     tempcols[i] = "Drawings and Design"
            # if col == 'MQIC':
            #     tempcols[i] = "Material Quality Inspection Certificate"
            # if col == 'LOC':
            #     tempcols[i] = "Letter of Credits"
            update_data[col] = st.text_input(f"{tempcols[i]}:", selected_row[i])
        if st.button("Update"):
            query = f"UPDATE {selected_table} SET {', '.join([f'{col} = %s' for col in update_data.keys()])}"
            values = tuple(update_data.values())
            where_clause = " AND ".join([f"{col} = %s" for col in cols])
            where_values = tuple([selected_row[i] for i in range(len(cols))])
            cursor.execute(query + " WHERE " + where_clause, values + where_values)
            db.commit()
            st.success("Data updated successfully!")

    # Delete
    st.subheader("Delete Data")
    cursor.execute(f"SELECT * FROM {selected_table}")
    data = cursor.fetchall()
    selected_row = st.selectbox("Select a row to delete", data, format_func=lambda x: str(x))
    if selected_row:
        if st.button("Delete"):
            where_clause = " AND ".join([f"{col} = %s" for col in cols])
            where_values = tuple([selected_row[i] for i in range(len(cols))])
            cursor.execute(f"DELETE FROM {selected_table} WHERE {where_clause}", where_values)
            db.commit()
            st.success("Data deleted successfully!")

# Close the database connection
db.close()
