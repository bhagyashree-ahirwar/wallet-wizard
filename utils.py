import pandas as pd
import os
import datetime
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# File path for the CSV data storage
DATA_FILE = "expenses.csv"

def load_data():
    """
    Load expense data from CSV file.
    Returns an empty DataFrame if the file doesn't exist.
    """
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        # Convert date column to datetime if it exists
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
        return df
    else:
        # Return an empty DataFrame with the correct columns
        return pd.DataFrame({
            'date': [],
            'amount': [],
            'category': [],
            'description': []
        })

def save_data(df):
    """
    Save the expense data to CSV file.
    """
    df.to_csv(DATA_FILE, index=False)

def filter_expenses(df, start_date=None, end_date=None, categories=None):
    """
    Filter expenses by date range and categories.
    """
    filtered_df = df.copy()
    
    # Filter by date if dates are provided
    if start_date and end_date:
        filtered_df = filtered_df[
            (pd.to_datetime(filtered_df['date']) >= pd.to_datetime(start_date)) & 
            (pd.to_datetime(filtered_df['date']) <= pd.to_datetime(end_date))
        ]
    
    # Filter by categories if provided
    if categories and len(categories) > 0:
        filtered_df = filtered_df[filtered_df['category'].isin(categories)]
    
    return filtered_df

def get_expense_summary(df):
    """
    Calculate summary statistics for expenses.
    """
    if df.empty:
        return {
            'total': 0,
            'average': 0,
            'max': 0,
            'min': 0,
            'count': 0
        }
    
    return {
        'total': df['amount'].sum(),
        'average': df['amount'].mean(),
        'max': df['amount'].max(),
        'min': df['amount'].min(),
        'count': len(df)
    }

def get_category_totals(df):
    """
    Calculate total expenses by category.
    """
    if df.empty:
        return pd.DataFrame({'category': [], 'total': []})
    
    category_totals = df.groupby('category')['amount'].sum().reset_index()
    category_totals = category_totals.rename(columns={'amount': 'total'})
    category_totals = category_totals.sort_values('total', ascending=False)
    
    return category_totals

def get_monthly_totals(df):
    """
    Calculate total expenses by month.
    """
    if df.empty:
        return pd.DataFrame({'month': [], 'total': []})
    
    # Convert date to datetime and extract month
    df_copy = df.copy()
    df_copy['month'] = pd.to_datetime(df_copy['date']).dt.strftime('%Y-%m')
    
    # Group by month and sum expenses
    monthly_totals = df_copy.groupby('month')['amount'].sum().reset_index()
    monthly_totals = monthly_totals.rename(columns={'amount': 'total'})
    monthly_totals = monthly_totals.sort_values('month')
    
    return monthly_totals

def create_category_pie_chart(df):
    """
    Create a pie chart showing expenses by category.
    """
    if df.empty:
        return None
    
    category_totals = get_category_totals(df)
    
    fig = px.pie(
        category_totals,
        values='total',
        names='category',
        title='Expenses by Category',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(showlegend=False)
    
    return fig

def create_monthly_bar_chart(df):
    """
    Create a bar chart showing expenses by month.
    """
    if df.empty:
        return None
    
    monthly_data = get_monthly_totals(df)
    
    fig = px.bar(
        monthly_data,
        x='month',
        y='total',
        title='Monthly Expense Trends',
        labels={'month': 'Month', 'total': 'Total Expense ($)'},
        color_discrete_sequence=['#4299E1']
    )
    
    fig.update_layout(xaxis_tickangle=-45)
    
    return fig

def create_category_comparison_chart(df):
    """
    Create a horizontal bar chart for category comparison.
    """
    if df.empty:
        return None
    
    category_data = get_category_totals(df)
    
    fig = px.bar(
        category_data,
        y='category',
        x='total',
        title='Expense Comparison by Category',
        labels={'category': 'Category', 'total': 'Total Expense ($)'},
        orientation='h',
        color='total',
        color_continuous_scale=['#48BB78', '#4299E1', '#F56565']
    )
    
    return fig
