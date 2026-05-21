"""
Analysis Module for European Banking Churn
Contains all KPI calculations and analytical functions
"""

import pandas as pd
import numpy as np

def calculate_kpis(df, filtered_df=None):
    """
    Calculate all Key Performance Indicators
    
    Parameters:
    df (pandas.DataFrame): Full dataframe
    filtered_df (pandas.DataFrame): Filtered dataframe (optional)
    
    Returns:
    dict: Dictionary of KPIs
    """
    if filtered_df is None:
        filtered_df = df
    
    total = len(filtered_df)
    churned = filtered_df['Exited'].sum() if 'Exited' in filtered_df.columns else 0
    churn_rate = (churned / total) * 100 if total > 0 else 0
    
    # High-value customers (top 25% by balance)
    high_balance_threshold = df['Balance'].quantile(0.75) if len(df) > 0 else 0
    high_value_df = filtered_df[filtered_df['Balance'] > high_balance_threshold]
    high_value_churn_rate = (high_value_df['Exited'].sum() / len(high_value_df)) * 100 if len(high_value_df) > 0 else 0
    
    # Active vs Inactive
    active_customers = filtered_df[filtered_df['IsActiveMember'] == 1]
    inactive_customers = filtered_df[filtered_df['IsActiveMember'] == 0]
    active_churn_rate = (active_customers['Exited'].sum() / len(active_customers)) * 100 if len(active_customers) > 0 else 0
    inactive_churn_rate = (inactive_customers['Exited'].sum() / len(inactive_customers)) * 100 if len(inactive_customers) > 0 else 0
    
    kpis = {
        'total_customers': total,
        'churned_customers': churned,
        'retained_customers': total - churned,
        'churn_rate': round(churn_rate, 2),
        'retention_rate': round(100 - churn_rate, 2),
        
        'avg_age': round(filtered_df['Age'].mean(), 1) if total > 0 else 0,
        'avg_credit_score': round(filtered_df['CreditScore'].mean(), 0) if total > 0 else 0,
        'avg_balance': round(filtered_df['Balance'].mean(), 0) if total > 0 else 0,
        'avg_salary': round(filtered_df['EstimatedSalary'].mean(), 0) if total > 0 else 0,
        'avg_tenure': round(filtered_df['Tenure'].mean(), 1) if total > 0 else 0,
        'avg_products': round(filtered_df['NumOfProducts'].mean(), 1) if total > 0 else 0,
        
        'active_members': filtered_df['IsActiveMember'].sum(),
        'inactive_members': total - filtered_df['IsActiveMember'].sum(),
        'active_churn_rate': round(active_churn_rate, 2),
        'inactive_churn_rate': round(inactive_churn_rate, 2),
        
        'credit_card_holders': filtered_df['HasCrCard'].sum(),
        'non_credit_card_holders': total - filtered_df['HasCrCard'].sum(),
        
        'high_value_customers': len(high_value_df),
        'high_value_churn_rate': round(high_value_churn_rate, 2),
        
        'zero_balance_customers': len(filtered_df[filtered_df['Balance'] == 0]),
        'zero_balance_churn_rate': round((filtered_df[filtered_df['Balance'] == 0]['Exited'].sum() / max(1, len(filtered_df[filtered_df['Balance'] == 0]))) * 100, 2)
    }
    
    return kpis

def get_geography_churn(df):
    """
    Calculate churn metrics by geography
    
    Parameters:
    df (pandas.DataFrame): Dataframe
    
    Returns:
    pandas.DataFrame: Churn analysis by geography
    """
    geo_churn = df.groupby('Geography').agg({
        'Exited': ['sum', 'count', 'mean']
    }).round(4)
    geo_churn.columns = ['Churned', 'Total', 'Churn_Rate']
    geo_churn['Churn_Rate_Pct'] = geo_churn['Churn_Rate'] * 100
    geo_churn = geo_churn.sort_values('Churn_Rate_Pct', ascending=False)
    return geo_churn

def get_age_churn(df):
    """
    Calculate churn metrics by age group
    
    Parameters:
    df (pandas.DataFrame): Dataframe with age_group column
    
    Returns:
    pandas.DataFrame: Churn analysis by age group
    """
    if 'age_group' not in df.columns:
        return pd.DataFrame()
    
    age_churn = df.groupby('age_group').agg({
        'Exited': ['sum', 'count', 'mean']
    }).round(4)
    age_churn.columns = ['Churned', 'Total', 'Churn_Rate']
    age_churn['Churn_Rate_Pct'] = age_churn['Churn_Rate'] * 100
    return age_churn

