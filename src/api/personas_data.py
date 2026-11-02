from src.api.schemas import FarmerProfile, Persona


PERSONAS = [
    Persona(
        id="flood_displaced",
        title="Flood-Displaced Smallholder",
        subtitle="Severe Climate Shock & High MEB Deficit",
        location="Ayeyarwady Delta (Bogale Township)",
        badge_label="Critical / High Risk",
        badge_type="critical",
        narrative=(
            "A family of 6 in the low-lying Ayeyarwady Delta whose monsoon paddy harvest was severely "
            "flooded. Household monthly income collapsed to 120,000 MMK, with 450,000 MMK in informal debt "
            "and disabled dependency. Disrupted waterways have severed access to functional markets."
        ),
        expected_outcome=(
            "High vulnerability (85-95%). A commercial loan would worsen debt trap; "
            "recommend immediate referral to humanitarian cash assistance (MPCA) and emergency seed stock."
        ),
        profile=FarmerProfile(
            state_region="Ayeyarwady",
            household_size=6,
            female_headed_household=0,
            disability_present=1,
            displacement_status="IDP",
            monthly_income=120000.0,
            has_debt=1,
            total_debt=450000.0,
            monthly_debt_repayment=45000.0,
            savings_duration_weeks=0.5,
            market_access=0,
            is_farming_household=1,
            main_crop="Rice",
            farm_size_acres=2.5,
            irrigation_access=0,
            fertilizer_cost=160000.0,
            crop_damage_recent=1,
            rCSI_score=32.0,
            basic_needs_score=0.0,
        ),
    ),
    Persona(
        id="commercial_resilient",
        title="Resilient Commercial Producer",
        subtitle="Diversified Cash Crops & Stable Cashflow",
        location="Shan South (Kalaw Highland)",
        badge_label="Stable / Low Risk",
        badge_type="success",
        narrative=(
            "A 4-member farming household cultivating 6 acres of mixed vegetables and maize in the southern Shan "
            "highlands. Equipped with private pump irrigation and open road access to trading centers. "
            "Maintains 8 weeks of emergency cash buffer and a strong income-to-expenditure ratio."
        ),
        expected_outcome=(
            "Low vulnerability (<25%). High repayment capacity; qualified for seasonal agricultural expansion "
            "credit or equipment financing."
        ),
        profile=FarmerProfile(
            state_region="Shan South",
            household_size=4,
            female_headed_household=0,
            disability_present=0,
            displacement_status="Resident",
            monthly_income=650000.0,
            has_debt=1,
            total_debt=200000.0,
            monthly_debt_repayment=25000.0,
            savings_duration_weeks=8.0,
            market_access=1,
            is_farming_household=1,
            main_crop="Vegetables",
            farm_size_acres=6.0,
            irrigation_access=1,
            fertilizer_cost=95000.0,
            crop_damage_recent=0,
            rCSI_score=4.0,
            basic_needs_score=3.0,
        ),
    ),
    Persona(
        id="inflation_borderline",
        title="Input-Stressed Borderline Farmer",
        subtitle="Fertilizer Inflation Shock & Moderate Debt",
        location="Sagaing (Central Dry Zone)",
        badge_label="Borderline / Moderate Risk",
        badge_type="warning",
        narrative=(
            "A female-headed household farming 4 acres of sesame and pulses in the Central Dry Zone. "
            "Production remains viable, but triple-digit fertilizer and diesel inflation have cut profit margins. "
            "Coping mechanisms (rCSI 18) are beginning to show strain."
        ),
        expected_outcome=(
            "Medium vulnerability (50-65%). Needs structured microfinance with flexible harvest-aligned "
            "repayment schedules, fertilizer subsidy linkages, or grace periods."
        ),
        profile=FarmerProfile(
            state_region="Sagaing",
            household_size=5,
            female_headed_household=1,
            disability_present=0,
            displacement_status="Resident",
            monthly_income=290000.0,
            has_debt=1,
            total_debt=350000.0,
            monthly_debt_repayment=35000.0,
            savings_duration_weeks=2.0,
            market_access=1,
            is_farming_household=1,
            main_crop="Pulses",
            farm_size_acres=4.0,
            irrigation_access=0,
            fertilizer_cost=180000.0,
            crop_damage_recent=0,
            rCSI_score=18.0,
            basic_needs_score=1.0,
        ),
    ),
]


def get_all_personas():
    """Return all demo case study personas."""
    return PERSONAS


def get_persona_by_id(persona_id: str):
    """Retrieve persona by unique ID."""
    for p in PERSONAS:
        if p.id == persona_id:
            return p
    return None

