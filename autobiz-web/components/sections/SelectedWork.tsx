"use client";

import React from "react";
import { Container } from "@/components/ui/Container";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { FadeIn } from "@/components/animations/FadeIn";
import { selectedWorkProjects } from "@/data/projects";
import { Clock, MessageSquareQuote } from "lucide-react";

export const SelectedWork: React.FC = () => {
  return (
    <section id="work" className="relative py-24 sm:py-32 bg-[#080a10] border-t border-white/[0.08] overflow-hidden">
      <Container>
        <FadeIn>
          <SectionHeading
            eyebrow="PORTFOLIO & BLUEPRINTS"
            title="Selected Work."
            description="Our project architecture blueprints. We present upcoming initiatives and case studies with complete transparency."
          />
        </FadeIn>

        {/* 3 Premium Project Blueprints */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-20">
          {selectedWorkProjects.map((project, idx) => (
            <FadeIn key={project.id} delay={0.15 * (idx + 1)} fullWidth>
              <Card className="h-full p-8 flex flex-col justify-between hover:border-white/20 transition-all duration-300 group" hoverEffect>
                <div>
                  <div className="flex items-center justify-between mb-5">
                    <span className="text-xs font-mono font-bold tracking-wider text-zinc-400">
                      {project.category}
                    </span>
                    <Badge variant="outline" size="sm" className={project.badgeColor}>
                      <Clock className="w-3 h-3 mr-1 inline" />
                      {project.status}
                    </Badge>
                  </div>

                  <h3 className="text-xl font-bold text-white tracking-tight mb-3 group-hover:text-cyan-400 transition-colors">
                    {project.title}
                  </h3>

                  <p className="text-xs sm:text-sm text-zinc-400 leading-relaxed mb-6">
                    {project.description}
                  </p>
                </div>

                <div className="pt-6 border-t border-white/[0.06] space-y-3">
                  <span className="text-[10px] font-mono uppercase tracking-wider text-zinc-400 block">
                    Architecture Stack
                  </span>
                  <div className="flex flex-wrap gap-1.5">
                    {project.architecture.map((tech) => (
                      <span
                        key={tech}
                        className="text-[11px] font-mono px-2 py-0.5 rounded bg-white/[0.03] text-zinc-300 border border-white/[0.06]"
                      >
                        {tech}
                      </span>
                    ))}
                  </div>

                  <div className="pt-2 text-[11px] font-mono text-zinc-400">
                    Scope: {project.scope}
                  </div>
                </div>
              </Card>
            </FadeIn>
          ))}
        </div>

        {/* Intentional, Beautiful Testimonial Placeholder */}
        <FadeIn delay={0.3}>
          <div className="rounded-2xl bg-gradient-to-b from-white/[0.03] to-transparent border border-white/[0.08] p-8 sm:p-10 text-center max-w-2xl mx-auto">
            <div className="w-10 h-10 rounded-full bg-cyan-500/10 text-cyan-400 flex items-center justify-center mx-auto mb-4 border border-cyan-500/20">
              <MessageSquareQuote className="w-5 h-5" />
            </div>

            <h4 className="text-base font-bold text-white mb-2">
              Verified Client Stories
            </h4>

            <p className="text-sm text-zinc-400 italic mb-4">
              &ldquo;Client stories and case evaluations will appear here as we deploy and measure them in the real world.&rdquo;
            </p>

            <span className="text-[11px] font-mono text-zinc-400 uppercase tracking-widest">
              Standard: 100% Verified Outcomes • No Fabricated Testimonials
            </span>
          </div>
        </FadeIn>
      </Container>
    </section>
  );
};
