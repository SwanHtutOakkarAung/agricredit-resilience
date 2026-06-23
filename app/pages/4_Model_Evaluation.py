import sys
from pathlib import Path

import pandas as pd
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from src.app_utils import load_model_comparison_summary  # noqa: E402


st.set_page_config(
    page_title="Model Evaluation",
    page_icon="📈",
    layout="wide",
)


st.title("📈 Model Evaluation")
st.subheader("Comparing Decision Tree and Logistic Regression")

st.markdown(
    """
This page summarizes the final model evaluation results.

The project compares two models:

- **Decision Tree**
- **Logistic Regression**

The goal is to choose the best main model for financial vulnerability prediction while keeping the system explainable.
"""
)

st.divider()


@st.cache_data
def get_model_summary() -> pd.DataFrame:
    return load_model_comparison_summary()


summary_df = get_model_summary()

st.header("Model Comparison Summary")

st.dataframe(summary_df, use_container_width=True)

st.divider()


st.header("Performance Metrics")

metric_columns = [
    "accuracy",
    "precision",
    "recall",
    "f1_score",
    "roc_auc",
]

performance_df = summary_df[["model_name"] + metric_columns].copy()

st.dataframe(performance_df, use_container_width=True)

chart_df = performance_df.set_index("model_name")

st.bar_chart(chart_df)

st.markdown(
    """
Higher values are better for these metrics.

In this project, Logistic Regression performs better than the Decision Tree across all major evaluation metrics.
"""
)

st.divider()


st.header("False Negative Comparison")

st.markdown(
    """
A false negative means the model predicts a household as **not vulnerable** when the household is actually vulnerable.

For this project, false negatives are especially important because missing vulnerable households may prevent them from receiving careful review or support.
"""
)

false_negative_df = summary_df[["model_name", "false_negative"]].copy()

st.dataframe(false_negative_df, use_container_width=True)

st.bar_chart(false_negative_df.set_index("model_name")["false_negative"])

best_false_negative_model = false_negative_df.sort_values(
    by="false_negative",
    ascending=True,
).iloc[0]

st.success(
    f"""
{best_false_negative_model["model_name"]} has fewer false negatives
({int(best_false_negative_model["false_negative"])}), so it misses fewer truly vulnerable households.
"""
)

st.divider()


st.header("Confusion Matrix Values")

st.markdown(
    """
The confusion matrix helps show how many predictions were correct or incorrect.

- **True Negative**: correctly predicted not vulnerable
- **False Positive**: predicted vulnerable, but actually not vulnerable
- **False Negative**: predicted not vulnerable, but actually vulnerable
- **True Positive**: correctly predicted vulnerable
"""
)

confusion_df = summary_df[
    [
        "model_name",
        "true_negative",
        "false_positive",
        "false_negative",
        "true_positive",
    ]
].copy()

st.dataframe(confusion_df, use_container_width=True)

col1, col2 = st.columns(2)

for index, row in confusion_df.iterrows():
    with col1 if index == 0 else col2:
        st.subheader(row["model_name"])
        st.metric("True Negative", int(row["true_negative"]))
        st.metric("False Positive", int(row["false_positive"]))
        st.metric("False Negative", int(row["false_negative"]))
        st.metric("True Positive", int(row["true_positive"]))

st.divider()


st.header("Final Model Recommendation")

logistic_row = summary_df[summary_df["model_name"] == "Logistic Regression"].iloc[0]
decision_tree_row = summary_df[summary_df["model_name"] == "Decision Tree"].iloc[0]

st.success(
    """
Logistic Regression is recommended as the main prediction model for the AgriCredit Resilience dashboard.
"""
)

rec_col1, rec_col2 = st.columns(2)

with rec_col1:
    st.subheader("Why Logistic Regression?")
    st.markdown(
        f"""
- Accuracy: **{logistic_row["accuracy"]}**
- Precision: **{logistic_row["precision"]}**
- Recall: **{logistic_row["recall"]}**
- F1-score: **{logistic_row["f1_score"]}**
- ROC-AUC: **{logistic_row["roc_auc"]}**
- False negatives: **{int(logistic_row["false_negative"])}**

It also produces vulnerability probability scores, which are useful for ranking households into low, medium, and high risk.
"""
    )

with rec_col2:
    st.subheader("Why Keep Decision Tree?")
    st.markdown(
        f"""
- Accuracy: **{decision_tree_row["accuracy"]}**
- Recall: **{decision_tree_row["recall"]}**
- ROC-AUC: **{decision_tree_row["roc_auc"]}**
- False negatives: **{int(decision_tree_row["false_negative"])}**

The Decision Tree is useful as a supporting model because its rules are easier to explain to non-technical users.
"""
    )

st.warning(
    """
Final recommendation: use Logistic Regression as the main probability-based prediction model,
and use Decision Tree as the supporting rule-based explanation model.
"""
)