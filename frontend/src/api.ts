import {
  FarmerProfile,
  HealthResponse,
  MetadataResponse,
  Persona,
  PredictionResponse,
  SimulationRequest,
  SimulationResponse,
} from './types';

const API_BASE = ''; // Uses Vite proxy in development, or relative path in production

export async function fetchHealth(): Promise<HealthResponse> {
  const res = await fetch(`${API_BASE}/health`);
  if (!res.ok) throw new Error('API server unreachable');
  return res.json();
}

export async function fetchMetadata(): Promise<MetadataResponse> {
  const res = await fetch(`${API_BASE}/api/v1/metadata`);
  if (!res.ok) throw new Error('Failed to load metadata');
  return res.json();
}

export async function fetchPersonas(): Promise<Persona[]> {
  const res = await fetch(`${API_BASE}/api/v1/personas`);
  if (!res.ok) throw new Error('Failed to load personas');
  const data = await res.json();
  return data.personas;
}

export async function predictVulnerability(
  profile: FarmerProfile,
  modelType: 'logistic_regression' | 'decision_tree' = 'logistic_regression'
): Promise<PredictionResponse> {
  const res = await fetch(`${API_BASE}/api/v1/predict`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ profile, model_type: modelType }),
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Inference failed');
  }
  return res.json();
}

export async function simulateIntervention(
  request: SimulationRequest
): Promise<SimulationResponse> {
  const res = await fetch(`${API_BASE}/api/v1/simulate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(request),
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Simulation failed');
  }
  return res.json();
}

