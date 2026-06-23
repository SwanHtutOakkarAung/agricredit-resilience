from pathlib import Path

import joblib
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
MODELS_DIR = PROJECT_ROOT / "models"
REPORTS_DIR = PROJECT_ROOT / "reports"

ABT_PATH = PROCESSED_DATA_DIR / "farmer_vulnerability_abt.csv"
DECISION_TREE_MODEL_PATH = MODELS_DIR / "decision_tree_model.joblib"
LOGISTIC_REGRESSION_MODEL_PATH = MODELS_DIR / "logistic_regression_model.joblib"
MODEL_COMPARISON_SUMMARY_PATH = REPORTS_DIR / "model_comparison_summary.csv"


FEATURE_COLUMNS = [
    "state_region",
    "household_size",
    "female_headed_household",
    "disability_present",
    "displacement_status",
    "monthly_income",
    "has_debt",
    "total_debt",
    "monthly_debt_repayment",
    "savings_duration_weeks",
    "debt_to_income_ratio",
    "monthly_debt_repayment_ratio",
    "market_access",
    "is_farming_household",
    "main_crop",
    "farm_size_acres",
    "irrigation_access",
    "fertilizer_cost",
    "crop_damage_recent",
    "rCSI_score",
    "basic_needs_score",
    "basic_food_basket_change_1y",
    "rice_price_change_1y",
    "fuel_price_change_1y",
    "market_disruption_score",
    "market_pressure_score",
    "mpca_per_person",
    "household_meb_requirement",
    "income_to_meb_ratio",
    "meb_gap",
    "coverage_rate",
    "coverage_gap_ratio",
    "response_gap",
    "number_of_partners_active",
]


def load_abt() -> pd.DataFrame:
    """Load the final analytical base table."""

    return pd.read_csv(ABT_PATH)


def load_model_comparison_summary() -> pd.DataFrame:
    """Load the model comparison summary report."""

    return pd.read_csv(MODEL_COMPARISON_SUMMARY_PATH)


def load_decision_tree_model():
    """Load the saved Decision Tree model."""

    return joblib.load(DECISION_TREE_MODEL_PATH)


def load_logistic_regression_model():
    """Load the saved Logistic Regression model."""

    return joblib.load(LOGISTIC_REGRESSION_MODEL_PATH)


def assign_risk_level(probability: float) -> str:
    """Assign a risk level based on vulnerability probability."""

    if probability < 0.40:
        return "Low risk"

    if probability < 0.70:
        return "Medium risk"

    return "High risk"


def create_recommendation(risk_level: str, market_access: int, crop_damage_recent: int) -> str:
    """Create a responsible decision-support recommendation."""

    if risk_level == "High risk":
        if market_access == 0 or crop_damage_recent == 1:
            return (
                "High vulnerability detected. A normal loan should not be approved automatically. "
                "Manual review is recommended, and livelihood support or cash assistance may be safer first."
            )

        return (
            "High vulnerability detected. Manual review is recommended before any loan decision. "
            "Support options should be considered together with repayment capacity."
        )

    if risk_level == "Medium risk":
        return (
            "Medium vulnerability detected. The household may need careful review. "
            "A smaller loan, flexible repayment plan, or combined support may be more responsible."
        )

    return (
        "Low vulnerability detected. The household appears more financially stable, "
        "but the final decision should still consider local context and manual review."
    )


def prepare_prediction_input(input_data: dict) -> pd.DataFrame:
    """Convert dashboard input dictionary into a model-ready DataFrame."""

    prediction_df = pd.DataFrame([input_data])

    prediction_df = prediction_df[FEATURE_COLUMNS]

    return prediction_df