"use client";

import React from "react";
import { Container } from "@/components/ui/Container";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { FadeIn } from "@/components/animations/FadeIn";
import { Button } from "@/components/ui/Button";
import { contactInfo } from "@/data/contact";
import { MapPin, Mail, Phone, ExternalLink } from "lucide-react";

export const AboutSection: React.FC = () => {
  return (
    <section id="about" className="relative py-24 sm:py-32 overflow-hidden">
      <Container>
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
          {/* Left Column: Narrative */}
          <div className="lg:col-span-7 flex flex-col items-start">
            <FadeIn>
              <SectionHeading
                eyebrow="ABOUT AUTO BIZ"
                title="Building the infrastructure behind modern growth."
                align="left"
                className="mb-8"
              />
            </FadeIn>

            <FadeIn delay={0.1}>
              <p className="text-base sm:text-lg text-zinc-200 leading-relaxed mb-6 font-medium">
                Auto BIZ brings technology, business strategy, automation, analytics, and marketing together into a connected growth system.
              </p>
            </FadeIn>

            <FadeIn delay={0.2}>
              <p className="text-sm sm:text-base text-zinc-400 leading-relaxed mb-8">
                We believe businesses should spend less time managing disconnected tools and more time building, improving, and growing. By aligning digital product development directly with data clarity and marketing distribution, we help partners move forward with purpose.
              </p>
            </FadeIn>

            <FadeIn delay={0.3}>
              <div className="flex flex-wrap items-center gap-4">
                <Button href="#contact" variant="glow" size="md" showArrow>
                  Start a Conversation
                </Button>
                <Button href="#services" variant="outline" size="md">
                  View Capabilities
                </Button>
              </div>
            </FadeIn>
          </div>

          {/* Right Column: Location & Verified Identity Card */}
          <div className="lg:col-span-5 w-full">
            <FadeIn delay={0.3} direction="left">
              <div className="p-8 rounded-2xl bg-[#0c0f18] border border-white/[0.1] shadow-2xl relative overflow-hidden">
                <div className="absolute top-0 right-0 w-48 h-48 bg-gradient-to-bl from-cyan-500/10 to-transparent rounded-full blur-2xl pointer-events-none" />

                <div className="relative z-10 space-y-6">
                  <div>
                    <span className="text-[10px] font-mono uppercase tracking-widest text-cyan-400 block mb-1">
                      HQ & Operational Base
                    </span>
                    <h4 className="text-xl font-bold text-white tracking-tight">
                      {contactInfo.name}
                    </h4>
                    <p className="text-xs text-zinc-400 font-mono mt-0.5">
                      {contactInfo.positioning}
                    </p>
                  </div>

                  <div className="space-y-3 pt-4 border-t border-white/[0.08] text-xs">
                    <div className="flex items-start gap-3 text-zinc-300">
                      <MapPin className="w-4 h-4 text-cyan-400 shrink-0 mt-0.5" />
                      <span>{contactInfo.location}</span>
                    </div>

                    <a
                      href={`mailto:${contactInfo.email}`}
                      className="flex items-center gap-3 text-zinc-300 hover:text-cyan-400 transition-colors"
                    >
                      <Mail className="w-4 h-4 text-cyan-400 shrink-0" />
                      <span>{contactInfo.email}</span>
                    </a>

                    <a
                      href={`tel:+91${contactInfo.phone}`}
                      className="flex items-center gap-3 text-zinc-300 hover:text-cyan-400 transition-colors"
                    >
                      <Phone className="w-4 h-4 text-cyan-400 shrink-0" />
                      <span>{contactInfo.formattedPhone}</span>
                    </a>

                    {contactInfo.linkedin && (
                      <a
                        href={contactInfo.linkedin}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center gap-3 text-zinc-300 hover:text-cyan-400 transition-colors"
                      >
                        <ExternalLink className="w-4 h-4 text-cyan-400 shrink-0" />
                        <span>LinkedIn Company Profile</span>
                      </a>
                    )}
                  </div>

                  <div className="pt-4 border-t border-white/[0.08]">
                    <span className="text-[11px] font-mono text-zinc-400 block">
                      Philosophy: Grounded engineering • Verified analytics • Intentional growth
                    </span>
                  </div>
                </div>
              </div>
            </FadeIn>
          </div>
        </div>
      </Container>
    </section>
  );
};
