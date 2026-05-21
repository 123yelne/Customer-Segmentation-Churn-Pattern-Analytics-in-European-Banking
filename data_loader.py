"""
Data Loader Module for European Banking Churn Analysis
Handles data loading, cleaning, and feature engineering
"""

import pandas as pd
import numpy as np

def load_data(file_path='European_Bank.csv'):
    """
    Load the European Banking dataset
    
    Parameters:
    file_path (str): Path to the CSV file
    
    Returns:
    pandas.DataFrame: Loaded and processed dataframe
    """
    try:
        df = pd.read_csv(file_path)
        print(f"✅ Data loaded successfully: {len(df)} rows, {len(df.columns)} columns")
        return df
    except FileNotFoundError:
        print(f"❌ Error: File '{file_path}' not found!")
        print("Please make sure the CSV file is in the same directory")
        return None
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return None

def create_segments(df):
    """
    Create segmentation columns for analysis
    
    Parameters:
    df (pandas.DataFrame): Raw dataframe
    
    Returns:
    pandas.DataFrame: Dataframe with additional segment columns
    """
    # Make a copy to avoid modifying original
    df_segmented = df.copy()
    
    # 1. Age Groups
    df_segmented['age_group'] = pd.cut(
        df_segmented['Age'], 
        bins=[0, 30, 45, 60, 100], 
        labels=['<30', '30-45', '46-60', '60+']
    )
    
    # 2. Credit Score Bands
    df_segmented['credit_band'] = pd.cut(
        df_segmented['CreditScore'],
        bins=[0, 580, 670, 740, 850],
        labels=['Poor', 'Fair', 'Good', 'Excellent']
    )
    
    # 3. Balance Segments
    def balance_category(balance):
        if balance == 0:
            return 'Zero Balance'
        elif balance < 50000:
            return 'Low Balance'
        elif balance < 100000:
            return 'Medium Balance'
        else:
            return 'High Balance'
    
    df_segmented['balance_segment'] = df_segmented['Balance'].apply(balance_category)
    
    # 4. Tenure Groups
    df_segmented['tenure_group'] = pd.cut(
        df_segmented['Tenure'],
        bins=[0, 2, 5, 11],
        labels=['New (<2yrs)', 'Mid (2-5yrs)', 'Long (5+yrs)']
    )
    
    # 5. Salary Segments
    def salary_category(salary):
        if salary < 50000:
            return 'Low Salary'
        elif salary < 100000:
            return 'Medium Salary'
        else:
            return 'High Salary'
    
    df_segmented['salary_segment'] = df_segmented['EstimatedSalary'].apply(salary_category)
    
    # 6. Product Usage Category
    def product_category(products):
        if products == 1:
            return 'Basic'
        elif products == 2:
            return 'Standard'
        elif products == 3:
            return 'Premium'
        else:
            return 'Ultra'
    
    df_segmented['product_category'] = df_segmented['NumOfProducts'].apply(product_category)
    
    # 7. Age x Tenure Interaction
    df_segmented['age_tenure_interaction'] = df_segmented['Age'] * df_segmented['Tenure']
    
    # 8. Balance to Salary Ratio
    df_segmented['balance_salary_ratio'] = df_segmented['Balance'] / (df_segmented['EstimatedSalary'] + 1)
    
    # 9. Customer Value Score (simple composite)
    # Normalize and combine Balance, CreditScore, Salary
    df_segmented['customer_value_score'] = (
        (df_segmented['Balance'] / (df_segmented['Balance'].max() + 1)) * 0.4 +
        (df_segmented['CreditScore'] / 850) * 0.3 +
        (df_segmented['EstimatedSalary'] / (df_segmented['EstimatedSalary'].max() + 1)) * 0.3
    )
    
    return df_segmented

def get_data_summary(df):
    """
    Get basic summary statistics of the dataset
    
    Parameters:
    df (pandas.DataFrame): Dataframe
    
    Returns:
    dict: Summary statistics
    """
    if df is None or len(df) == 0:
        return {}
    
    summary = {
        'total_customers': len(df),
        'total_features': len(df.columns),
        'churned_customers': df['Exited'].sum(),
        'churn_rate': (df['Exited'].sum() / len(df)) * 100,
        'avg_age': round(df['Age'].mean(), 1),
        'avg_credit_score': round(df['CreditScore'].mean(), 0),
        'avg_balance': round(df['Balance'].mean(), 0),
        'avg_salary': round(df['EstimatedSalary'].mean(), 0),
        'avg_tenure': round(df['Tenure'].mean(), 1),
        'avg_products': round(df['NumOfProducts'].mean(), 1),
        'active_members': df['IsActiveMember'].sum(),
        'credit_card_holders': df['HasCrCard'].sum(),
        'geographies': df['Geography'].nunique(),
        'gender_distribution': df['Gender'].value_counts().to_dict()
    }
    
    return summary

def get_column_descriptions():
    """
    Get descriptions of all columns in the dataset
    
    Returns:
    dict: Column descriptions
    """
    descriptions = {
        'Year': 'Year of the data record',
        'CustomerId': 'Unique identifier for each customer',
        'Surname': 'Customer last name',
        'CreditScore': 'Customer credit score (0-850)',
        'Geography': 'Country where customer is located (France, Spain, Germany)',
        'Gender': 'Customer gender (Male/Female)',
        'Age': 'Customer age in years',
        'Tenure': 'Number of years the customer has been with the bank',
        'Balance': 'Account balance amount',
        'NumOfProducts': 'Number of bank products the customer uses',
        'HasCrCard': 'Whether customer has a credit card (1=Yes, 0=No)',
        'IsActiveMember': 'Whether customer is an active member (1=Yes, 0=No)',
        'EstimatedSalary': 'Customer estimated annual salary',
        'Exited': 'Whether customer churned (1=Yes, 0=No) - TARGET VARIABLE'
    }
    
    return descriptions

if __name__ == "__main__":
    # Test the module
    print("Testing data_loader.py...")
    df = load_data()
    if df is not None:
        df_seg = create_segments(df)
        print(f"\n✅ Segmentation complete: {df_seg.shape}")
        print(f"\nSegment columns added: {[col for col in df_seg.columns if col not in df.columns]}")
        summary = get_data_summary(df)
        print(f"\n📊 Summary: {summary}")