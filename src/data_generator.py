import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

BUILTIN_BRANDS = [
    # Skincare & Beauty
    {"name": "Minimalist", "category": "Skincare & Science", "spend_mult": 1.4, "roas_target": 4.2},
    {"name": "Mamaearth", "category": "Personal Care", "spend_mult": 1.6, "roas_target": 3.4},
    {"name": "Nykaa", "category": "Beauty Retail", "spend_mult": 2.0, "roas_target": 3.8},
    {"name": "Sugar Cosmetics", "category": "Makeup & Beauty", "spend_mult": 1.2, "roas_target": 3.6},
    {"name": "Glossier", "category": "Beauty & Lifestyle", "spend_mult": 1.1, "roas_target": 4.0},
    {"name": "The Ordinary", "category": "Clinical Skincare", "spend_mult": 1.3, "roas_target": 4.5},
    {"name": "CeraVe", "category": "Dermatologist Skincare", "spend_mult": 1.8, "roas_target": 3.9},
    {"name": "Sephora", "category": "Beauty & Cosmetics", "spend_mult": 2.2, "roas_target": 3.7},
    {"name": "Fenty Beauty", "category": "Cosmetics", "spend_mult": 1.5, "roas_target": 3.8},
    {"name": "Rare Beauty", "category": "Cosmetics", "spend_mult": 1.4, "roas_target": 4.1},

    # Consumer Tech & Electronics
    {"name": "boAt Lifestyle", "category": "Audio & Wearables", "spend_mult": 1.9, "roas_target": 3.5},
    {"name": "Anker", "category": "Charging & Tech", "spend_mult": 1.3, "roas_target": 3.9},
    {"name": "Apple", "category": "Premium Electronics", "spend_mult": 3.0, "roas_target": 4.8},
    {"name": "Samsung", "category": "Consumer Electronics", "spend_mult": 2.8, "roas_target": 4.0},
    {"name": "Dyson", "category": "Premium Appliances", "spend_mult": 1.7, "roas_target": 3.6},

    # Fashion, Activewear & Footwear
    {"name": "Gymshark", "category": "Activewear & Fitness", "spend_mult": 1.8, "roas_target": 3.7},
    {"name": "Lululemon", "category": "Athletic Apparel", "spend_mult": 2.1, "roas_target": 4.2},
    {"name": "Zara", "category": "Fast Fashion", "spend_mult": 2.3, "roas_target": 3.3},
    {"name": "H&M", "category": "Fashion Apparel", "spend_mult": 2.0, "roas_target": 3.1},
    {"name": "Nike", "category": "Sportswear & Footwear", "spend_mult": 3.2, "roas_target": 4.5},
    {"name": "Adidas", "category": "Sportswear", "spend_mult": 2.7, "roas_target": 3.8},
    {"name": "Levi's", "category": "Denim & Apparel", "spend_mult": 1.5, "roas_target": 3.2},
    {"name": "Allbirds", "category": "Sustainable Shoes", "spend_mult": 1.0, "roas_target": 3.0},
    {"name": "Uniqlo", "category": "Casual Apparel", "spend_mult": 2.2, "roas_target": 3.6},

    # D2C & Lifestyle Innovations
    {"name": "Warby Parker", "category": "Eyewear", "spend_mult": 1.2, "roas_target": 3.4},
    {"name": "Casper", "category": "Sleep & Mattresses", "spend_mult": 1.4, "roas_target": 2.8},
    {"name": "Away Luggage", "category": "Travel & Gear", "spend_mult": 1.1, "roas_target": 3.5},
    {"name": "Dollar Shave Club", "category": "Grooming Subscriptions", "spend_mult": 1.0, "roas_target": 3.1},
    {"name": "Peloton", "category": "Connected Fitness", "spend_mult": 1.6, "roas_target": 2.6}
]

