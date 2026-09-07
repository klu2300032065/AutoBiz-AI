import os
import pytest
from unittest.mock import patch, MagicMock
from marketing.connectors.facebook import FacebookConnector
from marketing.connectors.instagram import InstagramConnector
from marketing.connectors.linkedin import LinkedInConnector
from marketing.connectors.x import XConnector
from marketing.connectors.reddit import RedditConnector
from marketing.campaign import CampaignBuilder, Campaign
from marketing.content_generator import ContentGenerator
from marketing.analytics import AnalyticsManager
from agents.marketing_sales_analytics_agent import MarketingSalesAnalyticsAgent
from memory.business_memory import BusinessMemory

def test_credential_loading_and_unconfigured_status():
    connectors = [
        FacebookConnector(),
        InstagramConnector(),
        LinkedInConnector(),
        XConnector(),
        RedditConnector()
    ]
    for c in connectors:
        res = c.validate_connection()
        assert res["status"] in ("NOT_CONNECTED", "REDDIT_API_ACCESS_REQUIRED")
        assert res["oauth_connected"] is False

def test_dry_run_publishing_no_network_call(monkeypatch):
    monkeypatch.setenv("SOCIAL_DRY_RUN", "true")
    connectors = {
        "facebook": FacebookConnector(),
        "instagram": InstagramConnector(),
        "linkedin": LinkedInConnector(),
        "x": XConnector(),
        "reddit": RedditConnector()
    }
    sample_post = {
        "headline": "Test Dry Run Headline",
        "caption": "Test Dry Run Caption",
        "cta": "Click link",
        "hashtags": "#Test"
    }

    for name, c in connectors.items():
        res = c.publish_post(sample_post)
        assert res["status"] == "DRY_RUN"
        assert res["platform_post_id"] is not None
        assert "dry_run" in res["url"].lower() or "simulation" in res["url"].lower()

def test_healthcare_compliance_campaign_generation():
    camp = CampaignBuilder.generate_campaign(
        cycle_id=5,
        product_name="Medical billing automation software for small medical practices"
    )
    assert isinstance(camp, Campaign)
    assert "prototype" in camp.positioning.lower()
    assert "hipaa" in camp.compliance_disclaimer.lower()
    assert len(camp.posting_schedule) >= 4

def test_platform_specific_content_generation():
    posts = ContentGenerator.generate_platform_posts(
        cycle_id=5,
        product_name="Medical billing automation software for small medical practices",
        brand_name="MedBill Flow"
    )
    platforms = set(p["platform"] for p in posts)
    assert platforms == {"instagram", "facebook", "linkedin", "x", "reddit"}
    assert len(posts) == 5

    # Check distinct platform tailoring
    ig_post = next(p for p in posts if p["platform"] == "instagram")
    x_post = next(p for p in posts if p["platform"] == "x")
    reddit_post = next(p for p in posts if p["platform"] == "reddit")

    assert "bio" in ig_post["cta"].lower() or "screenshot" in ig_post["cta"].lower()
    assert len(x_post["caption"]) <= 280
    assert "r/" in reddit_post["hashtags"]

def test_human_approval_gating():
    agent = MarketingSalesAnalyticsAgent()
    memory = BusinessMemory()
    c_id = memory.create_new_cycle().cycle_id

    res = agent.run(f"Create marketing for cycle {c_id}")
    assert res["status"] == "success"

    state = memory.get_business_state(cycle_id=c_id)
    assert state.stage == "WAITING_MARKETING_APPROVAL"
    assert state.marketing == "READY"

    # Pending approval must exist
    pending = memory.get_pending_approvals(cycle_id=c_id)
    assert any(a.action == "LAUNCH_MARKETING" for a in pending)

def test_analytics_metrics_labeling():
    connectors = {
        "facebook": FacebookConnector(),
        "instagram": InstagramConnector(),
        "linkedin": LinkedInConnector(),
        "x": XConnector(),
        "reddit": RedditConnector()
    }
    mgr = AnalyticsManager(connectors)

    # Unconnected post -> DEMO DATA
    res = mgr.get_post_analytics("facebook", "12345")
    assert res["source"] == "DEMO DATA"
    assert "metrics" in res

    # Mock connected connector -> REAL PLATFORM METRICS
    mock_conn = MagicMock()
    mock_conn.validate_connection.return_value = {"status": "CONNECTED", "oauth_connected": True}
    mock_conn.get_metrics.return_value = {"likes": 15, "impressions": 200}
    connectors["facebook"] = mock_conn

    res_real = mgr.get_post_analytics("facebook", "12345")
    assert res_real["source"] == "REAL PLATFORM METRICS"
    assert res_real["metrics"]["likes"] == 15

def test_secret_redaction():
    fb = FacebookConnector()
    fb.page_access_token = "secret_token_123456789"
    error_msg = f"Failed with token secret_token_123456789 on API call"
    redacted = fb._redact_secrets(error_msg)
    assert "secret_token_123456789" not in redacted
    assert "[REDACTED]" in redacted
