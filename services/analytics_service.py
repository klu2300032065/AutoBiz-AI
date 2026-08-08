from models.msa_db import get_db

class AnalyticsService:
    def __init__(self):
        pass

    def get_overview(self, product_id: int):
        conn = get_db()
        c = conn.cursor()
        
        c.execute("SELECT COUNT(id) as page_views FROM analytics_events WHERE product_id = ? AND event_type = 'PAGE_VIEW'", (product_id,))
        row = c.fetchone()
        page_views = row['page_views'] if row else 0
        
        c.execute("SELECT COUNT(DISTINCT user_id) as unique_visitors FROM analytics_events WHERE product_id = ? AND event_type = 'PAGE_VIEW'", (product_id,))
        row = c.fetchone()
        unique_visitors = row['unique_visitors'] if row else 0
        
        c.execute("SELECT source, COUNT(id) as count FROM analytics_events WHERE product_id = ? AND event_type = 'SIGNUP' GROUP BY source ORDER BY count DESC LIMIT 1", (product_id,))
        row = c.fetchone()
        top_source = row['source'] if row else "Unknown"
        
        conn.close()
        return {
            "page_views": page_views,
            "unique_visitors": unique_visitors,
            "top_source": top_source
        }

    def get_campaign_performance(self, product_id: int):
        conn = get_db()
        c = conn.cursor()
        
        c.execute("SELECT id, name, spend FROM campaigns WHERE product_id = ?", (product_id,))
        campaigns = c.fetchall()
        
        performance = []
        for camp in campaigns:
            camp_id = camp['id']
            # visitors
            c.execute("SELECT COUNT(DISTINCT user_id) as visitors FROM analytics_events WHERE campaign_id = ? AND event_type = 'PAGE_VIEW'", (camp_id,))
            visitors = c.fetchone()['visitors']
            
            # signups
            c.execute("SELECT COUNT(id) as signups FROM customers WHERE campaign_id = ?", (camp_id,))
            signups = c.fetchone()['signups']
            
            # customers
            c.execute("SELECT COUNT(DISTINCT t.customer_id) as cust FROM transactions t JOIN customers c ON t.customer_id = c.id WHERE c.campaign_id = ? AND t.type = 'PURCHASE'", (camp_id,))
            customers = c.fetchone()['cust']
            
            # revenue
            c.execute("SELECT SUM(t.amount) as rev FROM transactions t JOIN customers c ON t.customer_id = c.id WHERE c.campaign_id = ? AND t.type = 'PURCHASE'", (camp_id,))
            row = c.fetchone()
            revenue = row['rev'] if row and row['rev'] else 0.0
            
            conv_rate = (customers / visitors * 100) if visitors > 0 else 0
            
            perf = {
                "campaign": camp['name'],
                "spend": camp['spend'],
                "visitors": visitors,
                "signups": signups,
                "customers": customers,
                "revenue": revenue,
                "conversion_rate": conv_rate
            }
            if camp['spend'] > 0:
                perf['cac'] = camp['spend'] / customers if customers > 0 else 0
                perf['roas'] = revenue / camp['spend'] if camp['spend'] > 0 else 0
                
            performance.append(perf)
            
        conn.close()
        return performance
