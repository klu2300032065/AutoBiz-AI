export interface ServiceItem {
  id: string;
  number: string;
  title: string;
  description: string;
  iconName: string;
  tags: string[];
  capabilities: string[];
}

export const servicesList: ServiceItem[] = [
  {
    id: "web-dev",
    number: "01",
    title: "Web Development",
    description: "Modern websites and web applications built for performance and scale.",
    iconName: "Globe",
    tags: ["Next.js", "React", "TypeScript", "Tailwind CSS"],
    capabilities: [
      "High-speed server rendered web apps",
      "Responsive, mobile-first design systems",
      "API integrations & headless architectures",
      "Clean, modular, and maintainable codebases",
    ],
  },
  {
    id: "ai-solutions",
    number: "02",
    title: "AI Solutions",
    description: "AI-powered tools that automate work and support better decisions.",
    iconName: "Cpu",
    tags: ["Automated Workflows", "Decision Support", "Data Extraction", "Smart Agents"],
    capabilities: [
      "Task-specific intelligent automation",
      "Grounded decision intelligence systems",
      "Document and workflow processing",
      "Human-in-the-loop oversight systems",
    ],
  },
  {
    id: "ui-ux",
    number: "03",
    title: "UI/UX Design",
    description: "Digital experiences designed around clarity, usability, and conversion.",
    iconName: "Layout",
    tags: ["Design Systems", "User Research", "Interaction", "Prototyping"],
    capabilities: [
      "Comprehensive component design tokens",
      "User journey mapping & friction reduction",
      "High-fidelity interactive prototypes",
      "Accessibility-first interface design",
    ],
  },
  {
    id: "automation",
    number: "04",
    title: "Business Automation",
    description: "Replace repetitive processes with intelligent systems.",
    iconName: "Zap",
    tags: ["Workflow Pipelines", "CRM Sync", "Notification Systems", "Ops Tooling"],
    capabilities: [
      "End-to-end operational pipeline automation",
      "Cross-platform data synchronization",
      "Automated client reporting & notifications",
      "Error detection and recovery routines",
    ],
  },
  {
    id: "digital-product",
    number: "05",
    title: "Digital Product Development",
    description: "Turn ideas into functional digital products.",
    iconName: "Code2",
    tags: ["MVP to Scale", "SaaS Architecture", "Cloud Systems", "Database Design"],
    capabilities: [
      "Zero-to-one product engineering",
      "Robust relational & document database schemas",
      "Authentication and multi-tenant structures",
      "Scalable cloud deployment setups",
    ],
  },
  {
    id: "analytics",
    number: "06",
    title: "Analytics & Insights",
    description: "Understand performance using real business data.",
    iconName: "BarChart3",
    tags: ["Telemetry", "KPI Dashboards", "Conversion Funnels", "Data Audits"],
    capabilities: [
      "Event-driven telemetry tracking",
      "Executive summary dashboards",
      "Customer journey cohort analysis",
      "Truthful, unskewed performance metrics",
    ],
  },
  {
    id: "marketing-systems",
    number: "07",
    title: "Marketing Systems",
    description: "Build repeatable systems for content and customer acquisition.",
    iconName: "Megaphone",
    tags: ["Acquisition Funnels", "Content Engines", "Lead Flow", "Campaign Ops"],
    capabilities: [
      "Repeatable lead qualification funnels",
      "Structured content distribution engines",
      "Multi-channel campaign deployment",
      "Landing page optimization & A/B frameworks",
    ],
  },
  {
    id: "growth-strategy",
    number: "08",
    title: "Growth Strategy",
    description: "Identify opportunities and create practical paths to growth.",
    iconName: "TrendingUp",
    tags: ["Market Analysis", "Unit Economics", "Execution Roadmaps", "Retention"],
    capabilities: [
      "Systematic growth bottleneck audits",
      "Practical milestone-based roadmaps",
      "Retention and lifetime value enhancements",
      "Targeted channel prioritization",
    ],
  },
];
