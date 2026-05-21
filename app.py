import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.graph_objects as go
import plotly.express as px
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="European Banking Churn Analytics", page_icon="🏦", layout="wide")

@st.cache_resource
def load_models():
    model = pickle.load(open('model.pkl', 'rb'))
    scaler = pickle.load(open('scaler.pkl', 'rb'))
    columns = pickle.load(open('columns.pkl', 'rb'))
    return model, scaler, columns

model, scaler, feature_columns = load_models()

st.markdown("""
<style>
.main-header { font-size: 2.5rem; color: #1E3A5F; text-align: center; margin-bottom: 0; }
.sub-header { text-align: center; color: #666; margin-bottom: 2rem; }
.risk-low { background: linear-gradient(135deg, #28a745, #20c997); padding: 20px; border-radius: 15px; text-align: center; color: white; }
.risk-medium { background: linear-gradient(135deg, #ffc107, #ff9800); padding: 20px; border-radius: 15px; text-align: center; color: #333; }
.risk-high { background: linear-gradient(135deg, #dc3545, #c82333); padding: 20px; border-radius: 15px; text-align: center; color: white; }
.metric-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 15px; border-radius: 15px; text-align: center; color: white; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🏦 European Banking Customer Churn Analytics</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Data-driven insights for customer retention strategies</div>', unsafe_allow_html=True)
st.markdown("---")

st.sidebar.markdown("# 📝 Customer Profile")
col1, col2, col3 = st.sidebar.columns(3)

with col1:
    credit_score = st.number_input("Credit Score", 300, 900, 650, step=10)
    age = st.slider("Age", 18, 90, 35)
    tenure = st.slider("Tenure (Years)", 0, 10, 3)

with col2:
    balance = st.number_input("Balance (€)", 0.0, 500000.0, 50000.0, step=5000.0)
    num_products = st.slider("Number of Products", 1, 4, 1)
    has_cr_card = st.selectbox("Has Credit Card", ["Yes", "No"])

with col3:
    is_active = st.selectbox("Active Member", ["Yes", "No"])
    salary = st.number_input("Salary (€)", 0.0, 300000.0, 50000.0, step=5000.0)
    geography = st.selectbox("Geography", ["France", "Germany", "Spain"])
    gender = st.selectbox("Gender", ["Male", "Female"])

def get_age_group(age):
    if age < 30: return '18-30'
    elif age < 40: return '30-40'
    elif age < 50: return '40-50'
    elif age < 60: return '50-60'
    else: return '60+'

age_group = get_age_group(age)

input_data = {
    'CreditScore': credit_score, 'Age': age, 'Tenure': tenure,
    'Balance': balance, 'NumOfProducts': num_products,
    'HasCrCard': 1 if has_cr_card == "Yes" else 0,
    'IsActiveMember': 1 if is_active == "Yes" else 0,
    'EstimatedSalary': salary,
    'BalanceSalaryRatio': balance / (salary + 1),
    'ProductPerTenure': num_products / (tenure + 1),
    'EngagementScore': (1 if is_active == "Yes" else 0) * num_products,
    'AgeTenureInteraction': age * tenure,
    'Geography_Germany': 1 if geography == "Germany" else 0,
    'Geography_Spain': 1 if geography == "Spain" else 0,
    'Gender_Male': 1 if gender == "Male" else 0,
    f'AgeGroup_{age_group}': 1,
    'HighBalance': 1 if balance > 85000 else 0
}

input_df = pd.DataFrame([input_data])
for col in feature_columns:
    if col not in input_df.columns:
        input_df[col] = 0
input_df = input_df[feature_columns]

num_cols = ['CreditScore', 'Age', 'Tenure', 'Balance', 'NumOfProducts', 
            'EstimatedSalary', 'BalanceSalaryRatio', 'ProductPerTenure', 
            'EngagementScore', 'AgeTenureInteraction']
input_df[num_cols] = scaler.transform(input_df[num_cols])

churn_prob = model.predict_proba(input_df)[0][1]

if churn_prob < 0.3:
    risk_level, risk_class, risk_icon, action = "Low Risk", "risk-low", "🟢", "Standard Monitoring"
elif churn_prob < 0.7:
    risk_level, risk_class, risk_icon, action = "Medium Risk", "risk-medium", "🟡", "Proactive Engagement"
else:
    risk_level, risk_class, risk_icon, action = "High Risk", "risk-high", "🔴", "Immediate Action"

st.markdown("## 🎯 Prediction Results")
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f'<div class="metric-card"><h3>Churn Probability</h3><h2>{churn_prob:.1%}</h2></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="{risk_class}"><h3>{risk_icon} Risk Level</h3><h2>{risk_level}</h2></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="metric-card"><h3>Risk Score</h3><h2>{churn_prob * 100:.0f}<span style="font-size:1rem;">/100</span></h2></div>', unsafe_allow_html=True)
with c4:
    st.markdown(f'<div class="metric-card"><h3>Action Required</h3><h3>{action}</h3></div>', unsafe_allow_html=True)

st.markdown("## 📈 Risk Meter")
fig = go.Figure(go.Indicator(mode="gauge+number", value=churn_prob * 100,
    gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "#1E3A5F"},
           'steps': [{'range': [0, 30], 'color': '#d4edda'},
                     {'range': [30, 70], 'color': '#fff3cd'},
                     {'range': [70, 100], 'color': '#f8d7da'}]}))
fig.update_layout(height=300)
st.plotly_chart(fig, use_container_width=True)

st.markdown("## 💼 Business Recommendations")
if churn_prob > 0.7:
    st.error("🔴 **URGENT:** Schedule retention call, offer loyalty bonus, upgrade products")
    st.warning(f"💰 Estimated CLV at risk: €{salary * 0.3:,.0f}")
elif churn_prob > 0.3:
    st.info("🟡 **Proactive:** Send retention campaign, offer cross-sell, promote mobile banking")
    if is_active == "No":
        st.info("💡 Customer is inactive - activation could reduce risk by 40%")
    if num_products == 1:
        st.info("💡 Single product user - cross-selling could increase retention by 30%")
else:
    st.success("🟢 **Standard:** Send monthly statements, continue loyalty rewards")

st.markdown("---")
st.markdown("### 📊 Key Insights")
i1, i2 = st.columns(2)
with i1:
    st.markdown("- **Inactive members** are 3x more likely to churn")
    st.markdown("- **German customers** show 15-20% higher churn rate")
    st.markdown("- **Single product users** have 2x higher churn risk")
with i2:
    st.markdown("- **Young customers (<30)** churn more frequently")
    st.markdown("- **Zero balance accounts** indicate 40% higher churn probability")
st.markdown("---")
st.caption("© 2025 Unified Mentor - European Banking Customer Churn Analytics")
