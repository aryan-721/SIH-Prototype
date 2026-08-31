"use client";

import React from 'react';
import { X, CheckCircle2, AlertTriangle, ArrowRight, ShieldCheck, Info } from 'lucide-react';

interface ExplainabilityModalProps {
  isOpen: boolean;
  onClose: () => void;
  data: any;
}

export default function ExplainabilityModal({ isOpen, onClose, data }: ExplainabilityModalProps) {
  if (!isOpen || !data) return null;

  const {
    learner_name,
    current_role,
    target_role,
    competency_name,
    domain,
    assessed_level,
    required_level,
    gap,
    severity,
    course_title,
    course_provider,
    course_duration,
    coverage_level,
    recommendation_reason,
    score,
    score_breakdown
  } = data;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 backdrop-blur-sm p-4 animate-fade-in">
      <div className="bg-white rounded-2xl shadow-2xl border border-slate-200 w-full max-w-3xl overflow-hidden max-h-[90vh] flex flex-col">
        
        {/* Header */}
        <div className="bg-slate-900 text-white px-6 py-4 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-blue-600 rounded-lg">
              <ShieldCheck className="w-5 h-5 text-white" />
            </div>
            <div>
              <h2 className="text-lg font-bold">Competency Explainability Trail</h2>
              <p className="text-xs text-slate-300">Auditable, evidence-based recommendation reasoning</p>
            </div>
          </div>
          <button 
            onClick={onClose}
            className="p-1.5 text-slate-400 hover:text-white hover:bg-slate-800 rounded-lg transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 overflow-y-auto space-y-6">

          {/* Course Badge */}
          <div className="bg-blue-50 border border-blue-200 rounded-xl p-4 flex items-center justify-between">
            <div>
              <span className="text-xs font-semibold text-blue-700 uppercase tracking-wider">Recommended Course</span>
              <h3 className="text-xl font-bold text-slate-900">{course_title}</h3>
              <p className="text-sm text-slate-600">Provider: {course_provider} | Duration: {course_duration}</p>
            </div>
            <div className="text-right">
              <span className="text-2xl font-black text-blue-700">{score}/100</span>
              <p className="text-xs text-slate-500 font-medium">Relevance Score</p>
            </div>
          </div>

          {/* Visual Trail Flow (Image 3 layout) */}
          <div className="border border-slate-200 rounded-xl p-5 bg-slate-50">
            <h4 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-4 flex items-center gap-1.5">
              <Info className="w-4 h-4 text-blue-600" /> Audit Trail (Why this course?)
            </h4>

            <div className="grid grid-cols-5 gap-2 text-center text-xs">
              <div className="p-3 bg-white rounded-lg border border-slate-200 shadow-sm">
                <span className="text-slate-400 font-medium block mb-1">Profile</span>
                <span className="font-bold text-slate-800 block text-ellipsis overflow-hidden">{learner_name}</span>
                <span className="text-[10px] text-slate-500">{current_role}</span>
              </div>

              <div className="p-3 bg-white rounded-lg border border-slate-200 shadow-sm">
                <span className="text-slate-400 font-medium block mb-1">Assessed Level</span>
                <span className="font-bold text-slate-800 block text-base">{assessed_level}</span>
                <span className="text-[10px] text-slate-500">Current Capability</span>
              </div>

              <div className="p-3 bg-white rounded-lg border border-slate-200 shadow-sm">
                <span className="text-slate-400 font-medium block mb-1">Required Level</span>
                <span className="font-bold text-slate-800 block text-base">{required_level}</span>
                <span className="text-[10px] text-slate-500">Role Benchmark</span>
              </div>

              <div className="p-3 bg-red-50 rounded-lg border border-red-200 shadow-sm">
                <span className="text-red-600 font-medium block mb-1">Verified Gap</span>
                <span className="font-bold text-red-700 block text-base">{gap} Level{gap > 1 ? 's' : ''}</span>
                <span className="text-[10px] text-red-600 font-bold uppercase">{severity}</span>
              </div>

              <div className="p-3 bg-emerald-50 rounded-lg border border-emerald-200 shadow-sm">
                <span className="text-emerald-600 font-medium block mb-1">Course Coverage</span>
                <span className="font-bold text-emerald-800 block text-base">Level {coverage_level}</span>
                <span className="text-[10px] text-emerald-600 font-semibold">Verified Match</span>
              </div>
            </div>
          </div>

          {/* Reasoning Text */}
          <div className="bg-slate-900 text-white rounded-xl p-4 space-y-2">
            <h4 className="text-xs font-bold text-blue-400 uppercase tracking-wider">Deterministic Evidence Reasoning</h4>
            <p className="text-sm leading-relaxed text-slate-200">
              "{recommendation_reason}"
            </p>
          </div>

          {/* Score Breakdown Bars */}
          <div className="space-y-3">
            <h4 className="text-xs font-bold text-slate-500 uppercase tracking-wider">Score Breakdown Metrics</h4>
            
            <div className="grid grid-cols-5 gap-3">
              <div className="bg-slate-50 border border-slate-200 p-3 rounded-lg text-center">
                <span className="text-xs text-slate-500 block">Gap Match</span>
                <span className="text-lg font-bold text-blue-700">{score_breakdown.gap_match}/40</span>
              </div>

              <div className="bg-slate-50 border border-slate-200 p-3 rounded-lg text-center">
                <span className="text-xs text-slate-500 block">Role Relevance</span>
                <span className="text-lg font-bold text-blue-700">{score_breakdown.target_role}/25</span>
              </div>

              <div className="bg-slate-50 border border-slate-200 p-3 rounded-lg text-center">
                <span className="text-xs text-slate-500 block">Coverage</span>
                <span className="text-lg font-bold text-blue-700">{score_breakdown.competency_coverage}/15</span>
              </div>

              <div className="bg-slate-50 border border-slate-200 p-3 rounded-lg text-center">
                <span className="text-xs text-slate-500 block">Preference</span>
                <span className="text-lg font-bold text-blue-700">{score_breakdown.preference}/10</span>
              </div>

              <div className="bg-slate-50 border border-slate-200 p-3 rounded-lg text-center">
                <span className="text-xs text-slate-500 block">Quality</span>
                <span className="text-lg font-bold text-blue-700">{score_breakdown.quality}/10</span>
              </div>
            </div>
          </div>

        </div>

        {/* Footer */}
        <div className="bg-slate-50 border-t border-slate-200 px-6 py-3 flex items-center justify-between text-xs text-slate-500">
          <span>Rules Version: 1.2.0 | MoSPI Framework Standard</span>
          <button 
            onClick={onClose}
            className="px-4 py-2 bg-slate-900 text-white rounded-lg font-medium hover:bg-slate-800 transition"
          >
            Close Trail
          </button>
        </div>

      </div>
    </div>
  );
}
