import os
import sqlite3
import pandas as pd
from data_generator import generate_marketing_data

def run_etl():
    print("Starting Multi-Brand ETL pipeline...")
    
    # 1. Regenerate raw data for multi-brand architecture
    generate_marketing_data()
        
    # Read files
    df_google = pd.read_csv("data/raw/google_ads.csv")
    df_meta = pd.read_csv("data/raw/meta_ads.csv")
    df_web = pd.read_csv("data/raw/website_analytics.csv")
    
    # 2. Database connection & Schema creation
    os.makedirs("data", exist_ok=True)
    db_path = "data/marketing.db"
    if os.path.exists(db_path):
        conn = None
        os.remove(db_path)
        print("Removed legacy database for schema update.")
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Execute schema.sql
    with open("sql/schema.sql", "r") as f:
        schema_sql = f.read()
    cursor.executescript(schema_sql)
    conn.commit()
    print("Database tables and multi-brand schema initialized.")
    
    # Clear old data before loading
    cursor.execute("DELETE FROM raw_google_ads")
    cursor.execute("DELETE FROM raw_meta_ads")
    cursor.execute("DELETE FROM raw_website_analytics")
    cursor.execute("DELETE FROM dim_campaigns")
    cursor.execute("DELETE FROM fact_daily_ad_performance")
    cursor.execute("DELETE FROM fact_daily_website_performance")
    conn.commit()
    
    # 3. Load Raw Data
    df_google.to_sql("raw_google_ads", conn, if_exists="append", index=False)
    df_meta.to_sql("raw_meta_ads", conn, if_exists="append", index=False)
    df_web.to_sql("raw_website_analytics", conn, if_exists="append", index=False)
    print("Loaded raw stage tables in SQLite.")
    
    # 4. Transform & Build Dim Campaigns
    google_camps = df_google[["Campaign_ID", "Brand_Name", "Campaign_Name", "Platform"]].drop_duplicates()
    meta_camps = df_meta[["Campaign_ID", "Brand_Name", "Campaign_Name", "Platform"]].drop_duplicates()
    
    dim_campaigns = pd.concat([google_camps, meta_camps], ignore_index=True)
    
    def classify_campaign(name):
        name_lower = name.lower()
        if "brand" in name_lower:
            return "Brand"
        elif "search" in name_lower:
            return "Search"
        elif "pmax" in name_lower or "shopping" in name_lower:
            return "Performance Max"
        elif "catalog" in name_lower or "retargeting" in name_lower:
            return "Retargeting"
        elif "prospecting" in name_lower or "lookalike" in name_lower:
            return "Prospecting"
        return "Other"
        
    dim_campaigns["Campaign_Type"] = dim_campaigns["Campaign_Name"].apply(classify_campaign)
    dim_campaigns.to_sql("dim_campaigns", conn, if_exists="append", index=False)
    print(f"Dim campaigns built with {len(dim_campaigns)} records.")
    
    # 5. Transform & Build Fact Performance
    fact_cols = ["Date", "Brand_Name", "Campaign_ID", "Spend", "Impressions", "Clicks", "Leads", "Purchases", "Revenue"]
    fact_google = df_google[fact_cols]
    fact_meta = df_meta[fact_cols]
    
    fact_performance = pd.concat([fact_google, fact_meta], ignore_index=True)
    fact_performance.to_sql("fact_daily_ad_performance", conn, if_exists="append", index=False)
    print(f"Fact Daily Ad Performance built with {len(fact_performance)} records.")
    
    # 6. Load Website analytics
    df_web.to_sql("fact_daily_website_performance", conn, if_exists="append", index=False)
    print("Fact Daily Website Performance loaded.")
    
    conn.commit()
    
    # Run a test verify query
    cursor.execute("SELECT COUNT(*), SUM(Spend), SUM(Revenue) FROM fact_daily_ad_performance")
    cnt, spend, rev = cursor.fetchone()
    print(f"Verification Check: Loaded {cnt} daily campaign logs. Total spend: ${spend:,.2f}, Total revenue: ${rev:,.2f}")
    
    conn.close()
    print("Multi-Brand ETL execution successfully finished!")

if __name__ == "__main__":
    run_etl()
