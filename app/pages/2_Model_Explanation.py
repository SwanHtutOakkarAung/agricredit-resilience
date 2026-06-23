import sys
from pathlib import Path

import pandas as pd
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from src.app_utils import (  # noqa: E402
    FEATURE_COLUMNS,
    load_abt,
    load_decision_tree_model,
    load_logistic_regression_model,
)


st.set_page_config(
    page_title="Model Explanation",
    page_icon="🌳",
    layout="wide",
)


st.title("🌳 Model Explanation")
st.subheader("Understanding How the Models Support Decisions")

st.markdown(
    """
This page explains the two machine learning models used in the AgriCredit Resilience project.

The dashboard uses:

- **Logistic Regression** as the main prediction model
- **Decision Tree** as the supporting explanation model

The goal is not only to make predictions, but also to make the prediction logic easier to understand.
"""
)

st.divider()


@st.cache_data
def get_abt():
    return load_abt()


@st.cache_resource
def get_decision_tree_model():
    return load_decision_tree_model()


@st.cache_resource
def get_logistic_regression_model():
    return load_logistic_regression_model()


abt = get_abt()
decision_tree_pipeline = get_decision_tree_model()
logistic_regression_pipeline = get_logistic_regression_model()


st.header("Model Roles")

col1, col2 = st.columns(2)

with col1:
    st.info(
        """
### Main Model: Logistic Regression

Logistic Regression is used as the main model because it performed better during evaluation.

It gives a **vulnerability probability**, such as 72%, 35%, or 91%.

This is useful because households can be ranked by risk level instead of only receiving a yes/no result.
"""
    )

with col2:
    st.success(
        """
### Support Model: Decision Tree

The Decision Tree is used as an explanation support model.

It creates simple if-then decision rules.

This makes it easier to explain model behavior to non-technical users.
"""
    )

st.divider()


st.header("Decision Tree Feature Importance")

st.markdown(
    """
Feature importance shows which variables the Decision Tree used most when splitting households
into vulnerable and not vulnerable groups.
"""
)

dt_preprocessor = decision_tree_pipeline.named_steps["preprocessor"]
dt_model = decision_tree_pipeline.named_steps["model"]

dt_feature_names = dt_preprocessor.get_feature_names_out()
dt_importances = dt_model.feature_importances_

dt_importance_df = pd.DataFrame(
    {
        "feature": dt_feature_names,
        "importance": dt_importances,
    }
)

dt_importance_df = dt_importance_df.sort_values(
    by="importance",
    ascending=False,
)

dt_importance_df = dt_importance_df[dt_importance_df["importance"] > 0]

top_dt_features = dt_importance_df.head(10).copy()

top_dt_features["feature"] = (
    top_dt_features["feature"]
    .str.replace("numeric__", "", regex=False)
    .str.replace("categorical__", "", regex=False)
)

st.dataframe(top_dt_features, use_container_width=True)

st.bar_chart(
    top_dt_features.set_index("feature")["importance"]
)

st.markdown(
    """
In this project, the Decision Tree mainly focuses on financial stress, coping behavior,
crop damage, and market pressure.

This matches the project logic because financial vulnerability is expected to be affected by
debt burden, food coping, agricultural shocks, and market conditions.
"""
)

st.divider()


st.header("Logistic Regression Coefficients")

st.markdown(
    """
Logistic Regression uses coefficients to show how each feature is associated with vulnerability.

A **positive coefficient** means the feature increases the probability of being vulnerable.

A **negative coefficient** means the feature decreases the probability of being vulnerable.
"""
)

lr_preprocessor = logistic_regression_pipeline.named_steps["preprocessor"]
lr_model = logistic_regression_pipeline.named_steps["model"]

lr_feature_names = lr_preprocessor.get_feature_names_out()
lr_coefficients = lr_model.coef_[0]

lr_coef_df = pd.DataFrame(
    {
        "feature": lr_feature_names,
        "coefficient": lr_coefficients,
    }
)

lr_coef_df["absolute_coefficient"] = lr_coef_df["coefficient"].abs()

lr_coef_df = lr_coef_df.sort_values(
    by="absolute_coefficient",
    ascending=False,
)

lr_coef_df["feature"] = (
    lr_coef_df["feature"]
    .str.replace("numeric__", "", regex=False)
    .str.replace("categorical__", "", regex=False)
)

top_positive = lr_coef_df.sort_values(
    by="coefficient",
    ascending=False,
).head(10)

top_negative = lr_coef_df.sort_values(
    by="coefficient",
    ascending=True,
).head(10)

coef_col1, coef_col2 = st.columns(2)

with coef_col1:
    st.subheader("Top Features Increasing Vulnerability")
    st.dataframe(
        top_positive[["feature", "coefficient"]],
        use_container_width=True,
    )

with coef_col2:
    st.subheader("Top Features Decreasing Vulnerability")
    st.dataframe(
        top_negative[["feature", "coefficient"]],
        use_container_width=True,
    )

st.markdown(
    """
The coefficient results should be interpreted carefully.

Some features can look surprising because Logistic Regression considers all variables together.
For example, debt-related features may overlap with each other, so one coefficient should not
be interpreted alone without considering the full model context.
"""
)

st.divider()


st.header("Plain-Language Explanation")

st.markdown(
    """
The model is mainly trying to identify households that show signs of financial pressure.

Important warning signs include:

- high debt compared with income
- high monthly repayment burden
- frequent food coping behavior
- recent crop damage
- high market pressure
- weak ability to meet basic needs
- limited market access

A high-risk result does not mean a household should be rejected automatically.
It means the household should receive careful review before any loan decision.
"""
)

st.warning(
    """
This system is explainable decision support, not automatic decision-making.
Human review is still required, especially when the prediction may affect household access
to credit or assistance.
"""
)