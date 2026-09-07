export interface ProcessStage {
  step: string;
  name: string;
  headline: string;
  description: string;
  deliverables: string[];
  focus: string;
}

export const processStages: ProcessStage[] = [
  {
    step: "01",
    name: "DISCOVER",
    headline: "Understand the business, audience, problem, and opportunity.",
    description:
      "We begin by deconstructing your business model, customer requirements, existing friction points, and market dynamics. No assumptions — only structured requirements and clear success criteria.",
    deliverables: [
      "Requirements & Scope Architecture",
      "Technical Feasibility Assessment",
      "User Journey & Pain-Point Map",
      "Growth Opportunity Benchmark",
    ],
    focus: "Strategic Alignment & Clarity",
  },
  {
    step: "02",
    name: "BUILD",
    headline: "Create the digital foundation.",
    description:
      "We engineer clean, performant, and maintainable software systems. From modern frontends and solid backend APIs to database structures and automation routines.",
    deliverables: [
      "Production Next.js / React Architecture",
      "Responsive & Accessible UI Systems",
      "API Integrations & Database Layer",
      "Automated Workflow Pipelines",
    ],
    focus: "Engineering Rigor & Quality",
  },
  {
    step: "03",
    name: "LAUNCH",
    headline: "Bring the product or solution into the real world.",
    description:
      "Deploy with stability, continuous integration, and seamless DNS/hosting setups. We ensure testing, error monitoring, and performance safeguards are locked in prior to go-live.",
    deliverables: [
      "Production CI/CD Deployment",
      "Performance & SEO Optimization",
      "Security & Environment Audits",
      "Operational Handover & Documentation",
    ],
    focus: "Stability & Zero Downtime",
  },
  {
    step: "04",
    name: "MEASURE",
    headline: "Understand actual performance.",
    description:
      "Track verified metrics rather than guesswork. Monitor how real users interact, where drop-offs happen, and how business operations perform under real-world conditions.",
    deliverables: [
      "Telemetry & Conversion Tracking",
      "User Engagement Analysis",
      "System Reliability Metrics",
      "Verified Performance Baselines",
    ],
    focus: "Empirical Business Truth",
  },
  {
    step: "05",
    name: "SCALE",
    headline: "Improve what works and identify the next opportunity.",
    description:
      "Iterate systematically based on observed metrics. Automate high-friction tasks, strengthen marketing channels, and expand software capabilities to accelerate growth.",
    deliverables: [
      "Process Automation Expansion",
      "Acquisition Channel Scaling",
      "Feature Iteration & Refinement",
      "Continuous Optimization Roadmap",
    ],
    focus: "Compound Growth & Efficiency",
  },
];
