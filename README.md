# 🏦 European Banking Customer Churn Analytics

## 📌 Project Overview
This project analyzes customer churn patterns in European banking using segmentation analytics. The interactive Streamlit dashboard provides insights into which customer segments are most likely to leave the bank.

## 🎯 Key Features
- **Real-time Churn Analytics**: Interactive dashboard with dynamic filters
- **Segmentation Analysis**: Churn patterns by geography, age, gender, credit score, and more
- **High-Value Customer Tracking**: Special focus on premium customer churn
- **Engagement Metrics**: Analysis of active vs inactive member behavior

## 📊 Key Findings
- **Overall Churn Rate**: X% (replace with your actual number)
- **Highest Risk Segment**: Customers aged 60+ with poor credit scores
- **Protection Factors**: Active membership and multiple banking products reduce churn by X%

## 🛠️ Technologies Used
- **Python** - Core programming language
- **Streamlit** - Interactive dashboard framework
- **Pandas** - Data manipulation and analysis
- **Plotly** - Interactive visualizations
- **Ngrok** - Public URL deployment (for Colab)

## 📁 Project Structure
bank-churn-analytics/
├── app.py # Main Streamlit dashboard
├── data_loader.py # Data loading and preprocessing
├── analysis.py # KPI calculations and analytics
├── requirements.txt # Python dependencies
├── European_Bank.csv # Customer dataset
└── README.md # Project documentation

## 🚀 How to Run Locally
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/bank-churn-analytics.git

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run app.py
👤 Author
Atharva Yelne 
Dashboard - https://ap96wpbnp4caheedy6nnk7.streamlit.app/
📅 Project Date
May 2026

---

## 📝 requirements.txt File

Create this file with:

```txt
streamlit==1.28.1
pandas==2.0.3
plotly==5.17.0
numpy==1.24.3
pyngrok==7.0.0
