"""
European Banking Customer Churn Analytics Dashboard
Main Streamlit Application
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Import our custom modules
from data_loader import load_data, create_segments, get_data_summary, get_column_descriptions
from analysis import (
    calculate_kpis, get_geography_churn, get_age_churn, get_gender_churn,
    get_credit_band_churn, get_tenure_churn, get_balance_churn, get_product_churn,
    get_high_value_analysis, get_correlation_analysis, get_risk_segments,
    get_engagement_churn_analysis
)

# Page configuration
st.set_page_config(
    page_title="European Banking Churn Analytics",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title
st.title("🏦 European Banking Customer Churn Analytics")
st.markdown("*Data-driven insights for customer retention strategies*")
st.markdown("---")

# Load and process data
@st.cache_data
def load_and_process_data():
    df = load_data('European_Bank.csv')
    if df is not None:
        df = create_segments(df)
    return df

df = load_and_process_data()

if df is None:
    st.error("❌ Could not load data. Please make sure 'European_Bank.csv' is in the same directory.")
    st.stop()

# Sidebar - Filters
st.sidebar.header("🔍 Data Filters")

# Geography filter
geography_options = ['All'] + list(df['Geography'].unique())
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
age_options = ['<30', '30-45', '46-60', '60+']
selected_age = st.sidebar.multiselect(
    "🎂 Age Group",
    options=age_options,
    default=age_options
)

# Apply filters
filtered_df = df[
    (df['Geography'].isin(selected_geography)) &
    (df['Gender'].isin(selected_gender)) &
    (df['age_group'].isin(selected_age))
]

# Calculate KPIs
kpis = calculate_kpis(df, filtered_df)

# Display KPIs in a nice row
st.subheader("📊 Key Performance Indicators")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("🏦 Total Customers", f"{kpis['total_customers']:,}")
with col2:
    st.metric("⚠️ Churned Customers", f"{kpis['churned_customers']:,}")
with col3:
    st.metric("📉 Churn Rate", f"{kpis['churn_rate']}%", 
              delta="High Risk" if kpis['churn_rate'] > 20 else "Normal")
with col4:
    st.metric("✅ Retention Rate", f"{kpis['retention_rate']}%")
with col5:
    st.metric("💎 High-Value Churn", f"{kpis['high_value_churn_rate']}%",
              delta="At Risk" if kpis['high_value_churn_rate'] > kpis['churn_rate'] else "Stable")

st.markdown("---")

# Row 1: Geography and Gender
col1, col2 = st.columns(2)

with col1:
    st.subheader("📍 Churn Rate by Geography")
    geo_data = get_geography_churn(filtered_df)
    if len(geo_data) > 0:
        fig = px.bar(
            geo_data.reset_index(),
            x='Geography',
            y='Churn_Rate_Pct',
            title='Churn Rate by Country',
            color='Churn_Rate_Pct',
            color_continuous_scale='Reds',
            text='Churn_Rate_Pct'
        )
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig.update_layout(yaxis_title="Churn Rate (%)", xaxis_title="Country")
        st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("👥 Churn Rate by Gender")
    gender_data = get_gender_churn(filtered_df)
    if len(gender_data) > 0:
        fig = px.bar(
            gender_data.reset_index(),
            x='Gender',
            y='Churn_Rate_Pct',
            title='Churn Rate by Gender',
            color='Churn_Rate_Pct',
            color_continuous_scale='Reds',
            text='Churn_Rate_Pct'
        )
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig.update_layout(yaxis_title="Churn Rate (%)", xaxis_title="Gender")
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Row 2: Age and Credit Score
col1, col2 = st.columns(2)

with col1:
    st.subheader("🎂 Churn Rate by Age Group")
    age_data = get_age_churn(filtered_df)
    if len(age_data) > 0:
        fig = px.bar(
            age_data.reset_index(),
            x='age_group',
            y='Churn_Rate_Pct',
            title='Churn Rate by Age Group',
            color='Churn_Rate_Pct',
            color_continuous_scale='Reds',
            text='Churn_Rate_Pct'
        )
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig.update_layout(yaxis_title="Churn Rate (%)", xaxis_title="Age Group")
        st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("💳 Churn Rate by Credit Score")
    credit_data = get_credit_band_churn(filtered_df)
    if len(credit_data) > 0:
        fig = px.bar(
            credit_data.reset_index(),
            x='credit_band',
            y='Churn_Rate_Pct',
            title='Churn Rate by Credit Score',
            color='Churn_Rate_Pct',
            color_continuous_scale='Reds',
            text='Churn_Rate_Pct'
        )
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig.update_layout(yaxis_title="Churn Rate (%)", xaxis_title="Credit Score Band")
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Row 3: Tenure and Balance
col1, col2 = st.columns(2)

with col1:
    st.subheader("⏱️ Churn Rate by Tenure")
    tenure_data = get_tenure_churn(filtered_df)
    if len(tenure_data) > 0:
        fig = px.bar(
            tenure_data.reset_index(),
            x='tenure_group',
            y='Churn_Rate_Pct',
            title='Churn Rate by Customer Tenure',
            color='Churn_Rate_Pct',
            color_continuous_scale='Reds',
            text='Churn_Rate_Pct'
        )
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig.update_layout(yaxis_title="Churn Rate (%)", xaxis_title="Tenure Group")
        st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("💰 Churn Rate by Balance")
    balance_data = get_balance_churn(filtered_df)
    if len(balance_data) > 0:
        fig = px.bar(
            balance_data.reset_index(),
            x='balance_segment',
            y='Churn_Rate_Pct',
            title='Churn Rate by Account Balance',
            color='Churn_Rate_Pct',
            color_continuous_scale='Reds',
            text='Churn_Rate_Pct'
        )
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig.update_layout(yaxis_title="Churn Rate (%)", xaxis_title="Balance Segment")
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Row 4: Products and Engagement
col1, col2 = st.columns(2)

with col1:
    st.subheader("📦 Churn Rate by Number of Products")
    product_data = get_product_churn(filtered_df)
    if len(product_data) > 0:
        fig = px.bar(
            product_data.reset_index(),
            x='NumOfProducts',
            y='Churn_Rate_Pct',
            title='Churn Rate by Products Used',
            color='Churn_Rate_Pct',
            color_continuous_scale='Reds',
            text='Churn_Rate_Pct'
        )
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig.update_layout(yaxis_title="Churn Rate (%)", xaxis_title="Number of Products")
        st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("💪 Churn Rate by Engagement Level")
    engagement_data = get_engagement_churn_analysis(filtered_df)
    if len(engagement_data) > 0:
        fig = px.bar(
            engagement_data.reset_index(),
            x='engagement_level',
            y='Churn_Rate_Pct',
            title='Churn Rate by Engagement Level',
            color='Churn_Rate_Pct',
            color_continuous_scale='Reds',
            text='Churn_Rate_Pct'
        )
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig.update_layout(yaxis_title="Churn Rate (%)", xaxis_title="Engagement Level")
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# High-Value Customer Analysis
st.subheader("💎 High-Value Customer Churn Analysis")

hv_data = get_high_value_analysis(filtered_df)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("High Balance Customers (>75th %ile)", hv_data['high_balance_customers'])
    st.metric("Churn Rate", f"{hv_data['high_balance_churn_rate']}%")
with col2:
    st.metric("High Credit Score (>75th %ile)", hv_data['high_credit_customers'])
    st.metric("Churn Rate", f"{hv_data['high_credit_churn_rate']}%")
with col3:
    st.metric("High Salary (>75th %ile)", hv_data['high_salary_customers'])
    st.metric("Churn Rate", f"{hv_data['high_salary_churn_rate']}%")
with col4:
    st.metric("High Value Score (>75th %ile)", hv_data['high_value_customers'])
    st.metric("Churn Rate", f"{hv_data['high_value_churn_rate']}%")

st.markdown("---")

# Correlation Analysis
st.subheader("📈 Feature Correlation with Churn")

corr_data = get_correlation_analysis(filtered_df)
if len(corr_data) > 0:
    fig = px.bar(
        corr_data,
        x='Feature',
        y='Correlation_with_Churn',
        title='How Features Correlate with Customer Churn',
        color='Correlation_with_Churn',
        color_continuous_scale='RdBu',
        text='Correlation_with_Churn'
    )
    fig.update_traces(texttemplate='%{text:.3f}', textposition='outside')
    fig.update_layout(yaxis_title="Correlation with Churn", xaxis_title="Feature")
    fig.add_hline(y=0, line_dash="dash", line_color="gray")
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Risk Segments Table
st.subheader("⚠️ High-Risk Customer Segments")

risk_data = get_risk_segments(filtered_df)
if len(risk_data) > 0:
    # Display top 10 risk segments
    st.dataframe(
        risk_data.head(10).style.format({'Churn_Rate': '{:.1f}%'}),
        use_container_width=True
    )

st.markdown("---")

# Key Insights
st.subheader("💡 Key Business Insights")

insights = f"""
| Metric | Value | Insight |
|--------|-------|---------|
| Overall Churn Rate | **{kpis['churn_rate']}%** | {('Critical - Immediate action needed' if kpis['churn_rate'] > 25 else 'High - Retention focus needed' if kpis['churn_rate'] > 15 else 'Moderate - Monitor closely' if kpis['churn_rate'] > 10 else 'Good - Maintain current strategy')} |
| Retention Rate | **{kpis['retention_rate']}%** | Customer loyalty status |
| Active vs Inactive Churn | {kpis['active_churn_rate']}% vs {kpis['inactive_churn_rate']}% | Inactive members churn {kpis['inactive_churn_rate'] - kpis['active_churn_rate']:.1f}% more |
| High-Value Churn Risk | {kpis['high_value_churn_rate']}% | Premium customers at {('high risk' if kpis['high_value_churn_rate'] > kpis['churn_rate'] else 'lower risk than average')} |
| Zero Balance Churn | {kpis['zero_balance_churn_rate']}% | Customers with zero balance show {('higher' if kpis['zero_balance_churn_rate'] > kpis['churn_rate'] else 'lower')} churn |
"""

st.markdown(insights)

st.markdown("---")

# Recommendations
st.subheader("📋 Strategic Recommendations")

col1, col2 = st.columns(2)

with col1:
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

with col2:
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

# Footer
st.caption("📊 European Banking Customer Churn Analytics Dashboard")
st.caption("Built with Streamlit | Data-driven insights for customer retention")

# Sidebar additional info
st.sidebar.markdown("---")
st.sidebar.subheader("📊 Data Summary")

summary = get_data_summary(df)
st.sidebar.write(f"**Total Records:** {summary.get('total_customers', 'N/A'):,}")
st.sidebar.write(f"**Features:** {summary.get('total_features', 'N/A')}")
st.sidebar.write(f"**Churn Rate:** {summary.get('churn_rate', 'N/A'):.1f}%")
st.sidebar.write(f"**Avg Age:** {summary.get('avg_age', 'N/A')}")
st.sidebar.write(f"**Avg Credit Score:** {summary.get('avg_credit_score', 'N/A')}")

st.sidebar.markdown("---")
st.sidebar.caption("Filters affect all visualizations above")