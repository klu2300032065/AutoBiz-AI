"use client";

import React, { useState } from "react";
import { motion, useReducedMotion } from "framer-motion";
import { Code2, TrendingUp, Megaphone, CheckCircle2, ArrowRight, Activity } from "lucide-react";

export const HeroVisual: React.FC = () => {
  const [activeTab, setActiveTab] = useState<"build" | "scale" | "market">("scale");
  const shouldReduceMotion = useReducedMotion();

  const nodes = [
    {
      id: "build" as const,
      label: "01 BUILD",
      title: "Digital Foundation",
      icon: Code2,
      accent: "from-blue-500 to-indigo-600",
      pillColor: "text-blue-400 bg-blue-500/10 border-blue-500/30",
      status: "Architecture Active",
      metric: "Next.js • React • APIs",
      detail: "Clean codebases, resilient APIs & scalable cloud infrastructure.",
    },
    {
      id: "scale" as const,
      label: "02 SCALE",
      title: "Clarity & Automation",
      icon: TrendingUp,
      accent: "from-emerald-500 to-teal-600",
      pillColor: "text-emerald-400 bg-emerald-500/10 border-emerald-500/30",
      status: "Pipeline Optimized",
      metric: "Telemetry • Workflows",
      detail: "Real data telemetry, process automation & performance tracking.",
    },
    {
      id: "market" as const,
      label: "03 MARKET",
      title: "Intelligent Reach",
      icon: Megaphone,
      accent: "from-purple-500 to-pink-600",
      pillColor: "text-purple-400 bg-purple-500/10 border-purple-500/30",
      status: "Acquisition Active",
      metric: "Funnels • Attribution",
      detail: "Grounded marketing campaigns & repeatable customer acquisition.",
    },
  ];

  return (
    <div className="relative w-full max-w-xl mx-auto lg:max-w-none">
      {/* Outer ambient glow */}
      <div className="absolute -inset-1 rounded-3xl bg-gradient-to-tr from-cyan-500/20 via-indigo-500/10 to-purple-500/20 blur-xl opacity-60 pointer-events-none" />

      {/* Main Container */}
      <div className="relative rounded-2xl bg-[#0c0f17]/90 border border-white/[0.12] p-6 sm:p-7 shadow-2xl backdrop-blur-xl">
        {/* Terminal Header */}
        <div className="flex items-center justify-between pb-4 mb-6 border-b border-white/[0.08]">
          <div className="flex items-center gap-2">
            <div className="w-2.5 h-2.5 rounded-full bg-red-500/60" />
            <div className="w-2.5 h-2.5 rounded-full bg-yellow-500/60" />
            <div className="w-2.5 h-2.5 rounded-full bg-emerald-500/60" />
            <span className="text-[11px] font-mono text-zinc-400 ml-2 tracking-wider">
              autobiz-growth-engine.sys
            </span>
          </div>

          <div className="flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-white/[0.05] border border-white/[0.08]">
            <Activity className="w-3 h-3 text-cyan-400 animate-pulse" />
            <span className="text-[10px] font-mono text-zinc-300">SYSTEM HEALTHY</span>
          </div>
        </div>

        {/* 3 Pipeline Nodes */}
        <div className="grid grid-cols-3 gap-2 sm:gap-3 mb-6">
          {nodes.map((node) => {
            const isActive = activeTab === node.id;
            const Icon = node.icon;
            return (
              <button
                key={node.id}
                onClick={() => setActiveTab(node.id)}
                className={`relative flex flex-col items-start p-3 sm:p-3.5 rounded-xl text-left transition-all duration-300 border cursor-pointer ${
                  isActive
                    ? "bg-white/[0.08] border-white/30 shadow-lg shadow-black/40"
                    : "bg-white/[0.02] border-white/[0.06] hover:bg-white/[0.05] hover:border-white/15"
                }`}
              >
                {isActive && (
                  <motion.div
                    layoutId="activeTabIndicator"
                    className="absolute inset-0 rounded-xl bg-gradient-to-b from-white/[0.08] to-transparent pointer-events-none"
                    transition={{ type: "spring", stiffness: 400, damping: 30 }}
                  />
                )}
                <div className="flex items-center justify-between w-full mb-2">
                  <div className={`p-1.5 rounded-lg bg-gradient-to-br ${node.accent} text-white shadow-sm`}>
                    <Icon className="w-3.5 h-3.5" />
                  </div>
                  <span className="text-[9px] font-mono text-zinc-400">{node.label.split(" ")[0]}</span>
                </div>
                <span className="text-xs font-bold text-white tracking-tight">{node.label.split(" ")[1]}</span>
                <span className="text-[10px] text-zinc-400 line-clamp-1 mt-0.5">{node.metric.split("•")[0]}</span>
              </button>
            );
          })}
        </div>

        {/* Dynamic Detail Card with Connecting Indicator */}
        <div className="relative rounded-xl bg-zinc-950/80 border border-white/[0.08] p-4 sm:p-5 overflow-hidden">
          {/* Subtle top indicator bar */}
          <div className="absolute top-0 inset-x-0 h-[2px] bg-gradient-to-r from-transparent via-cyan-400 to-transparent" />

          {nodes
            .filter((n) => n.id === activeTab)
            .map((node) => {
              const Icon = node.icon;
              return (
                <motion.div
                  key={node.id}
                  initial={{ opacity: 0, y: shouldReduceMotion ? 0 : 8 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.3 }}
                  className="flex flex-col gap-3"
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <div className={`p-1 rounded-md bg-gradient-to-br ${node.accent} text-white`}>
                        <Icon className="w-4 h-4" />
                      </div>
                      <div>
                        <h4 className="text-sm font-bold text-white">{node.title}</h4>
                        <span className="text-[10px] font-mono text-zinc-400">{node.metric}</span>
                      </div>
                    </div>

                    <span className={`text-[10px] font-mono px-2 py-0.5 rounded-full border ${node.pillColor}`}>
                      {node.status}
                    </span>
                  </div>

                  <p className="text-xs text-zinc-300 leading-relaxed">{node.detail}</p>

                  <div className="grid grid-cols-2 gap-2 pt-2 border-t border-white/[0.06] text-[11px]">
                    <div className="flex items-center gap-1.5 text-zinc-400">
                      <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                      <span>Production Ready</span>
                    </div>
                    <div className="flex items-center gap-1.5 text-zinc-400">
                      <CheckCircle2 className="w-3.5 h-3.5 text-cyan-400 shrink-0" />
                      <span>Zero Guesswork</span>
                    </div>
                  </div>
                </motion.div>
              );
            })}
        </div>

        {/* Floating System Signal Indicators */}
        <div className="mt-4 flex items-center justify-between pt-3 border-t border-white/[0.06] text-[11px] text-zinc-400">
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-cyan-400 animate-pulse" />
            <span className="font-mono text-[10px]">FLOW: BUILD → SCALE → MARKET</span>
          </div>

          <a
            href="#what-we-do"
            className="inline-flex items-center gap-1 text-[11px] text-cyan-400 hover:text-cyan-300 font-medium transition-colors"
          >
            <span>Explore Architecture</span>
            <ArrowRight className="w-3 h-3" />
          </a>
        </div>
      </div>
    </div>
  );
};
