"use client";

import React, { useState } from "react";
import { Container } from "@/components/ui/Container";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { FadeIn } from "@/components/animations/FadeIn";
import { processStages, ProcessStage } from "@/data/process";
import { motion } from "framer-motion";
import { CheckCircle2, ArrowRight } from "lucide-react";

export const ProcessTimeline: React.FC = () => {
  const [activeStep, setActiveStep] = useState<number>(0);
  const currentStage: ProcessStage = processStages[activeStep];

  return (
    <section id="how-it-works" className="relative py-24 sm:py-32 bg-[#090b10]/80 border-y border-white/[0.08] overflow-hidden">
      <Container>
        <FadeIn>
          <SectionHeading
            eyebrow="EXECUTION FRAMEWORK"
            title="From idea to impact."
            description="Our structured five-stage methodology takes you from initial discovery to measurable, sustained growth without speculative risks."
          />
        </FadeIn>

        {/* Step Tabs / Timeline Nav */}
        <FadeIn delay={0.2}>
          <div className="flex items-center justify-between gap-2 overflow-x-auto pb-4 mb-8 no-scrollbar">
            {processStages.map((stage, idx) => {
              const isActive = activeStep === idx;
              return (
                <button
                  key={stage.step}
                  onClick={() => setActiveStep(idx)}
                  className={`relative flex-1 min-w-[140px] p-4 rounded-xl border text-left transition-all duration-300 cursor-pointer ${
                    isActive
                      ? "bg-white/[0.08] border-cyan-500/50 shadow-[0_0_20px_rgba(6,182,212,0.15)]"
                      : "bg-white/[0.02] border-white/[0.06] hover:bg-white/[0.04] hover:border-white/15"
                  }`}
                >
                  <div className="flex items-center justify-between mb-1">
                    <span
                      className={`text-xs font-mono font-bold ${
                        isActive ? "text-cyan-400" : "text-zinc-400"
                      }`}
                    >
                      STAGE {stage.step}
                    </span>
                    {isActive && (
                      <span className="w-1.5 h-1.5 rounded-full bg-cyan-400 animate-ping" />
                    )}
                  </div>
                  <span className="text-sm font-bold text-white tracking-tight block">
                    {stage.name}
                  </span>
                </button>
              );
            })}
          </div>
        </FadeIn>

        {/* Active Stage Deep Dive Display */}
        <FadeIn delay={0.3}>
          <div className="relative rounded-2xl bg-[#0d1017] border border-white/[0.1] p-6 sm:p-10 overflow-hidden shadow-2xl">
            {/* Ambient Background Accent */}
            <div className="absolute top-0 right-0 w-96 h-96 bg-cyan-500/5 rounded-full blur-3xl pointer-events-none" />

            <div className="relative z-10 grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
              {/* Left Details */}
              <div className="lg:col-span-7 flex flex-col gap-4">
                <div className="flex items-center gap-3">
                  <span className="text-2xl sm:text-3xl font-mono font-black text-cyan-400">
                    {currentStage.step}
                  </span>
                  <div className="w-[1px] h-6 bg-white/20" />
                  <span className="text-xs font-mono tracking-widest text-zinc-400 uppercase">
                    Focus: {currentStage.focus}
                  </span>
                </div>

                <h3 className="text-xl sm:text-2xl font-bold text-white tracking-tight">
                  {currentStage.headline}
                </h3>

                <p className="text-sm sm:text-base text-zinc-300 leading-relaxed">
                  {currentStage.description}
                </p>

                {/* Stage Navigator Controls */}
                <div className="flex items-center gap-4 pt-4">
                  <button
                    onClick={() => setActiveStep((prev) => (prev > 0 ? prev - 1 : processStages.length - 1))}
                    className="px-3 py-1.5 text-xs text-zinc-400 hover:text-white rounded-lg border border-white/10 hover:bg-white/5 transition-colors cursor-pointer"
                  >
                    ← Previous Stage
                  </button>
                  <button
                    onClick={() => setActiveStep((prev) => (prev < processStages.length - 1 ? prev + 1 : 0))}
                    className="px-3.5 py-1.5 text-xs text-cyan-400 font-semibold rounded-lg border border-cyan-500/30 bg-cyan-500/10 hover:bg-cyan-500/20 transition-colors flex items-center gap-1.5 cursor-pointer"
                  >
                    <span>Next Stage</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>

              {/* Right Deliverables Box */}
              <div className="lg:col-span-5 rounded-xl bg-black/40 border border-white/[0.08] p-6 flex flex-col gap-4">
                <div className="flex items-center justify-between pb-3 border-b border-white/[0.08]">
                  <span className="text-xs font-mono text-zinc-400 uppercase tracking-wider">
                    Core Deliverables
                  </span>
                  <span className="text-[10px] font-mono text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
                    Verified Outputs
                  </span>
                </div>

                <ul className="space-y-3">
                  {currentStage.deliverables.map((item, i) => (
                    <motion.li
                      key={item}
                      initial={{ opacity: 0, x: -6 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: i * 0.05 }}
                      className="flex items-start gap-2.5 text-xs sm:text-sm text-zinc-300"
                    >
                      <CheckCircle2 className="w-4 h-4 text-cyan-400 shrink-0 mt-0.5" />
                      <span>{item}</span>
                    </motion.li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        </FadeIn>
      </Container>
    </section>
  );
};
