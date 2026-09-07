"use client";

import React from "react";
import { Container } from "@/components/ui/Container";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { Card } from "@/components/ui/Card";
import { FadeIn } from "@/components/animations/FadeIn";
import { corePrinciples } from "@/data/principles";
import { CheckCircle2, ShieldCheck, Cpu, RefreshCw } from "lucide-react";

export const CorePrinciples: React.FC = () => {
  const getIcon = (iconName: string) => {
    switch (iconName) {
      case "CheckCircle2":
        return <CheckCircle2 className="w-5 h-5 text-cyan-400" />;
      case "ShieldCheck":
        return <ShieldCheck className="w-5 h-5 text-emerald-400" />;
      case "Cpu":
        return <Cpu className="w-5 h-5 text-indigo-400" />;
      case "RefreshCw":
        return <RefreshCw className="w-5 h-5 text-purple-400" />;
      default:
        return <CheckCircle2 className="w-5 h-5 text-cyan-400" />;
    }
  };

  return (
    <section id="principles" className="relative py-24 sm:py-32 bg-[#090b10] border-t border-white/[0.08] overflow-hidden">
      <Container>
        <FadeIn>
          <SectionHeading
            eyebrow="OUR PHILOSOPHY"
            title="Built around outcomes, not noise."
            description="We operate by foundational principles that prioritize engineering integrity, human authority, and empirical evidence above transient trends."
          />
        </FadeIn>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 lg:gap-8">
          {corePrinciples.map((item, idx) => (
            <FadeIn key={item.id} delay={0.1 * (idx + 1)} fullWidth>
              <Card className="h-full p-8 flex flex-col justify-between hover:border-white/20 transition-all duration-300" hoverEffect>
                <div>
                  <div className="flex items-center justify-between mb-6">
                    <div className="p-3 rounded-xl bg-white/[0.04] border border-white/[0.08]">
                      {getIcon(item.iconName)}
                    </div>
                    <span className="text-xs font-mono font-bold text-zinc-400">
                      PRINCIPLE {item.number}
                    </span>
                  </div>

                  <h3 className="text-xl font-bold text-white tracking-tight mb-2">
                    {item.title}
                  </h3>

                  <p className="text-sm font-medium text-cyan-300 mb-4 leading-snug">
                    &ldquo;{item.description}&rdquo;
                  </p>

                  <p className="text-xs sm:text-sm text-zinc-400 leading-relaxed">
                    {item.detail}
                  </p>
                </div>

                <div className="pt-6 mt-6 border-t border-white/[0.06] flex items-center gap-2">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
                  <span className="text-[11px] font-mono text-zinc-400 uppercase tracking-wider">
                    Non-negotiable Standard
                  </span>
                </div>
              </Card>
            </FadeIn>
          ))}
        </div>
      </Container>
    </section>
  );
};
