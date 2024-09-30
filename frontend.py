from backend import ItemModel, Items, Item
import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:5000/api/items"

st.title("👛 Expense Tracker 👛")

col1, col2, col3, col4 = st.columns(4)

# Add input fields to each column
with col1:
    option1 = st.selectbox("Type", ["Income", "Expense"])
with col2:
    if option1 == "Expense":
        option2 = st.selectbox("Title", ["Breakfast", "Lunch", "Dinner", "Dessert", "Snack", "Late-night Snack"])
    else:
        option2 = st.text_input("From where", "")
with col3:
    if option1 == "Expense":
        input3 = st.text_input("Cost", "")
    else:
        input3 = st.text_input("Amount", "")
with col4:
    input4 = st.text_input("Description", "")

# A function to check if input is valid
def is_valid_input(cost):
    try:
        int(cost)
        return True
    except ValueError:
        return False

# Function to apply conditional formatting
def highlight_cost_type(row):
    if row["type"] == "Expense":
        return ["background-color: #7FFFD4" if row["type"] == "Expense" else "" for _ in row]
    elif row["type"] == "Income":
        return ["background-color: #FFC0CB" if row["type"] == "Income" else '' for _ in row]
    return ["" for _ in row]

if st.button("Submit"):
    if not is_valid_input(input3):
        st.error("Please enter a valid integer value for cost.")
    else:
        item_data = {
            "type": option1,
            "title": option2,
            "cost": int(input3),
            "description": input4
        }

        response = requests.post(API_URL, json=item_data)

        if response.status_code == 201:
            st.success("Item added successfully!")
            items = response.json()
            df = pd.DataFrame(items)

            styled_df = df.style.apply(highlight_cost_type, axis=1)

            st.dataframe(styled_df)

        else:
            st.error(f"Error: {response.status_code}")

if st.button("Fetch Items"):
    response = requests.get(API_URL)
    if response.status_code == 200:
        items = response.json()
        df = pd.DataFrame(items)

        styled_df = df.style.apply(highlight_cost_type, axis=1)

        st.dataframe(styled_df)
    else:
        st.error(f"Error: {response.status_code}")
