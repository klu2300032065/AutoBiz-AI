"use client";

import React from "react";
import { Container } from "@/components/ui/Container";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { FadeIn } from "@/components/animations/FadeIn";
import { Code2, TrendingUp, Megaphone, CheckCircle2 } from "lucide-react";

export const PricingEngagement: React.FC = () => {
  const engagementModels = [
    {
      id: "build",
      number: "01",
      title: "BUILD ENGAGEMENT",
      subtitle: "Digital products & engineering",
      description:
        "Engineered for businesses requiring custom websites, web applications, internal tools, or integrated AI applications built from the ground up.",
      features: [
        "Full-stack Web & Application Engineering",
        "Next.js / React Architecture & Database Setup",
        "UI/UX Design Systems & Prototyping",
        "Custom AI Workflow & API Integrations",
      ],
      icon: Code2,
      accent: "text-blue-400 border-blue-500/30",
    },
    {
      id: "scale",
      number: "02",
      title: "SCALE ENGAGEMENT",
      subtitle: "Automation, analytics & systems",
      description:
        "Designed for established operations seeking to eliminate manual friction, implement telemetry tracking, and optimize performance.",
      features: [
        "End-to-end Process Automation",
        "Real Data Analytics & Telemetry Setup",
        "Operational Pipeline Restructuring",
        "System Health & Velocity Monitoring",
      ],
      icon: TrendingUp,
      accent: "text-emerald-400 border-emerald-500/30",
    },
    {
      id: "market",
      number: "03",
      title: "MARKET ENGAGEMENT",
      subtitle: "Acquisition & marketing systems",
      description:
        "Built for companies ready to reach targeted customer segments with structured campaigns, compelling messaging, and closed-loop ROI attribution.",
      features: [
        "Go-to-Market Strategy & Positioning",
        "Acquisition Funnel Design & Optimization",
        "Content Distribution & Campaign Frameworks",
        "Marketing Analytics & Attribution Matrix",
      ],
      icon: Megaphone,
      accent: "text-purple-400 border-purple-500/30",
    },
  ];

  return (
    <section id="engagement" className="relative py-24 sm:py-32 overflow-hidden">
      <Container>
        <FadeIn>
          <SectionHeading
            eyebrow="TAILORED COLLABORATION"
            title="Let's build around your needs."
            description="Every business has a different starting point. Let's identify what needs to be built, improved, or accelerated — with clear milestones and transparent scope."
          />
        </FadeIn>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-12">
          {engagementModels.map((item, idx) => {
            const Icon = item.icon;
            return (
              <FadeIn key={item.id} delay={0.15 * (idx + 1)} fullWidth>
                <Card className="h-full p-8 flex flex-col justify-between hover:border-white/20 transition-all duration-300" hoverEffect>
                  <div>
                    <div className="flex items-center justify-between mb-6">
                      <div className="p-2.5 rounded-xl bg-white/[0.04] border border-white/[0.08]">
                        <Icon className={`w-5 h-5 ${item.accent.split(" ")[0]}`} />
                      </div>
                      <span className="text-xs font-mono font-bold text-zinc-400">
                        {item.number}
                      </span>
                    </div>

                    <h3 className="text-xl font-bold text-white tracking-tight mb-1">
                      {item.title}
                    </h3>

                    <p className="text-xs font-mono text-cyan-400 mb-4 font-semibold">
                      {item.subtitle}
                    </p>

                    <p className="text-xs sm:text-sm text-zinc-400 leading-relaxed mb-6">
                      {item.description}
                    </p>

                    <div className="space-y-2.5 pt-6 border-t border-white/[0.06] mb-6">
                      <span className="text-[10px] font-mono uppercase tracking-wider text-zinc-400 block">
                        Scope Scope
                      </span>
                      {item.features.map((feat) => (
                        <div key={feat} className="flex items-center gap-2.5 text-xs text-zinc-300">
                          <CheckCircle2 className="w-3.5 h-3.5 text-cyan-400 shrink-0" />
                          <span>{feat}</span>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div className="pt-4 border-t border-white/[0.06]">
                    <Button
                      href="#contact"
                      variant="outline"
                      size="md"
                      className="w-full justify-center hover:border-cyan-500/40"
                      showArrow
                    >
                      Inquire for {item.title.split(" ")[0]}
                    </Button>
                  </div>
                </Card>
              </FadeIn>
            );
          })}
        </div>

        {/* Global CTA Banner */}
        <FadeIn delay={0.4}>
          <div className="p-8 sm:p-10 rounded-2xl bg-gradient-to-r from-cyan-950/40 via-zinc-900/60 to-purple-950/40 border border-white/[0.1] text-center max-w-3xl mx-auto flex flex-col items-center">
            <h3 className="text-2xl font-bold text-white mb-3">
              Need a hybrid solution combining Build, Scale & Market?
            </h3>
            <p className="text-sm text-zinc-300 max-w-xl mb-6">
              We frequently structure cross-engine engagements that develop your web platform while concurrently standing up analytics and marketing pipelines.
            </p>
            <Button href="#contact" variant="glow" size="lg" showArrow>
              Start a Conversation
            </Button>
          </div>
        </FadeIn>
      </Container>
    </section>
  );
};
