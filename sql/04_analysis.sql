USE MarketingDB;
GO
-- Full snapshot: 3,000 records; revenue 1,827,702.01; spend 463,281.75.
SELECT COUNT(*) AS records, MIN([date]) AS first_date, MAX([date]) AS last_date,
       SUM(spend) AS spend, SUM(revenue) AS revenue,
       SUM(clicks) * 1.0 / NULLIF(SUM(impressions), 0) AS ctr,
       SUM(conversions) * 1.0 / NULLIF(SUM(clicks), 0) AS cvr
FROM dbo.vw_marketing_clean;

-- Channel scorecard. Rate columns are ratios of sums, never sums of source rates.
SELECT channel, channel_type, SUM(spend) AS spend, SUM(revenue) AS revenue,
       SUM(conversions) AS conversions,
       SUM(revenue) / NULLIF(SUM(spend), 0) AS roas,
       SUM(clicks) * 1.0 / NULLIF(SUM(impressions), 0) AS ctr,
       SUM(conversions) * 1.0 / NULLIF(SUM(clicks), 0) AS cvr,
       SUM(spend) / NULLIF(SUM(conversions), 0) AS cpa
FROM dbo.vw_marketing_clean
GROUP BY channel, channel_type ORDER BY revenue DESC;

-- Paid campaign scorecard.
SELECT campaign, SUM(spend) AS spend, SUM(revenue) AS revenue,
       SUM(conversions) AS conversions,
       SUM(revenue) / NULLIF(SUM(spend), 0) AS paid_roas,
       SUM(conversions) * 1.0 / NULLIF(SUM(clicks), 0) AS paid_cvr,
       SUM(spend) / NULLIF(SUM(conversions), 0) AS paid_cpa
FROM dbo.vw_marketing_clean WHERE channel_type = N'Paid'
GROUP BY campaign ORDER BY revenue DESC;

-- Monthly trend; yyyy-MM avoids merging matching month names across years.
SELECT CONVERT(char(7), [date], 126) AS year_month,
       SUM(spend) AS spend, SUM(revenue) AS revenue
FROM dbo.vw_marketing_clean
GROUP BY CONVERT(char(7), [date], 126) ORDER BY year_month;

-- Paid region return and scale.
SELECT region, SUM(spend) AS spend, SUM(revenue) AS revenue,
       SUM(revenue) / NULLIF(SUM(spend), 0) AS paid_roas
FROM dbo.vw_marketing_clean WHERE channel_type = N'Paid'
GROUP BY region ORDER BY paid_roas DESC;

-- Audience efficiency.
SELECT device, SUM(clicks) AS clicks, SUM(conversions) AS conversions,
       SUM(conversions) * 1.0 / NULLIF(SUM(clicks), 0) AS cvr
FROM dbo.vw_marketing_clean GROUP BY device ORDER BY cvr DESC;
SELECT age_group, SUM(spend) AS spend, SUM(revenue) AS revenue,
       SUM(revenue) / NULLIF(SUM(spend), 0) AS paid_roas
FROM dbo.vw_marketing_clean WHERE channel_type = N'Paid'
GROUP BY age_group ORDER BY paid_roas DESC;

-- Data-quality checks: expected CVR mismatch count 442; zero-return spend 18,609.40.
SELECT SUM(cvr_mismatch) AS source_cvr_mismatches FROM dbo.vw_marketing_clean;
SELECT SUM(CASE WHEN spend > 0 AND revenue = 0 THEN spend ELSE 0 END) AS zero_return_spend
FROM dbo.vw_marketing_clean;
SELECT roas_category_fixed, COUNT(*) AS records, SUM(spend) AS spend, SUM(revenue) AS revenue
FROM dbo.vw_marketing_clean GROUP BY roas_category_fixed ORDER BY records DESC;
