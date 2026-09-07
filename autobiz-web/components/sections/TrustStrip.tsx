"use client";

import React from "react";
import { Container } from "@/components/ui/Container";
import { FadeIn } from "@/components/animations/FadeIn";
import { ArrowRight } from "lucide-react";

export const TrustStrip: React.FC = () => {
  const stages = [
    {
      number: "01",
      name: "BUILD",
      tagline: "Create the foundation.",
      accent: "hover:border-blue-500/40 text-blue-400",
    },
    {
      number: "02",
      name: "SCALE",
      tagline: "Turn traction into growth.",
      accent: "hover:border-emerald-500/40 text-emerald-400",
    },
    {
      number: "03",
      name: "MARKET",
      tagline: "Reach the right audience.",
      accent: "hover:border-purple-500/40 text-purple-400",
    },
  ];

  return (
    <section id="trust-strip" className="relative py-12 border-y border-white/[0.08] bg-[#090b10]/60">
      <Container>
        <FadeIn delay={0.1}>
          <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-6 pb-6 border-b border-white/[0.06]">
            <div className="flex items-center gap-2">
              <span className="w-1.5 h-1.5 rounded-full bg-cyan-400" />
              <span className="text-xs font-mono font-bold tracking-widest text-zinc-400 uppercase">
                THE SYSTEM TRANSITION
              </span>
            </div>
            <div className="text-xs font-mono tracking-wider text-zinc-400">
              FROM IDEA <span className="text-cyan-400">→</span> PRODUCT <span className="text-emerald-400">→</span> GROWTH
            </div>
          </div>
        </FadeIn>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 pt-6">
          {stages.map((stage, idx) => (
            <FadeIn key={stage.number} delay={0.15 * (idx + 1)}>
              <div
                className={`group relative p-5 rounded-xl bg-white/[0.02] border border-white/[0.06] transition-all duration-300 ${stage.accent}`}
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-mono text-zinc-400 font-bold">{stage.number}</span>
                  <span className={`text-xs font-mono font-bold tracking-wider ${stage.accent.split(" ")[1]}`}>
                    {stage.name}
                  </span>
                </div>
                <h3 className="text-base font-bold text-white tracking-tight mb-1">{stage.tagline}</h3>
                <div className="flex items-center gap-1 text-xs text-zinc-400 group-hover:text-zinc-300 transition-colors pt-2">
                  <span>Engine Blueprint</span>
                  <ArrowRight className="w-3 h-3 transition-transform group-hover:translate-x-1" />
                </div>
              </div>
            </FadeIn>
          ))}
        </div>
      </Container>
    </section>
  );
};
