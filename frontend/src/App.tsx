import { useState, useEffect } from 'react';
import {
  FarmerProfile,
  HealthResponse,
  MetadataResponse,
  Persona,
  PredictionResponse,
} from './types';
import { fetchHealth, fetchMetadata, fetchPersonas, predictVulnerability, DOCS_URL } from './api';
import { Navbar } from './components/Navbar';
import { PersonaSelector } from './components/PersonaSelector';
import { FarmerForm } from './components/FarmerForm';
import { RiskGaugeCard } from './components/RiskGaugeCard';
import { SimulationCard } from './components/SimulationCard';

const DEFAULT_PROFILE: FarmerProfile = {
  state_region: 'Ayeyarwady',
  household_size: 5,
  female_headed_household: 0,
  disability_present: 0,
  displacement_status: 'Resident',
  monthly_income: 250000,
  has_debt: 1,
  total_debt: 300000,
  monthly_debt_repayment: 30000,
  savings_duration_weeks: 2.0,
  market_access: 1,
  is_farming_household: 1,
  main_crop: 'Rice',
  farm_size_acres: 3.0,
  irrigation_access: 0,
  fertilizer_cost: 120000,
  crop_damage_recent: 0,
  rCSI_score: 15,
  basic_needs_score: 2,
};

export function App() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [isHealthLoading, setIsHealthLoading] = useState<boolean>(true);
  const [metadata, setMetadata] = useState<MetadataResponse | null>(null);
  const [personas, setPersonas] = useState<Persona[]>([]);
  const [selectedPersonaId, setSelectedPersonaId] = useState<string | null>(null);

  const [currentProfile, setCurrentProfile] = useState<FarmerProfile>(DEFAULT_PROFILE);
  const [modelType, setModelType] = useState<'logistic_regression' | 'decision_tree'>('logistic_regression');

  const [prediction, setPrediction] = useState<PredictionResponse | null>(null);
  const [isPredicting, setIsPredicting] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  // Initialize data on component mount with auto-retry for cloud cold-starts
  useEffect(() => {
    let timer: any;
    let isMounted = true;

    async function attemptConnection() {
      try {
        const healthData = await fetchHealth();
        if (!isMounted) return;
        setHealth(healthData);
        setIsHealthLoading(false);

        // Once healthy, fetch metadata and personas
        const [metaData, personasData] = await Promise.all([
          fetchMetadata().catch(() => null),
          fetchPersonas().catch(() => []),
        ]);

        if (!isMounted) return;
        if (metaData) setMetadata(metaData);
        if (personasData && personasData.length > 0) {
          setPersonas(personasData);
          if (!selectedPersonaId) {
            const first = personasData[0];
            setSelectedPersonaId(first.id);
            setCurrentProfile(first.profile);
            triggerPrediction(first.profile, modelType);
          }
        }
      } catch {
        if (!isMounted) return;
        setHealth(null);
        setIsHealthLoading(false);
        // Retry every 4 seconds until cloud server is awake
        timer = setTimeout(attemptConnection, 4000);
      }
    }

    attemptConnection();

    return () => {
      isMounted = false;
      if (timer) clearTimeout(timer);
    };
  }, [modelType, selectedPersonaId]);

  const triggerPrediction = async (
    profile: FarmerProfile,
    model: 'logistic_regression' | 'decision_tree'
  ) => {
    setIsPredicting(true);
    setError(null);
    try {
      const res = await predictVulnerability(profile, model);
      setPrediction(res);
    } catch (err: any) {
      setError(err.message || 'Inference failed');
    } finally {
      setIsPredicting(false);
    }
  };

  const handleSelectPersona = (persona: Persona) => {
    setSelectedPersonaId(persona.id);
    setCurrentProfile(persona.profile);
    triggerPrediction(persona.profile, modelType);
  };

  const handleResetCustom = () => {
    setSelectedPersonaId(null);
    setCurrentProfile(DEFAULT_PROFILE);
    triggerPrediction(DEFAULT_PROFILE, modelType);
  };

  const handleProfileChange = (updated: FarmerProfile) => {
    setCurrentProfile(updated);
    // If the user modified the profile, unselect active persona badge
    if (selectedPersonaId !== null) {
      setSelectedPersonaId(null);
    }
  };

  const handleModelChange = (newModel: 'logistic_regression' | 'decision_tree') => {
    setModelType(newModel);
    triggerPrediction(currentProfile, newModel);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col selection:bg-emerald-500 selection:text-white">
      {/* Top Navbar */}
      <Navbar
        health={health}
        isHealthLoading={isHealthLoading}
        modelType={modelType}
        onModelChange={handleModelChange}
      />

      {/* Main Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
        
        {/* Hero Banner / Problem Statement */}
        <div className="bg-gradient-to-r from-slate-900 via-slate-900/90 to-emerald-950/40 border border-slate-800 rounded-2xl p-6 sm:p-8 backdrop-blur shadow-sm">
          <div className="max-w-3xl space-y-3">
            <span className="text-xs font-semibold px-2.5 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 uppercase tracking-wider">
              Social Impact & Machine Learning
            </span>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
              Ethical Decision Support for Rural Agriculture
            </h2>
            <p className="text-sm text-slate-300 leading-relaxed">
              Evaluating smallholder farmer financial vulnerability across Myanmar. Designed to assist
              microfinance officers and humanitarian responders in identifying repayment distress, understanding
              underlying shock drivers, and structuring responsible livelihood assistance.
            </p>
          </div>
        </div>

        {/* 1. One-Click Case Study Presets (Persona Hero) */}
        <PersonaSelector
          personas={personas}
          selectedPersonaId={selectedPersonaId}
          onSelectPersona={handleSelectPersona}
          onResetCustom={handleResetCustom}
        />

        {/* 2. Main Two-Column Layout: Form (Left) & Results (Right) */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          
          {/* Left Column: Editable Form */}
          <div className="lg:col-span-7 space-y-6">
            <div className="flex items-center justify-between pb-2 border-b border-slate-800">
              <h2 className="text-base font-semibold text-white tracking-tight">
                Household Characteristics & Inputs
              </h2>
              <span className="text-xs text-slate-400">
                Preset + Custom Overrides
              </span>
            </div>

            <FarmerForm
              profile={currentProfile}
              metadata={metadata}
              onChange={handleProfileChange}
              onSubmit={() => triggerPrediction(currentProfile, modelType)}
              isLoading={isPredicting}
            />
          </div>

          {/* Right Column: Visual Assessment & Decision Support */}
          <div className="lg:col-span-5 space-y-6 lg:sticky lg:top-24">
            {error && (
              <div className="p-4 rounded-xl bg-rose-950/60 border border-rose-800/80 text-rose-300 text-xs">
                {error}
              </div>
            )}

            <RiskGaugeCard
              prediction={prediction}
              isLoading={isPredicting}
            />

            {/* What-If Counterfactual Sandbox */}
            <SimulationCard
              currentProfile={currentProfile}
              modelType={modelType}
            />
          </div>
        </div>

      </main>

      {/* Footer */}
      <footer className="border-t border-slate-800/80 bg-slate-900/60 py-6 text-xs text-slate-400">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-4">
          <p>© 2026 AgriCredit Resilience. Capstone Project by Swan Htut Oakkar Aung.</p>
          <div className="flex items-center gap-6">
            <a
              href="https://github.com/SwanHtutOakkarAung/agricredit-resilience"
              target="_blank"
              rel="noopener noreferrer"
              className="text-slate-400 hover:text-white transition"
            >
              GitHub Repository
            </a>
            <a
              href={DOCS_URL}
              target="_blank"
              rel="noopener noreferrer"
              className="text-emerald-400 hover:text-emerald-300 transition"
            >
              FastAPI Interactive Docs
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
