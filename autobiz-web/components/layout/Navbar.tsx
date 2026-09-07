"use client";

import React, { useState, useEffect } from "react";
import { navItems } from "@/data/navigation";
import { Button } from "@/components/ui/Button";
import { MobileMenu } from "./MobileMenu";
import { Menu } from "lucide-react";
import { cn } from "@/lib/utils";

export const Navbar: React.FC = () => {
  const [isScrolled, setIsScrolled] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [activeSection, setActiveSection] = useState("hero");

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);

      // Simple active section detection
      const sections = ["hero", "what-we-do", "how-it-works", "services", "preview", "about", "contact"];
      const scrollPosition = window.scrollY + 200;

      for (const section of sections) {
        const el = document.getElementById(section);
        if (el) {
          const top = el.offsetTop;
          const height = el.offsetHeight;
          if (scrollPosition >= top && scrollPosition < top + height) {
            setActiveSection(section);
            break;
          }
        }
      }
    };

    window.addEventListener("scroll", handleScroll, { passive: true });
    handleScroll();
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <>
      <header
        className={cn(
          "fixed top-0 inset-x-0 z-40 transition-all duration-300",
          isScrolled
            ? "bg-[#07080b]/80 backdrop-blur-md border-b border-white/[0.08] py-3.5 shadow-lg shadow-black/20"
            : "bg-transparent py-5"
        )}
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between">
          {/* Logo & Brand Identity */}
          <a
            href="#hero"
            className="flex items-center gap-3 group focus:outline-none"
            aria-label="Auto BIZ Home"
          >
            {/* Minimal Abstract Brand Mark */}
            <div className="relative w-8 h-8 rounded-lg bg-gradient-to-tr from-cyan-500 via-indigo-600 to-purple-600 p-[1px] shadow-[0_0_15px_rgba(6,182,212,0.3)] transition-transform duration-300 group-hover:scale-105">
              <div className="w-full h-full bg-[#0a0c12] rounded-[7px] flex items-center justify-center">
                <span className="font-black text-xs tracking-tighter bg-gradient-to-r from-cyan-400 to-white bg-clip-text text-transparent">
                  AB
                </span>
              </div>
            </div>

            <div className="flex flex-col">
              <span className="font-bold text-base tracking-wider text-white group-hover:text-cyan-400 transition-colors">
                AUTO BIZ
              </span>
              <span className="text-[9px] text-zinc-400 font-mono tracking-widest hidden sm:inline-block">
                BUILD • SCALE • MARKET
              </span>
            </div>
          </a>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center gap-1 rounded-full bg-zinc-900/60 border border-white/[0.08] px-3 py-1.5 backdrop-blur-md">
            {navItems.map((item) => {
              const sectionId = item.href.replace("#", "");
              const isActive = activeSection === sectionId;
              return (
                <a
                  key={item.label}
                  href={item.href}
                  className={cn(
                    "px-3.5 py-1.5 text-xs font-medium rounded-full transition-all duration-200",
                    isActive
                      ? "text-white bg-white/10 shadow-sm"
                      : "text-zinc-400 hover:text-zinc-200 hover:bg-white/[0.04]"
                  )}
                >
                  {item.label}
                </a>
              );
            })}
          </nav>

          {/* Desktop Right CTA */}
          <div className="hidden md:flex items-center gap-3">
            <Button
              href="#contact"
              variant="glow"
              size="sm"
              showArrow
            >
              Start a Conversation
            </Button>
          </div>

          {/* Mobile Hamburger Button */}
          <div className="flex md:hidden items-center gap-2">
            <Button
              href="#contact"
              variant="glow"
              size="sm"
              className="text-xs px-3 py-1.5"
            >
              Contact
            </Button>
            <button
              onClick={() => setMobileMenuOpen(true)}
              className="p-2 text-zinc-300 hover:text-white rounded-lg hover:bg-white/5 border border-white/10"
              aria-label="Open navigation menu"
              aria-expanded={mobileMenuOpen}
            >
              <Menu className="w-5 h-5" />
            </button>
          </div>
        </div>
      </header>

      {/* Mobile Menu Drawer */}
      <MobileMenu
        isOpen={mobileMenuOpen}
        onClose={() => setMobileMenuOpen(false)}
        activeSection={activeSection}
      />
    </>
  );
};
