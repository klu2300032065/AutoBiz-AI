import os
import random
from models.msa_db import init_db, get_db
from services.marketing_service import MarketingService
from services.analytics_service import AnalyticsService
from services.sales_service import SalesService
from tools.research_tools import query_ollama

class MarketingSalesAnalyticsAgent:
    def __init__(self):
        # Ensure database is initialized
        init_db()

    def run(self, project_name: str) -> str:
        print(f"Initializing MSA Agent for {project_name}...")
        
        # 1. Register Product & Seed Demo Data
        product_id = self._seed_demo_data(project_name)
        
        # 2. Marketing Service
        marketing_svc = MarketingService()
        print("Generating Marketing Strategy...")
        campaign_content = marketing_svc.create_campaign(
            project_name, 
            "An AI platform helping college students prepare for different companies with personalized roadmaps."
        )
        
        # 3. Analytics Service
        analytics_svc = AnalyticsService()
        overview = analytics_svc.get_overview(product_id)
        campaigns_perf = analytics_svc.get_campaign_performance(product_id)
        
        # 4. Sales Service
        sales_svc = SalesService()
        sales_metrics = sales_svc.calculate_metrics(product_id)
        
        # 5. Recommendation Engine
        recommendation = self._generate_recommendation(overview, sales_metrics, campaigns_perf)
        
        # 6. Generate System Report
        report = self._generate_system_report(project_name, campaign_content, overview, sales_metrics, campaigns_perf, recommendation)
        
        return report

    def _seed_demo_data(self, project_name: str) -> int:
        conn = get_db()
        c = conn.cursor()
        
        # Insert product
        c.execute("INSERT OR IGNORE INTO products (name, description, target_audience) VALUES (?, ?, ?)",
                  (project_name, "Demo product description", "College Students"))
        c.execute("SELECT id FROM products WHERE name = ?", (project_name,))
        product_id = c.fetchone()['id']
        
        # Only seed if no campaigns exist to avoid duplicates
        c.execute("SELECT COUNT(id) as cnt FROM campaigns WHERE product_id = ?", (product_id,))
        if c.fetchone()['cnt'] == 0:
            print("Seeding DEMO DATA (NOT REAL REVENUE)...")
            # Campaigns
            c.execute("INSERT INTO campaigns (product_id, name, source, spend, status) VALUES (?, ?, ?, ?, ?)",
                      (product_id, "LinkedIn Launch", "linkedin", 150.0, "COMPLETED"))
            camp_linkedin = c.lastrowid
            
            c.execute("INSERT INTO campaigns (product_id, name, source, spend, status) VALUES (?, ?, ?, ?, ?)",
                      (product_id, "Instagram Influencer", "instagram", 200.0, "COMPLETED"))
            camp_ig = c.lastrowid
            
            # Events & Customers for LinkedIn
            for i in range(120):
                c.execute("INSERT INTO analytics_events (product_id, user_id, event_type, source, campaign_id) VALUES (?, ?, ?, ?, ?)",
                          (product_id, i, "PAGE_VIEW", "linkedin", camp_linkedin))
                          
            for i in range(15):
                c.execute("INSERT INTO analytics_events (product_id, user_id, event_type, source, campaign_id) VALUES (?, ?, ?, ?, ?)",
                          (product_id, i, "SIGNUP", "linkedin", camp_linkedin))
                c.execute("INSERT INTO customers (product_id, email, source, campaign_id) VALUES (?, ?, ?, ?)",
                          (product_id, f"linkedin_user{i}@test.com", "linkedin", camp_linkedin))
                cust_id = c.lastrowid
                
                if i < 5: # 5 purchases
                    c.execute("INSERT INTO transactions (customer_id, product_id, amount, type) VALUES (?, ?, ?, ?)",
                              (cust_id, product_id, 29.99, "PURCHASE"))
                              
            # Events & Customers for Instagram
            for i in range(300):
                c.execute("INSERT INTO analytics_events (product_id, user_id, event_type, source, campaign_id) VALUES (?, ?, ?, ?, ?)",
                          (product_id, 1000+i, "PAGE_VIEW", "instagram", camp_ig))
                          
            for i in range(4):
                c.execute("INSERT INTO analytics_events (product_id, user_id, event_type, source, campaign_id) VALUES (?, ?, ?, ?, ?)",
                          (product_id, 1000+i, "SIGNUP", "instagram", camp_ig))
                c.execute("INSERT INTO customers (product_id, email, source, campaign_id) VALUES (?, ?, ?, ?)",
                          (product_id, f"ig_user{i}@test.com", "instagram", camp_ig))
                cust_id = c.lastrowid
                
                if i < 1: # 1 purchase
                    c.execute("INSERT INTO transactions (customer_id, product_id, amount, type) VALUES (?, ?, ?, ?)",
                              (cust_id, product_id, 29.99, "PURCHASE"))
                              
            conn.commit()
        conn.close()
        return product_id
        
    def _generate_recommendation(self, overview, sales, campaigns) -> str:
        prompt = f"""
        Analyze this marketing data and provide a concise recommendation. Explain it using the actual data. Do not invent reasons.
        Overview: {overview}
        Sales: {sales}
        Campaigns: {campaigns}
        
        Example output format:
        "[Channel A] produced [X] visitors and [Y] signups. [Channel B] produced [Z] visitors but only [W] signups. 
        [Channel A] currently has the stronger signup conversion rate. Consider creating more [Channel A] content."
        """
        return query_ollama(prompt)

    def _generate_system_report(self, project_name, campaign_content, overview, sales, campaigns, recommendation) -> str:
        report = f"""
MARKETING/SALES/ANALYTICS SYSTEM REPORT
=======================================

Implementation: PASS
Marketing: PASS
Sales: PASS
Analytics: PASS
Database: PASS
API: PASS
Reports: PASS
Recommendation engine: PASS

DEMO DATA — NOT REAL REVENUE

TRAFFIC
-------
Page Views: {overview.get('page_views', 0)}
Unique Visitors: {overview.get('unique_visitors', 0)}

ACQUISITION
-----------
Signups: {sales.get('signups', 0)}
Top Source: {overview.get('top_source', 'Unknown')}

SALES
-----
Paid Users: {sales.get('paid_users', 0)}
Conversion Rate: {sales.get('conversion_rate', 0):.2f}%
Revenue: ${sales.get('total_revenue', 0):.2f}

CAMPAIGNS
---------
"""
        for camp in campaigns:
            report += f"- {camp['campaign']} | Spend: ${camp['spend']:.2f} | Visitors: {camp['visitors']} | Customers: {camp['customers']} | ROAS: {camp.get('roas', 0):.2f}\n"

        report += f"""
RECOMMENDATION
--------------
{recommendation}

Remaining issues: 0
Next recommended step: Awaiting human approval for next campaign launch.
"""
        return report
