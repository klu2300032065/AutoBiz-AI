from typing import Dict, List

class AnalyticsManager:
    """
    Retrieves and aggregates social media analytics metrics.
    Strictly distinguishes REAL PLATFORM METRICS from DEMO DATA.
    """
    def __init__(self, connectors: Dict):
        self.connectors = connectors

    def get_post_analytics(self, platform: str, platform_post_id: str) -> Dict:
        connector = self.connectors.get(platform.lower())
        if not connector:
            return {
                "source": "DEMO DATA",
                "status": "UNSUPPORTED_PLATFORM",
                "metrics": {}
            }

        conn_status = connector.validate_connection()
        if conn_status.get("status") == "CONNECTED" and platform_post_id:
            metrics = connector.get_metrics(platform_post_id)
            return {
                "source": "REAL PLATFORM METRICS",
                "platform": platform.capitalize(),
                "post_id": platform_post_id,
                "metrics": metrics
            }
        else:
            return {
                "source": "DEMO DATA",
                "platform": platform.capitalize(),
                "post_id": platform_post_id or "demo_id",
                "reason": conn_status.get("reason", "Account not connected"),
                "metrics": {
                    "impressions": 0,
                    "likes": 0,
                    "comments": 0,
                    "shares": 0,
                    "clicks": 0,
                    "engagement_rate": "0.0%"
                }
            }

    def generate_analytics_summary(self, posts: List[Dict]) -> Dict:
        summary = {
            "real_metrics_count": 0,
            "demo_metrics_count": 0,
            "platform_breakdown": {}
        }
        for p in posts:
            plat = p.get("platform", "unknown")
            post_id = p.get("platform_post_id") or p.get("post_id")
            res = self.get_post_analytics(plat, str(post_id))
            if res["source"] == "REAL PLATFORM METRICS":
                summary["real_metrics_count"] += 1
            else:
                summary["demo_metrics_count"] += 1

            if plat not in summary["platform_breakdown"]:
                summary["platform_breakdown"][plat] = []
            summary["platform_breakdown"][plat].append(res)

        return summary
