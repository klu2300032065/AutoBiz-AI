"use client";

import React, { useState } from "react";
import { Container } from "@/components/ui/Container";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { FadeIn } from "@/components/animations/FadeIn";
import { motion } from "framer-motion";
import {
  LayoutDashboard,
  TrendingUp,
  FolderGit2,
  Megaphone,
  BarChart2,
  Lightbulb,
  CheckCircle2,
  AlertCircle,
  Activity,
  Layers,
  Sparkles,
} from "lucide-react";

export const DashboardPreview: React.FC = () => {
  const [activeTab, setActiveTab] = useState<
    "overview" | "growth" | "projects" | "marketing" | "analytics" | "opportunities"
  >("overview");

  const tabs = [
    { id: "overview" as const, label: "Overview", icon: LayoutDashboard },
    { id: "growth" as const, label: "Growth", icon: TrendingUp },
    { id: "projects" as const, label: "Projects", icon: FolderGit2 },
    { id: "marketing" as const, label: "Marketing", icon: Megaphone },
    { id: "analytics" as const, label: "Analytics", icon: BarChart2 },
    { id: "opportunities" as const, label: "Opportunities", icon: Lightbulb },
  ];

  return (
    <section id="preview" className="relative py-24 sm:py-32 bg-[#080a0f] border-t border-white/[0.08] overflow-hidden">
      <Container size="large">
        <FadeIn>
          <SectionHeading
            eyebrow="PLATFORM ARCHITECTURE"
            title="Your business, connected."
            description="Bring development, operations, analytics, and marketing into one view. Designed to eliminate data silos and keep leadership focused on verified outcomes."
          />
        </FadeIn>

        {/* Dashboard Frame Container */}
        <FadeIn delay={0.2}>
          <div className="relative rounded-2xl bg-[#0c0f18] border border-white/[0.12] shadow-2xl overflow-hidden">
            {/* Top Preview Watermark & Warning Bar */}
            <div className="flex flex-wrap items-center justify-between px-4 py-3 bg-white/[0.02] border-b border-white/[0.08] gap-2">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-red-500/80" />
                <div className="w-3 h-3 rounded-full bg-amber-500/80" />
                <div className="w-3 h-3 rounded-full bg-emerald-500/80" />
                <span className="text-xs font-mono text-zinc-400 ml-2 hidden sm:inline-block">
                  Auto BIZ Unified Operations Center
                </span>
              </div>

              {/* Strict Disclaimer Pill */}
              <div className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-300 text-[11px] font-mono">
                <AlertCircle className="w-3.5 h-3.5 shrink-0" />
                <span>SAMPLE DASHBOARD • DEMONSTRATION UI ONLY</span>
              </div>
            </div>

            {/* Dashboard Sub-Header & Navigation Tabs */}
            <div className="flex items-center justify-between px-4 sm:px-6 py-3 border-b border-white/[0.06] bg-black/40 overflow-x-auto gap-4 no-scrollbar">
              <div className="flex items-center gap-1.5 shrink-0">
                {tabs.map((tab) => {
                  const Icon = tab.icon;
                  const isActive = activeTab === tab.id;
                  return (
                    <button
                      key={tab.id}
                      onClick={() => setActiveTab(tab.id)}
                      className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-medium transition-all duration-200 cursor-pointer ${
                        isActive
                          ? "bg-white/10 text-white shadow-sm border border-white/15"
                          : "text-zinc-400 hover:text-zinc-200 hover:bg-white/[0.04]"
                      }`}
                    >
                      <Icon className="w-3.5 h-3.5" />
                      <span>{tab.label}</span>
                    </button>
                  );
                })}
              </div>

              <div className="flex items-center gap-2 shrink-0">
                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 flex items-center gap-1">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
                  Live Sync: Ready
                </span>
              </div>
            </div>

            {/* Dashboard Body Area */}
            <div className="p-4 sm:p-6 lg:p-8 bg-[#0a0c13] min-h-[440px]">
              {/* Tab 1: Overview */}
              {activeTab === "overview" && (
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.3 }}
                  className="space-y-6"
                >
                  {/* Top Metric Cards (Explicitly marked as Sample) */}
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                    <div className="p-4 rounded-xl bg-white/[0.02] border border-white/[0.06]">
                      <span className="text-[10px] font-mono text-zinc-400 uppercase tracking-wider block mb-1">
                        System Health (Sample)
                      </span>
                      <div className="text-2xl font-bold font-mono text-emerald-400">99.98%</div>
                      <span className="text-[11px] text-zinc-400 mt-1 block">Telemetry Active</span>
                    </div>

                    <div className="p-4 rounded-xl bg-white/[0.02] border border-white/[0.06]">
                      <span className="text-[10px] font-mono text-zinc-400 uppercase tracking-wider block mb-1">
                        Active Automations (Sample)
                      </span>
                      <div className="text-2xl font-bold font-mono text-cyan-400">14 Workflows</div>
                      <span className="text-[11px] text-zinc-400 mt-1 block">0 Failed Jobs</span>
                    </div>

                    <div className="p-4 rounded-xl bg-white/[0.02] border border-white/[0.06]">
                      <span className="text-[10px] font-mono text-zinc-400 uppercase tracking-wider block mb-1">
                        Acquisition Funnels (Sample)
                      </span>
                      <div className="text-2xl font-bold font-mono text-purple-400">3 Channels</div>
                      <span className="text-[11px] text-zinc-400 mt-1 block">Multi-touch Tracking</span>
                    </div>

                    <div className="p-4 rounded-xl bg-white/[0.02] border border-white/[0.06]">
                      <span className="text-[10px] font-mono text-zinc-400 uppercase tracking-wider block mb-1">
                        Data Integrity (Sample)
                      </span>
                      <div className="text-2xl font-bold font-mono text-blue-400">100% Grounded</div>
                      <span className="text-[11px] text-zinc-400 mt-1 block">Zero Fabrications</span>
                    </div>
                  </div>

                  {/* Middle Layout: Activity Stream & Operational Pipeline */}
                  <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    <div className="lg:col-span-2 p-5 rounded-xl bg-white/[0.02] border border-white/[0.06] flex flex-col justify-between">
                      <div>
                        <div className="flex items-center justify-between pb-3 mb-4 border-b border-white/[0.06]">
                          <span className="text-xs font-bold text-white uppercase tracking-wider font-mono">
                            Connected Infrastructure Pipeline
                          </span>
                          <span className="text-[10px] font-mono text-zinc-400">DEMO VIEW</span>
                        </div>
                        <div className="space-y-3">
                          <div className="flex items-center justify-between p-3 rounded-lg bg-white/[0.02] border border-white/[0.04]">
                            <div className="flex items-center gap-3">
                              <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
                              <div>
                                <h5 className="text-xs font-semibold text-white">Next.js Web Foundation Layer</h5>
                                <p className="text-[11px] text-zinc-400">Server Rendered • Responsive • SEO Configured</p>
                              </div>
                            </div>
                            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                              OPERATIONAL
                            </span>
                          </div>

                          <div className="flex items-center justify-between p-3 rounded-lg bg-white/[0.02] border border-white/[0.04]">
                            <div className="flex items-center gap-3">
                              <CheckCircle2 className="w-4 h-4 text-cyan-400 shrink-0" />
                              <div>
                                <h5 className="text-xs font-semibold text-white">Automated Lead Ingestion Engine</h5>
                                <p className="text-[11px] text-zinc-400">Real-time validation • Notification Routing</p>
                              </div>
                            </div>
                            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
                              RUNNING
                            </span>
                          </div>

                          <div className="flex items-center justify-between p-3 rounded-lg bg-white/[0.02] border border-white/[0.04]">
                            <div className="flex items-center gap-3">
                              <CheckCircle2 className="w-4 h-4 text-purple-400 shrink-0" />
                              <div>
                                <h5 className="text-xs font-semibold text-white">Attribution & Campaign Tracking</h5>
                                <p className="text-[11px] text-zinc-400">Conversion Event Bus • Verified ROI Matrix</p>
                              </div>
                            </div>
                            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-purple-500/10 text-purple-400 border border-purple-500/20">
                              MONITORING
                            </span>
                          </div>
                        </div>
                      </div>
                    </div>

                    {/* Operational Tasks */}
                    <div className="p-5 rounded-xl bg-white/[0.02] border border-white/[0.06]">
                      <div className="flex items-center justify-between pb-3 mb-4 border-b border-white/[0.06]">
                        <span className="text-xs font-bold text-white uppercase tracking-wider font-mono">
                          Recent System Tasks
                        </span>
                        <Activity className="w-3.5 h-3.5 text-cyan-400" />
                      </div>
                      <div className="space-y-2.5 text-xs text-zinc-300">
                        <div className="flex items-start gap-2">
                          <span className="w-1.5 h-1.5 rounded-full bg-cyan-400 mt-1.5 shrink-0" />
                          <div>
                            <p className="font-medium">Form verification completed</p>
                            <span className="text-[10px] text-zinc-400 font-mono">Sample telemetry log</span>
                          </div>
                        </div>
                        <div className="flex items-start gap-2">
                          <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 mt-1.5 shrink-0" />
                          <div>
                            <p className="font-medium">Data integrity check passed</p>
                            <span className="text-[10px] text-zinc-400 font-mono">100% verified sources</span>
                          </div>
                        </div>
                        <div className="flex items-start gap-2">
                          <span className="w-1.5 h-1.5 rounded-full bg-purple-400 mt-1.5 shrink-0" />
                          <div>
                            <p className="font-medium">Growth vector simulated</p>
                            <span className="text-[10px] text-zinc-400 font-mono">Human approval required</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </motion.div>
              )}

              {/* Tab 2: Growth */}
              {activeTab === "growth" && (
                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-4">
                  <div className="p-5 rounded-xl bg-white/[0.02] border border-white/[0.06]">
                    <h4 className="text-sm font-bold text-white mb-2">Growth Vector Modeling (Demonstration)</h4>
                    <p className="text-xs text-zinc-400 leading-relaxed mb-4">
                      Simulate high-impact opportunities by identifying friction points in your current customer acquisition and conversion workflows.
                    </p>
                    <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs font-mono">
                      <div className="p-3 rounded-lg bg-black/40 border border-white/5">
                        <span className="text-zinc-400 block mb-1">Acquisition Velocity</span>
                        <span className="text-emerald-400 font-bold text-sm">Demo Signal: Steady</span>
                      </div>
                      <div className="p-3 rounded-lg bg-black/40 border border-white/5">
                        <span className="text-zinc-400 block mb-1">Friction Reduction</span>
                        <span className="text-cyan-400 font-bold text-sm">Demo Signal: High Yield</span>
                      </div>
                      <div className="p-3 rounded-lg bg-black/40 border border-white/5">
                        <span className="text-zinc-400 block mb-1">Retention Index</span>
                        <span className="text-purple-400 font-bold text-sm">Demo Signal: Verified</span>
                      </div>
                    </div>
                  </div>
                </motion.div>
              )}

              {/* Tab 3: Projects */}
              {activeTab === "projects" && (
                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-4">
                  <div className="p-5 rounded-xl bg-white/[0.02] border border-white/[0.06]">
                    <h4 className="text-sm font-bold text-white mb-2">Active Engineering Workspaces</h4>
                    <div className="space-y-3 pt-2">
                      <div className="flex items-center justify-between p-3 rounded-lg bg-black/40 border border-white/5 text-xs">
                        <div className="flex items-center gap-2">
                          <Layers className="w-4 h-4 text-blue-400" />
                          <span className="font-semibold text-white">Next.js Client Platform Hub</span>
                        </div>
                        <span className="font-mono text-[10px] text-zinc-400">Phase 1 Blueprint</span>
                      </div>
                      <div className="flex items-center justify-between p-3 rounded-lg bg-black/40 border border-white/5 text-xs">
                        <div className="flex items-center gap-2">
                          <Sparkles className="w-4 h-4 text-emerald-400" />
                          <span className="font-semibold text-white">Automated Pipeline Integrations</span>
                        </div>
                        <span className="font-mono text-[10px] text-zinc-400">Phase 2 Planned</span>
                      </div>
                    </div>
                  </div>
                </motion.div>
              )}

              {/* Tab 4: Marketing */}
              {activeTab === "marketing" && (
                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-4">
                  <div className="p-5 rounded-xl bg-white/[0.02] border border-white/[0.06]">
                    <h4 className="text-sm font-bold text-white mb-2">Campaign & Funnel Attribution</h4>
                    <p className="text-xs text-zinc-400 leading-relaxed mb-4">
                      Closed-loop tracking connecting campaign spend directly to qualified leads and business outcomes.
                    </p>
                    <div className="p-3 rounded-lg bg-black/40 border border-white/5 text-xs text-zinc-400">
                      Sample metric view: Real marketing data will be synchronized once custom tracking tokens are provisioned.
                    </div>
                  </div>
                </motion.div>
              )}

              {/* Tab 5: Analytics */}
              {activeTab === "analytics" && (
                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-4">
                  <div className="p-5 rounded-xl bg-white/[0.02] border border-white/[0.06]">
                    <h4 className="text-sm font-bold text-white mb-2">Telemetry & Audit Trails</h4>
                    <p className="text-xs text-zinc-400 leading-relaxed mb-4">
                      Zero-speculation analytics: Every chart and metric is backed by verified event telemetry.
                    </p>
                    <div className="p-3 rounded-lg bg-black/40 border border-white/5 text-xs font-mono text-zinc-400">
                      [LOG_AUDIT] Event streams verified • No synthesized vanity statistics allowed.
                    </div>
                  </div>
                </motion.div>
              )}

              {/* Tab 6: Opportunities */}
              {activeTab === "opportunities" && (
                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-4">
                  <div className="p-5 rounded-xl bg-white/[0.02] border border-white/[0.06]">
                    <h4 className="text-sm font-bold text-white mb-2">Algorithmic Opportunity Scoring</h4>
                    <p className="text-xs text-zinc-400 leading-relaxed mb-4">
                      Highlighting where process automation and UX refinements generate immediate return on investment.
                    </p>
                    <div className="p-3 rounded-lg bg-cyan-500/10 border border-cyan-500/30 text-xs text-cyan-300">
                      Opportunity Detected (Sample): Onboarding automation could eliminate 60% of manual data entry.
                    </div>
                  </div>
                </motion.div>
              )}
            </div>
          </div>
        </FadeIn>
      </Container>
    </section>
  );
};
