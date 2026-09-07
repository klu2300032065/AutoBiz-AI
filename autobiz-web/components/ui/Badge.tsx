import React from "react";
import { cn } from "@/lib/utils";

interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  children: React.ReactNode;
  variant?: "default" | "outline" | "accent" | "success" | "muted";
  size?: "sm" | "md";
  className?: string;
  dot?: boolean;
}

export const Badge: React.FC<BadgeProps> = ({
  children,
  variant = "default",
  size = "md",
  className,
  dot = false,
  ...props
}) => {
  const variantClasses = {
    default: "bg-zinc-800/80 text-zinc-300 border border-zinc-700/60 shadow-inner",
    outline: "bg-transparent text-zinc-400 border border-zinc-800",
    accent: "bg-cyan-500/10 text-cyan-400 border border-cyan-500/30",
    success: "bg-emerald-500/10 text-emerald-400 border border-emerald-500/30",
    muted: "bg-zinc-900/60 text-zinc-500 border border-zinc-800/60",
  };

  const sizeClasses = {
    sm: "text-[11px] px-2.5 py-0.5 tracking-wider font-medium uppercase",
    md: "text-xs px-3 py-1 tracking-wider font-medium uppercase",
  };

  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 rounded-full transition-all duration-200",
        variantClasses[variant],
        sizeClasses[size],
        className
      )}
      {...props}
    >
      {dot && (
        <span
          className={cn(
            "w-1.5 h-1.5 rounded-full animate-pulse",
            variant === "accent"
              ? "bg-cyan-400"
              : variant === "success"
              ? "bg-emerald-400"
              : "bg-zinc-400"
          )}
        />
      )}
      {children}
    </span>
  );
};
