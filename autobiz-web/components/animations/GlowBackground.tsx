"use client";

import React from "react";

export const GlowBackground: React.FC = () => {
  return (
    <div className="fixed inset-0 pointer-events-none z-0 overflow-hidden" aria-hidden="true">
      {/* Radial Top Glow (Cyan / Indigo) */}
      <div className="absolute -top-40 left-1/2 -translate-x-1/2 w-[800px] h-[500px] bg-gradient-to-b from-cyan-500/10 via-indigo-600/5 to-transparent blur-3xl opacity-70" />

      {/* Subtle Right Glow (Purple) */}
      <div className="absolute top-1/3 -right-60 w-[600px] h-[600px] bg-purple-600/5 blur-3xl rounded-full opacity-60" />

      {/* Subtle Left Glow (Emerald) */}
      <div className="absolute top-2/3 -left-60 w-[600px] h-[600px] bg-emerald-600/5 blur-3xl rounded-full opacity-50" />

      {/* Subtle Grid Background Overlay */}
      <div
        className="absolute inset-0 opacity-[0.025]"
        style={{
          backgroundImage: `linear-gradient(to right, #ffffff 1px, transparent 1px), linear-gradient(to bottom, #ffffff 1px, transparent 1px)`,
          backgroundSize: "64px 64px",
        }}
      />
    </div>
  );
};
