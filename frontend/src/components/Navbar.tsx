"use client";

import React from 'react';
import { ShieldCheck, UserCheck, Bell, ChevronDown, Award } from 'lucide-react';

interface NavbarProps {
  user: any;
  currentRoleMode: 'learner' | 'admin';
  onToggleRoleMode: () => void;
}

export default function Navbar({ user, currentRoleMode, onToggleRoleMode }: NavbarProps) {
  return (
    <header className="bg-slate-900 border-b border-slate-800 text-white sticky top-0 z-40 px-6 py-3.5 flex items-center justify-between shadow-md">
      {/* Brand & Logo */}
      <div className="flex items-center space-x-4">
        <div className="flex items-center space-x-2.5">
          <div className="bg-gradient-to-tr from-blue-600 to-indigo-500 p-2 rounded-xl text-white shadow-lg">
            <ShieldCheck className="w-6 h-6" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="font-extrabold text-lg tracking-tight text-white">SkillIntelligence</span>
              <span className="text-[10px] uppercase font-bold bg-blue-500/20 text-blue-300 border border-blue-400/30 px-2 py-0.5 rounded-full">
                MoSPI / NSSTA
              </span>
            </div>
            <p className="text-[11px] text-slate-400 font-medium">iGOT Karmayogi Competency Engine</p>
          </div>
        </div>
      </div>

      {/* User Info & Role Switcher */}
      <div className="flex items-center space-x-4">
        {/* Role Switcher Pill */}
        <button
          onClick={onToggleRoleMode}
          className={`flex items-center space-x-2 px-3.5 py-1.5 rounded-lg text-xs font-semibold border transition ${
            currentRoleMode === 'admin'
              ? 'bg-amber-500/20 text-amber-300 border-amber-500/40 hover:bg-amber-500/30'
              : 'bg-blue-500/20 text-blue-300 border-blue-500/40 hover:bg-blue-500/30'
          }`}
        >
          <UserCheck className="w-4 h-4" />
          <span>{currentRoleMode === 'admin' ? 'Switch to Learner View' : 'Switch Role (Admin)'}</span>
        </button>

        {/* Notifications */}
        <button className="relative p-2 text-slate-300 hover:text-white hover:bg-slate-800 rounded-lg transition">
          <Bell className="w-5 h-5" />
          <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-blue-500 rounded-full animate-ping"></span>
          <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-blue-500 rounded-full"></span>
        </button>

        {/* Profile Dropdown Badge */}
        <div className="flex items-center space-x-3 pl-3 border-l border-slate-800">
          <div className="w-9 h-9 rounded-full bg-gradient-to-tr from-blue-700 to-indigo-600 flex items-center justify-center font-bold text-sm text-white shadow-inner border border-blue-400/30">
            {user?.name ? user.name.split(' ').map((n: string) => n[0]).join('') : 'AS'}
          </div>
          <div className="text-left hidden md:block">
            <span className="text-xs font-bold text-white block">{user?.name || 'Ananya Sharma'}</span>
            <span className="text-[11px] text-slate-400 block">{user?.designation || 'Statistical Officer'}</span>
          </div>
        </div>
      </div>
    </header>
  );
}
