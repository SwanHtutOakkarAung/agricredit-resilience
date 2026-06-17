import numpy as np
import pandas as pd

from config import RAW_DATA_DIR, RANDOM_SEED, N_HOUSEHOLDS


def ensure_raw_data_dir() -> None:
    """Create raw data folder if it does not exist."""
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)


def generate_households_raw(rng: np.random.Generator) -> pd.DataFrame:
    """Generate raw household finance and demographic data."""

    states = [
        "Sagaing", "Magway", "Mandalay", "Chin", "Kachin",
        "Kayah", "Kayin", "Rakhine", "Shan South", "Shan North",
        "Ayeyarwady", "Bago", "Mon", "Tanintharyi"
    ]

    townships_by_state = {
        "Sagaing": ["Monywa", "Shwebo", "Kalay"],
        "Magway": ["Pakokku", "Magway", "Minbu"],
        "Mandalay": ["Mandalay", "Kyaukse", "Myingyan"],
        "Chin": ["Hakha", "Tedim", "Matupi"],
        "Kachin": ["Myitkyina", "Bhamo", "Putao"],
        "Kayah": ["Loikaw", "Demoso", "Hpruso"],
        "Kayin": ["Hpa-An", "Myawaddy", "Kawkareik"],
        "Rakhine": ["Sittwe", "Mrauk-U", "Kyaukphyu"],
        "Shan South": ["Taunggyi", "Pekon", "Hopong"],
        "Shan North": ["Lashio", "Muse", "Laukkaing"],
        "Ayeyarwady": ["Pathein", "Hinthada", "Myaungmya"],
        "Bago": ["Bago", "Pyay", "Taungoo"],
        "Mon": ["Mawlamyine", "Thaton", "Ye"],
        "Tanintharyi": ["Dawei", "Myeik", "Kawthaung"],
    }

    household_ids = [f"HH{str(i).zfill(5)}" for i in range(1, N_HOUSEHOLDS + 1)]

    state_region = rng.choice(states, size=N_HOUSEHOLDS)

    township = [
        rng.choice(townships_by_state[state])
        for state in state_region
    ]

    household_size = rng.choice(
        [1, 2, 3, 4, 5, 6, 7, 8, 9],
        size=N_HOUSEHOLDS,
        p=[0.04, 0.08, 0.14, 0.20, 0.20, 0.16, 0.10, 0.05, 0.03]
    )

    monthly_income = rng.normal(loc=420_000, scale=180_000, size=N_HOUSEHOLDS)
    monthly_income = np.clip(monthly_income, 50_000, 1_500_000).round(0)

    has_debt = rng.choice(["Yes", "No", "Y", "N", "yes", "no"], size=N_HOUSEHOLDS,
                          p=[0.32, 0.18, 0.20, 0.10, 0.12, 0.08])

    total_debt = []
    monthly_debt_repayment = []

    for debt_status in has_debt:
        if str(debt_status).lower() in ["yes", "y"]:
            debt = rng.normal(loc=650_000, scale=350_000)
            repayment = rng.normal(loc=75_000, scale=45_000)
            total_debt.append(max(20_000, round(debt)))
            monthly_debt_repayment.append(max(5_000, round(repayment)))
        else:
            total_debt.append(0)
            monthly_debt_repayment.append(0)

    savings_duration_weeks = rng.choice(
        [0, 1, 2, 3, 4, 8, 12],
        size=N_HOUSEHOLDS,
        p=[0.20, 0.25, 0.18, 0.12, 0.10, 0.10, 0.05]
    )

    market_access = rng.choice(
        ["Yes", "No", "Y", "N", "Unknown"],
        size=N_HOUSEHOLDS,
        p=[0.52, 0.25, 0.10, 0.08, 0.05]
    )

    female_headed_household = rng.choice(["Yes", "No"], size=N_HOUSEHOLDS, p=[0.24, 0.76])
    disability_present = rng.choice(["Yes", "No"], size=N_HOUSEHOLDS, p=[0.14, 0.86])
    displacement_status = rng.choice(["Resident", "IDP", "Returnee"], size=N_HOUSEHOLDS, p=[0.72, 0.23, 0.05])

    df = pd.DataFrame({
        "household_id": household_ids,
        "state_region": state_region,
        "township": township,
        "household_size": household_size,
        "monthly_income": monthly_income,
        "has_debt": has_debt,
        "total_debt": total_debt,
        "monthly_debt_repayment": monthly_debt_repayment,
        "savings_duration_weeks": savings_duration_weeks,
        "market_access": market_access,
        "female_headed_household": female_headed_household,
        "disability_present": disability_present,
        "displacement_status": displacement_status,
    })

    # Allow mixed raw values such as numbers, missing values, and "330945 MMK"
    df["monthly_income"] = df["monthly_income"].astype("object")
    
    # Add realistic raw-data problems
    missing_income_idx = rng.choice(df.index, size=int(0.04 * N_HOUSEHOLDS), replace=False)
    df.loc[missing_income_idx, "monthly_income"] = np.nan

    text_income_idx = rng.choice(df.index, size=int(0.02 * N_HOUSEHOLDS), replace=False)
    df.loc[text_income_idx, "monthly_income"] = df.loc[text_income_idx, "monthly_income"].apply(
        lambda x: f"{int(x)} MMK" if pd.notna(x) else x
    )

    inconsistent_state_idx = rng.choice(df.index, size=int(0.02 * N_HOUSEHOLDS), replace=False)
    df.loc[inconsistent_state_idx, "state_region"] = df.loc[inconsistent_state_idx, "state_region"].replace({
        "Sagaing": "sagaing",
        "Magway": "Magwe",
        "Shan South": "Southern Shan",
        "Shan North": "Northern Shan",
    })

    return df


