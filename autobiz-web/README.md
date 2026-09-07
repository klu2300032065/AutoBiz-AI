# Auto BIZ — Official Platform & Landing Page

> **"Build better. Scale smarter. Market with purpose."**
> *Turn ideas into digital products. Turn products into growing businesses.*

---

## 🚀 Overview

**Auto BIZ** is a modern technology and business-growth company combining software development, business automation, performance telemetry, and customer acquisition into one unified growth engine.

This repository contains the standalone, production-quality Next.js web application engineered from the ground up with modular architecture, strict data integrity standards, and high-end aesthetic fidelity.

---

## 🛠️ Technology Stack

- **Framework**: [Next.js](https://nextjs.org/) (App Router, Server Components & Client Hydration)
- **UI & Components**: [React](https://react.dev/), [TypeScript](https://www.typescriptlang.org/)
- **Styling**: [Tailwind CSS](https://tailwindcss.com/) v4 with refined CSS variables & glassmorphic tokens
- **Animations & Micro-interactions**: [Framer Motion](https://www.framer.com/motion/) with `prefers-reduced-motion` compliance
- **Icons**: [Lucide React](https://lucide.dev/)
- **Class Utilities**: `clsx`, `tailwind-merge`

---

## 📂 Project Architecture

```
autobiz-web/
├── app/
│   ├── globals.css              # Design tokens, custom scrollbars, and dark theme layers
│   ├── icon.svg                 # Abstract vector brand mark
│   ├── layout.tsx               # Root layout, Inter typography & SEO OpenGraph metadata
│   ├── page.tsx                 # Master page assembling modular sections
│   ├── robots.ts                # Dynamic robots.txt configuration
│   └── sitemap.ts               # Dynamic XML sitemap
├── components/
│   ├── animations/
│   │   ├── FadeIn.tsx           # Motion scroll-reveal wrapper with accessible fallbacks
│   │   └── GlowBackground.tsx   # Atmospheric radial glow and grid mesh
│   ├── layout/
│   │   ├── Footer.tsx           # Footer with dynamic year & verified contact channels
│   │   ├── MobileMenu.tsx       # Animated mobile drawer navigation
│   │   └── Navbar.tsx           # Sticky glassmorphic navbar with active section observer
│   ├── sections/
│   │   ├── AboutSection.tsx     # Truthful about narrative & verified HQ coordinates
│   │   ├── AISection.tsx        # Grounded AI decision engine simulator
│   │   ├── ContactSection.tsx   # Direct contact cards + validated inquiry form
│   │   ├── CorePrinciples.tsx   # 4 core business principles
│   │   ├── DashboardPreview.tsx # Interactive sample operations dashboard
│   │   ├── FAQSection.tsx       # Animated FAQ accordion
│   │   ├── Hero.tsx             # High-impact typography & dual CTA triggers
│   │   ├── HeroVisual.tsx       # Interactive BUILD → SCALE → MARKET growth visualizer
│   │   ├── PricingEngagement.tsx# Transparent, unhyped engagement categories
│   │   ├── ProcessTimeline.tsx  # 5-stage execution methodology explorer
│   │   ├── SelectedWork.tsx     # Clean project blueprints & coming soon status
│   │   ├── Services.tsx         # 8-item comprehensive services grid
│   │   └── TrustStrip.tsx       # Minimal 3-engine transition banner
│   └── ui/
│       ├── Badge.tsx            # Pill badges with pulse dots
│       ├── Button.tsx           # Multi-variant button with glow, hover movement & states
│       ├── Card.tsx             # Fine-border elevated glassmorphic card
│       ├── Container.tsx        # Standardized responsive max-width wrapper
│       ├── Modal.tsx            # Accessible modal dialog
│       └── SectionHeading.tsx   # Consistent section typography & badges
├── data/
│   ├── contact.ts               # Centralized verified contact information
│   ├── engines.ts               # BUILD, SCALE, MARKET engine definitions
│   ├── faq.ts                   # 7 truthful FAQ items
│   ├── navigation.ts            # Header & footer routes
│   ├── principles.ts            # 4 company principles
│   ├── process.ts               # 5-stage methodology data
│   ├── projects.ts              # Selected work blueprints
│   └── services.ts              # 8 core capability specs
├── lib/
│   ├── animations.ts            # Shared Framer Motion variants
│   └── utils.ts                 # Class merging utility
├── .env.example
├── package.json
└── tsconfig.json
```

---

## ⚡ Getting Started

### Prerequisites

- **Node.js**: v18+ (tested on Node v22.18.0)
- **npm**: v9+ (tested on npm 11.10.1)

### Installation

```bash
# Navigate to the project directory
cd autobiz-web

# Install dependencies
npm install
```

### Local Development

```bash
# Start the local development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser to view the application.

### Production Build

```bash
# Compile and build production bundle
npm run build

# Start the production server
npm start
```

---

## 📞 Verified Contact Information

All components source contact details from `data/contact.ts`:

- **Company / Brand**: Auto BIZ
- **Email**: `autobizai01@gmail.com`
- **Phone**: `+91 93819 87069`
- **Location**: Vijayawada, Andhra Pradesh, India
- **LinkedIn**: [https://www.linkedin.com/in/auto-biz-a76154428/](https://www.linkedin.com/in/auto-biz-a76154428/)

---

## 🗺️ Future Roadmap

- **Phase 1**: Premium Standalone Landing Page *(Complete)*
- **Phase 2**: Authentication & User Profiles
- **Phase 3**: Client Portal & Workspace Dashboard
- **Phase 4**: Real-time Development Status Tracking
- **Phase 5**: Telemetry & Analytics Event Ingestion
- **Phase 6**: Marketing Campaign Builder
- **Phase 7**: Grounded AI Business Assistant Integration
- **Phase 8**: Subscription & Payment Gateway Processing
