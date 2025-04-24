import streamlit as st
import pandas as pd
import datetime
import os
from utils import load_data, save_data

st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables if they don't exist
if 'expenses' not in st.session_state:
    st.session_state.expenses = load_data()

# Define expense categories
CATEGORIES = [
    "Food & Dining", "Shopping", "Housing", "Transportation", 
    "Entertainment", "Health & Fitness", "Travel", "Education",
    "Personal Care", "Gifts & Donations", "Utilities", "Other"
]

# App title and description
st.title("💰 Expense Tracker")
st.markdown("""
Track your expenses, visualize your spending patterns, and take control of your finances.
Use the form below to add a new expense or navigate to the Dashboard to view your spending.
""")

# Create columns for better layout
col1, col2 = st.columns([1, 1])

with col1:
    st.header("Add New Expense")
    
    # Expense entry form
    with st.form("expense_form", clear_on_submit=True):
        expense_date = st.date_input(
            "Date",
            value=datetime.date.today(),
            max_value=datetime.date.today()
        )
        
        expense_amount = st.number_input(
            "Amount",
            min_value=0.01,
            format="%.2f",
            step=1.0
        )
        
        expense_category = st.selectbox(
            "Category",
            options=CATEGORIES
        )
        
        expense_description = st.text_input(
            "Description (Optional)"
        )
        
        submitted = st.form_submit_button("Add Expense")
        
        if submitted:
            # Create a new expense entry
            new_expense = {
                "date": expense_date.strftime("%Y-%m-%d"),
                "amount": round(expense_amount, 2),
                "category": expense_category,
                "description": expense_description
            }
            
            # Add to our data
            st.session_state.expenses = pd.concat([
                st.session_state.expenses, 
                pd.DataFrame([new_expense])
            ], ignore_index=True)
            
            # Save the updated data
            save_data(st.session_state.expenses)
            
            st.success("Expense added successfully!")

with col2:
    st.header("Recent Expenses")
    
    if st.session_state.expenses.empty:
        st.info("No expenses recorded yet. Add your first expense using the form!")
    else:
        # Show the 5 most recent expenses
        recent_expenses = st.session_state.expenses.sort_values(
            by='date', 
            ascending=False
        ).head(5)
        
        for _, expense in recent_expenses.iterrows():
            with st.container():
                cols = st.columns([2, 3, 3, 2])
                cols[0].markdown(f"**{expense['date']}**")
                cols[1].markdown(f"${expense['amount']:.2f}")
                cols[2].markdown(f"{expense['category']}")
                cols[3].markdown(f"{expense['description']}")
                st.divider()

# Footer
st.markdown("---")
st.markdown(
    "Navigate to the Dashboard and Data Analysis pages to view detailed insights about your spending."
)