def generate_agriculture_raw(rng: np.random.Generator, household_ids: list[str]) -> pd.DataFrame:
    """Generate raw agriculture data."""

    n = len(household_ids)

    is_farming_household = rng.choice(["Yes", "No"], size=n, p=[0.78, 0.22])

    main_crop = []
    farm_size_acres = []
    irrigation_access = []
    fertilizer_cost = []
    crop_damage_recent = []

    crop_options = ["Rice", "Pulses", "Maize", "Oilseed", "Vegetables", "Mixed"]

    for farming in is_farming_household:
        if farming == "Yes":
            main_crop.append(rng.choice(crop_options, p=[0.42, 0.18, 0.12, 0.10, 0.08, 0.10]))
            farm_size_acres.append(round(max(0.2, rng.normal(3.0, 1.7)), 2))
            irrigation_access.append(rng.choice(["Yes", "No"], p=[0.42, 0.58]))
            fertilizer_cost.append(round(max(0, rng.normal(150_000, 70_000))))
            crop_damage_recent.append(rng.choice(["Yes", "No"], p=[0.28, 0.72]))
        else:
            main_crop.append("None")
            farm_size_acres.append(0)
            irrigation_access.append("No")
            fertilizer_cost.append(0)
            crop_damage_recent.append("No")

    df = pd.DataFrame({
        "household_id": household_ids,
        "is_farming_household": is_farming_household,
        "main_crop": main_crop,
        "farm_size_acres": farm_size_acres,
        "irrigation_access": irrigation_access,
        "fertilizer_cost": fertilizer_cost,
        "crop_damage_recent": crop_damage_recent,
    })

    # Allow missing values in raw fertilizer cost data
    df["fertilizer_cost"] = df["fertilizer_cost"].astype("object")

    # Add some missing fertilizer costs
    missing_fert_idx = rng.choice(df.index, size=int(0.03 * n), replace=False)
    df.loc[missing_fert_idx, "fertilizer_cost"] = np.nan

    return df


def generate_coping_raw(rng: np.random.Generator, household_ids: list[str]) -> pd.DataFrame:
    """Generate raw coping strategy data for rCSI calculation."""

    n = len(household_ids)

    df = pd.DataFrame({
        "household_id": household_ids,
        "less_preferred_food_days": rng.integers(0, 8, size=n),
        "borrowed_food_days": rng.integers(0, 6, size=n),
        "reduced_meals_days": rng.integers(0, 6, size=n),
        "reduced_portion_days": rng.integers(0, 7, size=n),
        "adults_reduced_for_children_days": rng.integers(0, 5, size=n),
        "basic_needs_met": rng.choice(
            ["Yes fully", "Yes mostly", "Only some", "No"],
            size=n,
            p=[0.20, 0.34, 0.31, 0.15]
        )
    })

    coping_day_cols = [
        "less_preferred_food_days",
        "borrowed_food_days",
        "reduced_meals_days",
        "reduced_portion_days",
        "adults_reduced_for_children_days",
    ]

    for col in coping_day_cols:
        df[col] = df[col].astype("float")

    # Add missing values to simulate raw survey problems
    for col in [
        "less_preferred_food_days",
        "borrowed_food_days",
        "reduced_meals_days",
        "reduced_portion_days",
        "adults_reduced_for_children_days",
    ]:
        missing_idx = rng.choice(df.index, size=int(0.015 * n), replace=False)
        df.loc[missing_idx, col] = np.nan

    return df