def get_gender_churn(df):
    """
    Calculate churn metrics by gender
    
    Parameters:
    df (pandas.DataFrame): Dataframe
    
    Returns:
    pandas.DataFrame: Churn analysis by gender
    """
    gender_churn = df.groupby('Gender').agg({
        'Exited': ['sum', 'count', 'mean']
    }).round(4)
    gender_churn.columns = ['Churned', 'Total', 'Churn_Rate']
    gender_churn['Churn_Rate_Pct'] = gender_churn['Churn_Rate'] * 100
    return gender_churn

def get_credit_band_churn(df):
    """
    Calculate churn metrics by credit score band
    
    Parameters:
    df (pandas.DataFrame): Dataframe with credit_band column
    
    Returns:
    pandas.DataFrame: Churn analysis by credit band
    """
    if 'credit_band' not in df.columns:
        return pd.DataFrame()
    
    credit_churn = df.groupby('credit_band').agg({
        'Exited': ['sum', 'count', 'mean']
    }).round(4)
    credit_churn.columns = ['Churned', 'Total', 'Churn_Rate']
    credit_churn['Churn_Rate_Pct'] = credit_churn['Churn_Rate'] * 100
    return credit_churn

def get_tenure_churn(df):
    """
    Calculate churn metrics by tenure group
    
    Parameters:
    df (pandas.DataFrame): Dataframe with tenure_group column
    
    Returns:
    pandas.DataFrame: Churn analysis by tenure
    """
    if 'tenure_group' not in df.columns:
        return pd.DataFrame()
    
    tenure_churn = df.groupby('tenure_group').agg({
        'Exited': ['sum', 'count', 'mean']
    }).round(4)
    tenure_churn.columns = ['Churned', 'Total', 'Churn_Rate']
    tenure_churn['Churn_Rate_Pct'] = tenure_churn['Churn_Rate'] * 100
    return tenure_churn

def get_balance_churn(df):
    """
    Calculate churn metrics by balance segment
    
    Parameters:
    df (pandas.DataFrame): Dataframe with balance_segment column
    
    Returns:
    pandas.DataFrame: Churn analysis by balance segment
    """
    if 'balance_segment' not in df.columns:
        return pd.DataFrame()
    
    balance_churn = df.groupby('balance_segment').agg({
        'Exited': ['sum', 'count', 'mean']
    }).round(4)
    balance_churn.columns = ['Churned', 'Total', 'Churn_Rate']
    balance_churn['Churn_Rate_Pct'] = balance_churn['Churn_Rate'] * 100
    return balance_churn

def get_product_churn(df):
    """
    Calculate churn metrics by number of products
    
    Parameters:
    df (pandas.DataFrame): Dataframe
    
    Returns:
    pandas.DataFrame: Churn analysis by products
    """
    product_churn = df.groupby('NumOfProducts').agg({
        'Exited': ['sum', 'count', 'mean']
    }).round(4)
    product_churn.columns = ['Churned', 'Total', 'Churn_Rate']
    product_churn['Churn_Rate_Pct'] = product_churn['Churn_Rate'] * 100
    return product_churn

def get_high_value_analysis(df):
    """
    Analyze high-value customer churn
    
    Parameters:
    df (pandas.DataFrame): Dataframe
    
    Returns:
    dict: High-value analysis metrics
    """
    # Top 25% by Balance
    high_balance_threshold = df['Balance'].quantile(0.75)
    high_balance_customers = df[df['Balance'] > high_balance_threshold]
    
    # Top 25% by Credit Score
    high_credit_threshold = df['CreditScore'].quantile(0.75)
    high_credit_customers = df[df['CreditScore'] > high_credit_threshold]
    
    # Top 25% by Salary
    high_salary_threshold = df['EstimatedSalary'].quantile(0.75)
    high_salary_customers = df[df['EstimatedSalary'] > high_salary_threshold]
    
    # Top 25% by Customer Value Score
    if 'customer_value_score' in df.columns:
        high_value_threshold = df['customer_value_score'].quantile(0.75)
        high_value_customers = df[df['customer_value_score'] > high_value_threshold]
        high_value_churn_rate = (high_value_customers['Exited'].sum() / len(high_value_customers)) * 100 if len(high_value_customers) > 0 else 0
    else:
        high_value_customers = pd.DataFrame()
        high_value_churn_rate = 0
    
    results = {
        'high_balance_customers': len(high_balance_customers),
        'high_balance_churn_rate': round((high_balance_customers['Exited'].sum() / max(1, len(high_balance_customers))) * 100, 2),
        'high_credit_customers': len(high_credit_customers),
        'high_credit_churn_rate': round((high_credit_customers['Exited'].sum() / max(1, len(high_credit_customers))) * 100, 2),
        'high_salary_customers': len(high_salary_customers),
        'high_salary_churn_rate': round((high_salary_customers['Exited'].sum() / max(1, len(high_salary_customers))) * 100, 2),
        'high_value_customers': len(high_value_customers),
        'high_value_churn_rate': round(high_value_churn_rate, 2)
    }
    
    return results

