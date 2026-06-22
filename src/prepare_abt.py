import numpy as np
import pandas as pd

from config import RAW_DATA_DIR, PROCESSED_DATA_DIR


def load_raw_data() -> dict[str, pd.DataFrame]:
    """Load all raw CSV files into pandas DataFrames."""

    raw_files = {
        "households": "households_raw.csv",
        "agriculture": "agriculture_raw.csv",
        "coping": "coping_raw.csv",
        "market_prices": "market_prices_raw.csv",
        "meb_values": "meb_values_raw.csv",
        "assistance_coverage": "assistance_coverage_raw.csv",
    }

    data = {}

    for name, filename in raw_files.items():
        file_path = RAW_DATA_DIR / filename
        data[name] = pd.read_csv(file_path)

    return data


def clean_money_column(series: pd.Series) -> pd.Series:
    """Convert raw money values into numeric values."""

    cleaned = (
        series
        .astype("string")
        .str.replace("MMK", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
    )

    return pd.to_numeric(cleaned, errors="coerce")


def clean_yes_no_column(series: pd.Series) -> pd.Series:
    """Convert messy Yes/No values into 1/0."""

    cleaned = series.astype("string").str.strip().str.lower()

    mapping = {
        "yes": 1,
        "y": 1,
        "no": 0,
        "n": 0,
    }

    return cleaned.map(mapping)


def standardize_state_region(series: pd.Series) -> pd.Series:
    """Standardize inconsistent state/region names."""

    cleaned = series.astype("string").str.strip()

    mapping = {
        "sagaing": "Sagaing",
        "Magwe": "Magway",
        "Southern Shan": "Shan South",
        "Northern Shan": "Shan North",
    }

    return cleaned.replace(mapping)


def clean_basic_needs(series: pd.Series) -> pd.Series:
    """Convert basic needs coverage into an ordered numeric score."""

    cleaned = series.astype("string").str.strip().str.lower()

    mapping = {
        "yes fully": 3,
        "yes mostly": 2,
        "only some": 1,
        "no": 0,
    }

    return cleaned.map(mapping)


def clean_households(df: pd.DataFrame) -> pd.DataFrame:
    """Clean household raw table."""

    df = df.copy()

    df["state_region"] = standardize_state_region(df["state_region"])

    df["monthly_income"] = clean_money_column(df["monthly_income"])
    df["total_debt"] = clean_money_column(df["total_debt"])
    df["monthly_debt_repayment"] = clean_money_column(df["monthly_debt_repayment"])

    df["has_debt"] = clean_yes_no_column(df["has_debt"])
    df["market_access"] = clean_yes_no_column(df["market_access"])
    df["female_headed_household"] = clean_yes_no_column(df["female_headed_household"])
    df["disability_present"] = clean_yes_no_column(df["disability_present"])

    df["monthly_income"] = df["monthly_income"].fillna(df["monthly_income"].median())
    df["market_access"] = df["market_access"].fillna(0)

    return df


def clean_agriculture(df: pd.DataFrame) -> pd.DataFrame:
    """Clean agriculture raw table."""

    df = df.copy()

    df["fertilizer_cost"] = clean_money_column(df["fertilizer_cost"])

    df["is_farming_household"] = clean_yes_no_column(df["is_farming_household"])
    df["irrigation_access"] = clean_yes_no_column(df["irrigation_access"])
    df["crop_damage_recent"] = clean_yes_no_column(df["crop_damage_recent"])

    df["main_crop"] = df["main_crop"].fillna("None")
    df["fertilizer_cost"] = df["fertilizer_cost"].fillna(df["fertilizer_cost"].median())

    return df


def clean_coping(df: pd.DataFrame) -> pd.DataFrame:
    """Clean coping strategy raw table."""

    df = df.copy()

    coping_day_cols = [
        "less_preferred_food_days",
        "borrowed_food_days",
        "reduced_meals_days",
        "reduced_portion_days",
        "adults_reduced_for_children_days",
    ]

    for col in coping_day_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        df[col] = df[col].fillna(df[col].median())

    df["basic_needs_score"] = clean_basic_needs(df["basic_needs_met"])

    return df


def clean_market_prices(df: pd.DataFrame) -> pd.DataFrame:
    """Clean market prices raw table."""

    df = df.copy()

    df["state_region"] = standardize_state_region(df["state_region"])

    numeric_cols = [
        "basic_food_basket_change_1y",
        "rice_price_change_1y",
        "fuel_price_change_1y",
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    disruption_mapping = {
        "Low": 0,
        "Medium": 1,
        "High": 2,
    }

    df["market_disruption_score"] = df["market_disruption_level"].map(
        disruption_mapping
    )

    return df


def clean_meb_values(df: pd.DataFrame) -> pd.DataFrame:
    """Clean MEB values raw table."""

    df = df.copy()

    df["state_region"] = standardize_state_region(df["state_region"])
    df["mpca_per_person"] = clean_money_column(df["mpca_per_person"])
    df["cash_food_assistance_per_person"] = clean_money_column(
        df["cash_food_assistance_per_person"]
    )

    return df


def clean_assistance_coverage(df: pd.DataFrame) -> pd.DataFrame:
    """Clean assistance coverage raw table."""

    df = df.copy()

    df["state_region"] = standardize_state_region(df["state_region"])

    numeric_cols = [
        "people_targeted",
        "people_reached",
        "coverage_rate",
        "response_gap",
        "number_of_partners_active",
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def clean_raw_data(data: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    """Clean all raw source tables."""

    cleaned_data = {
        "households": clean_households(data["households"]),
        "agriculture": clean_agriculture(data["agriculture"]),
        "coping": clean_coping(data["coping"]),
        "market_prices": clean_market_prices(data["market_prices"]),
        "meb_values": clean_meb_values(data["meb_values"]),
        "assistance_coverage": clean_assistance_coverage(data["assistance_coverage"]),
    }

    return cleaned_data


def create_household_features(households: pd.DataFrame) -> pd.DataFrame:
    """Create household financial features."""

    df = households.copy()

    df["debt_to_income_ratio"] = df["total_debt"] / df["monthly_income"]
    df["monthly_debt_repayment_ratio"] = (
        df["monthly_debt_repayment"] / df["monthly_income"]
    )

    ratio_cols = [
        "debt_to_income_ratio",
        "monthly_debt_repayment_ratio",
    ]

    for col in ratio_cols:
        df[col] = df[col].replace([np.inf, -np.inf], np.nan)
        df[col] = df[col].fillna(0)

    return df


def create_coping_features(coping: pd.DataFrame) -> pd.DataFrame:
    """Create rCSI-style coping strategy score."""

    df = coping.copy()

    df["rCSI_score"] = (
        df["less_preferred_food_days"] * 1
        + df["borrowed_food_days"] * 2
        + df["reduced_meals_days"] * 1
        + df["reduced_portion_days"] * 1
        + df["adults_reduced_for_children_days"] * 3
    )

    return df


def create_market_features(market_prices: pd.DataFrame) -> pd.DataFrame:
    """Create market pressure score."""

    df = market_prices.copy()

    df["market_pressure_score"] = (
        df["basic_food_basket_change_1y"]
        + df["rice_price_change_1y"]
        + df["fuel_price_change_1y"]
        + (df["market_disruption_score"] * 10)
    )

    return df


def create_assistance_features(assistance_coverage: pd.DataFrame) -> pd.DataFrame:
    """Create assistance coverage gap feature."""

    df = assistance_coverage.copy()

    df["coverage_gap_ratio"] = 1 - df["coverage_rate"]

    return df


def merge_abt(
    households_features: pd.DataFrame,
    agriculture: pd.DataFrame,
    coping_features: pd.DataFrame,
    market_features: pd.DataFrame,
    meb_values: pd.DataFrame,
    assistance_features: pd.DataFrame,
) -> pd.DataFrame:
    """Merge household-level and state-level tables into one ABT."""

    abt = households_features.merge(
        agriculture,
        on="household_id",
        how="left",
    )

    abt = abt.merge(
        coping_features,
        on="household_id",
        how="left",
    )

    abt = abt.merge(
        market_features,
        on="state_region",
        how="left",
    )

    abt = abt.merge(
        meb_values,
        on="state_region",
        how="left",
    )

    abt = abt.merge(
        assistance_features,
        on="state_region",
        how="left",
    )

    return abt


def create_meb_features(abt: pd.DataFrame) -> pd.DataFrame:
    """Create MEB-related household features."""

    df = abt.copy()

    df["household_meb_requirement"] = (
        df["household_size"] * df["mpca_per_person"]
    )

    df["income_to_meb_ratio"] = (
        df["monthly_income"] / df["household_meb_requirement"]
    )

    df["meb_gap"] = (
        df["monthly_income"] - df["household_meb_requirement"]
    )

    return df


def create_target_feature(abt: pd.DataFrame) -> pd.DataFrame:
    """Create proxy target feature for financial vulnerability."""

    df = abt.copy()

    df["low_income_flag"] = (df["income_to_meb_ratio"] < 1).astype(int)
    df["high_debt_flag"] = (df["debt_to_income_ratio"] > 1).astype(int)

    df["high_repayment_pressure_flag"] = (
        df["monthly_debt_repayment_ratio"] > 0.20
    ).astype(int)

    df["high_rcsi_flag"] = (df["rCSI_score"] >= 20).astype(int)
    df["poor_basic_needs_flag"] = (df["basic_needs_score"] <= 1).astype(int)
    df["no_market_access_flag"] = (df["market_access"] == 0).astype(int)
    df["crop_damage_flag"] = (df["crop_damage_recent"] == 1).astype(int)

    df["high_market_pressure_flag"] = (
        df["market_pressure_score"] >= df["market_pressure_score"].median()
    ).astype(int)

    vulnerability_flags = [
        "low_income_flag",
        "high_debt_flag",
        "high_repayment_pressure_flag",
        "high_rcsi_flag",
        "poor_basic_needs_flag",
        "no_market_access_flag",
        "crop_damage_flag",
        "high_market_pressure_flag",
    ]

    df["vulnerability_score"] = df[vulnerability_flags].sum(axis=1)
    df["financial_vulnerability"] = (df["vulnerability_score"] >= 3).astype(int)

    return df


def select_final_columns(abt: pd.DataFrame) -> pd.DataFrame:
    """Select final columns for modeling."""

    final_columns = [
        "household_id",
        "state_region",
        "township",
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
        "less_preferred_food_days",
        "borrowed_food_days",
        "reduced_meals_days",
        "reduced_portion_days",
        "adults_reduced_for_children_days",
        "rCSI_score",
        "basic_needs_score",
        "basic_food_basket_change_1y",
        "rice_price_change_1y",
        "fuel_price_change_1y",
        "market_disruption_score",
        "market_pressure_score",
        "mpca_per_person",
        "cash_food_assistance_per_person",
        "household_meb_requirement",
        "income_to_meb_ratio",
        "meb_gap",
        "coverage_rate",
        "coverage_gap_ratio",
        "response_gap",
        "number_of_partners_active",
        "vulnerability_score",
        "financial_vulnerability",
    ]

    return abt[final_columns].copy()


def build_abt() -> pd.DataFrame:
    """Build the final Analytical Base Table."""

    raw_data = load_raw_data()
    cleaned_data = clean_raw_data(raw_data)

    households_features = create_household_features(cleaned_data["households"])
    coping_features = create_coping_features(cleaned_data["coping"])
    market_features = create_market_features(cleaned_data["market_prices"])
    assistance_features = create_assistance_features(
        cleaned_data["assistance_coverage"]
    )

    abt = merge_abt(
        households_features=households_features,
        agriculture=cleaned_data["agriculture"],
        coping_features=coping_features,
        market_features=market_features,
        meb_values=cleaned_data["meb_values"],
        assistance_features=assistance_features,
    )

    abt = create_meb_features(abt)
    abt = create_target_feature(abt)
    final_abt = select_final_columns(abt)

    return final_abt


def validate_abt(final_abt: pd.DataFrame) -> None:
    """Print validation checks for the final ABT."""

    print("Final ABT validation")
    print("=" * 60)
    print(f"Rows: {final_abt.shape[0]}")
    print(f"Columns: {final_abt.shape[1]}")
    print(f"Unique household IDs: {final_abt['household_id'].nunique()}")
    print(f"Duplicate household IDs: {final_abt['household_id'].duplicated().sum()}")
    print(f"Missing values: {final_abt.isna().sum().sum()}")
    print("\nTarget distribution:")
    print(final_abt["financial_vulnerability"].value_counts().sort_index())


def main() -> None:
    """Run the full ABT preparation pipeline."""

    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    final_abt = build_abt()

    output_path = PROCESSED_DATA_DIR / "farmer_vulnerability_abt.csv"
    final_abt.to_csv(output_path, index=False)

    validate_abt(final_abt)

    print("\nABT saved successfully.")
    print(f"Saved to: {output_path}")


if __name__ == "__main__":
    main()