def generate_market_prices_raw(rng: np.random.Generator) -> pd.DataFrame:
    """Generate state-level market price and access indicators."""

    states = [
        "Sagaing", "Magway", "Mandalay", "Chin", "Kachin",
        "Kayah", "Kayin", "Rakhine", "Shan South", "Shan North",
        "Ayeyarwady", "Bago", "Mon", "Tanintharyi"
    ]

    rows = []

    for state in states:
        if state in ["Sagaing", "Magway", "Chin", "Rakhine", "Shan North"]:
            pressure = rng.normal(38, 12)
            disruption = rng.choice(["High", "Medium"], p=[0.65, 0.35])
        elif state in ["Kayah", "Kayin", "Tanintharyi"]:
            pressure = rng.normal(30, 10)
            disruption = rng.choice(["High", "Medium", "Low"], p=[0.35, 0.45, 0.20])
        else:
            pressure = rng.normal(18, 8)
            disruption = rng.choice(["Medium", "Low"], p=[0.45, 0.55])

        rows.append({
            "state_region": state,
            "month": "2025-04",
            "basic_food_basket_change_1y": round(max(0, pressure), 1),
            "rice_price_change_1y": round(max(0, rng.normal(15, 8)), 1),
            "fuel_price_change_1y": round(max(0, rng.normal(28, 14)), 1),
            "market_disruption_level": disruption,
        })

    return pd.DataFrame(rows)


def generate_meb_values_raw() -> pd.DataFrame:
    """Generate state-level MPCA and Cash for Food Assistance values."""

    data = [
        ["Bago", 55000, 35000],
        ["Chin", 95000, 65000],
        ["Kachin", 65000, 50000],
        ["Kayah", 80000, 55000],
        ["Kayin", 65000, 40000],
        ["Magway", 55000, 30000],
        ["Mandalay", 55000, 30000],
        ["Mon", 55000, 30000],
        ["Rakhine", 55000, 35000],
        ["Sagaing", 55000, 35000],
        ["Shan North", 60000, 50000],
        ["Shan South", 55000, 35000],
        ["Tanintharyi", 55000, 30000],
        ["Ayeyarwady", 55000, 35000],
    ]

    return pd.DataFrame(data, columns=[
        "state_region",
        "mpca_per_person",
        "cash_food_assistance_per_person"
    ])


def generate_assistance_coverage_raw(rng: np.random.Generator) -> pd.DataFrame:
    """Generate state-level assistance coverage and response gap data."""

    states = [
        "Sagaing", "Magway", "Mandalay", "Chin", "Kachin",
        "Kayah", "Kayin", "Rakhine", "Shan South", "Shan North",
        "Ayeyarwady", "Bago", "Mon", "Tanintharyi"
    ]

    rows = []

    for state in states:
        targeted = rng.integers(20_000, 250_000)
        reached_rate = rng.uniform(0.20, 0.85)
        reached = int(targeted * reached_rate)
        response_gap = targeted - reached

        rows.append({
            "state_region": state,
            "people_targeted": targeted,
            "people_reached": reached,
            "coverage_rate": round(reached / targeted, 3),
            "response_gap": response_gap,
            "number_of_partners_active": int(rng.integers(3, 30)),
        })

    return pd.DataFrame(rows)


def main() -> None:
    ensure_raw_data_dir()

    rng = np.random.default_rng(RANDOM_SEED)

    households = generate_households_raw(rng)
    household_ids = households["household_id"].tolist()

    agriculture = generate_agriculture_raw(rng, household_ids)
    coping = generate_coping_raw(rng, household_ids)
    market_prices = generate_market_prices_raw(rng)
    meb_values = generate_meb_values_raw()
    assistance_coverage = generate_assistance_coverage_raw(rng)

    households.to_csv(RAW_DATA_DIR / "households_raw.csv", index=False)
    agriculture.to_csv(RAW_DATA_DIR / "agriculture_raw.csv", index=False)
    coping.to_csv(RAW_DATA_DIR / "coping_raw.csv", index=False)
    market_prices.to_csv(RAW_DATA_DIR / "market_prices_raw.csv", index=False)
    meb_values.to_csv(RAW_DATA_DIR / "meb_values_raw.csv", index=False)
    assistance_coverage.to_csv(RAW_DATA_DIR / "assistance_coverage_raw.csv", index=False)

    print("Raw data tables generated successfully.")
    print(f"Saved to: {RAW_DATA_DIR}")


if __name__ == "__main__":
    main()