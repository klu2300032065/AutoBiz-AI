export interface PrincipleItem {
  id: string;
  number: string;
  title: string;
  description: string;
  detail: string;
  iconName: string;
}

export const corePrinciples: PrincipleItem[] = [
  {
    id: "real-data",
    number: "01",
    title: "REAL DATA",
    description: "Decisions should be based on real information, not invented numbers.",
    detail: "We reject vanity metrics and ungrounded estimations. True optimization starts with empirical reality and transparent measurement.",
    iconName: "CheckCircle2",
  },
  {
    id: "human-control",
    number: "02",
    title: "HUMAN CONTROL",
    description: "Important external actions remain under human approval.",
    detail: "Automation is an accelerator, not an unchecked authority. Critical business decisions, customer communications, and financial actions require explicit human sign-off.",
    iconName: "ShieldCheck",
  },
  {
    id: "smart-systems",
    number: "03",
    title: "SMART SYSTEMS",
    description: "Automation should remove repetitive work without removing control.",
    detail: "We construct reliable workflows that handle operational friction seamlessly while maintaining clear visibility and manual override capability.",
    iconName: "Cpu",
  },
  {
    id: "continuous-improvement",
    number: "04",
    title: "CONTINUOUS IMPROVEMENT",
    description: "Measure what happens, learn from it, and improve.",
    detail: "Growth is not a one-time event; it is an iterative compounding feedback loop between building, measuring actual outcomes, and refining the system.",
    iconName: "RefreshCw",
  },
];
