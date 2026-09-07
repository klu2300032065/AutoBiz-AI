"use client";

import React from "react";
import { cn } from "@/lib/utils";
import { ArrowRight, Loader2 } from "lucide-react";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "outline" | "ghost" | "glow";
  size?: "sm" | "md" | "lg";
  href?: string;
  external?: boolean;
  showArrow?: boolean;
  isLoading?: boolean;
  icon?: React.ReactNode;
}

export const Button = React.forwardRef<HTMLButtonElement | HTMLAnchorElement, ButtonProps>(
  (
    {
      children,
      className,
      variant = "primary",
      size = "md",
      href,
      external,
      showArrow = false,
      isLoading = false,
      icon,
      disabled,
      ...props
    },
    ref
  ) => {
    const baseStyles =
      "relative group inline-flex items-center justify-center font-medium transition-all duration-300 rounded-lg select-none cursor-pointer focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-cyan-500/50 focus-visible:ring-offset-2 focus-visible:ring-offset-zinc-950 disabled:opacity-50 disabled:pointer-events-none";

    const variantStyles = {
      primary:
        "bg-white text-zinc-950 hover:bg-zinc-100 hover:shadow-[0_0_24px_rgba(255,255,255,0.25)] active:scale-[0.98] border border-white/20 font-semibold",
      secondary:
        "bg-zinc-900/90 text-zinc-100 hover:bg-zinc-800/90 border border-zinc-800 hover:border-zinc-700 active:scale-[0.98] backdrop-blur-sm",
      outline:
        "bg-transparent text-zinc-300 hover:text-white border border-zinc-700/80 hover:border-zinc-500 hover:bg-zinc-900/40 active:scale-[0.98]",
      ghost:
        "bg-transparent text-zinc-400 hover:text-white hover:bg-zinc-800/50 active:scale-[0.98]",
      glow:
        "bg-gradient-to-r from-cyan-500 to-blue-600 text-white font-semibold shadow-[0_0_25px_rgba(6,182,212,0.35)] hover:shadow-[0_0_35px_rgba(6,182,212,0.55)] hover:brightness-110 active:scale-[0.98] border border-cyan-400/30",
    };

    const sizeStyles = {
      sm: "text-xs px-3.5 py-2 gap-1.5",
      md: "text-sm px-5 py-2.5 gap-2",
      lg: "text-base px-6 py-3.5 gap-2.5",
    };

    const content = (
      <>
        {isLoading ? (
          <Loader2 className="w-4 h-4 animate-spin" />
        ) : (
          icon && <span className="transition-transform group-hover:scale-110">{icon}</span>
        )}
        <span>{children}</span>
        {showArrow && !isLoading && (
          <ArrowRight className="w-4 h-4 transition-transform duration-300 group-hover:translate-x-1" />
        )}
      </>
    );

    if (href) {
      if (external) {
        return (
          <a
            ref={ref as React.Ref<HTMLAnchorElement>}
            href={href}
            target="_blank"
            rel="noopener noreferrer"
            className={cn(baseStyles, variantStyles[variant], sizeStyles[size], className)}
            {...(props as React.AnchorHTMLAttributes<HTMLAnchorElement>)}
          >
            {content}
          </a>
        );
      }
      return (
        <a
          ref={ref as React.Ref<HTMLAnchorElement>}
          href={href}
          className={cn(baseStyles, variantStyles[variant], sizeStyles[size], className)}
          {...(props as React.AnchorHTMLAttributes<HTMLAnchorElement>)}
        >
          {content}
        </a>
      );
    }

    return (
      <button
        ref={ref as React.Ref<HTMLButtonElement>}
        disabled={disabled || isLoading}
        className={cn(baseStyles, variantStyles[variant], sizeStyles[size], className)}
        {...props}
      >
        {content}
      </button>
    );
  }
);

Button.displayName = "Button";
