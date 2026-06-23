import streamlit as st


st.set_page_config(
    page_title="AgriCredit Resilience",
    page_icon="🌾",
    layout="wide",
)


st.title("🌾 AgriCredit Resilience")
st.subheader("Explainable Financial Vulnerability Decision-Support System")

st.markdown(
    """
AgriCredit Resilience is a machine learning portfolio project that predicts household
financial vulnerability among rural farming households in Myanmar.

The system is designed as a **decision-support tool**, not an automatic loan approval system.
It helps identify households that may need careful financial review, livelihood support,
or safer assistance options before taking on new debt.
"""
)

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Final ABT Rows", "1,500")
    st.caption("Household-level analytical dataset")

with col2:
    st.metric("Main Model", "Logistic Regression")
    st.caption("Probability-based vulnerability prediction")

with col3:
    st.metric("Support Model", "Decision Tree")
    st.caption("Rule-based explainability support")

st.divider()

st.header("Project Problem")

st.markdown(
    """
Many rural households face financial pressure because of low income, debt, crop damage,
market disruption, food price increases, and limited access to assistance.

A normal loan may help some households, but it may also increase financial burden for
households that are already highly vulnerable.

This project asks:

> Can machine learning help identify financially vulnerable households and support
> more responsible loan or assistance decisions?
"""
)

st.header("What the Dashboard Does")

st.markdown(
    """
The dashboard allows users to:

- enter household and livelihood information
- predict financial vulnerability probability
- classify risk as low, medium, or high
- view responsible decision-support recommendations
- understand model performance and explainability
- connect the project to Sustainable Development Goals
"""
)

st.header("Model Recommendation")

st.success(
    """
Logistic Regression is used as the main prediction model because it performed better
than the Decision Tree across accuracy, precision, recall, F1-score, and ROC-AUC.

The Decision Tree is kept as a supporting explainability model because its if-then
rules are easier to explain to non-technical users.
"""
)

st.warning(
    """
Important: This dashboard should not be used to automatically approve or reject loans.
It is only a decision-support prototype for portfolio and learning purposes.
"""
)

st.divider()

st.header("Dashboard Pages")

st.markdown(
    """
Use the sidebar to navigate:

1. **Risk Prediction** — predict household vulnerability probability  
2. **Model Explanation** — understand important features and model logic  
3. **Market Feasibility** — connect risk with market conditions  
4. **Model Evaluation** — compare Decision Tree and Logistic Regression  
5. **SDG Impact** — explain the social impact of the project  
"""
)