"use client";

import React, { useState, useEffect } from 'react';
import Navbar from '@/components/Navbar';
import Sidebar from '@/components/Sidebar';
import CompetencyRadarChart from '@/components/CompetencyRadarChart';
import ExplainabilityModal from '@/components/ExplainabilityModal';
import AdminHeatmap from '@/components/AdminHeatmap';
import { api } from '@/lib/api';
import {
  ShieldAlert, BookOpen, Compass, Sparkles, Award, ArrowRight, CheckCircle2,
  AlertCircle, Upload, FileText, Send, Check, Play, FileCheck, Layers, RefreshCw, BarChart2
} from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

export default function Home() {
  const [roleMode, setRoleMode] = useState<'learner' | 'admin'>('learner');
  const [activeTab, setActiveTab] = useState<string>('dashboard');
  
  // Data states
  const [user, setUser] = useState<any>(null);
  const [gaps, setGaps] = useState<any[]>([]);
  const [recommendations, setRecommendations] = useState<any[]>([]);
  const [careerNav, setCareerNav] = useState<any>(null);
  const [selectedTargetRole, setSelectedTargetRole] = useState<number>(2);
  const [roles, setRoles] = useState<any[]>([]);
  const [analytics, setAnalytics] = useState<any>(null);

  // Modal state
  const [selectedExplainability, setSelectedExplainability] = useState<any>(null);
  const [isExplainModalOpen, setIsExplainModalOpen] = useState<boolean>(false);

  // Chat state
  const [chatMessages, setChatMessages] = useState<any[]>([
    {
      sender: 'assistant',
      text: 'Namaste Ananya Sharma! I am your MoSPI AI Learning Advisor. How can I assist with your competency gaps or target role requirements today?',
      citations: []
    }
  ]);
  const [chatInput, setChatInput] = useState<string>('');
  const [isChatLoading, setIsChatLoading] = useState<boolean>(false);

  // Quiz state
  const [quizDoc, setQuizDoc] = useState<any>(null);
  const [quizQuestions, setQuizQuestions] = useState<any[]>([]);
  const [isGeneratingQuiz, setIsGeneratingQuiz] = useState<boolean>(false);

  useEffect(() => {
    loadInitialData();
  }, []);

  const loadInitialData = async () => {
    try {
      const demoUser = await api.getDemoUser();
      setUser(demoUser);
      setSelectedTargetRole(demoUser.target_role_id || 2);

      const [gapRes, recRes, navRes, roleRes, adminRes] = await Promise.all([
        api.getLearnerGaps(demoUser.id),
        api.getRecommendations(demoUser.id),
        api.getCareerNavigator(demoUser.id, demoUser.target_role_id || 2),
        api.getRoles(),
        api.getAdminAnalytics()
      ]);

      setGaps(gapRes);
      setRecommendations(recRes);
      setCareerNav(navRes);
      setRoles(roleRes);
      setAnalytics(adminRes);
    } catch (err) {
      console.error("Failed loading data", err);
    }
  };

  const handleRoleChange = async (targetId: number) => {
    setSelectedTargetRole(targetId);
    if (user) {
      const [gapRes, navRes] = await Promise.all([
        api.getLearnerGaps(user.id, targetId),
        api.getCareerNavigator(user.id, targetId)
      ]);
      setGaps(gapRes);
      setCareerNav(navRes);
    }
  };

  const handleOpenExplainability = (rec: any) => {
    setSelectedExplainability(rec.explainability);
    setIsExplainModalOpen(true);
  };

  const handleSendChatMessage = async (msgText?: string) => {
    const textToSend = msgText || chatInput;
    if (!textToSend.trim() || !user) return;

    const userMsg = { sender: 'user', text: textToSend };
    setChatMessages(prev => [...prev, userMsg]);
    if (!msgText) setChatInput('');
    setIsChatLoading(true);

    try {
      const resp = await api.chatAssistant(user.id, textToSend);
      setChatMessages(prev => [...prev, {
        sender: 'assistant',
        text: resp.answer,
        citations: resp.citations,
        mode: resp.mode
      }]);
    } catch (err) {
      setChatMessages(prev => [...prev, {
        sender: 'assistant',
        text: "I couldn't find enough verified information to answer that question.",
        citations: []
      }]);
    } finally {
      setIsChatLoading(false);
    }
  };

  const handleGenerateQuizSample = async () => {
    setIsGeneratingQuiz(true);
    try {
      const res = await api.generateQuiz(1);
      setQuizQuestions(res.questions);
    } catch (err) {
      console.error(err);
    } finally {
      setIsGeneratingQuiz(false);
    }
  };

  const COLORS = ['#2563eb', '#3b82f6', '#60a5fa', '#93c5fd', '#cbd5e1'];

  return (
    <div className="min-h-screen bg-slate-100 flex flex-col font-sans">
      {/* Top Navbar */}
      <Navbar
        user={user}
        currentRoleMode={roleMode}
        onToggleRoleMode={() => setRoleMode(roleMode === 'learner' ? 'admin' : 'learner')}
      />

      <div className="flex flex-1">
        {/* Navigation Sidebar */}
        <Sidebar
          activeTab={activeTab}
          setActiveTab={setActiveTab}
          roleMode={roleMode}
        />

        {/* Main Content Area */}
        <main className="flex-1 p-6 overflow-y-auto max-w-7xl">
          
          {/* ========================================================================= */}
          {/* 1. LEARNER DASHBOARD (Image Panel 1 Layout) */}
          {/* ========================================================================= */}
          {roleMode === 'learner' && activeTab === 'dashboard' && (
            <div className="space-y-6">
              
              {/* Header Welcome Bar */}
              <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm flex items-center justify-between">
                <div>
                  <h1 className="text-2xl font-black text-slate-900 flex items-center gap-2">
                    Welcome, {user?.name || 'Ananya Sharma'}! <span className="text-xl">👋</span>
                  </h1>
                  <p className="text-sm text-slate-500 font-medium mt-1">
                    {user?.designation || 'Statistical Officer'} | {user?.department || 'Demo Statistics Department'}
                  </p>
                </div>

                <div className="flex items-center space-x-4 bg-slate-50 border border-slate-200 px-4 py-2.5 rounded-xl">
                  <div>
                    <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block">Target Role</span>
                    <span className="text-sm font-bold text-slate-800">
                      {roles.find(r => r.id === selectedTargetRole)?.name || 'Senior Statistical Officer'}
                    </span>
                  </div>
                  <button
                    onClick={() => setActiveTab('navigator')}
                    className="px-3 py-1.5 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-xs font-semibold transition"
                  >
                    Change Target Role
                  </button>
                </div>
              </div>

              {/* Grid Layout: Competency Radar vs Top Skill Gaps */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                
                {/* Competency Overview Radar Chart */}
                <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm flex flex-col justify-between">
                  <div className="flex items-center justify-between mb-2">
                    <h2 className="text-base font-bold text-slate-900">Competency Overview</h2>
                    <span className="text-xs text-slate-400 font-medium">6 Framework Domains</span>
                  </div>
                  
                  <CompetencyRadarChart />
                </div>

                {/* Top Skill Gaps List */}
                <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm flex flex-col justify-between">
                  <div className="flex items-center justify-between mb-4">
                    <h2 className="text-base font-bold text-slate-900">Top Skill Gaps</h2>
                    <button onClick={() => setActiveTab('competencies')} className="text-xs font-bold text-blue-600 hover:underline">
                      View all competencies →
                    </button>
                  </div>

                  <div className="space-y-3.5 flex-1">
                    {gaps.filter(g => g.gap > 0).slice(0, 3).map((gapItem, idx) => (
                      <div key={idx} className="flex items-center justify-between p-3.5 bg-slate-50 rounded-xl border border-slate-200/80">
                        <div className="flex items-center space-x-3">
                          <span className="font-extrabold text-slate-400 text-sm">{idx + 1}.</span>
                          <div>
                            <h3 className="text-sm font-bold text-slate-900">{gapItem.competency_name}</h3>
                            <p className="text-xs text-slate-500">Gap: {gapItem.gap} Level{gapItem.gap > 1 ? 's' : ''} (Assessed: {gapItem.assessed_level} vs Req: {gapItem.required_level})</p>
                          </div>
                        </div>

                        <span className={`px-3 py-1 rounded-full text-xs font-bold ${
                          gapItem.severity === 'Critical' ? 'bg-red-100 text-red-700 border border-red-200' :
                          gapItem.severity === 'Medium' ? 'bg-orange-100 text-orange-700 border border-orange-200' :
                          'bg-emerald-100 text-emerald-700 border border-emerald-200'
                        }`}>
                          {gapItem.severity}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>

              </div>

              {/* Recommended for You Grid */}
              <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <h2 className="text-lg font-bold text-slate-900">Recommended for You</h2>
                    <p className="text-xs text-slate-500">Grounded in verified skill gaps and current catalogue</p>
                  </div>
                  <button onClick={() => setActiveTab('recommendations')} className="text-xs font-bold text-blue-600 hover:underline">
                    Browse full catalogue →
                  </button>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {recommendations.slice(0, 2).map((rec, idx) => (
                    <div key={idx} className="border border-slate-200 rounded-xl p-5 hover:shadow-md transition bg-slate-50/50 flex flex-col justify-between">
                      <div>
                        <div className="flex items-start justify-between">
                          <div>
                            <span className="text-[11px] font-bold text-blue-700 uppercase bg-blue-100 px-2 py-0.5 rounded">
                              Score: {rec.score}/100
                            </span>
                            <h3 className="text-base font-bold text-slate-900 mt-2">{rec.course_title}</h3>
                            <p className="text-xs text-slate-500 mt-1">Provider: {rec.provider} | Duration: {rec.duration}</p>
                          </div>
                        </div>
                        <p className="text-xs text-slate-600 mt-3 line-clamp-2 bg-white p-2.5 rounded-lg border border-slate-200">
                          "{rec.explainability.recommendation_reason}"
                        </p>
                      </div>

                      <div className="mt-4 pt-3 border-t border-slate-200 flex items-center justify-between">
                        <button
                          onClick={() => handleOpenExplainability(rec)}
                          className="text-xs font-bold text-blue-600 hover:text-blue-800 flex items-center space-x-1"
                        >
                          <span>Why this course?</span>
                          <ArrowRight className="w-3.5 h-3.5" />
                        </button>
                        <button className="px-3 py-1.5 bg-slate-900 text-white rounded-lg text-xs font-semibold hover:bg-slate-800 transition">
                          Enroll now
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

            </div>
          )}

          {/* ========================================================================= */}
          {/* 2. CAREER NAVIGATOR (Unique Feature 2 - Image Panel 4 Layout) */}
          {/* ========================================================================= */}
          {(roleMode === 'learner' && activeTab === 'navigator') && (
            <div className="space-y-6">
              
              {/* Top Banner */}
              <div className="bg-slate-900 text-white rounded-2xl p-6 border border-slate-800 shadow-md">
                <div className="flex items-center justify-between">
                  <div>
                    <span className="text-xs font-bold text-blue-400 uppercase tracking-wider block">Career & Role Navigator</span>
                    <h1 className="text-2xl font-extrabold mt-1">Plan your learning for your target role</h1>
                    <p className="text-xs text-slate-300 mt-1">
                      Objective competency readiness matrix for government career progression
                    </p>
                  </div>

                  <div className="bg-slate-800 p-3 rounded-xl border border-slate-700 flex items-center space-x-4">
                    <div className="text-right">
                      <span className="text-xs text-slate-400 block font-medium">Select Target Role</span>
                      <select
                        value={selectedTargetRole}
                        onChange={(e) => handleRoleChange(Number(e.target.value))}
                        className="bg-slate-900 text-white border border-slate-700 text-sm font-bold rounded-lg px-3 py-1.5 focus:outline-none focus:border-blue-500"
                      >
                        {roles.map(r => (
                          <option key={r.id} value={r.id}>{r.name}</option>
                        ))}
                      </select>
                    </div>
                  </div>
                </div>
              </div>

              {/* Competency Readiness Gauge & Role Requirements Table */}
              <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-4">
                <div className="flex items-center justify-between border-b border-slate-200 pb-4">
                  <div>
                    <h2 className="text-lg font-bold text-slate-900">Competency Gap for Target Role</h2>
                    <p className="text-xs text-slate-500">Benchmark requirement comparison vs assessed capability</p>
                  </div>
                  <div className="text-right">
                    <span className="text-2xl font-black text-blue-700">{careerNav?.competency_readiness_pct || 78}%</span>
                    <span className="text-xs text-slate-500 block font-medium">Competency Readiness</span>
                  </div>
                </div>

                <div className="overflow-x-auto">
                  <table className="w-full text-xs text-left border-collapse">
                    <thead>
                      <tr className="bg-slate-50 text-slate-700 uppercase font-bold border-b border-slate-200">
                        <th className="p-3">Competency</th>
                        <th className="p-3">Domain</th>
                        <th className="p-3 text-center">Required Level</th>
                        <th className="p-3 text-center">Current Level</th>
                        <th className="p-3 text-center">Gap</th>
                        <th className="p-3 text-center">Priority</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-200">
                      {careerNav?.priority_gaps?.map((gapItem: any, idx: number) => (
                        <tr key={idx} className="hover:bg-slate-50">
                          <td className="p-3 font-bold text-slate-900">{gapItem.competency_name}</td>
                          <td className="p-3 text-slate-500">{gapItem.domain}</td>
                          <td className="p-3 text-center font-bold text-slate-800">{gapItem.required_level}</td>
                          <td className="p-3 text-center text-slate-600">{gapItem.current_level}</td>
                          <td className="p-3 text-center">
                            <span className={`px-2 py-0.5 rounded text-xs font-bold ${
                              gapItem.gap > 0 ? 'bg-red-100 text-red-700' : 'bg-emerald-100 text-emerald-700'
                            }`}>
                              {gapItem.gap}
                            </span>
                          </td>
                          <td className="p-3 text-center">
                            <span className="uppercase text-[10px] font-bold px-2 py-0.5 rounded bg-slate-100 text-slate-700">
                              {gapItem.priority}
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>

              {/* Sequenced Learning Path (Step 1..N) */}
              <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-4">
                <h2 className="text-lg font-bold text-slate-900">Recommended Learning Path Sequence</h2>
                <p className="text-xs text-slate-500">Ordered sequence to address target role competency requirements</p>

                <div className="space-y-4 pt-2">
                  {careerNav?.recommended_path?.map((step: any, idx: number) => (
                    <div key={idx} className="flex items-start space-x-4 p-4 rounded-xl border border-slate-200 bg-slate-50/70 hover:border-blue-300 transition">
                      <div className="w-8 h-8 rounded-full bg-blue-600 text-white flex items-center justify-center font-bold text-sm shrink-0 mt-0.5">
                        {step.step_number}
                      </div>

                      <div className="flex-1">
                        <div className="flex items-center justify-between">
                          <h3 className="text-base font-bold text-slate-900">{step.course_title}</h3>
                          <span className="text-xs font-semibold text-slate-500">{step.duration}</span>
                        </div>
                        <p className="text-xs text-slate-600 mt-1 font-medium">{step.reason}</p>
                        {step.prerequisites && (
                          <span className="text-[11px] text-blue-600 font-semibold block mt-2">
                            Prerequisite: {step.prerequisites}
                          </span>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>

            </div>
          )}

          {/* ========================================================================= */}
          {/* 3. AI ASSISTANT (RAG Powered - Image Panel 5 Layout) */}
          {/* ========================================================================= */}
          {(roleMode === 'learner' && activeTab === 'assistant') && (
            <div className="h-[calc(100vh-100px)] flex flex-col bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
              
              {/* Chat Header */}
              <div className="bg-slate-900 text-white p-4 flex items-center justify-between border-b border-slate-800">
                <div className="flex items-center space-x-3">
                  <div className="p-2 bg-blue-600 rounded-lg">
                    <Sparkles className="w-5 h-5 text-white" />
                  </div>
                  <div>
                    <h2 className="text-base font-bold">MoSPI AI Learning Advisor</h2>
                    <p className="text-xs text-slate-400">Context-Aware & Grounded in Official Frameworks</p>
                  </div>
                </div>
                <span className="text-[11px] bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 px-2.5 py-1 rounded-full font-semibold">
                  RAG Active
                </span>
              </div>

              {/* Suggested Prompt Pills */}
              <div className="bg-slate-50 p-3 border-b border-slate-200 flex flex-wrap gap-2">
                {[
                  "Why was Advanced Data Analysis recommended to me?",
                  "What competencies do I need for Senior Statistical Officer?",
                  "What should I learn next?",
                  "Explain my Data Analysis gap."
                ].map((prompt, idx) => (
                  <button
                    key={idx}
                    onClick={() => handleSendChatMessage(prompt)}
                    className="text-xs bg-white text-slate-700 border border-slate-300 hover:border-blue-500 hover:text-blue-700 px-3 py-1.5 rounded-full transition shadow-2xs font-medium"
                  >
                    "{prompt}"
                  </button>
                ))}
              </div>

              {/* Chat History */}
              <div className="flex-1 p-6 overflow-y-auto space-y-4">
                {chatMessages.map((msg, idx) => (
                  <div key={idx} className={`flex flex-col ${msg.sender === 'user' ? 'items-end' : 'items-start'}`}>
                    <div className={`max-w-2xl rounded-2xl p-4 text-sm ${
                      msg.sender === 'user'
                        ? 'bg-blue-600 text-white rounded-br-none'
                        : 'bg-slate-100 text-slate-800 border border-slate-200 rounded-bl-none'
                    }`}>
                      <p className="whitespace-pre-wrap leading-relaxed">{msg.text}</p>

                      {/* Source Citations */}
                      {msg.citations && msg.citations.length > 0 && (
                        <div className="mt-3 pt-2 border-t border-slate-300/50 space-y-1">
                          <span className="text-[10px] font-bold text-slate-500 uppercase tracking-wider block">Grounded Sources:</span>
                          {msg.citations.map((cite: any, cIdx: number) => (
                            <div key={cIdx} className="bg-white/80 p-2 rounded text-[11px] text-slate-700 border border-slate-200">
                              <span className="font-bold text-blue-700">{cite.title}</span> - {cite.clause_or_source}
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>
                ))}

                {isChatLoading && (
                  <div className="flex items-center space-x-2 text-slate-400 text-xs italic">
                    <RefreshCw className="w-4 h-4 animate-spin" />
                    <span>Retrieving context & synthesizing grounded answer...</span>
                  </div>
                )}
              </div>

              {/* Chat Input Bar */}
              <div className="p-4 border-t border-slate-200 bg-slate-50 flex items-center space-x-2">
                <input
                  type="text"
                  value={chatInput}
                  onChange={(e) => setChatInput(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && handleSendChatMessage()}
                  placeholder="Ask a question about your competency gaps, target role, or recommendations..."
                  className="flex-1 bg-white border border-slate-300 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-blue-500 text-slate-800"
                />
                <button
                  onClick={() => handleSendChatMessage()}
                  disabled={isChatLoading}
                  className="p-2.5 bg-blue-600 hover:bg-blue-700 text-white rounded-xl transition disabled:opacity-50"
                >
                  <Send className="w-5 h-5" />
                </button>
              </div>

            </div>
          )}

          {/* ========================================================================= */}
          {/* 4. ADMIN DASHBOARD (Image Panel 7 Layout) */}
          {/* ========================================================================= */}
          {roleMode === 'admin' && (
            <div className="space-y-6">
              
              {/* Executive KPI Stats Cards */}
              <div className="grid grid-cols-4 gap-4">
                <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex items-center space-x-4">
                  <div className="p-3 bg-blue-100 text-blue-700 rounded-xl">
                    <BarChart2 className="w-6 h-6" />
                  </div>
                  <div>
                    <span className="text-2xl font-black text-slate-900">{analytics?.total_officials || 248}</span>
                    <span className="text-xs text-slate-500 block font-medium">Total Officials</span>
                  </div>
                </div>

                <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex items-center space-x-4">
                  <div className="p-3 bg-red-100 text-red-700 rounded-xl">
                    <ShieldAlert className="w-6 h-6" />
                  </div>
                  <div>
                    <span className="text-2xl font-black text-slate-900">{analytics?.critical_skill_gaps || 36}</span>
                    <span className="text-xs text-slate-500 block font-medium">Critical Skill Gaps</span>
                  </div>
                </div>

                <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex items-center space-x-4">
                  <div className="p-3 bg-indigo-100 text-indigo-700 rounded-xl">
                    <BookOpen className="w-6 h-6" />
                  </div>
                  <div>
                    <span className="text-2xl font-black text-slate-900">{analytics?.courses_enrolled || 412}</span>
                    <span className="text-xs text-slate-500 block font-medium">Courses Enrolled</span>
                  </div>
                </div>

                <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex items-center space-x-4">
                  <div className="p-3 bg-emerald-100 text-emerald-700 rounded-xl">
                    <CheckCircle2 className="w-6 h-6" />
                  </div>
                  <div>
                    <span className="text-2xl font-black text-slate-900">{analytics?.completion_rate_pct || 68}%</span>
                    <span className="text-xs text-slate-500 block font-medium">Completion Rate</span>
                  </div>
                </div>
              </div>

              {/* Organization Competency Heatmap */}
              <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <h2 className="text-lg font-bold text-slate-900">Organization Competency Heatmap</h2>
                    <p className="text-xs text-slate-500">Average competency gap severity by role and framework domain</p>
                  </div>
                </div>

                <AdminHeatmap data={analytics?.heatmap || []} />
              </div>

              {/* Charts Grid: Skill Gaps Bar Chart vs Course Demand Pie Chart */}
              <div className="grid grid-cols-2 gap-6">
                
                {/* Top Skill Gaps Across Organization */}
                <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm">
                  <h2 className="text-base font-bold text-slate-900 mb-4">Top 5 Skill Gaps Across Organization</h2>
                  <div className="h-64">
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart data={analytics?.top_skill_gaps || []} layout="vertical">
                        <XAxis type="number" />
                        <YAxis dataKey="name" type="category" width={140} tick={{ fontSize: 11 }} />
                        <Tooltip />
                        <Bar dataKey="count" fill="#2563eb" radius={[0, 6, 6, 0]} />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                </div>

                {/* Course Demand */}
                <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm">
                  <h2 className="text-base font-bold text-slate-900 mb-4">Course Demand Share</h2>
                  <div className="h-64 flex items-center justify-center">
                    <ResponsiveContainer width="100%" height="100%">
                      <PieChart>
                        <Pie
                          data={analytics?.course_demand || []}
                          cx="50%"
                          cy="50%"
                          innerRadius={60}
                          outerRadius={90}
                          paddingAngle={3}
                          dataKey="value"
                        >
                          {analytics?.course_demand?.map((entry: any, index: number) => (
                            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                          ))}
                        </Pie>
                        <Tooltip />
                      </PieChart>
                    </ResponsiveContainer>
                  </div>
                </div>

              </div>

            </div>
          )}

          {/* ========================================================================= */}
          {/* 5. OTHER TABS (My Competencies, Learning Recommendations, Assessments) */}
          {/* ========================================================================= */}
          {roleMode === 'learner' && activeTab === 'competencies' && (
            <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-4">
              <h1 className="text-xl font-bold text-slate-900">My Competency Profile</h1>
              <p className="text-xs text-slate-500">Official capability assessment levels across 6 framework domains</p>
              
              <div className="grid grid-cols-2 gap-4 pt-4">
                {gaps.map((g, idx) => (
                  <div key={idx} className="p-4 border border-slate-200 rounded-xl bg-slate-50 flex items-center justify-between">
                    <div>
                      <span className="text-[10px] uppercase font-bold text-slate-400">{g.domain}</span>
                      <h3 className="text-base font-bold text-slate-900">{g.competency_name}</h3>
                      <p className="text-xs text-slate-500 mt-1">Assessed Level: {g.assessed_level} / Required: {g.required_level}</p>
                    </div>

                    <span className={`px-3 py-1 rounded-full text-xs font-bold ${
                      g.gap === 0 ? 'bg-emerald-100 text-emerald-700' : 'bg-red-100 text-red-700'
                    }`}>
                      {g.gap === 0 ? 'Satisfied' : `Gap: ${g.gap}`}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {roleMode === 'learner' && activeTab === 'recommendations' && (
            <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-4">
              <h1 className="text-xl font-bold text-slate-900">Learning Recommendations Catalogue</h1>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
                {recommendations.map((rec, idx) => (
                  <div key={idx} className="border border-slate-200 rounded-xl p-5 bg-slate-50 space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-bold text-blue-700 bg-blue-100 px-2 py-0.5 rounded">
                        Score: {rec.score}/100
                      </span>
                      <span className="text-xs text-slate-500">{rec.duration}</span>
                    </div>

                    <h3 className="text-base font-bold text-slate-900">{rec.course_title}</h3>
                    <p className="text-xs text-slate-600 bg-white p-2.5 rounded-lg border border-slate-200">
                      "{rec.explainability.recommendation_reason}"
                    </p>

                    <div className="pt-2 flex items-center justify-between">
                      <button
                        onClick={() => handleOpenExplainability(rec)}
                        className="text-xs font-bold text-blue-600 hover:underline"
                      >
                        Why this course? (Explainability Trail)
                      </button>
                      <button className="px-3 py-1 bg-slate-900 text-white rounded text-xs font-semibold">
                        Enroll
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'assessments' && (
            <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-6">
              <div>
                <h1 className="text-xl font-bold text-slate-900">Assessment Generator & Quiz Module</h1>
                <p className="text-xs text-slate-500">Generate structured MCQs from training material</p>
              </div>

              <div className="border-2 border-dashed border-slate-300 rounded-2xl p-8 text-center bg-slate-50 space-y-3">
                <Upload className="w-10 h-10 text-slate-400 mx-auto" />
                <h3 className="text-sm font-bold text-slate-800">Upload NSSTA Training Material (PDF, DOCX, TXT)</h3>
                <button
                  onClick={handleGenerateQuizSample}
                  disabled={isGeneratingQuiz}
                  className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold rounded-xl shadow transition"
                >
                  {isGeneratingQuiz ? 'Extracting & Generating MCQs...' : 'Generate Sample Assessment Quiz'}
                </button>
              </div>

              {quizQuestions.length > 0 && (
                <div className="space-y-4 pt-4 border-t border-slate-200">
                  <h3 className="text-base font-bold text-slate-900">Generated Questions ({quizQuestions.length})</h3>
                  <div className="space-y-4">
                    {quizQuestions.map((q, idx) => (
                      <div key={idx} className="p-4 rounded-xl border border-slate-200 bg-slate-50 space-y-2">
                        <span className="text-xs font-bold text-blue-700 uppercase">Question {idx + 1} - {q.competency_name}</span>
                        <h4 className="text-sm font-bold text-slate-900">{q.question}</h4>
                        <div className="grid grid-cols-2 gap-2 pt-2">
                          {q.options.map((opt: string, oIdx: number) => (
                            <div key={oIdx} className={`p-2 rounded text-xs border ${
                              oIdx === q.correct_answer ? 'bg-emerald-100 border-emerald-300 text-emerald-900 font-bold' : 'bg-white border-slate-200 text-slate-700'
                            }`}>
                              {String.fromCharCode(65 + oIdx)}. {opt}
                            </div>
                          ))}
                        </div>
                        <p className="text-xs text-slate-500 pt-2 font-medium italic">Explanation: {q.explanation}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

        </main>
      </div>

      {/* Unique Feature 1: Explainability Trail Modal */}
      <ExplainabilityModal
        isOpen={isExplainModalOpen}
        onClose={() => setIsExplainModalOpen(false)}
        data={selectedExplainability}
      />
    </div>
  );
}
