import React from 'react';
import { Persona } from '../types';
import { AlertTriangle, CheckCircle, ShieldAlert, Sparkles, RefreshCw } from 'lucide-react';

interface PersonaSelectorProps {
  personas: Persona[];
  selectedPersonaId: string | null;
  onSelectPersona: (persona: Persona) => void;
  onResetCustom: () => void;
}

export const PersonaSelector: React.FC<PersonaSelectorProps> = ({
  personas,
  selectedPersonaId,
  onSelectPersona,
  onResetCustom,
}) => {
  return (
    <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-4 sm:p-6 backdrop-blur shadow-sm">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-4 sm:mb-5">
        <div>
          <div className="flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-emerald-400" />
            <h2 className="text-sm sm:text-base font-semibold text-white tracking-tight">
              One-Click Farmer Case Studies
            </h2>
            <span className="text-[10px] sm:text-xs bg-slate-800 text-slate-300 px-2 py-0.5 rounded-full border border-slate-700">
              Demo Presets
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Tap any scenario below to instantly populate realistic regional household data.
          </p>
        </div>

        <button
          onClick={onResetCustom}
          className={`flex items-center justify-center gap-1.5 text-xs px-3 py-2 rounded-xl border transition font-medium w-full sm:w-auto ${
            selectedPersonaId === null
              ? 'bg-emerald-600/20 text-emerald-300 border-emerald-500/40'
              : 'bg-slate-800 text-slate-300 border-slate-700 hover:bg-slate-700'
          }`}
        >
          <RefreshCw className="w-3.5 h-3.5" />
          Custom / Blank Profile
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-3.5 sm:gap-4">
        {personas.map((persona) => {
          const isSelected = selectedPersonaId === persona.id;

          const badgeStyles = {
            critical: 'bg-rose-500/10 text-rose-400 border-rose-500/30',
            success: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30',
            warning: 'bg-amber-500/10 text-amber-400 border-amber-500/30',
          }[persona.badge_type];

          const IconComponent = {
            critical: ShieldAlert,
            success: CheckCircle,
            warning: AlertTriangle,
          }[persona.badge_type];

          return (
            <div
              key={persona.id}
              onClick={() => onSelectPersona(persona)}
              className={`cursor-pointer rounded-xl p-4 border transition-all text-left flex flex-col justify-between active:scale-[0.99] ${
                isSelected
                  ? 'bg-slate-800/90 border-emerald-500 shadow-md ring-2 ring-emerald-500/20'
                  : 'bg-slate-950/60 border-slate-800/80 hover:border-slate-700 hover:bg-slate-900/40'
              }`}
            >
              <div>
                <div className="flex items-center justify-between gap-2 mb-2">
                  <span className={`text-[10px] font-semibold uppercase px-2 py-0.5 rounded-full border ${badgeStyles}`}>
                    {persona.badge_label}
                  </span>
                  <IconComponent className={`w-4 h-4 ${
                    persona.badge_type === 'critical' ? 'text-rose-400' :
                    persona.badge_type === 'success' ? 'text-emerald-400' : 'text-amber-400'
                  }`} />
                </div>

                <h3 className="font-semibold text-sm text-white">{persona.title}</h3>
                <p className="text-xs text-emerald-400/90 font-medium mb-1.5">{persona.location}</p>
                <p className="text-xs text-slate-400 line-clamp-3 leading-relaxed mb-3">
                  {persona.narrative}
                </p>
              </div>

              <div className="pt-2 border-t border-slate-800/80 mt-auto">
                <p className="text-[11px] text-slate-300 font-medium flex items-center gap-1">
                  <span className="text-slate-500">Outcome:</span>
                  <span className="truncate">{persona.expected_outcome.split('.')[0]}</span>
                </p>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
