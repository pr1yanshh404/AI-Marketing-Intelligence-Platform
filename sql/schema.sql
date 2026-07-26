-- Schema definition for AI Marketing Intelligence Database (Multi-Brand Enabled)

-- Raw tables
CREATE TABLE IF NOT EXISTS raw_google_ads (
    Date TEXT,
    Brand_Name TEXT,
    Campaign_ID TEXT,
    Campaign_Name TEXT,
    Platform TEXT,
    Spend REAL,
    Impressions INTEGER,
    Clicks INTEGER,
    Leads INTEGER,
    Purchases INTEGER,
    Revenue REAL
);

CREATE TABLE IF NOT EXISTS raw_meta_ads (
    Date TEXT,
    Brand_Name TEXT,
    Campaign_ID TEXT,
    Campaign_Name TEXT,
    Platform TEXT,
    Spend REAL,
    Impressions INTEGER,
    Clicks INTEGER,
    Leads INTEGER,
    Purchases INTEGER,
    Revenue REAL
);

CREATE TABLE IF NOT EXISTS raw_website_analytics (
    Date TEXT,
    Brand_Name TEXT,
    Channel TEXT,
    Sessions INTEGER,
    Bounce_Rate REAL,
    Pageviews INTEGER,
    Conversions INTEGER
);

-- Dimension table: Campaigns
CREATE TABLE IF NOT EXISTS dim_campaigns (
    Campaign_ID TEXT PRIMARY KEY,
    Brand_Name TEXT,
    Campaign_Name TEXT,
    Platform TEXT,
    Campaign_Type TEXT
);

-- Fact table: Combined Daily Campaign Performance
CREATE TABLE IF NOT EXISTS fact_daily_ad_performance (
    Date TEXT,
    Brand_Name TEXT,
    Campaign_ID TEXT,
    Spend REAL,
    Impressions INTEGER,
    Clicks INTEGER,
    Leads INTEGER,
    Purchases INTEGER,
    Revenue REAL,
    FOREIGN KEY (Campaign_ID) REFERENCES dim_campaigns(Campaign_ID)
);

-- Fact table: Daily Website Channel Performance
CREATE TABLE IF NOT EXISTS fact_daily_website_performance (
    Date TEXT,
    Brand_Name TEXT,
    Channel TEXT,
    Sessions INTEGER,
    Bounce_Rate REAL,
    Pageviews INTEGER,
    Conversions INTEGER
);
