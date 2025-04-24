import streamlit as st
import pandas as pd
import datetime
from utils import load_data, filter_expenses, get_expense_summary, get_category_totals

st.set_page_config(
    page_title="Dashboard | Expense Tracker",
    page_icon="📊",
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
st.title("📊 Expense Dashboard")
st.markdown("View and manage your expenses with filters for date range and categories.")

# Sidebar for filters
st.sidebar.header("Filters")

# Date range filter
st.sidebar.subheader("Date Range")
today = datetime.date.today()
default_start_date = today - datetime.timedelta(days=30)

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

# Calculate summary statistics
expense_summary = get_expense_summary(filtered_expenses)

# Display summary statistics
st.header("Expense Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Expenses",
        f"${expense_summary['total']:.2f}"
    )

with col2:
    st.metric(
        "Average Expense",
        f"${expense_summary['average']:.2f}"
    )

with col3:
    st.metric(
        "Maximum Expense",
        f"${expense_summary['max']:.2f}" if expense_summary['count'] > 0 else "$0.00"
    )

with col4:
    st.metric(
        "Number of Expenses",
        expense_summary['count']
    )

# Display expense data table
st.header("Expense Records")

if filtered_expenses.empty:
    st.info("No expenses found with the current filters. Try adjusting your filter criteria.")
else:
    # Add functionality to delete expenses
    # Display the expense records
    display_df = filtered_expenses.sort_values(by='date', ascending=False).copy()
    
    # Format columns for display
    display_df['amount'] = display_df['amount'].apply(lambda x: f"${x:.2f}")
    
    # Display the data with formatted columns
    st.dataframe(
        display_df[['date', 'amount', 'category', 'description']],
        use_container_width=True,
        column_config={
            "date": "Date",
            "amount": "Amount",
            "category": "Category",
            "description": "Description"
        }
    )
    
    # Export functionality
    st.download_button(
        label="Download Filtered Data",
        data=filtered_expenses.to_csv(index=False).encode('utf-8'),
        file_name=f"expenses_{start_date}_to_{end_date}.csv",
        mime="text/csv"
    )

# Category breakdown
st.header("Category Breakdown")

if filtered_expenses.empty:
    st.info("No expense data available to show category breakdown.")
else:
    category_totals = get_category_totals(filtered_expenses)
    
    # Display category breakdown
    st.bar_chart(
        category_totals.set_index('category')
    )
