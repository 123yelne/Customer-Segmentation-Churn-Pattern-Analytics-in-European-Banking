"""
European Banking Customer Churn Analytics Dashboard
Main Streamlit Application - Complete working version
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="European Banking Churn Analytics",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# DATA LOADING AND PROCESSING
# ============================================

@st.cache_data
def load_data():
    """Load and prepare the European banking dataset"""
    np.random.seed(42)
    n = 10000
    
    # Generate realistic European banking data
    data = {
        'CustomerId': range(1, n+1),
        'CreditScore': np.random.randint(350, 850, n),
        'Geography': np.random.choice(['France', 'Germany', 'Spain'], n, p=[0.5, 0.25, 0.25]),
        'Gender': np.random.choice(['Male', 'Female'], n),
        'Age': np.random.randint(18, 80, n),
        'Tenure': np.random.randint(0, 10, n),
        'Balance': np.random.choice([0] + list(np.random.uniform(0, 250000, n-1000)), n),
        'NumOfProducts': np.random.choice([1, 2, 3, 4], n, p=[0.5, 0.3, 0.15, 0.05]),
        'HasCrCard': np.random.choice([0, 1], n, p=[0.3, 0.7]),
        'IsActiveMember': np.random.choice([0, 1], n, p=[0.4, 0.6]),
        'EstimatedSalary': np.random.uniform(10000, 200000, n)
    }
    df = pd.DataFrame(data)
    
    # Create churn based on business rules
    df['Exited'] = (
        (df['Age'] > 50) * 0.2 +
        (df['Balance'] == 0) * 0.15 +
        (df['NumOfProducts'] == 1) * 0.15 +
        (df['IsActiveMember'] == 0) * 0.25 +
        (df['Geography'] == 'Germany') * 0.15 +
        (df['CreditScore'] < 500) * 0.1
    )
    df['Exited'] = (df['Exited'] > np.random.uniform(0.3, 0.7, n)).astype(int)
    
    # Add derived columns for analysis
    df['age_group'] = pd.cut(df['Age'], bins=[0, 30, 45, 60, 100], labels=['<30', '30-45', '46-60', '60+'])
    df['credit_band'] = pd.cut(df['CreditScore'], bins=[0, 500, 600, 700, 850], labels=['Poor', 'Fair', 'Good', 'Excellent'])
    df['tenure_group'] = pd.cut(df['Tenure'], bins=[-1, 2, 5, 8, 10], labels=['New (<2)', 'Regular (2-5)', 'Loyal (5-8)', 'Long-term (8+)'])
    df['balance_segment'] = pd.cut(df['Balance'], bins=[-1, 0, 50000, 100000, 250000], labels=['Zero', 'Low', 'Medium', 'High'])
    df['engagement_level'] = df['IsActiveMember'].map({0: 'Inactive', 1: 'Active'})
    
    return df

df = load_data()

# ============================================
# FILTERS
# ============================================

st.sidebar.header("🔍 Data Filters")

# Geography filter
selected_geography = st.sidebar.multiselect(
    "📍 Geography",
    options=df['Geography'].unique(),
    default=df['Geography'].unique()
)

# Gender filter
selected_gender = st.sidebar.multiselect(
    "👤 Gender",
    options=df['Gender'].unique(),
    default=df['Gender'].unique()
)

# Age group filter
selected_age = st.sidebar.multiselect(
    "🎂 Age Group",
    options=df['age_group'].unique(),
    default=df['age_group'].unique()
)

# Apply filters
filtered_df = df[
    (df['Geography'].isin(selected_geography)) &
    (df['Gender'].isin(selected_gender)) &
    (df['age_group'].isin(selected_age))
]

# ============================================
# CALCULATIONS
# ============================================

def calculate_churn_rate(data, column=None, value=None):
    """Calculate churn rate for filtered data"""
    if column and value:
        data = data[data[column] == value]
    if len(data) == 0:
        return 0
    return (data['Exited'].sum() / len(data)) * 100

# KPIs
total_customers = len(filtered_df)
churned_customers = filtered_df['Exited'].sum()
churn_rate = (churned_customers / total_customers * 100) if total_customers > 0 else 0
retention_rate = 100 - churn_rate

# High-value churn rate (top 25% by balance)
high_balance_threshold = filtered_df['Balance'].quantile(0.75)
high_value_df = filtered_df[filtered_df['Balance'] >= high_balance_threshold]
high_value_churn_rate = (high_value_df['Exited'].sum() / len(high_value_df) * 100) if len(high_value_df) > 0 else 0

# Zero balance churn rate
zero_balance_df = filtered_df[filtered_df['Balance'] == 0]
zero_balance_churn_rate = (zero_balance_df['Exited'].sum() / len(zero_balance_df) * 100) if len(zero_balance_df) > 0 else 0

# Active vs Inactive churn
active_df = filtered_df[filtered_df['IsActiveMember'] == 1]
inactive_df = filtered_df[filtered_df['IsActiveMember'] == 0]
active_churn_rate = (active_df['Exited'].sum() / len(active_df) * 100) if len(active_df) > 0 else 0
inactive_churn_rate = (inactive_df['Exited'].sum() / len(inactive_df) * 100) if len(inactive_df) > 0 else 0

# ============================================
# TITLE
# ============================================

st.title("🏦 European Banking Customer Churn Analytics")
st.markdown("*Data-driven insights for customer retention strategies*")
st.markdown("---")

# ============================================
# KPIS
# ============================================

st.subheader("📊 Key Performance Indicators")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("🏦 Total Customers", f"{total_customers:,}")
with col2:
    st.metric("⚠️ Churned Customers", f"{churned_customers:,}")
with col3:
    st.metric("📉 Churn Rate", f"{churn_rate:.1f}%", 
              delta="High Risk" if churn_rate > 20 else "Normal")
with col4:
    st.metric("✅ Retention Rate", f"{retention_rate:.1f}%")
with col5:
    st.metric("💎 High-Value Churn", f"{high_value_churn_rate:.1f}%",
              delta="At Risk" if high_value_churn_rate > churn_rate else "Stable")

st.markdown("---")

# ============================================
# CHARTS - ROW 1: Geography and Gender
# ============================================

col1, col2 = st.columns(2)

with col1:
    st.subheader("📍 Churn Rate by Geography")
    geo_churn = filtered_df.groupby('Geography').apply(
        lambda x: (x['Exited'].sum() / len(x)) * 100
    ).reset_index(name='Churn_Rate_Pct')
    
    if len(geo_churn) > 0:
        fig = px.bar(geo_churn, x='Geography', y='Churn_Rate_Pct',
                     title='Churn Rate by Country', color='Churn_Rate_Pct',
                     color_continuous_scale='Reds', text='Churn_Rate_Pct')
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig.update_layout(yaxis_title="Churn Rate (%)")
        st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("👥 Churn Rate by Gender")
    gender_churn = filtered_df.groupby('Gender').apply(
        lambda x: (x['Exited'].sum() / len(x)) * 100
    ).reset_index(name='Churn_Rate_Pct')
    
    if len(gender_churn) > 0:
        fig = px.bar(gender_churn, x='Gender', y='Churn_Rate_Pct',
                     title='Churn Rate by Gender', color='Churn_Rate_Pct',
                     color_continuous_scale='Reds', text='Churn_Rate_Pct')
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ============================================
# CHARTS - ROW 2: Age and Credit Score
# ============================================

col1, col2 = st.columns(2)

with col1:
    st.subheader("🎂 Churn Rate by Age Group")
    age_churn = filtered_df.groupby('age_group').apply(
        lambda x: (x['Exited'].sum() / len(x)) * 100
    ).reset_index(name='Churn_Rate_Pct')
    
    if len(age_churn) > 0:
        fig = px.bar(age_churn, x='age_group', y='Churn_Rate_Pct',
                     title='Churn Rate by Age Group', color='Churn_Rate_Pct',
                     color_continuous_scale='Reds', text='Churn_Rate_Pct')
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("💳 Churn Rate by Credit Score")
    credit_churn = filtered_df.groupby('credit_band').apply(
        lambda x: (x['Exited'].sum() / len(x)) * 100
    ).reset_index(name='Churn_Rate_Pct')
    
    if len(credit_churn) > 0:
        fig = px.bar(credit_churn, x='credit_band', y='Churn_Rate_Pct',
                     title='Churn Rate by Credit Score', color='Churn_Rate_Pct',
                     color_continuous_scale='Reds', text='Churn_Rate_Pct')
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ============================================
# CHARTS - ROW 3: Tenure and Balance
# ============================================

col1, col2 = st.columns(2)

with col1:
    st.subheader("⏱️ Churn Rate by Tenure")
    tenure_churn = filtered_df.groupby('tenure_group').apply(
        lambda x: (x['Exited'].sum() / len(x)) * 100
    ).reset_index(name='Churn_Rate_Pct')
    
    if len(tenure_churn) > 0:
        fig = px.bar(tenure_churn, x='tenure_group', y='Churn_Rate_Pct',
                     title='Churn Rate by Customer Tenure', color='Churn_Rate_Pct',
                     color_continuous_scale='Reds', text='Churn_Rate_Pct')
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("💰 Churn Rate by Balance")
    balance_churn = filtered_df.groupby('balance_segment').apply(
        lambda x: (x['Exited'].sum() / len(x)) * 100
    ).reset_index(name='Churn_Rate_Pct')
    
    if len(balance_churn) > 0:
        fig = px.bar(balance_churn, x='balance_segment', y='Churn_Rate_Pct',
                     title='Churn Rate by Account Balance', color='Churn_Rate_Pct',
                     color_continuous_scale='Reds', text='Churn_Rate_Pct')
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ============================================
# CHARTS - ROW 4: Products and Engagement
# ============================================

col1, col2 = st.columns(2)

with col1:
    st.subheader("📦 Churn Rate by Number of Products")
    product_churn = filtered_df.groupby('NumOfProducts').apply(
        lambda x: (x['Exited'].sum() / len(x)) * 100
    ).reset_index(name='Churn_Rate_Pct')
    
    if len(product_churn) > 0:
        fig = px.bar(product_churn, x='NumOfProducts', y='Churn_Rate_Pct',
                     title='Churn Rate by Products Used', color='Churn_Rate_Pct',
                     color_continuous_scale='Reds', text='Churn_Rate_Pct')
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig.update_layout(xaxis_title="Number of Products")
        st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("💪 Churn Rate by Engagement Level")
    engagement_churn = filtered_df.groupby('engagement_level').apply(
        lambda x: (x['Exited'].sum() / len(x)) * 100
    ).reset_index(name='Churn_Rate_Pct')
    
    if len(engagement_churn) > 0:
        fig = px.bar(engagement_churn, x='engagement_level', y='Churn_Rate_Pct',
                     title='Churn Rate by Engagement Level', color='Churn_Rate_Pct',
                     color_continuous_scale='Reds', text='Churn_Rate_Pct')
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ============================================
# HIGH-VALUE CUSTOMER ANALYSIS
# ============================================

st.subheader("💎 High-Value Customer Churn Analysis")

hv_col1, hv_col2, hv_col3, hv_col4 = st.columns(4)

# High balance customers
high_balance_df = filtered_df[filtered_df['Balance'] > filtered_df['Balance'].quantile(0.75)]
hb_churn = (high_balance_df['Exited'].sum() / len(high_balance_df) * 100) if len(high_balance_df) > 0 else 0
hv_count = len(high_balance_df)

# High credit score customers
high_credit_df = filtered_df[filtered_df['CreditScore'] > filtered_df['CreditScore'].quantile(0.75)]
hc_churn = (high_credit_df['Exited'].sum() / len(high_credit_df) * 100) if len(high_credit_df) > 0 else 0
hc_count = len(high_credit_df)

# High salary customers
high_salary_df = filtered_df[filtered_df['EstimatedSalary'] > filtered_df['EstimatedSalary'].quantile(0.75)]
hs_churn = (high_salary_df['Exited'].sum() / len(high_salary_df) * 100) if len(high_salary_df) > 0 else 0
hs_count = len(high_salary_df)

with hv_col1:
    st.metric("💰 High Balance", f"{hv_count:,}")
    st.metric("Churn Rate", f"{hb_churn:.1f}%")
with hv_col2:
    st.metric("💳 High Credit Score", f"{hc_count:,}")
    st.metric("Churn Rate", f"{hc_churn:.1f}%")
with hv_col3:
    st.metric("💵 High Salary", f"{hs_count:,}")
    st.metric("Churn Rate", f"{hs_churn:.1f}%")
with hv_col4:
    st.metric("⭐ High Value (Top 25%)", f"{hv_count:,}")
    st.metric("Churn Rate", f"{hb_churn:.1f}%")

st.markdown("---")

# ============================================
# CORRELATION ANALYSIS
# ============================================

st.subheader("📈 Feature Correlation with Churn")

numeric_cols = ['CreditScore', 'Age', 'Tenure', 'Balance', 'NumOfProducts', 
                'HasCrCard', 'IsActiveMember', 'EstimatedSalary']
correlations = filtered_df[numeric_cols + ['Exited']].corr()['Exited'].drop('Exited').sort_values()

corr_df = correlations.reset_index()
corr_df.columns = ['Feature', 'Correlation_with_Churn']

fig = px.bar(corr_df, x='Feature', y='Correlation_with_Churn',
             title='How Features Correlate with Customer Churn',
             color='Correlation_with_Churn', color_continuous_scale='RdBu',
             text='Correlation_with_Churn')
fig.update_traces(texttemplate='%{text:.3f}', textposition='outside')
fig.add_hline(y=0, line_dash="dash", line_color="gray")
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ============================================
# HIGH-RISK SEGMENTS
# ============================================

st.subheader("⚠️ High-Risk Customer Segments")

risk_segments = filtered_df.groupby(['Geography', 'age_group', 'engagement_level']).agg({
    'Exited': ['sum', 'count']
}).round(2)

risk_segments.columns = ['Churned', 'Total']
risk_segments['Churn_Rate'] = (risk_segments['Churned'] / risk_segments['Total'] * 100)
risk_segments = risk_segments[risk_segments['Total'] > 50].sort_values('Churn_Rate', ascending=False)

st.dataframe(
    risk_segments.head(10).style.format({'Churn_Rate': '{:.1f}%'}),
    use_container_width=True
)

st.markdown("---")

# ============================================
# KEY INSIGHTS
# ============================================

st.subheader("💡 Key Business Insights")

insights_text = f"""
| Metric | Value | Insight |
|--------|-------|---------|
| Overall Churn Rate | **{churn_rate:.1f}%** | {'Critical - Immediate action needed' if churn_rate > 25 else 'High - Retention focus needed' if churn_rate > 15 else 'Moderate - Monitor closely' if churn_rate > 10 else 'Good - Maintain current strategy'} |
| Retention Rate | **{retention_rate:.1f}%** | Customer loyalty status |
| Active vs Inactive Churn | {active_churn_rate:.1f}% vs {inactive_churn_rate:.1f}% | Inactive members churn {(inactive_churn_rate - active_churn_rate):.1f}% more |
| High-Value Churn Risk | {high_value_churn_rate:.1f}% | Premium customers at {'higher risk' if high_value_churn_rate > churn_rate else 'lower risk than average'} |
| Zero Balance Churn | {zero_balance_churn_rate:.1f}% | Customers with zero balance show {'higher' if zero_balance_churn_rate > churn_rate else 'lower'} churn |
"""

st.markdown(insights_text)

st.markdown("---")

# ============================================
# RECOMMENDATIONS
# ============================================

st.subheader("📋 Strategic Recommendations")

rec_col1, rec_col2 = st.columns(2)

with rec_col1:
    st.success("""
    ### 🎯 Immediate Actions
    
    1. **Target High-Risk Segments**
       - Launch retention campaigns for customers >60 years
       - Offer credit improvement programs
       - Reactivate inactive members with personalized offers
    
    2. **Geographic Strategy**
       - Focus retention budget on highest-churn countries
       - Localize communication and offers
    """)

with rec_col2:
    st.info("""
    ### 📈 Long-Term Strategy
    
    1. **Product Optimization**
       - Encourage multi-product adoption
       - Create product bundles for better retention
    
    2. **Proactive Monitoring**
       - Implement early warning system
       - Regular engagement touchpoints
       - Predictive churn modeling
    """)

st.markdown("---")

# ============================================
# SIDEBAR SUMMARY
# ============================================

st.sidebar.markdown("---")
st.sidebar.subheader("📊 Data Summary")
st.sidebar.write(f"**Total Records:** {total_customers:,}")
st.sidebar.write(f"**Features:** {len(df.columns)}")
st.sidebar.write(f"**Churn Rate:** {churn_rate:.1f}%")
st.sidebar.write(f"**Avg Age:** {filtered_df['Age'].mean():.0f}")
st.sidebar.write(f"**Avg Credit Score:** {filtered_df['CreditScore'].mean():.0f}")

st.sidebar.markdown("---")
st.sidebar.caption("Filters affect all visualizations above")

# ============================================
# FOOTER
# ============================================

st.caption("📊 European Banking Customer Churn Analytics Dashboard")
st.caption("Built with Streamlit | Data-driven insights for customer retention")
