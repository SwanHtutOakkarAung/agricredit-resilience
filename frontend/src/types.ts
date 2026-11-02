export interface FarmerProfile {
  state_region: string;
  household_size: number;
  female_headed_household: number;
  disability_present: number;
  displacement_status: string;
  monthly_income: number;
  has_debt: number;
  total_debt: number;
  monthly_debt_repayment: number;
  savings_duration_weeks: number;
  market_access: number;
  is_farming_household: number;
  main_crop: string;
  farm_size_acres: number;
  irrigation_access: number;
  fertilizer_cost: number;
  crop_damage_recent: number;
  rCSI_score: number;
  basic_needs_score: number;
  basic_food_basket_change_1y?: number;
  rice_price_change_1y?: number;
  fuel_price_change_1y?: number;
  market_disruption_score?: number;
  market_pressure_score?: number;
  mpca_per_person?: number;
  coverage_rate?: number;
  coverage_gap_ratio?: number;
  response_gap?: number;
  number_of_partners_active?: number;
}

export interface KeyFactor {
  name: string;
  impact: 'risk_increasing' | 'risk_mitigating' | 'neutral';
  description: string;
}

export interface ComputedIndicators {
  household_meb_requirement: number;
  income_to_meb_ratio: number;
  meb_gap: number;
  debt_to_income_ratio: number;
  monthly_debt_repayment_ratio: number;
}

export interface PredictionResponse {
  model_used: string;
  vulnerability_probability: number;
  vulnerability_percentage: number;
  predicted_class: number;
  predicted_label: string;
  risk_level: 'Low risk' | 'Medium risk' | 'High risk';
  recommendation: string;
  computed_indicators: ComputedIndicators;
  key_drivers: KeyFactor[];
}

export interface Persona {
  id: string;
  title: string;
  subtitle: string;
  location: string;
  badge_label: string;
  badge_type: 'critical' | 'success' | 'warning';
  narrative: string;
  expected_outcome: string;
  profile: FarmerProfile;
}

export interface SimulationRequest {
  base_profile: FarmerProfile;
  model_type: 'logistic_regression' | 'decision_tree';
  cash_grant_mmk: number;
  fertilizer_subsidy_pct: number;
  debt_relief_pct: number;
  repair_crop_damage: boolean;
}

export interface SimulationResponse {
  baseline_probability: number;
  baseline_risk_level: string;
  simulated_probability: number;
  simulated_risk_level: string;
  risk_reduction_percentage: number;
  impact_summary: string;
  updated_recommendation: string;
}

export interface MetadataResponse {
  states_regions: string[];
  crops: string[];
  displacement_statuses: string[];
  model_versions: Record<string, string>;
}

export interface HealthResponse {
  status: string;
  api_version: string;
  loaded_models: string[];
  timestamp: string;
}

