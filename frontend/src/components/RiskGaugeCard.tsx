import React from 'react';
import { PredictionResponse } from '../types';
import { AlertCircle, CheckCircle2, AlertTriangle, Info, Scale } from 'lucide-react';

interface RiskGaugeCardProps {
  prediction: PredictionResponse | null;
  isLoading: boolean;
}

export const RiskGaugeCard: React.FC<RiskGaugeCardProps> = ({
  prediction,
  isLoading,
}) => {
  if (isLoading) {
    return (
      <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-8 backdrop-blur text-center flex flex-col items-center justify-center min-h-[350px]">
        <div className="w-12 h-12 rounded-full border-4 border-emerald-500/20 border-t-emerald-500 animate-spin mb-4" />
        <p className="text-sm text-slate-300 font-medium">Scoring household financial vulnerability...</p>
        <p className="text-xs text-slate-500 mt-1">Executing calibrated pipeline inference</p>
      </div>
    );
  }

  if (!prediction) {
    return (
      <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-8 backdrop-blur text-center flex flex-col items-center justify-center min-h-[350px]">
        <Info className="w-10 h-10 text-slate-600 mb-3" />
        <p className="text-sm text-slate-400 font-medium">No assessment generated yet</p>
        <p className="text-xs text-slate-500 mt-1">Select a demo persona or click "Evaluate Household Vulnerability"</p>
      </div>
    );
  }

  const {
    vulnerability_percentage,
    risk_level,
    recommendation,
    model_used,
    computed_indicators,
    key_drivers,
  } = prediction;

  const isHigh = risk_level === 'High risk';
  const isMedium = risk_level === 'Medium risk';

  const riskColor = isHigh ? 'text-rose-400' : isMedium ? 'text-amber-400' : 'text-emerald-400';
  const riskBg = isHigh ? 'bg-rose-500/10 border-rose-500/30' : isMedium ? 'bg-amber-500/10 border-amber-500/30' : 'bg-emerald-500/10 border-emerald-500/30';
  const bannerBg = isHigh ? 'bg-rose-950/40 border-rose-800/50 text-rose-200' : isMedium ? 'bg-amber-950/40 border-amber-800/50 text-amber-200' : 'bg-emerald-950/40 border-emerald-800/50 text-emerald-200';

  const StatusIcon = isHigh ? AlertCircle : isMedium ? AlertTriangle : CheckCircle2;

  return (
    <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-4 sm:p-6 backdrop-blur shadow-sm space-y-5 sm:space-y-6">
      
      {/* Header */}
      <div className="flex items-center justify-between pb-3 border-b border-slate-800">
        <div>
          <h2 className="text-sm sm:text-base font-semibold text-white tracking-tight">Financial Vulnerability Assessment</h2>
          <p className="text-[11px] sm:text-xs text-slate-400">Powered by {model_used}</p>
        </div>
        <span className={`text-[11px] sm:text-xs font-semibold px-2.5 sm:px-3 py-1 rounded-full border ${riskBg} ${riskColor}`}>
          {risk_level}
        </span>
      </div>

      {/* Visual Radial Dial / Progress */}
      <div className="flex flex-col sm:flex-row items-center gap-5 sm:gap-6 justify-around bg-slate-950/60 rounded-xl p-4 sm:p-5 border border-slate-800/80">
        
        {/* Gauge display */}
        <div className="flex flex-col items-center">
          <div className="relative w-32 h-32 sm:w-36 sm:h-36 flex items-center justify-center">
            {/* Background Circle */}
            <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
              <circle
                cx="50"
                cy="50"
                r="42"
                strokeWidth="10"
                className="text-slate-800 stroke-current"
                fill="transparent"
              />
              {/* Progress Circle */}
              <circle
                cx="50"
                cy="50"
                r="42"
                strokeWidth="10"
                strokeDasharray={264}
                strokeDashoffset={264 - (264 * Math.min(100, Math.max(0, vulnerability_percentage))) / 100}
                strokeLinecap="round"
                className={`stroke-current transition-all duration-1000 ${
                  isHigh ? 'text-rose-500' : isMedium ? 'text-amber-500' : 'text-emerald-500'
                }`}
                fill="transparent"
              />
            </svg>
            <div className="absolute flex flex-col items-center">
              <span className={`text-3xl font-bold font-mono ${riskColor}`}>
                {vulnerability_percentage}%
              </span>
              <span className="text-[10px] text-slate-400 uppercase tracking-wider font-semibold">
                Risk Score
              </span>
            </div>
          </div>
        </div>

        {/* Economic Ratios Summary */}
        <div className="grid grid-cols-2 gap-3 text-xs w-full sm:w-auto">
          <div className="bg-slate-900 p-2.5 rounded-lg border border-slate-800">
            <span className="text-slate-400 block text-[10px]">Income-to-MEB Ratio</span>
            <span className={`font-mono font-bold text-sm ${
              computed_indicators.income_to_meb_ratio < 0.8 ? 'text-rose-400' : 'text-emerald-400'
            }`}>
              {(computed_indicators.income_to_meb_ratio * 100).toFixed(1)}%
            </span>
          </div>

          <div className="bg-slate-900 p-2.5 rounded-lg border border-slate-800">
            <span className="text-slate-400 block text-[10px]">Debt-to-Income (DTI)</span>
            <span className={`font-mono font-bold text-sm ${
              computed_indicators.debt_to_income_ratio > 1.0 ? 'text-rose-400' : 'text-slate-200'
            }`}>
              {computed_indicators.debt_to_income_ratio.toFixed(2)}x
            </span>
          </div>

          <div className="bg-slate-900 p-2.5 rounded-lg border border-slate-800">
            <span className="text-slate-400 block text-[10px]">MEB Gap (Deficit)</span>
            <span className="font-mono font-bold text-sm text-slate-200">
              {computed_indicators.meb_gap.toLocaleString()} MMK
            </span>
          </div>

          <div className="bg-slate-900 p-2.5 rounded-lg border border-slate-800">
            <span className="text-slate-400 block text-[10px]">Household MEB Basket</span>
            <span className="font-mono font-bold text-sm text-slate-200">
              {computed_indicators.household_meb_requirement.toLocaleString()} MMK
            </span>
          </div>
        </div>
      </div>

      {/* Decision-Support Recommendation Banner */}
      <div className={`p-4 rounded-xl border flex items-start gap-3 ${bannerBg}`}>
        <StatusIcon className="w-5 h-5 flex-shrink-0 mt-0.5" />
        <div>
          <h4 className="font-semibold text-xs tracking-wide uppercase mb-1">
            Responsible Decision-Support Recommendation
          </h4>
          <p className="text-xs leading-relaxed opacity-95">
            {recommendation}
          </p>
        </div>
      </div>

      {/* Key Drivers / Explainability Badges */}
      <div>
        <h4 className="text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2.5 flex items-center gap-1.5">
          <Scale className="w-3.5 h-3.5 text-slate-400" />
          Primary Contributing Factors
        </h4>
        <div className="space-y-2">
          {key_drivers.map((driver, idx) => {
            const isNegative = driver.impact === 'risk_increasing';
            return (
              <div
                key={idx}
                className="flex items-start gap-2 text-xs p-2.5 rounded-lg bg-slate-950/60 border border-slate-800/80"
              >
                <span className={`text-[10px] px-1.5 py-0.5 rounded font-mono font-bold uppercase mt-0.5 ${
                  isNegative ? 'bg-rose-500/20 text-rose-300' : 'bg-emerald-500/20 text-emerald-300'
                }`}>
                  {isNegative ? '+ Risk' : '- Mitigation'}
                </span>
                <div>
                  <span className="font-semibold text-slate-200">{driver.name}: </span>
                  <span className="text-slate-400">{driver.description}</span>
                </div>
              </div>
            );
          })}
        </div>
      </div>

    </div>
  );
};
