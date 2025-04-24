import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
from utils import (
    load_data, filter_expenses, create_category_pie_chart,
    create_monthly_bar_chart, create_category_comparison_chart,
    get_monthly_totals
)

st.set_page_config(
    page_title="Data Analysis | Expense Tracker",
    page_icon="📈",
    layout="wide"
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

# Dashboard title
st.title("📈 Expense Analysis")
st.markdown("Visualize your spending patterns with interactive charts and graphs.")

# Sidebar for filters
st.sidebar.header("Filters")

# Date range filter
st.sidebar.subheader("Date Range")
today = datetime.date.today()
default_start_date = today.replace(day=1, month=1)  # First day of current year

start_date = st.sidebar.date_input(
    "Start Date",
    value=default_start_date,
    max_value=today
)

end_date = st.sidebar.date_input(
    "End Date",
    value=today,
    max_value=today,
    min_value=start_date
)

# Category filter
st.sidebar.subheader("Categories")
selected_categories = st.sidebar.multiselect(
    "Select Categories",
    options=CATEGORIES,
    default=[]
)

# Apply filters
filtered_expenses = filter_expenses(
    st.session_state.expenses,
    start_date,
    end_date,
    selected_categories
)

# Check if we have data
if filtered_expenses.empty:
    st.warning("No expense data available for the selected filters. Please adjust your filter criteria or add some expenses.")
else:
    # Create two columns for charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Expense Distribution by Category")
        category_pie = create_category_pie_chart(filtered_expenses)
        if category_pie:
            st.plotly_chart(category_pie, use_container_width=True)
        else:
            st.info("Not enough data to create category distribution chart.")
    
    with col2:
        st.subheader("Monthly Expense Trends")
        monthly_bar = create_monthly_bar_chart(filtered_expenses)
        if monthly_bar:
            st.plotly_chart(monthly_bar, use_container_width=True)
        else:
            st.info("Not enough data to create monthly trends chart.")
    
    # Full width for the category comparison
    st.subheader("Category Comparison")
    category_comparison = create_category_comparison_chart(filtered_expenses)
    if category_comparison:
        st.plotly_chart(category_comparison, use_container_width=True)
    else:
        st.info("Not enough data to create category comparison chart.")
    
    # Monthly Data Table
    st.subheader("Monthly Expense Summary")
    monthly_data = get_monthly_totals(filtered_expenses)
    
    if not monthly_data.empty:
        # Format the data for display
        monthly_data['total'] = monthly_data['total'].apply(lambda x: f"${x:.2f}")
        
        # Display the monthly summary
        st.dataframe(
            monthly_data,
            use_container_width=True,
            column_config={
                "month": "Month",
                "total": "Total Expenses"
            }
        )
    else:
        st.info("No monthly data available for the selected period.")
