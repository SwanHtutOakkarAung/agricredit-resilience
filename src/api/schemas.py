from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, Field


class FarmerProfile(BaseModel):
    """Input payload representing a rural farmer household in Myanmar."""

    # Location & Demographics
    state_region: str = Field(
        default="Ayeyarwady",
        description="State or Region in Myanmar (e.g., Ayeyarwady, Shan South, Sagaing)",
        examples=["Ayeyarwady"],
    )
    household_size: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Total number of members living in the household",
    )
    female_headed_household: int = Field(
        default=0,
        ge=0,
        le=1,
        description="1 if household head is female, 0 otherwise",
    )
    disability_present: int = Field(
        default=0,
        ge=0,
        le=1,
        description="1 if any household member has a disability, 0 otherwise",
    )
    displacement_status: str = Field(
        default="Resident",
        description="Displacement status: 'Resident', 'IDP', or 'Returnee'",
        examples=["Resident"],
    )

    # Financial Status
    monthly_income: float = Field(
        default=250000.0,
        ge=0.0,
        description="Total household monthly income in MMK",
    )
    has_debt: int = Field(
        default=1,
        ge=0,
        le=1,
        description="1 if household has outstanding debt, 0 otherwise",
    )
    total_debt: float = Field(
        default=300000.0,
        ge=0.0,
        description="Total outstanding debt amount in MMK",
    )
    monthly_debt_repayment: float = Field(
        default=30000.0,
        ge=0.0,
        description="Monthly debt repayment obligation in MMK",
    )
    savings_duration_weeks: float = Field(
        default=2.0,
        ge=0.0,
        description="Estimated number of weeks savings can support household needs",
    )

    # Agriculture & Livelihood
    market_access: int = Field(
        default=1,
        ge=0,
        le=1,
        description="1 if household has regular physical access to functional local markets, 0 otherwise",
    )
    is_farming_household: int = Field(
        default=1,
        ge=0,
        le=1,
        description="1 if farming is primary household livelihood, 0 otherwise",
    )
    main_crop: str = Field(
        default="Rice",
        description="Primary crop grown (e.g., 'Rice', 'Maize', 'Pulses', 'Oilseed', 'Vegetables', 'Mixed')",
        examples=["Rice"],
    )
    farm_size_acres: float = Field(
        default=3.0,
        ge=0.0,
        description="Total cultivated agricultural land in acres",
    )
    irrigation_access: int = Field(
        default=0,
        ge=0,
        le=1,
        description="1 if land has formal irrigation access, 0 otherwise",
    )
    fertilizer_cost: float = Field(
        default=120000.0,
        ge=0.0,
        description="Seasonal/monthly expenditure on chemical or organic fertilizers in MMK",
    )
    crop_damage_recent: int = Field(
        default=0,
        ge=0,
        le=1,
        description="1 if crops suffered damage from flood, drought, pests, or conflict, 0 otherwise",
    )

    # Coping Strategy & Basic Needs
    rCSI_score: float = Field(
        default=15.0,
        ge=0.0,
        le=60.0,
        description="Reduced Coping Strategy Index score (higher indicates greater food-related stress)",
    )
    basic_needs_score: float = Field(
        default=2.0,
        ge=0.0,
        le=4.0,
        description="Self-reported capacity to meet basic needs (0=severe deficit, 3=sufficient)",
    )

    # Optional Overrides for Regional / Context Indicators (Auto-filled if None)
    basic_food_basket_change_1y: Optional[float] = Field(
        default=None,
        description="1-year percentage change in local food basket price",
    )
    rice_price_change_1y: Optional[float] = Field(
        default=None,
        description="1-year percentage change in local rice price",
    )
    fuel_price_change_1y: Optional[float] = Field(
        default=None,
        description="1-year percentage change in local fuel price",
    )
    market_disruption_score: Optional[float] = Field(
        default=None,
        description="Local market supply disruption score",
    )
    market_pressure_score: Optional[float] = Field(
        default=None,
        description="Composite market pressure score",
    )
    mpca_per_person: Optional[float] = Field(
        default=None,
        description="Multi-Purpose Cash Assistance (MEB benchmark per person) in MMK",
    )
    coverage_rate: Optional[float] = Field(
        default=None,
        description="Regional humanitarian assistance coverage rate",
    )
    coverage_gap_ratio: Optional[float] = Field(
        default=None,
        description="Assistance coverage gap ratio in region",
    )
    response_gap: Optional[float] = Field(
        default=None,
        description="Regional response gap indicator",
    )
    number_of_partners_active: Optional[float] = Field(
        default=None,
        description="Number of humanitarian/development partners active in region",
    )


class PredictionRequest(BaseModel):
    """Wrapper request allowing model choice."""

    profile: FarmerProfile
    model_type: Literal["logistic_regression", "decision_tree"] = Field(
        default="logistic_regression",
        description="Model architecture to use for inference",
    )


class KeyFactor(BaseModel):
    """Individual driver contributing to vulnerability risk."""

    name: str
    impact: Literal["risk_increasing", "risk_mitigating", "neutral"]
    description: str


class ComputedIndicators(BaseModel):
    """Engineered household financial indicators."""

    household_meb_requirement: float
    income_to_meb_ratio: float
    meb_gap: float
    debt_to_income_ratio: float
    monthly_debt_repayment_ratio: float


class PredictionResponse(BaseModel):
    """Output prediction payload from machine learning models."""

    model_used: str
    vulnerability_probability: float
    vulnerability_percentage: float
    predicted_class: int
    predicted_label: str
    risk_level: Literal["Low risk", "Medium risk", "High risk"]
    recommendation: str
    computed_indicators: ComputedIndicators
    key_drivers: List[KeyFactor]


class Persona(BaseModel):
    """Case study profile for one-click demo presets."""

    id: str
    title: str
    subtitle: str
    location: str
    badge_label: str
    badge_type: Literal["critical", "success", "warning"]
    narrative: str
    expected_outcome: str
    profile: FarmerProfile


class PersonaListResponse(BaseModel):
    """List of available case study personas."""

    total: int
    personas: List[Persona]


class SimulationRequest(BaseModel):
    """What-If counterfactual scenario request."""

    base_profile: FarmerProfile
    model_type: Literal["logistic_regression", "decision_tree"] = "logistic_regression"
    cash_grant_mmk: float = Field(
        default=0.0,
        ge=0.0,
        description="One-time emergency cash grant assistance in MMK",
    )
    fertilizer_subsidy_pct: float = Field(
        default=0.0,
        ge=0.0,
        le=100.0,
        description="Percentage reduction in fertilizer costs through agricultural subsidy",
    )
    debt_relief_pct: float = Field(
        default=0.0,
        ge=0.0,
        le=100.0,
        description="Percentage of total debt forgiven or restructured",
    )
    repair_crop_damage: bool = Field(
        default=False,
        description="Whether emergency crop rehabilitation or flood defense was deployed",
    )


class SimulationResponse(BaseModel):
    """Results of counterfactual intervention simulation."""

    baseline_probability: float
    baseline_risk_level: str
    simulated_probability: float
    simulated_risk_level: str
    risk_reduction_percentage: float
    impact_summary: str
    updated_recommendation: str


class MetadataResponse(BaseModel):
    """Metadata regarding available regions, crops, displacement statuses."""

    states_regions: List[str]
    crops: List[str]
    displacement_statuses: List[str]
    model_versions: Dict[str, str]


class HealthResponse(BaseModel):
    """Health check endpoint response."""

    status: str
    api_version: str
    loaded_models: List[str]
    timestamp: str

