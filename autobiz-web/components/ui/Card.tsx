import React from "react";
import { cn } from "@/lib/utils";

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
  className?: string;
  hoverEffect?: boolean;
  glowOnHover?: boolean;
  borderAccent?: boolean;
}

export const Card: React.FC<CardProps> = ({
  children,
  className,
  hoverEffect = false,
  glowOnHover = false,
  borderAccent = false,
  ...props
}) => {
  return (
    <div
      className={cn(
        "relative rounded-2xl bg-[#0e1118]/80 backdrop-blur-md border border-white/[0.08] transition-all duration-300 overflow-hidden",
        hoverEffect && "hover:border-white/20 hover:-translate-y-1 hover:shadow-xl hover:shadow-black/40",
        glowOnHover && "group hover:shadow-[0_0_30px_rgba(6,182,212,0.12)]",
        borderAccent && "border-t-white/20",
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
};
