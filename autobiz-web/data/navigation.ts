export interface NavItem {
  label: string;
  href: string;
}

export const navItems: NavItem[] = [
  { label: "Home", href: "#hero" },
  { label: "What We Do", href: "#what-we-do" },
  { label: "How It Works", href: "#how-it-works" },
  { label: "Services", href: "#services" },
  { label: "Preview", href: "#preview" },
  { label: "About", href: "#about" },
  { label: "Contact", href: "#contact" },
];

export const footerNavigation = {
  explore: [
    { label: "Home", href: "#hero" },
    { label: "What We Do", href: "#what-we-do" },
    { label: "How It Works", href: "#how-it-works" },
    { label: "Services", href: "#services" },
    { label: "Principles", href: "#principles" },
    { label: "About", href: "#about" },
    { label: "Contact", href: "#contact" },
  ],
  services: [
    { label: "Web Development", href: "#services" },
    { label: "Digital Product Development", href: "#services" },
    { label: "AI Solutions", href: "#services" },
    { label: "Business Automation", href: "#services" },
    { label: "Analytics & Insights", href: "#services" },
    { label: "Marketing Systems", href: "#services" },
  ],
  engines: [
    { label: "01. BUILD Engine", href: "#what-we-do" },
    { label: "02. SCALE Engine", href: "#what-we-do" },
    { label: "03. MARKET Engine", href: "#what-we-do" },
  ],
};
