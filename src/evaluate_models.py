from pathlib import Path

import joblib
import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
)
from sklearn.model_selection import train_test_split


PROJECT_ROOT = Path(__file__).resolve().parents[1]

PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"
MODELS_DIR = PROJECT_ROOT / "models"
REPORTS_DIR = PROJECT_ROOT / "reports"

ABT_PATH = PROCESSED_DATA_DIR / "farmer_vulnerability_abt.csv"

DECISION_TREE_MODEL_PATH = MODELS_DIR / "decision_tree_model.joblib"
LOGISTIC_REGRESSION_MODEL_PATH = MODELS_DIR / "logistic_regression_model.joblib"

MODEL_COMPARISON_SUMMARY_PATH = REPORTS_DIR / "model_comparison_summary.csv"


TARGET_COLUMN = "financial_vulnerability"

FEATURE_COLUMNS = [
    # Location/context
    "state_region",

    # Household characteristics
    "household_size",
    "female_headed_household",
    "disability_present",
    "displacement_status",

    # Financial features
    "monthly_income",
    "has_debt",
    "total_debt",
    "monthly_debt_repayment",
    "savings_duration_weeks",
    "debt_to_income_ratio",
    "monthly_debt_repayment_ratio",

    # Market access
    "market_access",

    # Agriculture features
    "is_farming_household",
    "main_crop",
    "farm_size_acres",
    "irrigation_access",
    "fertilizer_cost",
    "crop_damage_recent",

    # Coping and basic needs
    "rCSI_score",
    "basic_needs_score",

    # Market context
    "basic_food_basket_change_1y",
    "rice_price_change_1y",
    "fuel_price_change_1y",
    "market_disruption_score",
    "market_pressure_score",

    # MEB features
    "mpca_per_person",
    "household_meb_requirement",
    "income_to_meb_ratio",
    "meb_gap",

    # Assistance coverage
    "coverage_rate",
    "coverage_gap_ratio",
    "response_gap",
    "number_of_partners_active",
]


def load_abt() -> pd.DataFrame:
    """Load the final analytical base table."""

    return pd.read_csv(ABT_PATH)


def load_models():
    """Load the saved Decision Tree and Logistic Regression models."""

    decision_tree_model = joblib.load(DECISION_TREE_MODEL_PATH)
    logistic_regression_model = joblib.load(LOGISTIC_REGRESSION_MODEL_PATH)

    return decision_tree_model, logistic_regression_model


def create_test_set(abt: pd.DataFrame):
    """Create the same train/test split used during model training."""

    X = abt[FEATURE_COLUMNS].copy()
    y = abt[TARGET_COLUMN]

    _, X_test, _, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    return X_test, y_test


def evaluate_model(model_name: str, model, X_test: pd.DataFrame, y_test: pd.Series) -> dict:
    """Evaluate a saved model and return model metrics."""

    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    cm = confusion_matrix(y_test, y_pred)

    return {
        "model_name": model_name,
        "accuracy": round(accuracy_score(y_test, y_pred), 4),
        "precision": round(precision_score(y_test, y_pred), 4),
        "recall": round(recall_score(y_test, y_pred), 4),
        "f1_score": round(f1_score(y_test, y_pred), 4),
        "roc_auc": round(roc_auc_score(y_test, y_proba), 4),
        "true_negative": int(cm[0, 0]),
        "false_positive": int(cm[0, 1]),
        "false_negative": int(cm[1, 0]),
        "true_positive": int(cm[1, 1]),
    }


def add_recommended_use(summary_df: pd.DataFrame) -> pd.DataFrame:
    """Add recommended use for each model."""

    recommended_use = {
        "Decision Tree": "Explainable rule-based support model",
        "Logistic Regression": "Main probability-based prediction model",
    }

    summary_df = summary_df.copy()
    summary_df["recommended_use"] = summary_df["model_name"].map(recommended_use)

    return summary_df


def main() -> None:
    """Evaluate saved models and save model comparison summary."""

    print("Loading final ABT...")
    abt = load_abt()

    print(f"ABT shape: {abt.shape}")

    print("\nLoading saved models...")
    decision_tree_model, logistic_regression_model = load_models()

    print("Models loaded successfully.")

    print("\nCreating test set...")
    X_test, y_test = create_test_set(abt)

    print(f"Testing rows: {X_test.shape[0]}")
    print("Testing target distribution:")
    print(y_test.value_counts().sort_index())

    print("\nEvaluating models...")

    evaluation_results = [
        evaluate_model(
            model_name="Decision Tree",
            model=decision_tree_model,
            X_test=X_test,
            y_test=y_test,
        ),
        evaluate_model(
            model_name="Logistic Regression",
            model=logistic_regression_model,
            X_test=X_test,
            y_test=y_test,
        ),
    ]

    summary_df = pd.DataFrame(evaluation_results)
    summary_df = add_recommended_use(summary_df)

    print("\nModel comparison summary:")
    print(summary_df)

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    summary_df.to_csv(MODEL_COMPARISON_SUMMARY_PATH, index=False)

    print("\nModel comparison summary saved successfully.")
    print(f"Saved to: {MODEL_COMPARISON_SUMMARY_PATH}")


if __name__ == "__main__":
    main()