def generate_marketing_data(brands_list=None):
    print("Generating comprehensive multi-brand dataset for iconic brands...")
    np.random.seed(42)
    
    if brands_list is None:
        brands_list = BUILTIN_BRANDS
        
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    date_range = [start_date + timedelta(days=i) for i in range(366)]
    
    os.makedirs("data/raw", exist_ok=True)
    
    google_templates = [
        {"id_prefix": "G001", "suffix": "Search_Brand", "ctr_base": 0.08, "cpc_base": 0.80, "conv_base": 0.05, "revenue_multiplier": 4.8},
        {"id_prefix": "G002", "suffix": "Search_Competitor", "ctr_base": 0.02, "cpc_base": 2.40, "conv_base": 0.02, "revenue_multiplier": 1.8},
        {"id_prefix": "G003", "suffix": "PMax_Shopping", "ctr_base": 0.04, "cpc_base": 1.10, "conv_base": 0.035, "revenue_multiplier": 3.4},
        {"id_prefix": "G004", "suffix": "Display_Prospecting", "ctr_base": 0.003, "cpc_base": 0.40, "conv_base": 0.002, "revenue_multiplier": 0.45}
    ]
    
    meta_templates = [
        {"id_prefix": "M001", "suffix": "Prospecting_Lookalike", "ctr_base": 0.015, "cpc_base": 1.40, "conv_base": 0.025, "revenue_multiplier": 2.7},
        {"id_prefix": "M002", "suffix": "Retargeting_Catalog", "ctr_base": 0.035, "cpc_base": 0.85, "conv_base": 0.06, "revenue_multiplier": 4.6},
        {"id_prefix": "M003", "suffix": "Brand_Awareness", "ctr_base": 0.005, "cpc_base": 0.55, "conv_base": 0.001, "revenue_multiplier": 0.2}
    ]
    
    google_rows = []
    meta_rows = []
    web_rows = []
    
    channels = ["Organic Search", "Direct", "Paid Search", "Paid Social", "Referral", "Email"]
    
    for brand in brands_list:
        b_name = brand["name"]
        b_mult = brand.get("spend_mult", 1.0)
        
        for dt in date_range:
            month = dt.month
            day_of_week = dt.weekday()
            season_mult = 1.6 if month in [11, 12] else 1.0
            weekend_mult = 0.85 if day_of_week >= 5 else 1.0
            day_mult = season_mult * weekend_mult * b_mult * np.random.uniform(0.9, 1.1)
            
            # Google Ads
            for tmpl in google_templates:
                camp_id = f"{b_name[:3].upper()}_{tmpl['id_prefix']}"
                camp_name = f"{b_name} - {tmpl['suffix']}"
                spend = np.random.uniform(80, 250) * day_mult
                cpc = tmpl["cpc_base"] * np.random.uniform(0.85, 1.15)
                clicks = max(1, int(spend / cpc))
                ctr = tmpl["ctr_base"] * np.random.uniform(0.9, 1.1)
                impressions = int(clicks / ctr) if ctr > 0 else 0
                conv_rate = tmpl["conv_base"] * np.random.uniform(0.85, 1.15)
                conversions = max(0, int(clicks * conv_rate))
                avg_order_val = np.random.uniform(60, 100)
                if tmpl["revenue_multiplier"] < 1.0: avg_order_val *= 0.4
                revenue = conversions * avg_order_val * tmpl["revenue_multiplier"] * np.random.uniform(0.9, 1.1)
                
                google_rows.append({
                    "Date": dt.strftime("%Y-%m-%d"),
                    "Brand_Name": b_name,
                    "Campaign_ID": camp_id,
                    "Campaign_Name": camp_name,
                    "Platform": "Google Ads",
                    "Spend": round(spend, 2),
                    "Impressions": impressions,
                    "Clicks": clicks,
                    "Leads": int(conversions * 1.5),
                    "Purchases": conversions,
                    "Revenue": round(revenue, 2)
                })
                
            # Meta Ads
            for tmpl in meta_templates:
                camp_id = f"{b_name[:3].upper()}_{tmpl['id_prefix']}"
                camp_name = f"{b_name} - {tmpl['suffix']}"
                spend = np.random.uniform(90, 220) * day_mult
                cpc = tmpl["cpc_base"] * np.random.uniform(0.85, 1.15)
                clicks = max(1, int(spend / cpc))
                ctr = tmpl["ctr_base"] * np.random.uniform(0.9, 1.1)
                impressions = int(clicks / ctr) if ctr > 0 else 0
                conv_rate = tmpl["conv_base"] * np.random.uniform(0.85, 1.15)
                conversions = max(0, int(clicks * conv_rate))
                avg_order_val = np.random.uniform(65, 110)
                if tmpl["revenue_multiplier"] < 1.0: avg_order_val *= 0.35
                revenue = conversions * avg_order_val * tmpl["revenue_multiplier"] * np.random.uniform(0.9, 1.1)
                
                meta_rows.append({
                    "Date": dt.strftime("%Y-%m-%d"),
                    "Brand_Name": b_name,
                    "Campaign_ID": camp_id,
                    "Campaign_Name": camp_name,
                    "Platform": "Meta Ads",
                    "Spend": round(spend, 2),
                    "Impressions": impressions,
                    "Clicks": clicks,
                    "Leads": int(conversions * 1.6),
                    "Purchases": conversions,
                    "Revenue": round(revenue, 2)
                })
                
            # Web analytics
            for chan in channels:
                sessions = int(1200 * day_mult)
                bounce_rate = np.random.uniform(0.35, 0.50)
                pageviews = int(sessions * np.random.uniform(2.2, 3.2))
                conversions = int(sessions * 0.025 * np.random.uniform(0.9, 1.1))
                
                web_rows.append({
                    "Date": dt.strftime("%Y-%m-%d"),
                    "Brand_Name": b_name,
                    "Channel": chan,
                    "Sessions": sessions,
                    "Bounce_Rate": round(bounce_rate, 4),
                    "Pageviews": pageviews,
                    "Conversions": conversions
                })
                
    df_google = pd.DataFrame(google_rows)
    df_google.to_csv("data/raw/google_ads.csv", index=False)
    
    df_meta = pd.DataFrame(meta_rows)
    df_meta.to_csv("data/raw/meta_ads.csv", index=False)
    
    df_web = pd.DataFrame(web_rows)
    df_web.to_csv("data/raw/website_analytics.csv", index=False)
    
    print(f"Generated datasets for {len(brands_list)} brands!")

if __name__ == "__main__":
    generate_marketing_data()