def get_correlation_analysis(df):
    """
    Get correlation between numerical features and churn
    
    Parameters:
    df (pandas.DataFrame): Dataframe
    
    Returns:
    pandas.DataFrame: Correlation with churn
    """
    numerical_cols = ['CreditScore', 'Age', 'Tenure', 'Balance', 'NumOfProducts', 'EstimatedSalary']
    correlations = {}
    
    for col in numerical_cols:
        if col in df.columns:
            correlations[col] = df[col].corr(df['Exited'])
    
    corr_df = pd.DataFrame(list(correlations.items()), columns=['Feature', 'Correlation_with_Churn'])
    corr_df['Absolute_Correlation'] = abs(corr_df['Correlation_with_Churn'])
    corr_df = corr_df.sort_values('Absolute_Correlation', ascending=False)
    
    return corr_df

def get_risk_segments(df):
    """
    Identify high-risk customer segments
    
    Parameters:
    df (pandas.DataFrame): Dataframe with segment columns
    
    Returns:
    pandas.DataFrame: Risk analysis by segment
    """
    risk_data = []
    
    # Age segments
    if 'age_group' in df.columns:
        age_churn = get_age_churn(df)
        for idx in age_churn.index:
            risk_data.append({
                'Segment_Type': 'Age Group',
                'Segment': idx,
                'Customers': age_churn.loc[idx, 'Total'],
                'Churn_Rate': age_churn.loc[idx, 'Churn_Rate_Pct']
            })
    
    # Geography segments
    geo_churn = get_geography_churn(df)
    for idx in geo_churn.index:
        risk_data.append({
            'Segment_Type': 'Geography',
            'Segment': idx,
            'Customers': geo_churn.loc[idx, 'Total'],
            'Churn_Rate': geo_churn.loc[idx, 'Churn_Rate_Pct']
        })
    
    # Credit segments
    if 'credit_band' in df.columns:
        credit_churn = get_credit_band_churn(df)
        for idx in credit_churn.index:
            risk_data.append({
                'Segment_Type': 'Credit Score',
                'Segment': idx,
                'Customers': credit_churn.loc[idx, 'Total'],
                'Churn_Rate': credit_churn.loc[idx, 'Churn_Rate_Pct']
            })
    
    risk_df = pd.DataFrame(risk_data)
    risk_df = risk_df.sort_values('Churn_Rate', ascending=False)
    
    return risk_df

def get_engagement_score(df):
    """
    Calculate engagement score for customers
    
    Parameters:
    df (pandas.DataFrame): Dataframe
    
    Returns:
    pandas.DataFrame: Customers with engagement scores
    """
    df_copy = df.copy()
    
    # Engagement score based on multiple factors (0-100)
    df_copy['engagement_score'] = (
        df_copy['IsActiveMember'] * 40 +
        df_copy['HasCrCard'] * 20 +
        (df_copy['NumOfProducts'] / 4) * 20 +
        (df_copy['Tenure'] / 10) * 20
    )
    
    df_copy['engagement_score'] = df_copy['engagement_score'].clip(0, 100)
    
    # Engagement level
    def engagement_level(score):
        if score < 30:
            return 'Low Engagement'
        elif score < 60:
            return 'Medium Engagement'
        else:
            return 'High Engagement'
    
    df_copy['engagement_level'] = df_copy['engagement_score'].apply(engagement_level)
    
    return df_copy

def get_engagement_churn_analysis(df):
    """
    Analyze churn by engagement level
    
    Parameters:
    df (pandas.DataFrame): Dataframe
    
    Returns:
    pandas.DataFrame: Engagement vs churn analysis
    """
    df_engaged = get_engagement_score(df)
    
    engagement_churn = df_engaged.groupby('engagement_level').agg({
        'Exited': ['sum', 'count', 'mean']
    }).round(4)
    engagement_churn.columns = ['Churned', 'Total', 'Churn_Rate']
    engagement_churn['Churn_Rate_Pct'] = engagement_churn['Churn_Rate'] * 100
    
    return engagement_churn

if __name__ == "__main__":
    print("Analysis module loaded successfully")
    print("Available functions:")
    print("  - calculate_kpis()")
    print("  - get_geography_churn()")
    print("  - get_age_churn()")
    print("  - get_gender_churn()")
    print("  - get_credit_band_churn()")
    print("  - get_tenure_churn()")
    print("  - get_balance_churn()")
    print("  - get_product_churn()")
    print("  - get_high_value_analysis()")
    print("  - get_correlation_analysis()")
    print("  - get_risk_segments()")
    print("  - get_engagement_churn_analysis()")