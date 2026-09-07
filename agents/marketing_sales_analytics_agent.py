import os
import json
from datetime import datetime
from models.msa_db import init_db, get_db
from memory.business_memory import BusinessMemory
from services.marketing_service import MarketingService
from services.analytics_service import AnalyticsService
from services.sales_service import SalesService
from tools.research_tools import query_ollama
from models.task import Task
from marketing.connectors.facebook import FacebookConnector
from marketing.connectors.instagram import InstagramConnector
from marketing.connectors.linkedin import LinkedInConnector
from marketing.connectors.x import XConnector
from marketing.connectors.reddit import RedditConnector
from marketing.campaign import CampaignBuilder
from marketing.content_generator import ContentGenerator
from services.approval_manager import ApprovalManager

class MarketingSalesAnalyticsAgent:
    def __init__(self):
        init_db()
        self.memory = BusinessMemory()
        self.approval_manager = ApprovalManager()
        self.connectors = {
            "facebook": FacebookConnector(),
            "instagram": InstagramConnector(),
            "linkedin": LinkedInConnector(),
            "x": XConnector(),
            "reddit": RedditConnector()
        }

    def run(self, task_or_input) -> dict:
        if isinstance(task_or_input, Task):
            task_id = task_or_input.task_id
            input_data = task_or_input.input_data
        else:
            task_id = 0
            input_data = str(task_or_input)

        if not input_data:
            return {"status": "error", "agent": "MarketingSalesAnalyticsAgent", "task_id": task_id, "result": None, "errors": ["No input_data provided"]}

        state = self.memory.get_business_state()
        cycle_id = state.cycle_id
        product_name = state.product or input_data.replace("Create marketing for ", "").strip()

        print(f"Initializing MSA Social Media Operations System for Cycle {cycle_id}: {product_name}...")

        # 1. Generate Campaign & Brand Profile
        campaign = CampaignBuilder.generate_campaign(cycle_id, product_name)
        brand_profile = self._ensure_brand_profile(cycle_id, product_name, campaign)

        # 2. Sync Social Accounts for facebook, instagram, linkedin, x, reddit
        social_accounts = self._sync_social_accounts(cycle_id)

        # 3. Generate Platform-Tailored Content & Draft Posts
        posts = self._generate_draft_posts(cycle_id, product_name, brand_profile["brand_name"])

        # 4. Generate Strategy Report
        report = self._generate_operations_report(cycle_id, product_name, brand_profile, social_accounts, posts, campaign)

        # 5. Request Human Approval for Marketing
        self.approval_manager.request_approval(
            "LAUNCH_MARKETING",
            f"Approve launch of marketing campaign for '{product_name}'.",
            risk_level="HIGH",
            estimated_cost=350.0,
            actual_cost=0.0,
            demo_cost=350.0,
            deployment_mode="LOCAL/DEMO",
            cycle_id=cycle_id
        )

        # Update business state to WAITING_MARKETING_APPROVAL
        state.marketing = "READY"
        state.stage = "WAITING_MARKETING_APPROVAL"
        self.memory.update_business_state(state)

        return {
            "status": "success",
            "agent": "MarketingSalesAnalyticsAgent",
            "task_id": task_id,
            "result": report,
            "artifacts": [],
            "errors": []
        }

    def _ensure_brand_profile(self, cycle_id: int, product_name: str, campaign=None) -> dict:
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT * FROM brand_profiles WHERE cycle_id = ?", (cycle_id,))
        row = c.fetchone()
        if row:
            conn.close()
            return dict(row)

        prod_lower = (product_name or "").lower()
        if "medical" in prod_lower or "clinic" in prod_lower or "health" in prod_lower:
            brand_data = {
                "cycle_id": cycle_id,
                "product_name": product_name,
                "brand_name": "MedBill Flow",
                "tagline": "Automated Clinic Billing Workflow Prototype",
                "short_description": "Streamlines clinic invoice tracking and claim matching for small medical practices.",
                "long_description": "Lightweight workflow automation prototype helping clinic office managers organize billing logs and claim status.",
                "target_audience": "Office managers, billing coordinators, and clinic administrative leads at small medical practices.",
                "value_proposition": "Reduce administrative paperwork burden and keep clinic billing logs organized.",
                "tone": "Professional, Respectful, Compliant B2B Healthcare Workflow Prototype",
                "keywords": "Clinic Automation, Medical Billing Prototype, Practice Workflow",
                "cta": "Explore the clinic workflow automation prototype [PROTOTYPE DEMO]",
                "website_placeholder": "https://autobiz.local/medical-billing-demo",
                "social_bio": "Streamlining billing workflow tracking for independent medical clinics."
            }
        else:
            brand_data = {
                "cycle_id": cycle_id,
                "product_name": product_name,
                "brand_name": f"{product_name.split()[0]} Flow" if product_name else "AutoMatch Flow",
                "tagline": "Automated Line-Item Freight Bill Matching for Logistics",
                "short_description": "Automates freight bill auditing and line-item matching against purchase orders and carrier rates.",
                "long_description": "Enterprise B2B SaaS platform that eliminates manual invoice auditing for freight forwarders, brokers, and 3PL logistics teams.",
                "target_audience": "Accounts Payable Leads & Logistics Operations Directors at mid-sized freight firms.",
                "value_proposition": "Cut freight bill processing time by 80% and eliminate costly carrier overpayment errors.",
                "tone": "Professional, Direct, Data-Driven B2B Enterprise",
                "keywords": "Logistics Automation, Freight Bill Audit, AP Automation, B2B SaaS, Freight Tech",
                "cta": "Schedule a 15-minute Freight Audit Demo [UNVERIFIED]",
                "website_placeholder": "https://automatch-logistics.demo.local [UNVERIFIED]",
                "social_bio": "Automating freight invoice auditing & PO matching for modern 3PLs and freight teams."
            }

        c.execute("""
            INSERT INTO brand_profiles (cycle_id, product_name, brand_name, tagline, short_description, long_description, target_audience, value_proposition, tone, keywords, cta, website_placeholder, social_bio)
            VALUES (:cycle_id, :product_name, :brand_name, :tagline, :short_description, :long_description, :target_audience, :value_proposition, :tone, :keywords, :cta, :website_placeholder, :social_bio)
        """, brand_data)
        conn.commit()
        conn.close()
        return brand_data

    def _sync_social_accounts(self, cycle_id: int) -> list:
        conn = get_db()
        c = conn.cursor()
        accounts = []
        for platform_name, connector in self.connectors.items():
            val = connector.validate_connection()
            status = val["status"]
            oauth_connected = 1 if val.get("oauth_connected") else 0
            acc_name = val.get("account_name", f"{platform_name.capitalize()} Account")
            acc_id = val.get("account_id", "unbound")
            acc_type = val.get("account_type", "user")

            c.execute("""
                SELECT id FROM social_accounts WHERE cycle_id = ? AND platform = ?
            """, (cycle_id, platform_name))
            row = c.fetchone()
            if row:
                c.execute("""
                    UPDATE social_accounts SET status=?, oauth_connected=?, account_name=?, account_id=?, account_type=?, updated_at=CURRENT_TIMESTAMP WHERE id=?
                """, (status, oauth_connected, acc_name, acc_id, acc_type, row['id']))
            else:
                c.execute("""
                    INSERT INTO social_accounts (cycle_id, platform, account_name, account_id, account_type, status, oauth_connected, credential_reference)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (cycle_id, platform_name, acc_name, acc_id, acc_type, status, oauth_connected, f"{platform_name.upper()}_ACCESS_TOKEN"))

            accounts.append({
                "platform": platform_name,
                "status": status,
                "account_name": acc_name,
                "account_type": acc_type,
                "oauth_connected": oauth_connected
            })
        conn.commit()
        conn.close()
        return accounts

    def _generate_draft_posts(self, cycle_id: int, product_name: str, brand_name: str) -> list:
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT COUNT(*) as cnt FROM posts WHERE cycle_id = ?", (cycle_id,))
        if c.fetchone()['cnt'] > 0:
            c.execute("SELECT * FROM posts WHERE cycle_id = ? ORDER BY post_id ASC", (cycle_id,))
            rows = c.fetchall()
            conn.close()
            return [dict(r) for r in rows]

        posts_data = ContentGenerator.generate_platform_posts(cycle_id, product_name, brand_name)

        generated_posts = []
        for p in posts_data:
            c.execute("""
                INSERT INTO posts (cycle_id, platform, content_type, caption, headline, cta, hashtags, media_prompt, status)
                VALUES (:cycle_id, :platform, :content_type, :caption, :headline, :cta, :hashtags, :media_prompt, :status)
            """, p)
            p["post_id"] = c.lastrowid
            generated_posts.append(p)

        conn.commit()
        conn.close()
        return generated_posts

    def _generate_operations_report(self, cycle_id: int, product_name: str, brand: dict, accounts: list, posts: list, campaign=None) -> str:
        report = f"""
SOCIAL MEDIA OPERATIONS SYSTEM REPORT
=====================================
Cycle ID: {cycle_id}
Product: {product_name}
Brand Name: {brand['brand_name']}
Tagline: {brand['tagline']}
"""
        if campaign:
            report += f"""
CAMPAIGN HIGHLIGHTS
-------------------
Objective: {campaign.objective}
Target Audience: {campaign.target_audience}
Positioning: {campaign.positioning}
Compliance Disclaimer: {campaign.compliance_disclaimer}
"""

        report += f"""
CONNECTED SOCIAL PLATFORMS
--------------------------
"""
        for a in accounts:
            report += f"- {a['platform'].capitalize()}: {a['status']} (Account Type: {a['account_type']}, OAuth Connected: {bool(a['oauth_connected'])})\n"

        report += f"""
CONTENT CALENDAR & POST GENERATION
----------------------------------
Total Draft Posts Generated: {len(posts)}
Supported Platforms: facebook, instagram, linkedin, x, reddit

Draft Posts Summary:
"""
        for p in posts:
            report += f"- [{p.get('post_id')}] {p['platform'].capitalize()} ({p['content_type']}): \"{p['headline']}\" -> Status: {p['status']}\n"

        report += f"""
PUBLISHING WORKFLOW
-------------------
Status: WAITING_MARKETING_APPROVAL
Safety Guardrail: NO POSTS ARE PUBLISHED AUTOMATICALLY.
Human Action Required: Run 'python ceo.py social status' to inspect account status, and approve campaign via 'python ceo.py approve <id>'.
"""
        return report
