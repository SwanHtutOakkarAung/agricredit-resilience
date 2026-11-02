from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from src.api.personas_data import get_all_personas, get_persona_by_id
from src.api.schemas import (
    ComputedIndicators,
    FarmerProfile,
    HealthResponse,
    KeyFactor,
    MetadataResponse,
    Persona,
    PersonaListResponse,
    PredictionRequest,
    PredictionResponse,
    SimulationRequest,
    SimulationResponse,
)
from src.app_utils import (
    FEATURE_COLUMNS,
    assign_risk_level,
    create_recommendation,
    load_abt,
    load_decision_tree_model,
    load_logistic_regression_model,
)


# In-memory model and reference cache
MODELS: Dict[str, object] = {}
ABT_CACHE: Optional[pd.DataFrame] = None
REGIONAL_CONTEXT_CACHE: Dict[str, dict] = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load models and reference tables into memory during application startup."""
    global ABT_CACHE, REGIONAL_CONTEXT_CACHE

    print("[API] Initializing AgriCredit models and reference tables...")

    # Load scikit-learn model pipelines
    MODELS["logistic_regression"] = load_logistic_regression_model()
    MODELS["decision_tree"] = load_decision_tree_model()

    # Load ABT and extract default regional averages
    ABT_CACHE = load_abt()

    context_cols = [
        "basic_food_basket_change_1y",
        "rice_price_change_1y",
        "fuel_price_change_1y",
        "market_disruption_score",
        "market_pressure_score",
        "mpca_per_person",
        "coverage_rate",
        "coverage_gap_ratio",
        "response_gap",
        "number_of_partners_active",
    ]

    for state, group in ABT_CACHE.groupby("state_region"):
        first_row = group.iloc[0]
        REGIONAL_CONTEXT_CACHE[state] = {col: float(first_row[col]) for col in context_cols}

    print(f"[API] Startup complete. Loaded {len(MODELS)} models across {len(REGIONAL_CONTEXT_CACHE)} regions.")
    yield
    print("[API] Shutting down AgriCredit API.")


app = FastAPI(
    title="AgriCredit Resilience REST API",
    description=(
        "Production inference service for explainable rural household financial vulnerability "
        "and responsible microfinance decision support in Myanmar."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# Enable CORS for frontend clients (Next.js, Vite, Streamlit, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def build_feature_row(profile: FarmerProfile) -> (pd.DataFrame, ComputedIndicators):
    """Combine farmer profile with regional context and derived economic ratios."""
    region = profile.state_region

    # Fallback to defaults if region not found
    regional_defaults = REGIONAL_CONTEXT_CACHE.get(
        region,
        {
            "basic_food_basket_change_1y": 25.0,
            "rice_price_change_1y": 20.0,
            "fuel_price_change_1y": 30.0,
            "market_disruption_score": 1.5,
            "market_pressure_score": 2.0,
            "mpca_per_person": 45000.0,
            "coverage_rate": 0.35,
            "coverage_gap_ratio": 0.65,
            "response_gap": 0.65,
            "number_of_partners_active": 12.0,
        },
    )

    # Use explicit overrides if provided, otherwise apply regional lookup
    mpca = profile.mpca_per_person if profile.mpca_per_person is not None else regional_defaults["mpca_per_person"]
    food_basket = (
        profile.basic_food_basket_change_1y
        if profile.basic_food_basket_change_1y is not None
        else regional_defaults["basic_food_basket_change_1y"]
    )
    rice_change = (
        profile.rice_price_change_1y
        if profile.rice_price_change_1y is not None
        else regional_defaults["rice_price_change_1y"]
    )
    fuel_change = (
        profile.fuel_price_change_1y
        if profile.fuel_price_change_1y is not None
        else regional_defaults["fuel_price_change_1y"]
    )
    market_disruption = (
        profile.market_disruption_score
        if profile.market_disruption_score is not None
        else regional_defaults["market_disruption_score"]
    )
    market_pressure = (
        profile.market_pressure_score
        if profile.market_pressure_score is not None
        else regional_defaults["market_pressure_score"]
    )
    cov_rate = (
        profile.coverage_rate
        if profile.coverage_rate is not None
        else regional_defaults["coverage_rate"]
    )
    cov_gap = (
        profile.coverage_gap_ratio
        if profile.coverage_gap_ratio is not None
        else regional_defaults["coverage_gap_ratio"]
    )
    resp_gap = (
        profile.response_gap
        if profile.response_gap is not None
        else regional_defaults["response_gap"]
    )
    partners = (
        profile.number_of_partners_active
        if profile.number_of_partners_active is not None
        else regional_defaults["number_of_partners_active"]
    )

    # Compute derived ratios
    meb_requirement = float(mpca * profile.household_size)

    if profile.monthly_income > 0:
        dti = float(profile.total_debt / profile.monthly_income)
        monthly_repayment_ratio = float(profile.monthly_debt_repayment / profile.monthly_income)
        income_to_meb = float(profile.monthly_income / meb_requirement) if meb_requirement > 0 else 0.0
    else:
        dti = 0.0
        monthly_repayment_ratio = 0.0
        income_to_meb = 0.0

    meb_gap_val = float(meb_requirement - profile.monthly_income)

    computed = ComputedIndicators(
        household_meb_requirement=round(meb_requirement, 2),
        income_to_meb_ratio=round(income_to_meb, 3),
        meb_gap=round(meb_gap_val, 2),
        debt_to_income_ratio=round(dti, 3),
        monthly_debt_repayment_ratio=round(monthly_repayment_ratio, 3),
    )

    row_data = {
        "state_region": profile.state_region,
        "household_size": profile.household_size,
        "female_headed_household": profile.female_headed_household,
        "disability_present": profile.disability_present,
        "displacement_status": profile.displacement_status,
        "monthly_income": profile.monthly_income,
        "has_debt": profile.has_debt,
        "total_debt": profile.total_debt,
        "monthly_debt_repayment": profile.monthly_debt_repayment,
        "savings_duration_weeks": profile.savings_duration_weeks,
        "debt_to_income_ratio": dti,
        "monthly_debt_repayment_ratio": monthly_repayment_ratio,
        "market_access": profile.market_access,
        "is_farming_household": profile.is_farming_household,
        "main_crop": profile.main_crop,
        "farm_size_acres": profile.farm_size_acres,
        "irrigation_access": profile.irrigation_access,
        "fertilizer_cost": profile.fertilizer_cost,
        "crop_damage_recent": profile.crop_damage_recent,
        "rCSI_score": profile.rCSI_score,
        "basic_needs_score": profile.basic_needs_score,
        "basic_food_basket_change_1y": food_basket,
        "rice_price_change_1y": rice_change,
        "fuel_price_change_1y": fuel_change,
        "market_disruption_score": market_disruption,
        "market_pressure_score": market_pressure,
        "mpca_per_person": mpca,
        "household_meb_requirement": meb_requirement,
        "income_to_meb_ratio": income_to_meb,
        "meb_gap": meb_gap_val,
        "coverage_rate": cov_rate,
        "coverage_gap_ratio": cov_gap,
        "response_gap": resp_gap,
        "number_of_partners_active": partners,
    }

    df = pd.DataFrame([row_data])[FEATURE_COLUMNS]
    return df, computed


def extract_key_drivers(profile: FarmerProfile, computed: ComputedIndicators) -> List[KeyFactor]:
    """Generate interpretable factor contributions explaining risk drivers."""
    factors = []

    if profile.crop_damage_recent == 1:
        factors.append(
            KeyFactor(
                name="Recent Crop Inundation / Loss",
                impact="risk_increasing",
                description="Severe crop loss directly undermines harvest yields and primary cashflow.",
            )
        )

    if computed.income_to_meb_ratio < 0.8:
        factors.append(
            KeyFactor(
                name="High Basic Expenditure (MEB) Deficit",
                impact="risk_increasing",
                description=f"Household income covers only {computed.income_to_meb_ratio*100:.1f}% of minimum survival needs.",
            )
        )

    if computed.debt_to_income_ratio > 1.0:
        factors.append(
            KeyFactor(
                name="Elevated Debt-to-Income Ratio",
                impact="risk_increasing",
                description=f"Outstanding liabilities exceed total monthly household earnings by {computed.debt_to_income_ratio:.1f}x.",
            )
        )

    if profile.market_access == 0:
        factors.append(
            KeyFactor(
                name="Severe Market Disruption",
                impact="risk_increasing",
                description="Severed market linkages obstruct input procurement and surplus crop sales.",
            )
        )

    if profile.displacement_status == "IDP":
        factors.append(
            KeyFactor(
                name="Internal Displacement Status",
                impact="risk_increasing",
                description="Lack of secure land tenure and disrupted community safety networks.",
            )
        )

    # Mitigating factors
    if profile.savings_duration_weeks >= 4.0:
        factors.append(
            KeyFactor(
                name="Emergency Liquidity Buffer",
                impact="risk_mitigating",
                description=f"{profile.savings_duration_weeks:.0f} weeks of savings provide buffer against sudden shocks.",
            )
        )

    if profile.irrigation_access == 1:
        factors.append(
            KeyFactor(
                name="Reliable Irrigation Infrastructure",
                impact="risk_mitigating",
                description="Water security protects multiple planting cycles against seasonal drought.",
            )
        )

    if computed.income_to_meb_ratio >= 1.2:
        factors.append(
            KeyFactor(
                name="Positive Cashflow Surplus",
                impact="risk_mitigating",
                description="Earnings comfortably exceed regional Minimum Expenditure Basket requirements.",
            )
        )

    if not factors:
        factors.append(
            KeyFactor(
                name="Balanced Household Baseline",
                impact="neutral",
                description="Indicators fall within standard regional operating variances.",
            )
        )

    return factors


@app.get("/health", response_model=HealthResponse, tags=["Monitoring"])
def health_check():
    """Verify API service health, loaded models, and timestamp."""
    return HealthResponse(
        status="healthy",
        api_version="1.0.0",
        loaded_models=list(MODELS.keys()),
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


@app.get("/api/v1/metadata", response_model=MetadataResponse, tags=["Metadata"])
def get_metadata():
    """Retrieve available administrative regions, crops, and displacement statuses."""
    if ABT_CACHE is None:
        raise HTTPException(status_code=503, detail="Reference data not loaded yet")

    return MetadataResponse(
        states_regions=sorted(ABT_CACHE["state_region"].dropna().unique().tolist()),
        crops=sorted(ABT_CACHE["main_crop"].dropna().unique().tolist()),
        displacement_statuses=sorted(ABT_CACHE["displacement_status"].dropna().unique().tolist()),
        model_versions={
            "logistic_regression": "v1.0 (Balanced, ROC-AUC: 0.948)",
            "decision_tree": "v1.0 (max_depth=4, ROC-AUC: 0.901)",
        },
    )


@app.get("/api/v1/personas", response_model=PersonaListResponse, tags=["Personas"])
def list_personas():
    """Retrieve pre-configured case study personas for instant demo presets."""
    personas = get_all_personas()
    return PersonaListResponse(total=len(personas), personas=personas)


@app.get("/api/v1/personas/{persona_id}", response_model=Persona, tags=["Personas"])
def get_persona(persona_id: str):
    """Retrieve a single demo persona profile by its identifier."""
    persona = get_persona_by_id(persona_id)
    if not persona:
        raise HTTPException(status_code=404, detail=f"Persona '{persona_id}' not found.")
    return persona


@app.post("/api/v1/predict", response_model=PredictionResponse, tags=["Inference"])
def predict_vulnerability(request: PredictionRequest):
    """
    Score household financial vulnerability and generate tailored decision-support recommendations.
    Accepts full farmer profile and choice of model architecture.
    """
    model_key = request.model_type
    if model_key not in MODELS:
        raise HTTPException(status_code=400, detail=f"Model '{model_key}' is not available.")

    model = MODELS[model_key]

    # Build model-ready DataFrame
    feature_df, computed = build_feature_row(request.profile)

    # Execute inference
    prob = float(model.predict_proba(feature_df)[0, 1])
    predicted_class = int(model.predict(feature_df)[0])
    risk_level = assign_risk_level(prob)

    # Generate responsible recommendation
    recommendation = create_recommendation(
        risk_level=risk_level,
        market_access=request.profile.market_access,
        crop_damage_recent=request.profile.crop_damage_recent,
    )

    # Extract key drivers
    key_drivers = extract_key_drivers(request.profile, computed)

    return PredictionResponse(
        model_used="Logistic Regression (Main)" if model_key == "logistic_regression" else "Decision Tree (Explainable)",
        vulnerability_probability=round(prob, 4),
        vulnerability_percentage=round(prob * 100, 1),
        predicted_class=predicted_class,
        predicted_label="Vulnerable" if predicted_class == 1 else "Not Vulnerable",
        risk_level=risk_level,
        recommendation=recommendation,
        computed_indicators=computed,
        key_drivers=key_drivers,
    )


@app.post("/api/v1/simulate", response_model=SimulationResponse, tags=["Counterfactual Simulation"])
def simulate_intervention(request: SimulationRequest):
    """
    Simulate what-if humanitarian or financial interventions (e.g. emergency cash grants,
    fertilizer subsidies, debt relief) and measure resulting risk reduction in real time.
    """
    # 1. Baseline prediction
    baseline_req = PredictionRequest(profile=request.base_profile, model_type=request.model_type)
    baseline_res = predict_vulnerability(baseline_req)

    # 2. Apply simulated interventions to a cloned profile
    sim_profile_data = request.base_profile.model_dump()

    # Cash grant increases monthly liquidity buffer / effective income
    if request.cash_grant_mmk > 0:
        sim_profile_data["monthly_income"] += request.cash_grant_mmk / 3.0  # Distributed over 3-month cycle
        sim_profile_data["savings_duration_weeks"] += 2.0

    # Fertilizer subsidy directly reduces agricultural input expense
    if request.fertilizer_subsidy_pct > 0:
        reduction_multiplier = 1.0 - (request.fertilizer_subsidy_pct / 100.0)
        sim_profile_data["fertilizer_cost"] = max(0.0, sim_profile_data["fertilizer_cost"] * reduction_multiplier)

    # Debt relief reduces outstanding balance and monthly repayment
    if request.debt_relief_pct > 0:
        debt_multiplier = 1.0 - (request.debt_relief_pct / 100.0)
        sim_profile_data["total_debt"] = max(0.0, sim_profile_data["total_debt"] * debt_multiplier)
        sim_profile_data["monthly_debt_repayment"] = max(0.0, sim_profile_data["monthly_debt_repayment"] * debt_multiplier)
        if sim_profile_data["total_debt"] == 0:
            sim_profile_data["has_debt"] = 0

    # Repair crop damage
    if request.repair_crop_damage:
        sim_profile_data["crop_damage_recent"] = 0
        sim_profile_data["rCSI_score"] = max(0.0, sim_profile_data["rCSI_score"] - 8.0)

    sim_profile = FarmerProfile(**sim_profile_data)
    sim_res = predict_vulnerability(PredictionRequest(profile=sim_profile, model_type=request.model_type))

    # Calculate delta
    risk_reduction = (baseline_res.vulnerability_probability - sim_res.vulnerability_probability) * 100.0

    summary = (
        f"Intervention reduced vulnerability from {baseline_res.vulnerability_percentage:.1f}% "
        f"to {sim_res.vulnerability_percentage:.1f}% (a {risk_reduction:.1f}% absolute risk reduction). "
        f"Risk tier shifted from {baseline_res.risk_level} to {sim_res.risk_level}."
    )

    return SimulationResponse(
        baseline_probability=baseline_res.vulnerability_probability,
        baseline_risk_level=baseline_res.risk_level,
        simulated_probability=sim_res.vulnerability_probability,
        simulated_risk_level=sim_res.risk_level,
        risk_reduction_percentage=round(risk_reduction, 1),
        impact_summary=summary,
        updated_recommendation=sim_res.recommendation,
    )

