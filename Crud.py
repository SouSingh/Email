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
    host="sql12.freesqldatabase.com",
    user="sql12714086",
    password="fAbSxAerrP",
    database="sql12714086",
    port=3306
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
    response = requests.post(base_url, json={"time_string": time_string,"days_before": days_before })
    return response.json()

st.sidebar.image(add_logo(logo_path="logo.png", width=190, height=60, radius=15))
st.sidebar.markdown("# Automation Admin Portal")
st.sidebar.subheader("Select Time")

# Get the user's time input
hour = st.sidebar.slider("Hour", 0, 23, 12)
minute = st.sidebar.slider("Minute", 0, 59, 0)
second = st.sidebar.slider("Second", 0, 59, 0)

days_before = st.sidebar.number_input("Enter the number of Days Before the Reminder")


# Create a time object from the user's input
user_time = time(hour, minute, second)
if st.sidebar.button("Send Alert"):
    pas = user_time.strftime('%H:%M:%S')
    base_url = "http://54.173.90.210:8000/time/"
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

# Streamlit app
st.sidebar.title("Maintain Configuration")
selected_table = st.sidebar.selectbox("Table", tables)

# CRUD operations based on the selected table
if selected_table:
    gone  = ' '.join(word.capitalize() for word in selected_table.split('_'))
    if gone == 'Documents Received Tobuyer Bysupplier':
        gone = "Documents Received from Supplier"
    if gone == 'Documents Received Tosupplier Bybuyer':
        gone = "Documents Received from Buyer"
    if gone == 'Incharge':
        gone = "Document Reviewer"
    st.title(gone)
    

    # Read
    st.subheader("Read Data")
    cursor.execute(f"SELECT * FROM {selected_table}")
    data = cursor.fetchall()
    cols = [desc[0] for desc in cursor.description]  # Get column names
    if data:
        for i, col in enumerate(cols):
            if col == 'BOL':
                cols[i] = "Bill of Ladding"
            if col == 'PFI':
                cols[i] = "Pro Forma Invoice"
            if col == 'Drawings':
                cols[i] = "Drawings and Design"
            if col == 'MQIC':
                cols[i] = "Material Quality Inspection Certificate"
            if col == 'LOC':
                cols[i] = "Letter of Credits"
        st.table(pd.DataFrame(data, columns=cols))
    else:
        st.write("No data found.")

    # Create
    st.subheader("Create Data")
    cols = [desc[0] for desc in cursor.description]
    new_data = {}
    for col in cols:
        if col == 'BOL':
            col = "Bill of Ladding"
        if col == 'PFI':
            col = "Pro Forma Invoice"
        if col == 'Drawings':
            col = "Drawings and Design"
        if col == 'MQIC':
            col = "Material Quality Inspection Certificate"
        if col == 'LOC':
            col = "Letter of Credits"
        new_data[col] = st.text_input(f"{col}:", "")
    if st.button("Insert"):
        query = f"INSERT INTO {selected_table} ({', '.join(cols)}) VALUES ({', '.join(['%s'] * len(cols))})"
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
            update_data[col] = st.text_input(f"{col}:", selected_row[i])
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
