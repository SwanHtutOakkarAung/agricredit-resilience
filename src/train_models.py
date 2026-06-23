from pathlib import Path

import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier


PROJECT_ROOT = Path(__file__).resolve().parents[1]

PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"
MODELS_DIR = PROJECT_ROOT / "models"

ABT_PATH = PROCESSED_DATA_DIR / "farmer_vulnerability_abt.csv"

DECISION_TREE_MODEL_PATH = MODELS_DIR / "decision_tree_model.joblib"
LOGISTIC_REGRESSION_MODEL_PATH = MODELS_DIR / "logistic_regression_model.joblib"


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


CATEGORICAL_FEATURES = [
    "state_region",
    "displacement_status",
    "main_crop",
]

NUMERIC_FEATURES = [
    col for col in FEATURE_COLUMNS
    if col not in CATEGORICAL_FEATURES
]


def load_abt() -> pd.DataFrame:
    """Load the final analytical base table."""

    return pd.read_csv(ABT_PATH)


def split_features_target(abt: pd.DataFrame):
    """Split the ABT into features and target."""

    X = abt[FEATURE_COLUMNS].copy()
    y = abt[TARGET_COLUMN]

    return train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )


def build_decision_tree_pipeline() -> Pipeline:
    """Build the Decision Tree pipeline."""

    preprocessor = ColumnTransformer(
        transformers=[
            ("categorical", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES),
            ("numeric", "passthrough", NUMERIC_FEATURES),
        ]
    )

    decision_tree_model = DecisionTreeClassifier(
        max_depth=4,
        min_samples_leaf=30,
        random_state=42,
    )

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", decision_tree_model),
        ]
    )

    return pipeline


def build_logistic_regression_pipeline() -> Pipeline:
    """Build the Logistic Regression pipeline."""

    preprocessor = ColumnTransformer(
        transformers=[
            ("categorical", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES),
            ("numeric", StandardScaler(), NUMERIC_FEATURES),
        ]
    )

    logistic_regression_model = LogisticRegression(
        max_iter=1000,
        class_weight="balanced",
        random_state=42,
    )

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", logistic_regression_model),
        ]
    )

    return pipeline


def evaluate_model(model_name: str, model: Pipeline, X_test: pd.DataFrame, y_test: pd.Series) -> dict:
    """Evaluate a trained model."""

    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    return {
        "model_name": model_name,
        "accuracy": round(accuracy_score(y_test, y_pred), 4),
        "precision": round(precision_score(y_test, y_pred), 4),
        "recall": round(recall_score(y_test, y_pred), 4),
        "f1_score": round(f1_score(y_test, y_pred), 4),
        "roc_auc": round(roc_auc_score(y_test, y_proba), 4),
    }


def main() -> None:
    """Train and save both machine learning models."""

    print("Loading final ABT...")
    abt = load_abt()

    print(f"ABT shape: {abt.shape}")

    X_train, X_test, y_train, y_test = split_features_target(abt)

    print(f"Training rows: {X_train.shape[0]}")
    print(f"Testing rows: {X_test.shape[0]}")

    print("\nTraining Decision Tree model...")
    decision_tree_pipeline = build_decision_tree_pipeline()
    decision_tree_pipeline.fit(X_train, y_train)

    print("Training Logistic Regression model...")
    logistic_regression_pipeline = build_logistic_regression_pipeline()
    logistic_regression_pipeline.fit(X_train, y_train)

    print("\nEvaluation results:")
    results = [
        evaluate_model("Decision Tree", decision_tree_pipeline, X_test, y_test),
        evaluate_model("Logistic Regression", logistic_regression_pipeline, X_test, y_test),
    ]

    results_df = pd.DataFrame(results)
    print(results_df)

    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    joblib.dump(decision_tree_pipeline, DECISION_TREE_MODEL_PATH)
    joblib.dump(logistic_regression_pipeline, LOGISTIC_REGRESSION_MODEL_PATH)

    print("\nModels saved successfully.")
    print(f"Decision Tree model saved to: {DECISION_TREE_MODEL_PATH}")
    print(f"Logistic Regression model saved to: {LOGISTIC_REGRESSION_MODEL_PATH}")


if __name__ == "__main__":
    main()