"use client";

import React from "react";
import { Container } from "@/components/ui/Container";
import { contactInfo } from "@/data/contact";
import { footerNavigation } from "@/data/navigation";
import { Mail, Phone, MapPin, ExternalLink, ArrowUp } from "lucide-react";

export const Footer: React.FC = () => {
  const currentYear = new Date().getFullYear();

  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  return (
    <footer className="relative bg-[#07080b] border-t border-white/[0.08] pt-16 pb-12 overflow-hidden text-zinc-400">
      {/* Subtle top ambient glow */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-3/4 h-[1px] bg-gradient-to-r from-transparent via-cyan-500/40 to-transparent" />

      <Container>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-10 pb-12 border-b border-white/[0.08]">
          {/* Brand Column */}
          <div className="lg:col-span-2 flex flex-col gap-4">
            <a href="#hero" className="flex items-center gap-3 group">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-cyan-500 via-indigo-600 to-purple-600 p-[1px] shadow-[0_0_15px_rgba(6,182,212,0.3)]">
                <div className="w-full h-full bg-[#0a0c12] rounded-[7px] flex items-center justify-center">
                  <span className="font-black text-xs tracking-tighter bg-gradient-to-r from-cyan-400 to-white bg-clip-text text-transparent">
                    AB
                  </span>
                </div>
              </div>
              <div className="flex flex-col">
                <span className="font-bold text-lg tracking-wider text-white">AUTO BIZ</span>
                <span className="text-[10px] text-zinc-400 font-mono tracking-widest">
                  BUILD • SCALE • MARKET
                </span>
              </div>
            </a>

            <p className="text-sm text-zinc-400 leading-relaxed max-w-sm mt-2">
              &ldquo;{contactInfo.tagline}&rdquo;
            </p>

            <p className="text-xs text-zinc-400 leading-relaxed max-w-sm">
              We help businesses move systematically from concept to software foundation, scale operations with clarity, and market with intelligence.
            </p>

            <div className="flex items-center gap-2 text-xs text-cyan-400/80 font-mono mt-2">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
              Available for Strategic Engagements
            </div>
          </div>

          {/* Column 1: Explore */}
          <div className="flex flex-col gap-3">
            <h4 className="text-xs font-semibold text-white tracking-wider uppercase font-mono">
              Explore
            </h4>
            <ul className="flex flex-col gap-2 text-sm">
              {footerNavigation.explore.map((item) => (
                <li key={item.label}>
                  <a
                    href={item.href}
                    className="hover:text-white transition-colors duration-200"
                  >
                    {item.label}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* Column 2: Services */}
          <div className="flex flex-col gap-3">
            <h4 className="text-xs font-semibold text-white tracking-wider uppercase font-mono">
              Services
            </h4>
            <ul className="flex flex-col gap-2 text-sm">
              {footerNavigation.services.map((item) => (
                <li key={item.label}>
                  <a
                    href={item.href}
                    className="hover:text-white transition-colors duration-200"
                  >
                    {item.label}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* Column 3: Connect */}
          <div className="flex flex-col gap-3">
            <h4 className="text-xs font-semibold text-white tracking-wider uppercase font-mono">
              Connect
            </h4>
            <ul className="flex flex-col gap-3 text-sm">
              <li>
                <a
                  href={`mailto:${contactInfo.email}`}
                  className="flex items-center gap-2 hover:text-white transition-colors text-xs break-all"
                >
                  <Mail className="w-3.5 h-3.5 text-cyan-400 shrink-0" />
                  <span>{contactInfo.email}</span>
                </a>
              </li>
              <li>
                <a
                  href={`tel:+91${contactInfo.phone}`}
                  className="flex items-center gap-2 hover:text-white transition-colors text-xs"
                >
                  <Phone className="w-3.5 h-3.5 text-cyan-400 shrink-0" />
                  <span>{contactInfo.formattedPhone}</span>
                </a>
              </li>
              <li className="flex items-start gap-2 text-xs text-zinc-400">
                <MapPin className="w-3.5 h-3.5 text-cyan-400 shrink-0 mt-0.5" />
                <span>{contactInfo.location}</span>
              </li>
              {contactInfo.linkedin && (
                <li>
                  <a
                    href={contactInfo.linkedin}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-1.5 text-xs text-zinc-300 hover:text-cyan-400 transition-colors"
                  >
                    <ExternalLink className="w-3.5 h-3.5 text-cyan-400" />
                    <span>LinkedIn Profile</span>
                  </a>
                </li>
              )}
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-8 text-xs text-zinc-400">
          <p>© {currentYear} Auto BIZ. All rights reserved.</p>

          <div className="flex items-center gap-6">
            <span className="text-[11px] font-mono text-zinc-400">
              BUILD • SCALE • MARKET
            </span>
            <button
              onClick={scrollToTop}
              className="flex items-center gap-1 text-zinc-400 hover:text-white transition-colors p-1 cursor-pointer"
              aria-label="Back to top"
            >
              <span>Top</span>
              <ArrowUp className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      </Container>
    </footer>
  );
};
