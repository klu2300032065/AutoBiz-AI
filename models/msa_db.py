import sqlite3
import os

DB_PATH = os.path.join(os.getcwd(), "msa_data.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    
    # Products
    c.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            description TEXT,
            target_audience TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Campaigns
    c.execute("""
        CREATE TABLE IF NOT EXISTS campaigns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            name TEXT,
            source TEXT,
            status TEXT DEFAULT 'DRAFT',
            spend REAL DEFAULT 0,
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(product_id) REFERENCES products(id)
        )
    """)
    
    # Customers
    c.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            email TEXT,
            source TEXT,
            campaign_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(product_id) REFERENCES products(id),
            FOREIGN KEY(campaign_id) REFERENCES campaigns(id)
        )
    """)
    
    # Transactions
    c.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            product_id INTEGER,
            amount REAL,
            type TEXT, -- PURCHASE, REFUND
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(customer_id) REFERENCES customers(id),
            FOREIGN KEY(product_id) REFERENCES products(id)
        )
    """)
    
    # Analytics Events
    c.execute("""
        CREATE TABLE IF NOT EXISTS analytics_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            user_id INTEGER,
            event_type TEXT,
            source TEXT,
            campaign_id INTEGER,
            metadata TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(product_id) REFERENCES products(id),
            FOREIGN KEY(campaign_id) REFERENCES campaigns(id)
        )
    """)
    
    # Experiments (A/B testing)
    c.execute("""
        CREATE TABLE IF NOT EXISTS experiments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            name TEXT,
            variant_a TEXT,
            variant_b TEXT,
            winner TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(product_id) REFERENCES products(id)
        )
    """)
    
    # Feedback
    c.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            customer_id INTEGER,
            category TEXT,
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(product_id) REFERENCES products(id),
            FOREIGN KEY(customer_id) REFERENCES customers(id)
        )
    """)
    
    # Social Accounts
    c.execute("""
        CREATE TABLE IF NOT EXISTS social_accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cycle_id INTEGER DEFAULT 1,
            platform TEXT,
            account_id TEXT,
            account_name TEXT,
            account_type TEXT,
            status TEXT DEFAULT 'NOT_CONNECTED',
            oauth_connected INTEGER DEFAULT 0,
            credential_reference TEXT,
            token_expires_at TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    for col, col_type in [("account_type", "TEXT"), ("credential_reference", "TEXT"), ("token_expires_at", "TEXT")]:
        try:
            c.execute(f"ALTER TABLE social_accounts ADD COLUMN {col} {col_type}")
        except Exception:
            pass
    
    # Brand Profiles
    c.execute("""
        CREATE TABLE IF NOT EXISTS brand_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cycle_id INTEGER DEFAULT 1,
            product_name TEXT,
            brand_name TEXT,
            tagline TEXT,
            short_description TEXT,
            long_description TEXT,
            target_audience TEXT,
            value_proposition TEXT,
            tone TEXT,
            keywords TEXT,
            cta TEXT,
            website_placeholder TEXT,
            social_bio TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Posts (Social Media Content Calendar & Queue)
    c.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            post_id INTEGER PRIMARY KEY AUTOINCREMENT,
            cycle_id INTEGER DEFAULT 1,
            platform TEXT,
            content_type TEXT,
            caption TEXT,
            headline TEXT,
            cta TEXT,
            hashtags TEXT,
            media_prompt TEXT,
            status TEXT DEFAULT 'DRAFT',
            scheduled_at TEXT,
            platform_post_id TEXT,
            published_at TEXT,
            url TEXT,
            post_url TEXT,
            error_message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    for col, col_type in [("post_url", "TEXT"), ("error_message", "TEXT")]:
        try:
            c.execute(f"ALTER TABLE posts ADD COLUMN {col} {col_type}")
        except Exception:
            pass
    
    # Migration helper for cycle_id on existing tables
    for tbl in ["products", "campaigns", "customers", "transactions", "analytics_events"]:
        try:
            c.execute(f"ALTER TABLE {tbl} ADD COLUMN cycle_id INTEGER DEFAULT 1")
        except Exception:
            pass

    # Indexes
    c.execute("CREATE INDEX IF NOT EXISTS idx_analytics_events_type ON analytics_events(event_type)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_transactions_type ON transactions(type)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_customers_source ON customers(source)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_posts_status ON posts(status)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_posts_cycle ON posts(cycle_id)")
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
