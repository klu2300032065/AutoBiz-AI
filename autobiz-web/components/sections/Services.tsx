"use client";

import React, { useState } from "react";
import { Container } from "@/components/ui/Container";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { Card } from "@/components/ui/Card";
import { Modal } from "@/components/ui/Modal";
import { Button } from "@/components/ui/Button";
import { FadeIn } from "@/components/animations/FadeIn";
import { servicesList, ServiceItem } from "@/data/services";
import {
  Globe,
  Cpu,
  Layout,
  Zap,
  Code2,
  BarChart3,
  Megaphone,
  TrendingUp,
  ArrowRight,
  CheckCircle2,
} from "lucide-react";

export const Services: React.FC = () => {
  const [selectedService, setSelectedService] = useState<ServiceItem | null>(null);

  const getServiceIcon = (name: string) => {
    switch (name) {
      case "Globe":
        return <Globe className="w-5 h-5 text-blue-400" />;
      case "Cpu":
        return <Cpu className="w-5 h-5 text-cyan-400" />;
      case "Layout":
        return <Layout className="w-5 h-5 text-purple-400" />;
      case "Zap":
        return <Zap className="w-5 h-5 text-amber-400" />;
      case "Code2":
        return <Code2 className="w-5 h-5 text-indigo-400" />;
      case "BarChart3":
        return <BarChart3 className="w-5 h-5 text-emerald-400" />;
      case "Megaphone":
        return <Megaphone className="w-5 h-5 text-pink-400" />;
      case "TrendingUp":
        return <TrendingUp className="w-5 h-5 text-teal-400" />;
      default:
        return <Globe className="w-5 h-5 text-cyan-400" />;
    }
  };

  return (
    <section id="services" className="relative py-24 sm:py-32 overflow-hidden">
      <Container>
        <FadeIn>
          <SectionHeading
            eyebrow="CAPABILITIES & SERVICES"
            title="Everything you need to move forward."
            description="Comprehensive technology, design, analytics, and marketing solutions tailored to solve specific business problems and unlock sustainable scale."
          />
        </FadeIn>

        {/* 8 Services Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {servicesList.map((service, idx) => (
            <FadeIn key={service.id} delay={0.08 * (idx + 1)} fullWidth>
              <Card
                className="group h-full p-6 sm:p-7 flex flex-col justify-between cursor-pointer hover:border-white/20 transition-all duration-300"
                onClick={() => setSelectedService(service)}
                hoverEffect
              >
                <div>
                  {/* Icon & Number */}
                  <div className="flex items-center justify-between mb-5">
                    <div className="p-2.5 rounded-xl bg-white/[0.04] border border-white/[0.08] transition-transform duration-300 group-hover:scale-110">
                      {getServiceIcon(service.iconName)}
                    </div>
                    <span className="text-xs font-mono font-bold text-zinc-400">
                      {service.number}
                    </span>
                  </div>

                  <h3 className="text-lg font-bold text-white tracking-tight mb-2 group-hover:text-cyan-400 transition-colors">
                    {service.title}
                  </h3>

                  <p className="text-xs sm:text-sm text-zinc-400 leading-relaxed mb-6">
                    {service.description}
                  </p>
                </div>

                {/* Bottom Tags & Action */}
                <div className="pt-4 border-t border-white/[0.06]">
                  <div className="flex flex-wrap gap-1.5 mb-4">
                    {service.tags.slice(0, 2).map((tag) => (
                      <span
                        key={tag}
                        className="text-[10px] font-mono px-2 py-0.5 rounded bg-white/[0.03] text-zinc-400 border border-white/[0.05]"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>

                  <div className="flex items-center justify-between text-xs font-semibold text-zinc-400 group-hover:text-white transition-colors">
                    <span>View Details</span>
                    <ArrowRight className="w-3.5 h-3.5 transition-transform group-hover:translate-x-1 text-cyan-400" />
                  </div>
                </div>
              </Card>
            </FadeIn>
          ))}
        </div>

        {/* Modal for Service Deep Dive */}
        <Modal
          isOpen={!!selectedService}
          onClose={() => setSelectedService(null)}
          title={selectedService ? `${selectedService.number} • ${selectedService.title}` : ""}
        >
          {selectedService && (
            <div className="flex flex-col gap-6">
              <p className="text-sm text-zinc-300 leading-relaxed">
                {selectedService.description}
              </p>

              <div className="space-y-3">
                <h4 className="text-xs font-mono uppercase tracking-wider text-cyan-400">
                  Included Technical Deliverables
                </h4>
                <ul className="space-y-2">
                  {selectedService.capabilities.map((cap) => (
                    <li key={cap} className="flex items-center gap-2.5 text-xs sm:text-sm text-zinc-300">
                      <CheckCircle2 className="w-4 h-4 text-cyan-400 shrink-0" />
                      <span>{cap}</span>
                    </li>
                  ))}
                </ul>
              </div>

              <div className="flex flex-wrap gap-2 pt-2">
                {selectedService.tags.map((tag) => (
                  <span
                    key={tag}
                    className="text-[11px] font-mono px-2.5 py-1 rounded-md bg-white/[0.05] text-zinc-300 border border-white/10"
                  >
                    {tag}
                  </span>
                ))}
              </div>

              <div className="pt-4 border-t border-white/10 flex items-center justify-between">
                <Button
                  href="#contact"
                  onClick={() => setSelectedService(null)}
                  variant="glow"
                  size="md"
                  showArrow
                >
                  Inquire About {selectedService.title}
                </Button>
                <button
                  onClick={() => setSelectedService(null)}
                  className="text-xs text-zinc-400 hover:text-white transition-colors cursor-pointer"
                >
                  Close
                </button>
              </div>
            </div>
          )}
        </Modal>
      </Container>
    </section>
  );
};
