"use client";

import React from 'react';

interface HeatmapProps {
  data: any[];
}

export default function AdminHeatmap({ data }: HeatmapProps) {
  const getSeverityBg = (gapAvg: number) => {
    if (gapAvg <= 0.3) return 'bg-emerald-500 text-white';
    if (gapAvg <= 0.8) return 'bg-yellow-400 text-slate-900';
    if (gapAvg <= 1.5) return 'bg-orange-500 text-white';
    return 'bg-red-600 text-white font-bold';
  };

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-xs text-left border-collapse">
        <thead>
          <tr className="bg-slate-900 text-white">
            <th className="p-3 font-semibold rounded-tl-lg">Government Role</th>
            <th className="p-3 font-semibold">Department</th>
            <th className="p-3 text-center font-semibold">Statistical</th>
            <th className="p-3 text-center font-semibold">Technical</th>
            <th className="p-3 text-center font-semibold">Digital Gov</th>
            <th className="p-3 text-center font-semibold">Behavioural</th>
            <th className="p-3 text-center font-semibold">Data</th>
            <th className="p-3 text-center font-semibold rounded-tr-lg">Leadership</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-200">
          {data && data.length > 0 ? (
            data.map((item, idx) => (
              <tr key={idx} className="hover:bg-slate-50 transition">
                <td className="p-3 font-bold text-slate-900">{item.role_name}</td>
                <td className="p-3 text-slate-500">{item.department}</td>
                <td className="p-2 text-center">
                  <span className={`px-2.5 py-1 rounded-md text-xs inline-block w-12 text-center ${getSeverityBg(item.statistical_avg_gap)}`}>
                    {item.statistical_avg_gap.toFixed(1)}
                  </span>
                </td>
                <td className="p-2 text-center">
                  <span className={`px-2.5 py-1 rounded-md text-xs inline-block w-12 text-center ${getSeverityBg(item.technical_avg_gap)}`}>
                    {item.technical_avg_gap.toFixed(1)}
                  </span>
                </td>
                <td className="p-2 text-center">
                  <span className={`px-2.5 py-1 rounded-md text-xs inline-block w-12 text-center ${getSeverityBg(item.governance_avg_gap)}`}>
                    {item.governance_avg_gap.toFixed(1)}
                  </span>
                </td>
                <td className="p-2 text-center">
                  <span className={`px-2.5 py-1 rounded-md text-xs inline-block w-12 text-center ${getSeverityBg(item.behavioural_avg_gap)}`}>
                    {item.behavioural_avg_gap.toFixed(1)}
                  </span>
                </td>
                <td className="p-2 text-center">
                  <span className={`px-2.5 py-1 rounded-md text-xs inline-block w-12 text-center ${getSeverityBg(item.data_avg_gap)}`}>
                    {item.data_avg_gap.toFixed(1)}
                  </span>
                </td>
                <td className="p-2 text-center">
                  <span className={`px-2.5 py-1 rounded-md text-xs inline-block w-12 text-center ${getSeverityBg(item.leadership_avg_gap)}`}>
                    {item.leadership_avg_gap.toFixed(1)}
                  </span>
                </td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan={8} className="p-4 text-center text-slate-400">Loading Heatmap...</td>
            </tr>
          )}
        </tbody>
      </table>

      <div className="flex items-center justify-end space-x-4 text-[11px] text-slate-500 mt-3 font-medium">
        <div className="flex items-center space-x-1.5">
          <span className="w-3 h-3 bg-emerald-500 rounded"></span>
          <span>Satisfied (&lt;0.3)</span>
        </div>
        <div className="flex items-center space-x-1.5">
          <span className="w-3 h-3 bg-yellow-400 rounded"></span>
          <span>Low Gap (0.4 - 0.8)</span>
        </div>
        <div className="flex items-center space-x-1.5">
          <span className="w-3 h-3 bg-orange-500 rounded"></span>
          <span>Medium Gap (0.9 - 1.5)</span>
        </div>
        <div className="flex items-center space-x-1.5">
          <span className="w-3 h-3 bg-red-600 rounded"></span>
          <span>Critical Gap (&gt;1.5)</span>
        </div>
      </div>
    </div>
  );
}
