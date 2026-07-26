-- KPI Queries for Marketing Intelligence Reporting

-- 1. Executive Summary KPIs (Overall)
-- Calculate total spend, revenue, ROAS, CAC, CTR, CPC, Conversion Rate
-- ROAS = Revenue / Spend
-- CAC = Spend / Purchases
-- CTR = Clicks / Impressions
-- CPC = Spend / Clicks
-- Conversion Rate (from web analytics conversions/sessions)
SELECT 
    SUM(Spend) AS Total_Spend,
    SUM(Revenue) AS Total_Revenue,
    SUM(Revenue) / SUM(Spend) AS ROAS,
    SUM(Spend) / SUM(Purchases) AS CAC,
    CAST(SUM(Clicks) AS REAL) / SUM(Impressions) AS CTR,
    SUM(Spend) / SUM(Clicks) AS CPC,
    SUM(Leads) AS Total_Leads,
    SUM(Purchases) AS Total_Purchases
FROM fact_daily_ad_performance;

-- 2. Performance by Marketing Platform
SELECT 
    c.Platform,
    SUM(p.Spend) AS Total_Spend,
    SUM(p.Revenue) AS Total_Revenue,
    SUM(p.Revenue) / SUM(p.Spend) AS ROAS,
    SUM(p.Spend) / SUM(p.Purchases) AS CAC,
    CAST(SUM(p.Clicks) AS REAL) / SUM(p.Impressions) AS CTR,
    SUM(p.Spend) / SUM(p.Clicks) AS CPC,
    SUM(p.Purchases) AS Purchases
FROM fact_daily_ad_performance p
JOIN dim_campaigns c ON p.Campaign_ID = c.Campaign_ID
GROUP BY c.Platform;

-- 3. Campaign Performance Ranking (High to Low ROAS)
SELECT 
    c.Campaign_Name,
    c.Platform,
    SUM(p.Spend) AS Spend,
    SUM(p.Revenue) AS Revenue,
    SUM(p.Revenue) / SUM(p.Spend) AS ROAS,
    SUM(p.Spend) / SUM(p.Purchases) AS CAC,
    CAST(SUM(p.Clicks) AS REAL) / SUM(p.Impressions) AS CTR,
    SUM(p.Spend) / SUM(p.Clicks) AS CPC
FROM fact_daily_ad_performance p
JOIN dim_campaigns c ON p.Campaign_ID = c.Campaign_ID
GROUP BY c.Campaign_ID, c.Campaign_Name, c.Platform
ORDER BY ROAS DESC;

-- 4. Monthly Trend Performance
SELECT 
    strftime('%Y-%m', Date) AS Month,
    SUM(Spend) AS Spend,
    SUM(Revenue) AS Revenue,
    SUM(Revenue) / SUM(Spend) AS ROAS,
    SUM(Purchases) AS Purchases,
    SUM(Spend) / SUM(Purchases) AS CAC
FROM fact_daily_ad_performance
GROUP BY Month
ORDER BY Month;
