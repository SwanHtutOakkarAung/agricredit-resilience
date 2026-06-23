import sys
from pathlib import Path

import pandas as pd
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from src.app_utils import load_abt  # noqa: E402


st.set_page_config(
    page_title="Market Feasibility",
    page_icon="🛒",
    layout="wide",
)


st.title("🛒 Market Feasibility")
st.subheader("Connecting Financial Vulnerability With Market Conditions")

st.markdown(
    """
This page helps explain why financial vulnerability prediction should not be used alone.

A household may be financially vulnerable, but the responsible response depends on local market conditions.
If markets are functioning, cash or livelihood support may be useful. If markets are highly disrupted,
a normal loan may increase household burden.
"""
)

st.divider()


@st.cache_data
def get_abt():
    return load_abt()


abt = get_abt()


market_columns = [
    "state_region",
    "basic_food_basket_change_1y",
    "rice_price_change_1y",
    "fuel_price_change_1y",
    "market_disruption_score",
    "market_pressure_score",
    "coverage_rate",
    "coverage_gap_ratio",
    "response_gap",
    "number_of_partners_active",
]


market_df = (
    abt[market_columns]
    .drop_duplicates(subset=["state_region"])
    .sort_values("state_region")
    .reset_index(drop=True)
)


def classify_market_condition(market_pressure_score: float) -> str:
    """Classify market condition from market pressure score."""

    if market_pressure_score < 55:
        return "Green - More feasible"

    if market_pressure_score < 80:
        return "Yellow - Caution needed"

    return "Red - High pressure"


def create_market_recommendation(condition: str) -> str:
    """Create a decision-support recommendation based on market condition."""

    if condition.startswith("Green"):
        return (
            "Market conditions appear more feasible. Cash-based support or carefully reviewed "
            "livelihood finance may be possible, but household repayment capacity still needs review."
        )

    if condition.startswith("Yellow"):
        return (
            "Market conditions show some pressure. Loan decisions should be cautious. "
            "Smaller loan sizes, flexible repayment, or mixed assistance may be safer."
        )

    return (
        "Market conditions show high pressure. A normal loan may increase financial burden. "
        "Manual review, livelihood support, or assistance-first options are recommended."
    )


market_df["market_condition"] = market_df["market_pressure_score"].apply(
    classify_market_condition
)

market_df["recommendation"] = market_df["market_condition"].apply(
    create_market_recommendation
)


st.header("State/Region Market Overview")

selected_state = st.selectbox(
    "Select State/Region",
    options=market_df["state_region"].tolist(),
)

selected_market = market_df[market_df["state_region"] == selected_state].iloc[0]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Market pressure score",
        round(float(selected_market["market_pressure_score"]), 2),
    )

    st.metric(
        "Market disruption score",
        round(float(selected_market["market_disruption_score"]), 2),
    )

with col2:
    st.metric(
        "Food basket price change",
        f"{round(float(selected_market['basic_food_basket_change_1y']), 1)}%",
    )

    st.metric(
        "Rice price change",
        f"{round(float(selected_market['rice_price_change_1y']), 1)}%",
    )

with col3:
    st.metric(
        "Fuel price change",
        f"{round(float(selected_market['fuel_price_change_1y']), 1)}%",
    )

    st.metric(
        "Coverage gap ratio",
        round(float(selected_market["coverage_gap_ratio"]), 2),
    )


condition = selected_market["market_condition"]
recommendation = selected_market["recommendation"]

st.subheader("Market Condition Classification")

if condition.startswith("Green"):
    st.success(condition)
elif condition.startswith("Yellow"):
    st.warning(condition)
else:
    st.error(condition)

st.markdown(recommendation)

st.divider()


st.header("How to Interpret Market Feasibility")

st.markdown(
    """
The market condition classification is a simple decision-support layer.

It does not replace the vulnerability model. Instead, it adds context.

A responsible decision should consider both:

1. **Household vulnerability**  
   Is the household financially vulnerable?

2. **Market feasibility**  
   Is the local market stable enough for cash, livelihood finance, or loan repayment?
"""
)

st.info(
    """
Example: If a household is high-risk and the market condition is red, the safest response may be
manual review, grant support, food/cash assistance, or livelihood support before offering a normal loan.
"""
)

st.divider()


st.header("Market Comparison Table")

display_df = market_df[
    [
        "state_region",
        "market_pressure_score",
        "market_disruption_score",
        "basic_food_basket_change_1y",
        "rice_price_change_1y",
        "fuel_price_change_1y",
        "coverage_gap_ratio",
        "response_gap",
        "number_of_partners_active",
        "market_condition",
    ]
].copy()

st.dataframe(display_df, use_container_width=True)

st.divider()


st.header("Market Pressure Ranking")

ranking_df = market_df[
    ["state_region", "market_pressure_score"]
].sort_values(
    by="market_pressure_score",
    ascending=False,
)

st.bar_chart(
    ranking_df.set_index("state_region")["market_pressure_score"]
)


st.markdown(
    """
Higher market pressure means the area may face more difficulty related to food prices,
fuel prices, disruption, or market access. In these areas, financial products should be
used more carefully.
"""
)

st.warning(
    """
This page is a prototype market feasibility layer. It supports responsible thinking,
but final decisions should still include local field knowledge and human review.
"""
)