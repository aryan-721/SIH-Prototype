"use client";

import React from 'react';
import {
  Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Tooltip
} from 'recharts';

interface CompetencyRadarChartProps {
  data?: any[];
}

const defaultData = [
  { domain: 'Statistical', assessed: 4, required: 4, fullMark: 5 },
  { domain: 'Technical', assessed: 1, required: 3, fullMark: 5 },
  { domain: 'Digital Governance', assessed: 3, required: 3, fullMark: 5 },
  { domain: 'Behavioural', assessed: 2, required: 2, fullMark: 5 },
  { domain: 'Data', assessed: 2, required: 3, fullMark: 5 },
  { domain: 'Leadership', assessed: 1, required: 2, fullMark: 5 }
];

export default function CompetencyRadarChart({ data }: CompetencyRadarChartProps) {
  const chartData = data && data.length > 0 ? data : defaultData;

  return (
    <div className="w-full h-[280px]">
      <ResponsiveContainer width="100%" height="100%">
        <RadarChart cx="50%" cy="50%" outerRadius="75%" data={chartData}>
          <PolarGrid stroke="#e2e8f0" />
          <PolarAngleAxis dataKey="domain" tick={{ fill: '#475569', fontSize: 11, fontWeight: 600 }} />
          <PolarRadiusAxis angle={30} domain={[0, 5]} tick={{ fill: '#94a3b8', fontSize: 10 }} />
          
          <Radar
            name="Assessed Capability"
            dataKey="assessed"
            stroke="#2563eb"
            fill="#3b82f6"
            fillOpacity={0.4}
          />
          <Radar
            name="Required Level"
            dataKey="required"
            stroke="#dc2626"
            fill="#ef4444"
            fillOpacity={0.15}
            strokeDasharray="4 4"
          />
          <Tooltip />
        </RadarChart>
      </ResponsiveContainer>

      <div className="flex items-center justify-center space-x-6 text-xs text-slate-600 mt-1 font-medium">
        <div className="flex items-center space-x-2">
          <span className="w-3 h-3 rounded-full bg-blue-500 inline-block"></span>
          <span>Assessed Level</span>
        </div>
        <div className="flex items-center space-x-2">
          <span className="w-3 h-3 rounded-full border border-red-500 bg-red-100 inline-block"></span>
          <span>Role Required Benchmark</span>
        </div>
      </div>
    </div>
  );
}
