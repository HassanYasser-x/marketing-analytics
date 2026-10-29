USE MarketingDB;
GO
-- Rebuild cleaning rules from the provided project. Email/SEO is the source grouping.
-- The CSV contains the already-cleaned category; original raw labels were unavailable.
CREATE OR ALTER VIEW dbo.vw_marketing_clean AS
SELECT
    m.[date],
    m.[year],
    m.[quarter],
    m.[month],
    m.[month_num],
    m.[day_of_week],
    m.[is_weekend],
    m.[channel],
    m.[campaign],
    m.[region],
    m.[device],
    m.[age_group],
    m.[gender],
    m.[impressions],
    m.[clicks],
    m.[ctr],
    m.[cpc],
    m.[spend],
    m.[conversions],
    m.[conversion_rate],
    m.[revenue],
    m.[cost_per_conversion],
    m.[roas],
    m.[revenue_per_click],
    m.[bounce_rate],
    m.[avg_session_duration_sec],
    m.[pages_per_session],
    m.[engagement_score],
    m.[spend_tier],
    CASE WHEN m.channel IN (N'Email', N'SEO') THEN N'Organic' ELSE N'Paid' END AS channel_type,
    CASE WHEN m.spend = 0 THEN N'No Spend' WHEN m.revenue = 0 THEN N'Zero Return' ELSE m.roas_category_fixed END AS roas_category_fixed,
    m.clicks * 1.0 / NULLIF(m.impressions, 0) AS ctr_recalculated,
    m.conversions * 1.0 / NULLIF(m.clicks, 0) AS cvr_recalculated,
    m.revenue / NULLIF(m.spend, 0) AS roas_recalculated,
    CASE WHEN m.clicks > 0 AND ABS(m.conversions * 1.0 / m.clicks - m.conversion_rate) > 0.01 THEN 1 ELSE 0 END AS cvr_mismatch
FROM dbo.marketing_snapshot AS m;
GO
