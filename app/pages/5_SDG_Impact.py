import streamlit as st


st.set_page_config(
    page_title="SDG Impact",
    page_icon="🌍",
    layout="wide",
)


st.title("🌍 SDG Impact")
st.subheader("Connecting AgriCredit Resilience With Sustainable Development Goals")

st.markdown(
    """
AgriCredit Resilience is not only a machine learning project.

It is also a decision-support prototype designed around responsible financial inclusion,
rural livelihoods, food security, and climate-related vulnerability.
"""
)

st.divider()


st.header("Why This Project Matters")

st.markdown(
    """
Rural farming households can face many overlapping risks:

- low or unstable income
- high debt burden
- crop damage
- food price increases
- weak market access
- displacement or shocks
- limited assistance coverage

When these risks overlap, a normal loan may not always be the safest solution.
Some households may need livelihood support, flexible repayment, cash assistance,
or manual review before taking on more debt.

This project uses machine learning to support better decision-making.
"""
)

st.warning(
    """
The goal is not to automatically approve or reject households.
The goal is to identify possible financial vulnerability and support responsible human review.
"""
)

st.divider()


st.header("SDG Alignment")

col1, col2 = st.columns(2)

with col1:
    st.info(
        """
### SDG 1: No Poverty

The project supports SDG 1 by identifying households that may be financially vulnerable.

By detecting financial stress early, decision-makers can consider safer support options
before households fall deeper into debt or poverty.
"""
    )

    st.success(
        """
### SDG 2: Zero Hunger

The model includes food coping behavior and basic needs indicators.

This helps connect financial vulnerability with food security concerns.
Households using more coping strategies may need support before taking on new loans.
"""
    )

with col2:
    st.warning(
        """
### SDG 8: Decent Work and Economic Growth

The project supports more responsible financial inclusion.

Instead of treating loans as always positive, it encourages careful review of repayment capacity,
market conditions, and livelihood stability.
"""
    )

    st.error(
        """
### SDG 13: Climate Action

The model includes crop damage and agricultural shock indicators.

This connects rural finance decisions with climate-related risks that can affect farmers'
income, production, and repayment ability.
"""
    )

st.divider()


st.header("Responsible AI Perspective")

st.markdown(
    """
This project follows a responsible AI mindset.

A model prediction should not replace human judgment, especially when decisions may affect
people's access to credit, assistance, or livelihood support.

The dashboard therefore uses three layers:

1. **Prediction**  
   Estimate household financial vulnerability.

2. **Explanation**  
   Show important model features and decision logic.

3. **Context**  
   Consider market feasibility and social impact before making decisions.
"""
)

st.divider()


st.header("From Prediction to Responsible Support")

support_col1, support_col2, support_col3 = st.columns(3)

with support_col1:
    st.metric("Low Risk", "Review normally")
    st.markdown(
        """
Households with lower predicted vulnerability may be more financially stable.

However, final decisions should still consider local context.
"""
    )

with support_col2:
    st.metric("Medium Risk", "Review carefully")
    st.markdown(
        """
Households with medium predicted vulnerability may need smaller loans,
flexible repayment, or combined support.
"""
    )

with support_col3:
    st.metric("High Risk", "Support first")
    st.markdown(
        """
Households with high predicted vulnerability should not be automatically given normal loans.

Manual review, livelihood support, or assistance-first options may be safer.
"""
    )

st.divider()


st.header("Portfolio Value")

st.markdown(
    """
This project demonstrates several practical data and machine learning skills:

- business problem framing
- data generation and documentation
- data understanding
- data cleaning and feature engineering
- Decision Tree modeling
- Logistic Regression modeling
- model evaluation and comparison
- explainability
- Streamlit dashboard development
- responsible AI thinking
"""
)

st.success(
    """
AgriCredit Resilience shows how machine learning can be used not just for prediction,
but also for responsible decision support in a real-world development context.
"""
)

st.divider()


st.header("Final Message")

st.markdown(
    """
The main purpose of this project is to show how data science can support better,
more careful decisions for rural households.

A good model should not only be accurate.

It should also be explainable, responsible, and connected to the real-world problem it is trying to solve.
"""
)