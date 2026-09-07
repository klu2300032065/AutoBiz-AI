export interface GrowthEngine {
  id: "build" | "scale" | "market";
  number: string;
  tagline: string;
  title: string;
  subtitle: string;
  description: string;
  features: string[];
  capabilities: {
    title: string;
    description: string;
  }[];
  ctaText: string;
  badge: string;
  accentGradient: string;
  borderHover: string;
}

export const growthEngines: GrowthEngine[] = [
  {
    id: "build",
    number: "01",
    tagline: "Create the foundation.",
    title: "BUILD",
    subtitle: "Build with purpose.",
    description:
      "From websites and web applications to digital products and internal systems, we create technology designed around real business needs.",
    features: [
      "Web Development",
      "Product Development",
      "Business Systems",
      "AI Integration",
    ],
    capabilities: [
      {
        title: "Modern Web Architectures",
        description: "High-performance, responsive web applications engineered with Next.js, React, and robust API layers.",
      },
      {
        title: "Digital Product Crafting",
        description: "Translating complex operational workflows into intuitive, resilient digital software.",
      },
      {
        title: "AI Integration & Workflows",
        description: "Embedded machine intelligence that automates routine tasks and provides actionable context.",
      },
      {
        title: "Scalable Internal Systems",
        description: "Custom admin platforms, databases, and tooling configured for operational longevity.",
      },
    ],
    ctaText: "Explore Build",
    badge: "Foundation Engine",
    accentGradient: "from-blue-500/20 via-indigo-500/10 to-transparent",
    borderHover: "group-hover:border-blue-500/40",
  },
  {
    id: "scale",
    number: "02",
    tagline: "Turn traction into growth.",
    title: "SCALE",
    subtitle: "Scale with clarity.",
    description:
      "Use data, automation, and intelligent systems to understand what's working and identify where the next opportunity lies.",
    features: [
      "Business Analytics",
      "Process Automation",
      "Growth Insights",
      "Performance Tracking",
    ],
    capabilities: [
      {
        title: "Operational Automation",
        description: "Eliminating manual bottlenecks across customer onboarding, reporting, and fulfillment.",
      },
      {
        title: "Performance & Growth Analytics",
        description: "Real-time metrics tracking pipeline health, user engagement, and unit economics.",
      },
      {
        title: "Opportunity Discovery",
        description: "Systematic evaluation of business signals to highlight high-yield growth vectors.",
      },
      {
        title: "Process Optimization",
        description: "Restructuring business pipelines for maximum efficiency, speed, and reliability.",
      },
    ],
    ctaText: "Explore Scale",
    badge: "Velocity Engine",
    accentGradient: "from-emerald-500/20 via-teal-500/10 to-transparent",
    borderHover: "group-hover:border-emerald-500/40",
  },
  {
    id: "market",
    number: "03",
    tagline: "Reach the right audience.",
    title: "MARKET",
    subtitle: "Market with intelligence.",
    description:
      "Create campaigns, content, and customer acquisition systems that connect your business with the people who matter.",
    features: [
      "Marketing Strategy",
      "Content Systems",
      "Campaign Development",
      "Performance Analysis",
    ],
    capabilities: [
      {
        title: "Strategic Positioning",
        description: "Clarifying value propositions and differentiating offerings in competitive landscapes.",
      },
      {
        title: "Predictable Acquisition Channels",
        description: "Multi-touch campaign architecture focused on qualified leads and sustainable ROI.",
      },
      {
        title: "Content & Narrative Systems",
        description: "High-impact storytelling, technical copywriting, and distribution playbooks.",
      },
      {
        title: "Attribution & ROI Analytics",
        description: "Closed-loop measurement connecting marketing investment directly to business outcomes.",
      },
    ],
    ctaText: "Explore Market",
    badge: "Distribution Engine",
    accentGradient: "from-purple-500/20 via-pink-500/10 to-transparent",
    borderHover: "group-hover:border-purple-500/40",
  },
];
