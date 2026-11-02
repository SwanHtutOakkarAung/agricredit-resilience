import React from 'react';
import { Activity, BookOpen, ExternalLink, Cpu } from 'lucide-react';
import { HealthResponse } from '../types';
import { DOCS_URL } from '../api';

interface NavbarProps {
  health: HealthResponse | null;
  isHealthLoading: boolean;
  modelType: 'logistic_regression' | 'decision_tree';
  onModelChange: (model: 'logistic_regression' | 'decision_tree') => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  health,
  isHealthLoading,
  modelType,
  onModelChange,
}) => {
  return (
    <header className="border-b border-slate-800 bg-slate-900/80 backdrop-blur sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Brand */}
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-xl shadow-inner">
            🌾
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="font-bold text-lg text-white tracking-tight">AgriCredit Resilience</h1>
              <span className="text-xs px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-medium">
                Decision Support
              </span>
            </div>
            <p className="text-xs text-slate-400">Explainable Financial Vulnerability Engine for Rural Myanmar</p>
          </div>
        </div>

        {/* Right Actions */}
        <div className="flex items-center gap-4">
          {/* Model Selector */}
          <div className="hidden sm:flex items-center gap-1.5 bg-slate-950 p-1 rounded-lg border border-slate-800 text-xs">
            <span className="px-2 text-slate-400 flex items-center gap-1 font-medium">
              <Cpu className="w-3.5 h-3.5 text-slate-500" />
              Model:
            </span>
            <button
              onClick={() => onModelChange('logistic_regression')}
              className={`px-2.5 py-1 rounded font-medium transition ${
                modelType === 'logistic_regression'
                  ? 'bg-emerald-600 text-white shadow-sm'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              Logistic Regression
            </button>
            <button
              onClick={() => onModelChange('decision_tree')}
              className={`px-2.5 py-1 rounded font-medium transition ${
                modelType === 'decision_tree'
                  ? 'bg-emerald-600 text-white shadow-sm'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              Decision Tree
            </button>
          </div>

          {/* API Health Status */}
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-950 border border-slate-800 text-xs">
            {isHealthLoading ? (
              <span className="flex items-center gap-1.5 text-slate-400">
                <Activity className="w-3.5 h-3.5 animate-spin text-slate-500" />
                Connecting API...
              </span>
            ) : health?.status === 'healthy' ? (
              <span className="flex items-center gap-1.5 text-emerald-400 font-medium">
                <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
                FastAPI v{health.api_version}
              </span>
            ) : (
              <span className="flex items-center gap-1.5 text-amber-400 font-medium" title="Render free tier takes ~30s to wake up on first visit">
                <Activity className="w-3.5 h-3.5 animate-spin text-amber-500" />
                Waking up API...
              </span>
            )}
          </div>

          {/* Swagger Link */}
          <a
            href={DOCS_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="hidden md:flex items-center gap-1.5 text-xs text-slate-300 hover:text-white bg-slate-800 hover:bg-slate-700 px-3 py-1.5 rounded-lg border border-slate-700 transition"
          >
            <BookOpen className="w-3.5 h-3.5 text-emerald-400" />
            Swagger Docs
            <ExternalLink className="w-3 h-3 text-slate-400" />
          </a>
        </div>
      </div>
    </header>
  );
};
