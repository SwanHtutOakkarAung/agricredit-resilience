import React, { useState } from 'react';
import { FarmerProfile, SimulationResponse } from '../types';
import { simulateIntervention } from '../api';
import { Sparkles, ArrowRight, CheckCircle, RefreshCcw } from 'lucide-react';

interface SimulationCardProps {
  currentProfile: FarmerProfile;
  modelType: 'logistic_regression' | 'decision_tree';
}

export const SimulationCard: React.FC<SimulationCardProps> = ({
  currentProfile,
  modelType,
}) => {
  const [cashGrant, setCashGrant] = useState<number>(0);
  const [fertilizerSubsidy, setFertilizerSubsidy] = useState<number>(0);
  const [debtRelief, setDebtRelief] = useState<number>(0);
  const [repairCropDamage, setRepairCropDamage] = useState<boolean>(false);

  const [simulationResult, setSimulationResult] = useState<SimulationResponse | null>(null);
  const [isSimulating, setIsSimulating] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleSimulate = async () => {
    setIsSimulating(true);
    setError(null);
    try {
      const res = await simulateIntervention({
        base_profile: currentProfile,
        model_type: modelType,
        cash_grant_mmk: cashGrant,
        fertilizer_subsidy_pct: fertilizerSubsidy,
        debt_relief_pct: debtRelief,
        repair_crop_damage: repairCropDamage,
      });
      setSimulationResult(res);
    } catch (err: any) {
      setError(err.message || 'Simulation failed');
    } finally {
      setIsSimulating(false);
    }
  };

  const handleReset = () => {
    setCashGrant(0);
    setFertilizerSubsidy(0);
    setDebtRelief(0);
    setRepairCropDamage(false);
    setSimulationResult(null);
    setError(null);
  };

  return (
    <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 backdrop-blur shadow-sm space-y-5">
      <div className="flex items-center justify-between pb-3 border-b border-slate-800">
        <div>
          <div className="flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-emerald-400" />
            <h3 className="text-base font-semibold text-white tracking-tight">
              "What-If" Counterfactual Intervention Sandbox
            </h3>
          </div>
          <p className="text-xs text-slate-400 mt-0.5">
            Simulate policy interventions (cash grants, subsidies, debt restructuring) to evaluate risk reduction.
          </p>
        </div>

        <button
          onClick={handleReset}
          className="text-xs text-slate-400 hover:text-white flex items-center gap-1 bg-slate-800 hover:bg-slate-700 px-2.5 py-1.5 rounded-lg border border-slate-700 transition"
        >
          <RefreshCcw className="w-3 h-3" />
          Reset Sliders
        </button>
      </div>

      {/* Sliders Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5 text-xs">
        
        {/* Cash Grant */}
        <div className="bg-slate-950/60 p-4 rounded-xl border border-slate-800/80 space-y-2">
          <div className="flex justify-between items-center">
            <label className="text-slate-300 font-medium">Emergency Cash Grant:</label>
            <span className="font-mono font-bold text-emerald-400">
              {cashGrant.toLocaleString()} MMK
            </span>
          </div>
          <input
            type="range"
            min="0"
            max="600000"
            step="50000"
            value={cashGrant}
            onChange={(e) => setCashGrant(parseFloat(e.target.value))}
            className="w-full accent-emerald-500 h-1.5 bg-slate-800 rounded-lg cursor-pointer"
          />
          <span className="text-[10px] text-slate-500 block">
            Multi-Purpose Cash Assistance (MPCA) grant
          </span>
        </div>

        {/* Fertilizer Subsidy */}
        <div className="bg-slate-950/60 p-4 rounded-xl border border-slate-800/80 space-y-2">
          <div className="flex justify-between items-center">
            <label className="text-slate-300 font-medium">Fertilizer Cost Subsidy:</label>
            <span className="font-mono font-bold text-emerald-400">
              {fertilizerSubsidy}%
            </span>
          </div>
          <input
            type="range"
            min="0"
            max="100"
            step="10"
            value={fertilizerSubsidy}
            onChange={(e) => setFertilizerSubsidy(parseFloat(e.target.value))}
            className="w-full accent-emerald-500 h-1.5 bg-slate-800 rounded-lg cursor-pointer"
          />
          <span className="text-[10px] text-slate-500 block">
            Direct discount on agricultural input costs
          </span>
        </div>

        {/* Debt Relief */}
        <div className="bg-slate-950/60 p-4 rounded-xl border border-slate-800/80 space-y-2">
          <div className="flex justify-between items-center">
            <label className="text-slate-300 font-medium">Debt Relief / Restructuring:</label>
            <span className="font-mono font-bold text-emerald-400">
              {debtRelief}%
            </span>
          </div>
          <input
            type="range"
            min="0"
            max="100"
            step="10"
            value={debtRelief}
            onChange={(e) => setDebtRelief(parseFloat(e.target.value))}
            className="w-full accent-emerald-500 h-1.5 bg-slate-800 rounded-lg cursor-pointer"
          />
          <span className="text-[10px] text-slate-500 block">
            Principal debt forgiveness or deferred repayment
          </span>
        </div>
      </div>

      {/* Crop recovery toggle & action button */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pt-1">
        <label className="flex items-center gap-2 text-xs text-slate-300 cursor-pointer">
          <input
            type="checkbox"
            checked={repairCropDamage}
            onChange={(e) => setRepairCropDamage(e.target.checked)}
            className="rounded bg-slate-950 border-slate-700 text-emerald-500 focus:ring-0"
          />
          <span className="font-medium text-emerald-300">
            Emergency Flood Rehabilitation (Restore Inundated Land)
          </span>
        </label>

        <button
          onClick={handleSimulate}
          disabled={isSimulating}
          className="flex items-center justify-center gap-2 px-5 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-xs shadow-md transition disabled:opacity-50"
        >
          {isSimulating ? 'Evaluating Policy...' : 'Run Counterfactual Simulation'}
          <ArrowRight className="w-3.5 h-3.5" />
        </button>
      </div>

      {/* Simulation Results Display */}
      {error && (
        <div className="p-3 rounded-lg bg-rose-950/50 border border-rose-800/50 text-rose-300 text-xs">
          {error}
        </div>
      )}

      {simulationResult && (
        <div className="mt-4 p-5 rounded-xl bg-slate-950/80 border border-emerald-500/30 space-y-4 animate-in fade-in">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-emerald-400 flex items-center gap-1.5">
              <CheckCircle className="w-4 h-4" />
              Simulation Outcome
            </span>
            <span className="text-xs font-mono font-bold px-2.5 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              Risk Reduction: -{simulationResult.risk_reduction_percentage}%
            </span>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
            <div className="bg-slate-900 p-2.5 rounded-lg border border-slate-800">
              <span className="text-slate-400 text-[10px] block">Baseline Risk</span>
              <span className="font-mono font-bold text-slate-300 text-sm">
                {(simulationResult.baseline_probability * 100).toFixed(1)}%
              </span>
              <span className="text-[10px] text-slate-500 block">({simulationResult.baseline_risk_level})</span>
            </div>

            <div className="bg-slate-900 p-2.5 rounded-lg border border-slate-800">
              <span className="text-slate-400 text-[10px] block">Simulated Risk</span>
              <span className="font-mono font-bold text-emerald-400 text-sm">
                {(simulationResult.simulated_probability * 100).toFixed(1)}%
              </span>
              <span className="text-[10px] text-emerald-400/80 block">({simulationResult.simulated_risk_level})</span>
            </div>

            <div className="col-span-2 bg-slate-900 p-2.5 rounded-lg border border-slate-800 flex flex-col justify-center">
              <span className="text-slate-400 text-[10px] block">Updated Decision Advice</span>
              <p className="text-slate-200 text-xs font-medium line-clamp-2 mt-0.5">
                {simulationResult.updated_recommendation}
              </p>
            </div>
          </div>

          <p className="text-xs text-slate-300 bg-emerald-950/20 border border-emerald-500/20 rounded-lg p-3 leading-relaxed">
            {simulationResult.impact_summary}
          </p>
        </div>
      )}
    </div>
  );
};

