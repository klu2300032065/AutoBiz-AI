"use client";

import React, { useState } from "react";
import { Container } from "@/components/ui/Container";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { FadeIn } from "@/components/animations/FadeIn";
import { motion, AnimatePresence } from "framer-motion";
import {
  Cpu,
  Sparkles,
  ShieldCheck,
  CheckCircle2,
  AlertTriangle,
  ArrowRight,
  Bot,
  User,
} from "lucide-react";

export const AISection: React.FC = () => {
  const [scenario, setScenario] = useState<"verified" | "insufficient">("verified");
  const [isSimulating, setIsSimulating] = useState<boolean>(false);

  const handleScenarioChange = (newScenario: "verified" | "insufficient") => {
    setIsSimulating(true);
    setScenario(newScenario);
    setTimeout(() => {
      setIsSimulating(false);
    }, 400);
  };

  return (
    <section id="ai-intelligence" className="relative py-24 sm:py-32 overflow-hidden">
      <Container>
        <FadeIn>
          <SectionHeading
            eyebrow="GROUNDED AI ARCHITECTURE"
            title="Intelligence that works with you."
            description="Use AI to understand information, automate repetitive work, discover opportunities, and make better decisions — grounded in verified business truth."
          />
        </FadeIn>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
          {/* Left Column: AI Product Philosophy */}
          <div className="lg:col-span-5 flex flex-col gap-6">
            <FadeIn delay={0.1}>
              <div className="p-6 rounded-2xl bg-white/[0.02] border border-white/[0.08]">
                <div className="flex items-center gap-2.5 mb-3">
                  <ShieldCheck className="w-5 h-5 text-emerald-400" />
                  <h3 className="text-base font-bold text-white tracking-tight">
                    The Grounded AI Principle
                  </h3>
                </div>
                <p className="text-xs sm:text-sm text-zinc-300 leading-relaxed">
                  Most AI tools hallucinate optimistic numbers when data is scarce. At Auto BIZ, our systems adhere to a strict rule: <strong className="text-white">AI must never invent business data.</strong> If sufficient real data is not present, the system states it truthfully.
                </p>
              </div>
            </FadeIn>

            <FadeIn delay={0.2}>
              <div className="space-y-3">
                <span className="text-xs font-mono uppercase tracking-wider text-zinc-400">
                  Interactive Demonstration
                </span>
                <div className="flex flex-col sm:flex-row gap-2">
                  <button
                    onClick={() => handleScenarioChange("verified")}
                    className={`flex-1 p-3 rounded-xl border text-left text-xs font-medium transition-all duration-200 cursor-pointer ${
                      scenario === "verified"
                        ? "bg-cyan-500/10 border-cyan-500/40 text-white"
                        : "bg-white/[0.02] border-white/[0.06] text-zinc-400 hover:text-white"
                    }`}
                  >
                    <span className="font-bold block text-cyan-400">Scenario 1</span>
                    <span>Verified Data Present</span>
                  </button>

                  <button
                    onClick={() => handleScenarioChange("insufficient")}
                    className={`flex-1 p-3 rounded-xl border text-left text-xs font-medium transition-all duration-200 cursor-pointer ${
                      scenario === "insufficient"
                        ? "bg-amber-500/10 border-amber-500/40 text-white"
                        : "bg-white/[0.02] border-white/[0.06] text-zinc-400 hover:text-white"
                    }`}
                  >
                    <span className="font-bold block text-amber-400">Scenario 2</span>
                    <span>Data Not Available</span>
                  </button>
                </div>
              </div>
            </FadeIn>
          </div>

          {/* Right Column: AI Simulated Chat Console */}
          <div className="lg:col-span-7 w-full">
            <FadeIn delay={0.3}>
              <Card className="p-6 sm:p-8 bg-[#0b0e16] border-white/[0.12] shadow-2xl">
                {/* Console Header */}
                <div className="flex items-center justify-between pb-4 mb-6 border-b border-white/[0.08]">
                  <div className="flex items-center gap-2.5">
                    <div className="p-1.5 rounded-lg bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
                      <Cpu className="w-4 h-4" />
                    </div>
                    <div>
                      <h4 className="text-xs font-bold text-white">Auto BIZ Decision Assistant</h4>
                      <span className="text-[10px] font-mono text-zinc-400">Grounded Reasoning Agent</span>
                    </div>
                  </div>

                  <Badge variant={scenario === "verified" ? "accent" : "muted"} size="sm">
                    {scenario === "verified" ? "Telemetry Grounded" : "Safeguard Active"}
                  </Badge>
                </div>

                {/* Conversation Flow */}
                <div className="space-y-4">
                  {/* User Query */}
                  <div className="flex items-start gap-3">
                    <div className="w-7 h-7 rounded-full bg-white/10 flex items-center justify-center shrink-0 mt-0.5">
                      <User className="w-3.5 h-3.5 text-zinc-300" />
                    </div>
                    <div className="p-3.5 rounded-2xl rounded-tl-sm bg-white/[0.04] border border-white/[0.08] text-xs sm:text-sm text-zinc-200 max-w-lg">
                      &ldquo;Where should we focus our next growth effort?&rdquo;
                    </div>
                  </div>

                  {/* AI Response */}
                  <div className="flex items-start gap-3">
                    <div className="w-7 h-7 rounded-full bg-gradient-to-tr from-cyan-500 to-indigo-600 flex items-center justify-center shrink-0 mt-0.5">
                      <Bot className="w-3.5 h-3.5 text-white" />
                    </div>

                    <div className="flex-1">
                      <AnimatePresence mode="wait">
                        {isSimulating ? (
                          <motion.div
                            key="simulating"
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            className="p-4 rounded-2xl bg-zinc-950/80 border border-white/[0.08] text-xs font-mono text-zinc-400 flex items-center gap-2"
                          >
                            <Sparkles className="w-4 h-4 text-cyan-400 animate-spin" />
                            <span>Analyzing available business telemetry...</span>
                          </motion.div>
                        ) : scenario === "verified" ? (
                          <motion.div
                            key="verified-output"
                            initial={{ opacity: 0, y: 6 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0 }}
                            className="space-y-3 p-4 rounded-2xl rounded-tl-sm bg-zinc-950 border border-white/[0.08]"
                          >
                            <div className="text-xs text-zinc-400 font-mono flex items-center gap-1.5 pb-2 border-b border-white/[0.06]">
                              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                              <span>Analysis complete: 3 verified telemetry sources correlated.</span>
                            </div>

                            <div className="space-y-2">
                              <div className="p-2.5 rounded-lg bg-white/[0.02] border border-white/[0.04]">
                                <span className="text-[10px] font-mono text-cyan-400 uppercase tracking-wider block font-bold">
                                  01. Verified Insight
                                </span>
                                <p className="text-xs text-zinc-300 mt-0.5">
                                  72% of qualified inquiries express demand for automated onboarding workflows before signing.
                                </p>
                              </div>

                              <div className="p-2.5 rounded-lg bg-white/[0.02] border border-white/[0.04]">
                                <span className="text-[10px] font-mono text-emerald-400 uppercase tracking-wider block font-bold">
                                  02. High-Yield Opportunity
                                </span>
                                <p className="text-xs text-zinc-300 mt-0.5">
                                  Deploying an interactive onboarding portal reduces initial friction and shortens sales cycles.
                                </p>
                              </div>

                              <div className="p-2.5 rounded-lg bg-white/[0.02] border border-white/[0.04]">
                                <span className="text-[10px] font-mono text-purple-400 uppercase tracking-wider block font-bold">
                                  03. Recommended Action
                                </span>
                                <p className="text-xs text-zinc-300 mt-0.5">
                                  Prioritize BUILD engine for client portal. Prepare automated notification webhooks for sign-up triggers.
                                </p>
                              </div>
                            </div>
                          </motion.div>
                        ) : (
                          <motion.div
                            key="insufficient-output"
                            initial={{ opacity: 0, y: 6 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0 }}
                            className="p-4 rounded-2xl rounded-tl-sm bg-zinc-950 border border-amber-500/20 space-y-3"
                          >
                            <div className="flex items-center gap-2 text-amber-400 text-xs font-mono font-bold">
                              <AlertTriangle className="w-4 h-4 shrink-0" />
                              <span>INSUFFICIENT DATA SAFEGUARD</span>
                            </div>

                            <p className="text-xs text-zinc-300 leading-relaxed font-mono">
                              &ldquo;Insufficient data to make a verified recommendation. Inbound traffic telemetry has not accumulated the baseline sample size needed for statistical validity.&rdquo;
                            </p>

                            <div className="p-2.5 rounded-lg bg-amber-500/5 border border-amber-500/10 text-[11px] text-zinc-400">
                              <span className="font-semibold text-zinc-300">Action:</span> Continue telemetry ingestion across acquisition channels before committing capital to speculative expansion.
                            </div>
                          </motion.div>
                        )}
                      </AnimatePresence>
                    </div>
                  </div>
                </div>
              </Card>
            </FadeIn>
          </div>
        </div>
      </Container>
    </section>
  );
};
