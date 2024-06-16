import streamlit as st
import mysql.connector
from datetime import time
import pandas as pd
import requests


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
    base_url = "http://54.165.60.17:8000/time/"
    response = call_fastapi_endpoints(base_url, pas,days_before)


cursor = db.cursor()

# Get a list of tables
cursor.execute("SHOW TABLES")
tables = [table[0] for table in cursor.fetchall()]

# Streamlit app
st.sidebar.title("Select Table")
selected_table = st.sidebar.selectbox("Table", ' '.join(word.split('_').capitalize() for word in tables))

# CRUD operations based on the selected table
if selected_table:
    st.title(' '.join(word.capitalize() for word in selected_table.split('_')))

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
