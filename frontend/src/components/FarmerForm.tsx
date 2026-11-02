import React from 'react';
import { FarmerProfile, MetadataResponse } from '../types';
import { Home, DollarSign, Sprout, HeartPulse, Sliders } from 'lucide-react';

interface FarmerFormProps {
  profile: FarmerProfile;
  metadata: MetadataResponse | null;
  onChange: (updated: FarmerProfile) => void;
  onSubmit: () => void;
  isLoading: boolean;
}

export const FarmerForm: React.FC<FarmerFormProps> = ({
  profile,
  metadata,
  onChange,
  onSubmit,
  isLoading,
}) => {
  const handleChange = (field: keyof FarmerProfile, value: any) => {
    onChange({
      ...profile,
      [field]: value,
    });
  };

  const regions = metadata?.states_regions || [
    'Ayeyarwady', 'Bago', 'Chin', 'Kachin', 'Kayah', 'Kayin',
    'Magway', 'Mandalay', 'Mon', 'Rakhine', 'Sagaing', 'Shan North', 'Shan South', 'Tanintharyi'
  ];

  const crops = metadata?.crops || ['Maize', 'Mixed', 'Oilseed', 'Pulses', 'Rice', 'Vegetables'];
  const displacementStatuses = metadata?.displacement_statuses || ['IDP', 'Resident', 'Returnee'];

  return (
    <div className="space-y-6">
      {/* Grid of form cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        
        {/* CARD 1: Location & Demographics */}
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 shadow-sm space-y-4">
          <div className="flex items-center gap-2 pb-2 border-b border-slate-800 text-white font-semibold text-sm">
            <Home className="w-4 h-4 text-emerald-400" />
            <h3>1. Location & Demographics</h3>
          </div>

          <div className="grid grid-cols-2 gap-3 text-xs">
            <div>
              <label className="block text-slate-400 mb-1 font-medium">State / Region</label>
              <select
                value={profile.state_region}
                onChange={(e) => handleChange('state_region', e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-emerald-500 text-xs"
              >
                {regions.map((r) => (
                  <option key={r} value={r}>{r}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-slate-400 mb-1 font-medium">Displacement Status</label>
              <select
                value={profile.displacement_status}
                onChange={(e) => handleChange('displacement_status', e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-emerald-500 text-xs"
              >
                {displacementStatuses.map((s) => (
                  <option key={s} value={s}>{s}</option>
                ))}
              </select>
            </div>
          </div>

          <div className="grid grid-cols-3 gap-3 text-xs">
            <div>
              <label className="block text-slate-400 mb-1 font-medium">Family Size</label>
              <input
                type="number"
                min="1"
                max="20"
                value={profile.household_size}
                onChange={(e) => handleChange('household_size', parseInt(e.target.value) || 1)}
                className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-emerald-500 text-xs"
              />
            </div>

            <div>
              <label className="block text-slate-400 mb-1 font-medium">Female Head?</label>
              <select
                value={profile.female_headed_household}
                onChange={(e) => handleChange('female_headed_household', parseInt(e.target.value))}
                className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-emerald-500 text-xs"
              >
                <option value={0}>No</option>
                <option value={1}>Yes</option>
              </select>
            </div>

            <div>
              <label className="block text-slate-400 mb-1 font-medium">Disability?</label>
              <select
                value={profile.disability_present}
                onChange={(e) => handleChange('disability_present', parseInt(e.target.value))}
                className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-emerald-500 text-xs"
              >
                <option value={0}>No</option>
                <option value={1}>Yes</option>
              </select>
            </div>
          </div>
        </div>

        {/* CARD 2: Financial Health */}
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 shadow-sm space-y-4">
          <div className="flex items-center gap-2 pb-2 border-b border-slate-800 text-white font-semibold text-sm">
            <DollarSign className="w-4 h-4 text-emerald-400" />
            <h3>2. Financial Health (MMK)</h3>
          </div>

          <div className="grid grid-cols-2 gap-3 text-xs">
            <div>
              <label className="block text-slate-400 mb-1 font-medium">Monthly Income</label>
              <input
                type="number"
                step="10000"
                value={profile.monthly_income}
                onChange={(e) => handleChange('monthly_income', parseFloat(e.target.value) || 0)}
                className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-emerald-500 text-xs font-mono"
              />
            </div>

            <div>
              <label className="block text-slate-400 mb-1 font-medium">Total Outstanding Debt</label>
              <input
                type="number"
                step="10000"
                value={profile.total_debt}
                onChange={(e) => {
                  const val = parseFloat(e.target.value) || 0;
                  onChange({
                    ...profile,
                    total_debt: val,
                    has_debt: val > 0 ? 1 : 0,
                  });
                }}
                className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-emerald-500 text-xs font-mono"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3 text-xs">
            <div>
              <label className="block text-slate-400 mb-1 font-medium">Monthly Debt Repayment</label>
              <input
                type="number"
                step="5000"
                value={profile.monthly_debt_repayment}
                onChange={(e) => handleChange('monthly_debt_repayment', parseFloat(e.target.value) || 0)}
                className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-emerald-500 text-xs font-mono"
              />
            </div>

            <div>
              <label className="block text-slate-400 mb-1 font-medium">Savings Buffer (Weeks)</label>
              <input
                type="number"
                step="0.5"
                min="0"
                value={profile.savings_duration_weeks}
                onChange={(e) => handleChange('savings_duration_weeks', parseFloat(e.target.value) || 0)}
                className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-emerald-500 text-xs font-mono"
              />
            </div>
          </div>
        </div>

        {/* CARD 3: Agriculture & Yield */}
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 shadow-sm space-y-4">
          <div className="flex items-center gap-2 pb-2 border-b border-slate-800 text-white font-semibold text-sm">
            <Sprout className="w-4 h-4 text-emerald-400" />
            <h3>3. Agriculture & Production</h3>
          </div>

          <div className="grid grid-cols-2 gap-3 text-xs">
            <div>
              <label className="block text-slate-400 mb-1 font-medium">Primary Crop</label>
              <select
                value={profile.main_crop}
                onChange={(e) => handleChange('main_crop', e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-emerald-500 text-xs"
              >
                {crops.map((c) => (
                  <option key={c} value={c}>{c}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-slate-400 mb-1 font-medium">Cultivated Land (Acres)</label>
              <input
                type="number"
                step="0.5"
                value={profile.farm_size_acres}
                onChange={(e) => handleChange('farm_size_acres', parseFloat(e.target.value) || 0)}
                className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-emerald-500 text-xs font-mono"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3 text-xs">
            <div>
              <label className="block text-slate-400 mb-1 font-medium">Fertilizer Cost (MMK)</label>
              <input
                type="number"
                step="10000"
                value={profile.fertilizer_cost}
                onChange={(e) => handleChange('fertilizer_cost', parseFloat(e.target.value) || 0)}
                className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-emerald-500 text-xs font-mono"
              />
            </div>

            <div>
              <label className="block text-slate-400 mb-1 font-medium">Irrigation Access?</label>
              <select
                value={profile.irrigation_access}
                onChange={(e) => handleChange('irrigation_access', parseInt(e.target.value))}
                className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-emerald-500 text-xs"
              >
                <option value={1}>Yes (Irrigated)</option>
                <option value={0}>No (Rainfed)</option>
              </select>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3 pt-1">
            <label className="flex items-center gap-2 text-xs text-slate-300 cursor-pointer">
              <input
                type="checkbox"
                checked={profile.crop_damage_recent === 1}
                onChange={(e) => handleChange('crop_damage_recent', e.target.checked ? 1 : 0)}
                className="rounded bg-slate-950 border-slate-700 text-emerald-500 focus:ring-0"
              />
              <span className="font-medium text-rose-300">Recent Crop Inundation / Damage?</span>
            </label>

            <label className="flex items-center gap-2 text-xs text-slate-300 cursor-pointer">
              <input
                type="checkbox"
                checked={profile.market_access === 1}
                onChange={(e) => handleChange('market_access', e.target.checked ? 1 : 0)}
                className="rounded bg-slate-950 border-slate-700 text-emerald-500 focus:ring-0"
              />
              <span className="font-medium">Market Access Functional?</span>
            </label>
          </div>
        </div>

        {/* CARD 4: Coping Capacity & Food Security */}
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 shadow-sm space-y-4">
          <div className="flex items-center gap-2 pb-2 border-b border-slate-800 text-white font-semibold text-sm">
            <HeartPulse className="w-4 h-4 text-emerald-400" />
            <h3>4. Stress & Coping Index</h3>
          </div>

          <div className="space-y-3 text-xs">
            <div>
              <div className="flex justify-between items-center mb-1">
                <label className="text-slate-400 font-medium">
                  Reduced Coping Strategy Index (rCSI):
                </label>
                <span className="text-emerald-400 font-mono font-bold">{profile.rCSI_score}</span>
              </div>
              <input
                type="range"
                min="0"
                max="50"
                step="1"
                value={profile.rCSI_score}
                onChange={(e) => handleChange('rCSI_score', parseFloat(e.target.value))}
                className="w-full accent-emerald-500 h-1.5 bg-slate-800 rounded-lg cursor-pointer"
              />
              <div className="flex justify-between text-[10px] text-slate-500 mt-0.5">
                <span>0 (No stress)</span>
                <span>20 (Moderate stress)</span>
                <span>50 (Severe stress)</span>
              </div>
            </div>

            <div>
              <div className="flex justify-between items-center mb-1">
                <label className="text-slate-400 font-medium">
                  Basic Needs Capacity Score:
                </label>
                <span className="text-emerald-400 font-mono font-bold">{profile.basic_needs_score} / 3</span>
              </div>
              <input
                type="range"
                min="0"
                max="3"
                step="1"
                value={profile.basic_needs_score}
                onChange={(e) => handleChange('basic_needs_score', parseFloat(e.target.value))}
                className="w-full accent-emerald-500 h-1.5 bg-slate-800 rounded-lg cursor-pointer"
              />
              <div className="flex justify-between text-[10px] text-slate-500 mt-0.5">
                <span>0 (Unable to meet needs)</span>
                <span>3 (Fully sufficient)</span>
              </div>
            </div>
          </div>
        </div>

      </div>

      {/* Trigger Predict Button */}
      <div className="flex justify-end">
        <button
          onClick={onSubmit}
          disabled={isLoading}
          className="flex items-center gap-2 px-6 py-3 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-sm shadow-lg shadow-emerald-900/30 transition disabled:opacity-50"
        >
          <Sliders className="w-4 h-4" />
          {isLoading ? 'Running ML Inference...' : 'Evaluate Household Vulnerability'}
        </button>
      </div>
    </div>
  );
};

