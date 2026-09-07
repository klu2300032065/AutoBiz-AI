"use client";

import React, { useState } from "react";
import { Container } from "@/components/ui/Container";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Modal } from "@/components/ui/Modal";
import { FadeIn } from "@/components/animations/FadeIn";
import { growthEngines, GrowthEngine } from "@/data/engines";
import { CheckCircle2, ArrowRight, Code2, TrendingUp, Megaphone } from "lucide-react";

export const WhatWeDo: React.FC = () => {
  const [selectedEngine, setSelectedEngine] = useState<GrowthEngine | null>(null);

  const getIcon = (id: string) => {
    switch (id) {
      case "build":
        return <Code2 className="w-5 h-5 text-blue-400" />;
      case "scale":
        return <TrendingUp className="w-5 h-5 text-emerald-400" />;
      case "market":
        return <Megaphone className="w-5 h-5 text-purple-400" />;
      default:
        return null;
    }
  };

  return (
    <section id="what-we-do" className="relative py-24 sm:py-32 overflow-hidden">
      <Container>
        <FadeIn>
          <SectionHeading
            eyebrow="GROWTH ARCHITECTURE"
            title="One partner. Three growth engines."
            description="We eliminate fragmented agencies and disconnected tools by unifying modern software engineering, operational automation, and market acquisition."
          />
        </FadeIn>

        {/* 3 Large Premium Engine Cards */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {growthEngines.map((engine, idx) => (
            <FadeIn key={engine.id} delay={0.15 * (idx + 1)} fullWidth>
              <Card
                className={`group h-full flex flex-col justify-between p-8 sm:p-10 transition-all duration-300 hover:-translate-y-1.5 ${engine.borderHover}`}
                borderAccent
              >
                {/* Background ambient accent */}
                <div
                  className={`absolute top-0 right-0 w-64 h-64 bg-gradient-to-bl ${engine.accentGradient} rounded-full blur-3xl opacity-40 pointer-events-none transition-opacity group-hover:opacity-80`}
                />

                <div className="relative z-10">
                  {/* Header info */}
                  <div className="flex items-center justify-between mb-6">
                    <div className="flex items-center gap-3">
                      <div className="p-2.5 rounded-xl bg-white/[0.05] border border-white/[0.1]">
                        {getIcon(engine.id)}
                      </div>
                      <Badge variant="outline" size="sm">
                        {engine.badge}
                      </Badge>
                    </div>
                    <span className="text-xl font-mono font-bold text-zinc-400">
                      {engine.number}
                    </span>
                  </div>

                  <h3 className="text-2xl font-bold text-white tracking-tight mb-2">
                    {engine.title}
                  </h3>

                  <p className="text-sm font-semibold text-cyan-400/90 mb-4 font-mono">
                    &ldquo;{engine.subtitle}&rdquo;
                  </p>

                  <p className="text-sm text-zinc-400 leading-relaxed mb-8">
                    {engine.description}
                  </p>

                  {/* Feature Checklist */}
                  <div className="space-y-3 pt-6 border-t border-white/[0.08] mb-8">
                    <span className="text-[11px] font-mono uppercase tracking-wider text-zinc-400">
                      Key Capabilities
                    </span>
                    <ul className="space-y-2.5">
                      {engine.features.map((feature) => (
                        <li key={feature} className="flex items-center gap-2.5 text-xs text-zinc-300">
                          <CheckCircle2 className="w-4 h-4 text-cyan-400 shrink-0" />
                          <span>{feature}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>

                {/* Bottom CTA */}
                <div className="relative z-10 pt-4">
                  <Button
                    onClick={() => setSelectedEngine(engine)}
                    variant="outline"
                    size="md"
                    className="w-full justify-between group-hover:border-white/40"
                    showArrow
                  >
                    {engine.ctaText}
                  </Button>
                </div>
              </Card>
            </FadeIn>
          ))}
        </div>

        {/* Modal for detailed engine specs */}
        <Modal
          isOpen={!!selectedEngine}
          onClose={() => setSelectedEngine(null)}
          title={selectedEngine ? `${selectedEngine.number} • ${selectedEngine.title} ENGINE ARCHITECTURE` : ""}
        >
          {selectedEngine && (
            <div className="flex flex-col gap-6">
              <p className="text-sm text-zinc-300 leading-relaxed">
                {selectedEngine.description}
              </p>

              <div className="space-y-4">
                <h4 className="text-xs font-mono uppercase tracking-wider text-cyan-400">
                  Detailed Implementation Capabilities
                </h4>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  {selectedEngine.capabilities.map((cap) => (
                    <div
                      key={cap.title}
                      className="p-4 rounded-xl bg-white/[0.03] border border-white/[0.08]"
                    >
                      <h5 className="text-xs font-bold text-white mb-1">{cap.title}</h5>
                      <p className="text-xs text-zinc-400 leading-relaxed">{cap.description}</p>
                    </div>
                  ))}
                </div>
              </div>

              <div className="pt-4 border-t border-white/10 flex items-center justify-between">
                <Button
                  href="#contact"
                  onClick={() => setSelectedEngine(null)}
                  variant="glow"
                  size="md"
                  showArrow
                >
                  Start with {selectedEngine.title}
                </Button>
                <button
                  onClick={() => setSelectedEngine(null)}
                  className="text-xs text-zinc-400 hover:text-white transition-colors cursor-pointer"
                >
                  Close Specification
                </button>
              </div>
            </div>
          )}
        </Modal>
      </Container>
    </section>
  );
};
