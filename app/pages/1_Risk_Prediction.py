import sys
from pathlib import Path

import pandas as pd
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from src.app_utils import (  # noqa: E402
    assign_risk_level,
    create_recommendation,
    load_abt,
    load_logistic_regression_model,
    prepare_prediction_input,
)


st.set_page_config(
    page_title="Risk Prediction",
    page_icon="📊",
    layout="wide",
)


st.title("📊 Risk Prediction")
st.subheader("Predict Household Financial Vulnerability")

st.markdown(
    """
This page uses the trained **Logistic Regression model** to estimate the probability
that a household is financially vulnerable.

The prediction is used for **decision support only**. It should not be used to
automatically approve or reject a loan.
"""
)

st.divider()


@st.cache_data
def get_abt():
    return load_abt()


@st.cache_resource
def get_model():
    return load_logistic_regression_model()


abt = get_abt()
model = get_model()


st.header("Household Input Form")

state_options = sorted(abt["state_region"].dropna().unique())
displacement_options = sorted(abt["displacement_status"].dropna().unique())
crop_options = sorted(abt["main_crop"].dropna().unique())

col1, col2 = st.columns(2)

with col1:
    state_region = st.selectbox(
        "State/Region",
        state_options,
        index=state_options.index("Magway") if "Magway" in state_options else 0,
    )

    household_size = st.number_input(
        "Household size",
        min_value=1,
        max_value=15,
        value=5,
        step=1,
    )

    female_headed_household = st.selectbox(
        "Female-headed household",
        options=["No", "Yes"],
    )

    disability_present = st.selectbox(
        "Disability present in household",
        options=["No", "Yes"],
    )

    displacement_status = st.selectbox(
        "Displacement status",
        displacement_options,
    )

    monthly_income = st.number_input(
        "Monthly income (MMK)",
        min_value=0,
        value=250000,
        step=10000,
    )

    has_debt = st.selectbox(
        "Does the household have debt?",
        options=["No", "Yes"],
        index=1,
    )

    total_debt = st.number_input(
        "Total debt (MMK)",
        min_value=0,
        value=350000,
        step=10000,
    )

    monthly_debt_repayment = st.number_input(
        "Monthly debt repayment (MMK)",
        min_value=0,
        value=50000,
        step=5000,
    )

with col2:
    savings_duration_weeks = st.number_input(
        "Savings duration (weeks)",
        min_value=0,
        max_value=52,
        value=4,
        step=1,
    )

    market_access = st.selectbox(
        "Market access",
        options=["No", "Yes"],
        index=1,
    )

    is_farming_household = st.selectbox(
        "Farming household",
        options=["No", "Yes"],
        index=1,
    )

    main_crop = st.selectbox(
        "Main crop",
        crop_options,
    )

    farm_size_acres = st.number_input(
        "Farm size (acres)",
        min_value=0.0,
        value=3.0,
        step=0.5,
    )

    irrigation_access = st.selectbox(
        "Irrigation access",
        options=["No", "Yes"],
    )

    fertilizer_cost = st.number_input(
        "Fertilizer cost (MMK)",
        min_value=0,
        value=120000,
        step=10000,
    )

    crop_damage_recent = st.selectbox(
        "Recent crop damage",
        options=["No", "Yes"],
    )

    rCSI_score = st.slider(
        "Reduced Coping Strategy Index score",
        min_value=0,
        max_value=50,
        value=20,
    )

    basic_needs_score = st.slider(
        "Basic needs score",
        min_value=0,
        max_value=3,
        value=2,
    )


st.divider()

st.header("Context Values")

st.markdown(
    """
The values below are automatically filled using the selected State/Region.
They come from the final analytical base table.
"""
)

state_context = abt[abt["state_region"] == state_region].iloc[0]

basic_food_basket_change_1y = float(state_context["basic_food_basket_change_1y"])
rice_price_change_1y = float(state_context["rice_price_change_1y"])
fuel_price_change_1y = float(state_context["fuel_price_change_1y"])
market_disruption_score = float(state_context["market_disruption_score"])
market_pressure_score = float(state_context["market_pressure_score"])
mpca_per_person = float(state_context["mpca_per_person"])
coverage_rate = float(state_context["coverage_rate"])
coverage_gap_ratio = float(state_context["coverage_gap_ratio"])
response_gap = float(state_context["response_gap"])
number_of_partners_active = float(state_context["number_of_partners_active"])

