import streamlit as st
import pandas as pd
import datetime
import json
from utils import load_data, filter_expenses

st.set_page_config(
    page_title="Export Data | Expense Tracker",
    page_icon="📤",
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
st.title("📤 Export Expense Data")
st.markdown("Export your expense data in various formats for backup or external analysis.")

# Sidebar for filters
st.sidebar.header("Filters")

# Date range filter
st.sidebar.subheader("Date Range")
today = datetime.date.today()
default_start_date = today - datetime.timedelta(days=365)  # Last year

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
    # Display preview of the data to be exported
    st.subheader("Data Preview")
    st.dataframe(filtered_expenses, use_container_width=True)
    
    # Export formats
    st.subheader("Export Options")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### CSV Format")
        st.markdown("Export your data as a CSV file that can be opened in Excel or Google Sheets.")
        st.download_button(
            label="Download CSV",
            data=filtered_expenses.to_csv(index=False).encode('utf-8'),
            file_name=f"expenses_{start_date}_to_{end_date}.csv",
            mime="text/csv"
        )
    
    with col2:
        st.markdown("### JSON Format")
        st.markdown("Export your data as a JSON file for use in other applications.")
        
        # Convert DataFrame to JSON
        json_data = filtered_expenses.to_json(orient='records', date_format='iso')
        
        st.download_button(
            label="Download JSON",
            data=json_data,
            file_name=f"expenses_{start_date}_to_{end_date}.json",
            mime="application/json"
        )
    
    with col3:
        st.markdown("### Excel Format")
        st.markdown("Export your data as an Excel file for more advanced analysis.")
        
        # We can't directly export to Excel, but we can suggest the CSV option
        st.info("For Excel format, please download the CSV file and open it in Excel.")
    
    # Data summary
    st.subheader("Data Summary")
    
    total_amount = filtered_expenses['amount'].sum()
    avg_amount = filtered_expenses['amount'].mean()
    num_records = len(filtered_expenses)
    date_range = f"{start_date} to {end_date}"
    
    summary_data = {
        "Total Amount": f"${total_amount:.2f}",
        "Average Expense": f"${avg_amount:.2f}",
        "Number of Records": num_records,
        "Date Range": date_range,
        "Categories Included": "All" if not selected_categories else ", ".join(selected_categories)
    }
    
    # Display summary as a table
    summary_df = pd.DataFrame(list(summary_data.items()), columns=["Metric", "Value"])
    st.table(summary_df)
