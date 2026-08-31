"use client";

import React from 'react';
import {
  LayoutDashboard, Award, Compass, Sparkles, FileCheck, BookOpen, User, BarChart3, Settings, ShieldAlert, Layers
} from 'lucide-react';

interface SidebarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  roleMode: 'learner' | 'admin';
}

interface NavItem {
  id: string;
  label: string;
  icon: any;
  badge?: string;
}

export default function Sidebar({ activeTab, setActiveTab, roleMode }: SidebarProps) {
  const learnerNav: NavItem[] = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'competencies', label: 'My Competencies', icon: Award },
    { id: 'recommendations', label: 'Learning Recommendations', icon: BookOpen },
    { id: 'navigator', label: 'Career Navigator', icon: Compass, badge: 'Unique' },
    { id: 'assistant', label: 'AI Assistant', icon: Sparkles, badge: 'RAG' },
    { id: 'assessments', label: 'Assessments', icon: FileCheck },
    { id: 'my-learning', label: 'My Learning', icon: Layers }
  ];

  const adminNav: NavItem[] = [
    { id: 'admin-overview', label: 'Overview', icon: BarChart3 },
    { id: 'admin-heatmap', label: 'Workforce Competencies', icon: Award },
    { id: 'admin-gaps', label: 'Skill Gaps', icon: ShieldAlert },
    { id: 'admin-assessments', label: 'Assessment Generator', icon: FileCheck },
    { id: 'admin-rules', label: 'Rules & Framework', icon: Settings }
  ];

  const navItems = roleMode === 'admin' ? adminNav : learnerNav;

  return (
    <aside className="w-64 bg-slate-900 border-r border-slate-800 text-slate-300 min-h-[calc(100vh-57px)] p-4 flex flex-col justify-between">
      <div className="space-y-6">
        <div className="px-3 py-2 text-[11px] font-bold uppercase tracking-wider text-slate-500">
          {roleMode === 'admin' ? 'Government Admin Panel' : 'Officer Portal'}
        </div>

        <nav className="space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl text-xs font-semibold transition ${
                  isActive
                    ? 'bg-blue-600 text-white shadow-md shadow-blue-900/50'
                    : 'text-slate-400 hover:text-white hover:bg-slate-800/70'
                }`}
              >
                <div className="flex items-center space-x-3">
                  <Icon className={`w-4 h-4 ${isActive ? 'text-white' : 'text-slate-400'}`} />
                  <span>{item.label}</span>
                </div>
                {item.badge && (
                  <span className={`text-[9px] font-bold uppercase px-1.5 py-0.5 rounded-md ${
                    isActive ? 'bg-white text-blue-700' : 'bg-blue-500/20 text-blue-400 border border-blue-400/30'
                  }`}>
                    {item.badge}
                  </span>
                )}
              </button>
            );
          })}
        </nav>
      </div>

      <div className="pt-4 border-t border-slate-800 text-center">
        <div className="p-3 bg-slate-800/60 rounded-xl border border-slate-700/50">
          <span className="text-[10px] text-slate-400 block font-medium">MoSPI Competency Model</span>
          <span className="text-xs font-bold text-white block mt-0.5">NSSTA Certified v1.2</span>
        </div>
      </div>
    </aside>
  );
}
