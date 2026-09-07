export interface ProjectItem {
  id: string;
  category: string;
  title: string;
  status: string;
  description: string;
  architecture: string[];
  scope: string;
  badgeColor: string;
}

export const selectedWorkProjects: ProjectItem[] = [
  {
    id: "digital-product-suite",
    category: "DIGITAL PRODUCT",
    title: "Enterprise Workflow & Client Portal",
    status: "Coming Soon",
    description:
      "A centralized web application engineered for streamlined team collaboration, task routing, and transparent client reporting.",
    architecture: ["Next.js App Router", "TypeScript", "PostgreSQL", "Real-time Telemetry"],
    scope: "End-to-End System Development",
    badgeColor: "text-blue-400 border-blue-500/30 bg-blue-500/10",
  },
  {
    id: "ai-decision-engine",
    category: "AI SYSTEM",
    title: "Grounded Business Decision & Pipeline Agent",
    status: "Coming Soon",
    description:
      "An intelligent operations assistant providing verifiable insights from real business metrics while preserving human-in-the-loop governance.",
    architecture: ["Grounded Reasoning Engine", "Workflow Automation", "API Gateway", "Audit Logs"],
    scope: "Autonomous Workflow Intelligence",
    badgeColor: "text-emerald-400 border-emerald-500/30 bg-emerald-500/10",
  },
  {
    id: "growth-attribution-platform",
    category: "GROWTH PLATFORM",
    title: "Closed-Loop Acquisition & Analytics Hub",
    status: "Coming Soon",
    description:
      "A unified performance and marketing attribution dashboard connecting inbound lead generation directly to operational revenue.",
    architecture: ["Conversion Telemetry", "Event Bus", "Multi-Touch Attribution", "BI Interface"],
    scope: "Scale & Marketing Infrastructure",
    badgeColor: "text-purple-400 border-purple-500/30 bg-purple-500/10",
  },
];
