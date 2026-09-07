"use client";

import React from "react";
import { motion, AnimatePresence } from "framer-motion";
import { X, ArrowRight, Mail, Phone, ExternalLink } from "lucide-react";
import { navItems } from "@/data/navigation";
import { contactInfo } from "@/data/contact";
import { Button } from "@/components/ui/Button";

interface MobileMenuProps {
  isOpen: boolean;
  onClose: () => void;
  activeSection: string;
}

export const MobileMenu: React.FC<MobileMenuProps> = ({
  isOpen,
  onClose,
  activeSection,
}) => {
  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 z-40 bg-black/80 backdrop-blur-md lg:hidden"
            aria-hidden="true"
          />

          {/* Drawer Menu */}
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.25, ease: "easeOut" }}
            className="fixed inset-x-4 top-20 z-50 rounded-2xl bg-[#0e1118] border border-white/10 p-6 shadow-2xl lg:hidden flex flex-col gap-6 max-h-[calc(100vh-6rem)] overflow-y-auto"
          >
            <div className="flex items-center justify-between pb-4 border-b border-white/10">
              <div className="flex flex-col">
                <span className="font-bold tracking-wider text-white">AUTO BIZ</span>
                <span className="text-[10px] text-zinc-400 tracking-widest font-mono">
                  BUILD • SCALE • MARKET
                </span>
              </div>
              <button
                onClick={onClose}
                className="p-2 text-zinc-400 hover:text-white rounded-lg hover:bg-white/5 cursor-pointer"
                aria-label="Close menu"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Navigation links */}
            <nav className="flex flex-col gap-1">
              {navItems.map((item) => {
                const isActive = activeSection === item.href.replace("#", "");
                return (
                  <a
                    key={item.label}
                    href={item.href}
                    onClick={onClose}
                    className={`flex items-center justify-between px-3 py-3 rounded-lg text-base font-medium transition-colors ${
                      isActive
                        ? "bg-white/10 text-white font-semibold"
                        : "text-zinc-300 hover:text-white hover:bg-white/5"
                    }`}
                  >
                    <span>{item.label}</span>
                    <ArrowRight className="w-4 h-4 text-zinc-500" />
                  </a>
                );
              })}
            </nav>

            {/* Quick Contact & Action */}
            <div className="flex flex-col gap-3 pt-4 border-t border-white/10">
              <Button
                href="#contact"
                onClick={onClose}
                variant="glow"
                size="md"
                className="w-full"
                showArrow
              >
                Start a Conversation
              </Button>

              <div className="flex flex-col gap-2 pt-2 text-xs text-zinc-400">
                <a
                  href={`mailto:${contactInfo.email}`}
                  className="flex items-center gap-2 hover:text-cyan-400 transition-colors py-1"
                >
                  <Mail className="w-3.5 h-3.5 text-cyan-400" />
                  <span>{contactInfo.email}</span>
                </a>
                <a
                  href={`tel:+91${contactInfo.phone}`}
                  className="flex items-center gap-2 hover:text-cyan-400 transition-colors py-1"
                >
                  <Phone className="w-3.5 h-3.5 text-cyan-400" />
                  <span>{contactInfo.formattedPhone}</span>
                </a>
                {contactInfo.linkedin && (
                  <a
                    href={contactInfo.linkedin}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center gap-2 hover:text-cyan-400 transition-colors py-1"
                  >
                    <ExternalLink className="w-3.5 h-3.5 text-cyan-400" />
                    <span>LinkedIn Profile</span>
                  </a>
                )}
              </div>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
};
