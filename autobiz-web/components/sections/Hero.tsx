"use client";

import React from "react";
import { Container } from "@/components/ui/Container";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { HeroVisual } from "./HeroVisual";
import { FadeIn } from "@/components/animations/FadeIn";
import { Sparkles, ArrowDown } from "lucide-react";

export const Hero: React.FC = () => {
  return (
    <section
      id="hero"
      className="relative min-h-[92vh] flex items-center justify-center pt-28 pb-16 lg:pt-36 lg:pb-24 overflow-hidden"
    >
      <Container>
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-8 items-center">
          {/* Left Column: Hero Content */}
          <div className="lg:col-span-7 flex flex-col items-start text-left">
            <FadeIn delay={0.1}>
              <Badge variant="accent" dot className="mb-6">
                <Sparkles className="w-3.5 h-3.5 text-cyan-400 mr-1 inline" />
                AUTO BIZ • MODERN TECHNOLOGY & GROWTH
              </Badge>
            </FadeIn>

            <FadeIn delay={0.2}>
              <h1 className="text-5xl sm:text-6xl md:text-7xl xl:text-8xl font-black tracking-tighter text-white leading-[0.95] mb-6">
                <span className="block hover:text-cyan-400 transition-colors duration-300">BUILD.</span>
                <span className="block text-zinc-300 hover:text-emerald-400 transition-colors duration-300">SCALE.</span>
                <span className="block text-zinc-400 hover:text-purple-400 transition-colors duration-300">MARKET.</span>
              </h1>
            </FadeIn>

            <FadeIn delay={0.3}>
              <p className="text-lg sm:text-xl font-medium text-zinc-200 tracking-tight mb-4 max-w-xl">
                &ldquo;Turn ideas into digital products. Turn products into growing businesses.&rdquo;
              </p>
            </FadeIn>

            <FadeIn delay={0.4}>
              <p className="text-sm sm:text-base text-zinc-400 leading-relaxed max-w-xl mb-8">
                Auto BIZ combines technology, automation, analytics, and marketing to help businesses build stronger digital foundations and move toward sustainable growth.
              </p>
            </FadeIn>

            <FadeIn delay={0.5}>
              <div className="flex flex-wrap items-center gap-4 w-full sm:w-auto">
                <Button
                  href="#contact"
                  variant="glow"
                  size="lg"
                  showArrow
                  className="w-full sm:w-auto"
                >
                  Start a Conversation
                </Button>

                <Button
                  href="#what-we-do"
                  variant="secondary"
                  size="lg"
                  className="w-full sm:w-auto"
                >
                  Explore What We Do
                </Button>
              </div>
            </FadeIn>

            <FadeIn delay={0.6}>
              <div className="mt-10 flex items-center gap-6 text-xs text-zinc-400 pt-6 border-t border-white/[0.08] w-full max-w-lg">
                <div className="flex flex-col">
                  <span className="font-semibold text-zinc-300">Grounded Architecture</span>
                  <span className="text-[11px] text-zinc-400">Next.js & Cloud Systems</span>
                </div>
                <div className="w-[1px] h-6 bg-white/10" />
                <div className="flex flex-col">
                  <span className="font-semibold text-zinc-300">Real Data Telemetry</span>
                  <span className="text-[11px] text-zinc-400">Zero Fabricated Numbers</span>
                </div>
                <div className="w-[1px] h-6 bg-white/10" />
                <div className="flex flex-col">
                  <span className="font-semibold text-zinc-300">Human Governance</span>
                  <span className="text-[11px] text-zinc-400">Operator-in-the-loop</span>
                </div>
              </div>
            </FadeIn>
          </div>

          {/* Right Column: Original Interactive Growth Engine Visual */}
          <div className="lg:col-span-5 w-full">
            <FadeIn delay={0.3} direction="left">
              <HeroVisual />
            </FadeIn>
          </div>
        </div>

        {/* Subtle scroll down hint */}
        <div className="hidden md:flex justify-center mt-12">
          <a
            href="#trust-strip"
            className="flex flex-col items-center gap-1.5 text-[11px] font-mono text-zinc-400 hover:text-zinc-300 transition-colors"
            aria-label="Scroll to next section"
          >
            <span>SCROLL TO EXPLORE</span>
            <ArrowDown className="w-3.5 h-3.5 animate-bounce text-cyan-400/80" />
          </a>
        </div>
      </Container>
    </section>
  );
};
