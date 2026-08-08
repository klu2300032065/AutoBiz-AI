import os
from tools.content_generator import (
    generate_marketing_strategy,
    generate_landing_page_copy,
    generate_social_posts,
    generate_email_drafts,
    generate_seo_metadata
)
from models.msa_db import get_db

class MarketingService:
    def __init__(self):
        pass
        
    def create_campaign(self, product_name: str, product_desc: str) -> dict:
        print("Generating marketing strategy...")
        strategy = generate_marketing_strategy(product_name, product_desc)
        
        print("Generating landing page copy...")
        landing_page = generate_landing_page_copy(product_name, product_desc)
        
        print("Generating SEO metadata...")
        seo = generate_seo_metadata(product_name, product_desc)
        
        print("Generating social posts...")
        social = generate_social_posts(product_name, product_desc)
        
        print("Generating email drafts...")
        emails = generate_email_drafts(product_name, product_desc)
        
        return {
            "strategy": strategy,
            "landing_page": landing_page,
            "seo": seo,
            "social": social,
            "emails": emails
        }

    def save_campaign_to_db(self, product_id: int, campaign_name: str, source: str, content: str):
        conn = get_db()
        c = conn.cursor()
        c.execute(
            "INSERT INTO campaigns (product_id, name, source, status, content) VALUES (?, ?, ?, ?, ?)",
            (product_id, campaign_name, source, "DRAFT", content)
        )
        conn.commit()
        campaign_id = c.lastrowid
        conn.close()
        return campaign_id
