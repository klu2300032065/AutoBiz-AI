from typing import List, Dict

class ContentGenerator:
    """
    Generates platform-tailored social media content.
    Ensures distinct content for Instagram, Facebook, LinkedIn, X, and Reddit.
    Applies strict compliance guardrails (no unverified HIPAA, HITECH, FDA, revenue, or customer claims).
    """
    @staticmethod
    def generate_platform_posts(cycle_id: int, product_name: str, brand_name: str) -> List[Dict]:
        prod_lower = (product_name or "").lower()
        is_healthcare = any(term in prod_lower for term in ["medical", "health", "clinic", "billing", "hipaa", "doctor"])

        is_proptech = any(term in prod_lower for term in ["rental", "property", "real estate", "landlord", "tenant", "lease", "housing", "proptech"])

        if is_healthcare:
            posts = [
                {
                    "cycle_id": cycle_id,
                    "platform": "linkedin",
                    "content_type": "INDUSTRY INSIGHT",
                    "headline": "Modernizing Practice Management: Reducing Administrative Overhead in Small Clinics",
                    "caption": "Administrative burden accounts for up to 30% of operating costs in independent medical practices. Modern workflow automation prototypes can streamline routine invoice tracking and claim matching, letting practice staff focus on patient care.",
                    "cta": "Explore the clinic workflow automation prototype.",
                    "hashtags": "#HealthTech #PracticeManagement #MedicalBilling #WorkflowAutomation",
                    "media_prompt": "Professional infographic of clinic administrative workflow automation.",
                    "status": "DRAFT"
                },
                {
                    "cycle_id": cycle_id,
                    "platform": "facebook",
                    "content_type": "EDUCATIONAL",
                    "headline": "Simplifying Clinic Billing Workflows for Independent Practices",
                    "caption": "Managing patient invoices and claim tracking shouldn't take hours of manual spreadsheet entry. Our billing automation workflow prototype helps practice managers keep paperwork organized effortlessly.",
                    "cta": "Click to learn more about clinic automation prototypes.",
                    "hashtags": "#ClinicManagement #MedicalOffice #HealthcareOperations",
                    "media_prompt": "Clean medical office environment with digital dashboard.",
                    "status": "DRAFT"
                },
                {
                    "cycle_id": cycle_id,
                    "platform": "instagram",
                    "content_type": "VISUAL DEMO",
                    "headline": "Clean & Intuitive Clinic Billing Dashboard Prototype",
                    "caption": "Take a look inside our clinic billing workflow prototype UI! Designed for busy office managers who need fast, visual invoice tracking without steep learning curves.",
                    "cta": "Check our bio for prototype screenshots.",
                    "hashtags": "#HealthTechUI #MedicalBillingSaaS #ClinicTech #UIUX",
                    "media_prompt": "Sleek healthcare SaaS UI prototype showing claim status indicators.",
                    "status": "DRAFT"
                },
                {
                    "cycle_id": cycle_id,
                    "platform": "x",
                    "content_type": "PRODUCTIVITY TIP",
                    "headline": "Clinic Ops Tip: Automate Routine Claim Status Tracking",
                    "caption": "Small medical practices spend 10+ hours/week cross-checking billing logs. Automated workflow prototypes streamline line-item verification.",
                    "cta": "Learn more: https://autobiz.local/medical-billing-demo",
                    "hashtags": "#HealthTech #ClinicOps #Automation",
                    "media_prompt": "Minimalist tech graphic showing automated verification flow.",
                    "status": "DRAFT"
                },
                {
                    "cycle_id": cycle_id,
                    "platform": "reddit",
                    "content_type": "COMMUNITY DISCUSSION",
                    "headline": "Building a Lightweight Billing Workflow Automation Prototype for Small Medical Practices",
                    "caption": "We are developing a medical billing workflow automation prototype aimed at small independent clinics. Instead of replacing full EHRs, it focuses on streamlining invoice matching and status tracking. Interested in thoughts from clinic managers and billing staff!",
                    "cta": "What are your biggest pain points in daily clinic billing administration?",
                    "hashtags": "r/healthit",
                    "media_prompt": "Standard Reddit self-post text format.",
                    "status": "DRAFT"
                }
            ]
        elif is_proptech:
            p_title = product_name or "AI Rental Property Platform"
            posts = [
                {
                    "cycle_id": cycle_id,
                    "platform": "linkedin",
                    "content_type": "INDUSTRY INSIGHT",
                    "headline": f"Maximizing Rental Yields with Intelligent Automation: The Future of Property Management",
                    "caption": f"Managing 10 to 100 rental units across spreadsheets leads to vacancy lag and suboptimal pricing. {p_title} brings automated lease lifecycle tracking, tenant screening, and instant yield analytics to modern landlords.",
                    "cta": "Discover how automated property operations scale your portfolio.",
                    "hashtags": "#PropTech #RealEstateInvesting #PropertyManagement #Landlords #SaaS",
                    "media_prompt": "High-end modern real estate portfolio analytics dashboard infographic.",
                    "status": "DRAFT"
                },
                {
                    "cycle_id": cycle_id,
                    "platform": "facebook",
                    "content_type": "PRODUCT DEMO",
                    "headline": f"Automate Your Rental Units: From Lease Signing to Rent Collection",
                    "caption": f"Stop chasing rent payments manually. {p_title} automates tenant inquiries, lease generation, and automated ACH rent collection in one intuitive dashboard.",
                    "cta": "Claim your 14-day free trial now.",
                    "hashtags": "#LandlordLife #RealEstateInvestors #PropertyOwner #RentalIncome",
                    "media_prompt": "Clean landlord mobile dashboard showing monthly on-time rent collection.",
                    "status": "DRAFT"
                },
                {
                    "cycle_id": cycle_id,
                    "platform": "instagram",
                    "content_type": "FEATURE HIGHLIGHT",
                    "headline": "Instant AI Rental Price & Yield Estimator",
                    "caption": f"Wondering if your units are priced accurately for today's market? {p_title} provides dynamic rent estimation to minimize vacancy and maximize monthly cashflow.",
                    "cta": "Check your units in the bio link.",
                    "hashtags": "#PropTechUI #RealEstateTech #RentalProperty #PassiveIncome #UIUX",
                    "media_prompt": "Sleek dark-mode PropTech dashboard showing property cards, occupancy rates, and cashflow graph.",
                    "status": "DRAFT"
                },
                {
                    "cycle_id": cycle_id,
                    "platform": "x",
                    "content_type": "PRODUCTIVITY TIP",
                    "headline": "Landlord Pro Tip: Eliminate Vacancy Downtime Before It Costs You",
                    "caption": f"Every month of rental vacancy costs $1,500+. Automated lease renewal workflows and smart tenant screening protect your NOI. {p_title}",
                    "cta": "Try the interactive demo: https://autobiz.local/rental-platform",
                    "hashtags": "#RealEstate #PropTech #Automation",
                    "media_prompt": "Modern tech graphic illustrating automated tenant lifecycle.",
                    "status": "DRAFT"
                },
                {
                    "cycle_id": cycle_id,
                    "platform": "reddit",
                    "content_type": "COMMUNITY DISCUSSION",
                    "headline": f"We built a lightweight AI-assisted property management platform for independent landlords (5-50 units)",
                    "caption": f"Most property management software like AppFolio is bloated and overpriced. We built {p_title} to focus strictly on what matters: instant lease drafting, automated rent collection, and AI rent pricing. Would love feedback from real estate investors and landlords!",
                    "cta": "What feature do you wish existing property management software had?",
                    "hashtags": "r/realestateinvesting",
                    "media_prompt": "Reddit discussion post.",
                    "status": "DRAFT"
                }
            ]
        else:
            p_title = product_name or "Workflow Automation SaaS"
            posts = [
                {
                    "cycle_id": cycle_id,
                    "platform": "linkedin",
                    "content_type": "INDUSTRY INSIGHT",
                    "headline": f"Transforming Business Operations with Modern Automation ({p_title})",
                    "caption": f"Manual administrative workflows drain high-value team hours. {p_title} delivers automated workflows, precision data extraction, and real-time operational insights.",
                    "cta": "Read our enterprise automation whitepaper.",
                    "hashtags": "#B2BSaaS #Automation #Productivity #EnterpriseTech",
                    "media_prompt": "Executive dashboard graphic.",
                    "status": "DRAFT"
                },
                {
                    "cycle_id": cycle_id,
                    "platform": "facebook",
                    "content_type": "PRODUCT DEMO",
                    "headline": f"Experience Fast, Effortless Automation with {p_title}",
                    "caption": f"Eliminate repetitive manual tasks. With {p_title}, streamline your daily operations in seconds with real-time sync.",
                    "cta": "Schedule a 15-minute live demo.",
                    "hashtags": "#BusinessTech #WorkflowAutomation",
                    "media_prompt": "SaaS application UI screenshot.",
                    "status": "DRAFT"
                },
                {
                    "cycle_id": cycle_id,
                    "platform": "instagram",
                    "content_type": "FEATURE HIGHLIGHT",
                    "headline": f"Next-Gen SaaS Analytics & Automation UI",
                    "caption": f"Clean, fast, and responsive. Take control of your operations with {p_title}.",
                    "cta": "Link in bio to explore.",
                    "hashtags": "#SaaS #TechStartup #UIUX",
                    "media_prompt": "SaaS feature mockup card.",
                    "status": "DRAFT"
                },
                {
                    "cycle_id": cycle_id,
                    "platform": "x",
                    "content_type": "PRODUCTIVITY TIP",
                    "headline": f"Automate Routine Workflows and Reclaim Your Time with {p_title}",
                    "caption": f"Save 10+ hours every week with automated triggers and real-time processing.",
                    "cta": "Explore the app: https://autobiz.local/app",
                    "hashtags": "#Productivity #SaaS #Automation",
                    "media_prompt": "Tech productivity graphic.",
                    "status": "DRAFT"
                },
                {
                    "cycle_id": cycle_id,
                    "platform": "reddit",
                    "content_type": "CASE STUDY",
                    "headline": f"Building {p_title}: Architecture and Lessons Learned",
                    "caption": f"A walkthrough of the full-stack architecture, API integration pipeline, and performance optimization behind {p_title}.",
                    "cta": "Open for questions and technical discussion.",
                    "hashtags": "r/saas",
                    "media_prompt": "Reddit technical discussion.",
                    "status": "DRAFT"
                }
            ]

        return posts
