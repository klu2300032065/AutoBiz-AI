import React from "react";
import { GlowBackground } from "@/components/animations/GlowBackground";
import { Navbar } from "@/components/layout/Navbar";
import { Hero } from "@/components/sections/Hero";
import { TrustStrip } from "@/components/sections/TrustStrip";
import { WhatWeDo } from "@/components/sections/WhatWeDo";
import { ProcessTimeline } from "@/components/sections/ProcessTimeline";
import { Services } from "@/components/sections/Services";
import { DashboardPreview } from "@/components/sections/DashboardPreview";
import { AISection } from "@/components/sections/AISection";
import { CorePrinciples } from "@/components/sections/CorePrinciples";
import { AboutSection } from "@/components/sections/AboutSection";
import { SelectedWork } from "@/components/sections/SelectedWork";
import { PricingEngagement } from "@/components/sections/PricingEngagement";
import { FAQSection } from "@/components/sections/FAQSection";
import { ContactSection } from "@/components/sections/ContactSection";
import { Footer } from "@/components/layout/Footer";

export default function HomePage() {
  return (
    <div className="relative min-h-screen bg-[#07080b] text-white flex flex-col selection:bg-cyan-500 selection:text-black">
      {/* Ambient background glow & grid */}
      <GlowBackground />

      {/* Sticky Navigation */}
      <Navbar />

      {/* Main Content Sections */}
      <main className="relative z-10 flex-grow">
        <Hero />
        <TrustStrip />
        <WhatWeDo />
        <ProcessTimeline />
        <Services />
        <DashboardPreview />
        <AISection />
        <CorePrinciples />
        <AboutSection />
        <SelectedWork />
        <PricingEngagement />
        <FAQSection />
        <ContactSection />
      </main>

      {/* Unified Footer */}
      <Footer />
    </div>
  );
}