household_meb_requirement = mpca_per_person * household_size

if monthly_income > 0:
    debt_to_income_ratio = total_debt / monthly_income
    monthly_debt_repayment_ratio = monthly_debt_repayment / monthly_income
    income_to_meb_ratio = monthly_income / household_meb_requirement
else:
    debt_to_income_ratio = 0
    monthly_debt_repayment_ratio = 0
    income_to_meb_ratio = 0

meb_gap = household_meb_requirement - monthly_income

context_col1, context_col2, context_col3 = st.columns(3)

with context_col1:
    st.metric("Market pressure score", round(market_pressure_score, 2))
    st.metric("Food basket price change", f"{round(basic_food_basket_change_1y, 1)}%")

with context_col2:
    st.metric("Household MEB requirement", f"{round(household_meb_requirement):,} MMK")
    st.metric("Income to MEB ratio", round(income_to_meb_ratio, 2))

with context_col3:
    st.metric("Coverage gap ratio", round(coverage_gap_ratio, 2))
    st.metric("Response gap", round(response_gap, 2))


st.divider()

predict_button = st.button("Predict Vulnerability Risk", type="primary")

if predict_button:
    input_data = {
        "state_region": state_region,
        "household_size": household_size,
        "female_headed_household": 1 if female_headed_household == "Yes" else 0,
        "disability_present": 1 if disability_present == "Yes" else 0,
        "displacement_status": displacement_status,
        "monthly_income": monthly_income,
        "has_debt": 1 if has_debt == "Yes" else 0,
        "total_debt": total_debt,
        "monthly_debt_repayment": monthly_debt_repayment,
        "savings_duration_weeks": savings_duration_weeks,
        "debt_to_income_ratio": debt_to_income_ratio,
        "monthly_debt_repayment_ratio": monthly_debt_repayment_ratio,
        "market_access": 1 if market_access == "Yes" else 0,
        "is_farming_household": 1 if is_farming_household == "Yes" else 0,
        "main_crop": main_crop,
        "farm_size_acres": farm_size_acres,
        "irrigation_access": 1 if irrigation_access == "Yes" else 0,
        "fertilizer_cost": fertilizer_cost,
        "crop_damage_recent": 1 if crop_damage_recent == "Yes" else 0,
        "rCSI_score": rCSI_score,
        "basic_needs_score": basic_needs_score,
        "basic_food_basket_change_1y": basic_food_basket_change_1y,
        "rice_price_change_1y": rice_price_change_1y,
        "fuel_price_change_1y": fuel_price_change_1y,
        "market_disruption_score": market_disruption_score,
        "market_pressure_score": market_pressure_score,
        "mpca_per_person": mpca_per_person,
        "household_meb_requirement": household_meb_requirement,
        "income_to_meb_ratio": income_to_meb_ratio,
        "meb_gap": meb_gap,
        "coverage_rate": coverage_rate,
        "coverage_gap_ratio": coverage_gap_ratio,
        "response_gap": response_gap,
        "number_of_partners_active": number_of_partners_active,
    }

    prediction_df = prepare_prediction_input(input_data)

    vulnerability_probability = model.predict_proba(prediction_df)[0, 1]
    predicted_class = model.predict(prediction_df)[0]

    risk_level = assign_risk_level(vulnerability_probability)

    recommendation = create_recommendation(
        risk_level=risk_level,
        market_access=input_data["market_access"],
        crop_damage_recent=input_data["crop_damage_recent"],
    )

    st.header("Prediction Result")

    result_col1, result_col2, result_col3 = st.columns(3)

    with result_col1:
        st.metric(
            "Vulnerability probability",
            f"{vulnerability_probability * 100:.1f}%",
        )

    with result_col2:
        st.metric(
            "Predicted class",
            "Vulnerable" if predicted_class == 1 else "Not vulnerable",
        )

    with result_col3:
        st.metric("Risk level", risk_level)

    if risk_level == "High risk":
        st.error(recommendation)
    elif risk_level == "Medium risk":
        st.warning(recommendation)
    else:
        st.success(recommendation)

    with st.expander("View model input data"):
        st.dataframe(prediction_df)