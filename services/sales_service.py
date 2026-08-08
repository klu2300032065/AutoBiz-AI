from models.msa_db import get_db

class SalesService:
    def __init__(self):
        pass

    def calculate_metrics(self, product_id: int):
        conn = get_db()
        c = conn.cursor()
        
        # Total revenue
        c.execute("SELECT SUM(amount) as rev FROM transactions WHERE product_id = ? AND type = 'PURCHASE'", (product_id,))
        row = c.fetchone()
        total_revenue = row['rev'] if row and row['rev'] else 0.0
        
        # Refunds
        c.execute("SELECT SUM(amount) as ref FROM transactions WHERE product_id = ? AND type = 'REFUND'", (product_id,))
        row = c.fetchone()
        total_refunds = row['ref'] if row and row['ref'] else 0.0
        
        # Paid users
        c.execute("SELECT COUNT(DISTINCT customer_id) as paid_users FROM transactions WHERE product_id = ? AND type = 'PURCHASE'", (product_id,))
        row = c.fetchone()
        paid_users = row['paid_users'] if row else 0
        
        # Total trials (from analytics events)
        c.execute("SELECT COUNT(DISTINCT user_id) as trials FROM analytics_events WHERE product_id = ? AND event_type = 'TRIAL_STARTED'", (product_id,))
        row = c.fetchone()
        trials = row['trials'] if row else 0
        
        # Signups
        c.execute("SELECT COUNT(id) as signups FROM customers WHERE product_id = ?", (product_id,))
        row = c.fetchone()
        signups = row['signups'] if row else 0
        
        # Spend
        c.execute("SELECT SUM(spend) as total_spend FROM campaigns WHERE product_id = ?", (product_id,))
        row = c.fetchone()
        spend = row['total_spend'] if row and row['total_spend'] else 0.0

        conn.close()

        # Derived metrics
        conversion_rate = (paid_users / signups * 100) if signups > 0 else 0
        trial_conversion_rate = (paid_users / trials * 100) if trials > 0 else 0
        cac = (spend / paid_users) if paid_users > 0 else 0
        revenue_per_customer = (total_revenue / paid_users) if paid_users > 0 else 0

        if signups == 0 and trials == 0 and paid_users == 0:
            return "Insufficient data"
            
        return {
            "signups": signups,
            "trials": trials,
            "paid_users": paid_users,
            "total_revenue": total_revenue,
            "total_refunds": total_refunds,
            "conversion_rate": conversion_rate,
            "trial_conversion_rate": trial_conversion_rate,
            "cac": cac,
            "revenue_per_customer": revenue_per_customer
        }
