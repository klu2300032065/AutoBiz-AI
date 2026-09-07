export interface FAQItem {
  id: string;
  question: string;
  answer: string;
  category: string;
}

export const faqList: FAQItem[] = [
  {
    id: "faq-1",
    question: "What does Auto BIZ do?",
    answer:
      "Auto BIZ focuses on building digital products, improving business systems, supporting growth, and developing marketing capabilities. We operate across three core engines: BUILD (websites, web applications, digital products, and AI solutions), SCALE (process automation, analytics, and optimization), and MARKET (strategy, campaigns, and customer acquisition).",
    category: "General",
  },
  {
    id: "faq-2",
    question: "Do you build custom websites?",
    answer:
      "Yes. We design and build modern, high-performance websites and web applications tailored specifically to your business requirements. We use production-grade stacks such as Next.js, React, TypeScript, and modern CSS architecture to ensure speed, SEO excellence, and smooth user experience.",
    category: "Development",
  },
  {
    id: "faq-3",
    question: "Can you develop AI-powered applications?",
    answer:
      "Yes. We build grounded AI solutions that integrate seamlessly into real business workflows. Our approach prioritizes reliability, human control, and truthful data processing over ungrounded hype.",
    category: "AI & Tech",
  },
  {
    id: "faq-4",
    question: "Can you help improve an existing business?",
    answer:
      "Absolutely. We frequently work with businesses to audit existing operational bottlenecks, automate repetitive tasks, modernize legacy web applications, and implement clear analytics tracking to unlock new efficiencies.",
    category: "Scaling",
  },
  {
    id: "faq-5",
    question: "Do you provide marketing services?",
    answer:
      "Yes. We design and execute cohesive marketing strategies, content distribution frameworks, and campaign architectures focused on acquiring high-intent customers and measuring actual ROI.",
    category: "Marketing",
  },
  {
    id: "faq-6",
    question: "Can projects start small and grow over time?",
    answer:
      "Yes. Every engagement is structured around your current needs and stage. You can begin with a targeted foundational build (such as a modern web application or an automation pipeline) and expand into scaling and marketing engines as your traction grows.",
    category: "Engagement",
  },
  {
    id: "faq-7",
    question: "How do I get started?",
    answer:
      "You can start by submitting the contact form on this page or reaching out directly via email at autobizai01@gmail.com or phone at +91 93819 87069. We will schedule a strategic discussion to understand your requirements, define clear milestones, and map out a practical execution plan.",
    category: "Getting Started",
  },
];
