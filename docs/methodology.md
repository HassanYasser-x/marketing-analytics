# Model and metric notes

- Revenue, spend, impressions, clicks and conversions sum the recorded amounts/counts.
- CTR = total clicks / total impressions. CVR = total conversions / total clicks. CPC = spend / clicks. CPA = spend / conversions. ROAS = revenue / spend. Undefined ratios return blank.
- Paid measures intersect the current selection with `channel_type = Paid` using KEEPFILTERS. Organic revenue share is organic revenue / revenue within the current selection. Its denominator does not silently clear a selected channel.
- Organic is the source project's grouping for Email and SEO. Email is often called an owned channel elsewhere; this package retains the supplied grouping.
- Zero-return spend is an amount on records with spend > 0 and revenue = 0. Zero-return spend share divides that amount by paid spend. This corrects the original model's amount/percentage naming ambiguity.
- Source CVR mismatches count records with clicks > 0 and an absolute difference greater than 0.01 between supplied conversion_rate and conversions / clicks. There are 442 such records in the unfiltered snapshot. The dashboard uses recalculated weighted CVR; raw values remain hidden and available for audit.
- The original model had no relationships. This project adds Calendar[Date] (one) to Marketing[date] (many), active and single direction, so date slicers filter fact measures.
- Charts use Year-Month and ascending chronological sorting. The observation window is 31 July 2025 to 31 July 2026, so both endpoint months are partial. The calendar covers both complete years for date filtering.
- Source ROAS categories and spend tiers are retained. Their original numeric thresholds were not supplied, so labels such as Break-even and Profitable are not reinterpreted as accounting profit. ROAS measures are always recalculated.
- Campaign scorecards group the source campaign label across the current channel selection. Select a channel when a label occurs in more than one channel.
- No currency symbol is shown because the source currency was not specified. Revenue less advertising spend would exclude other operating costs; no profit claim is made.
- The report contains an embedded, fixed data snapshot. Refresh reimports that snapshot; it does not contact a live SQL Server.

## Reference totals

| Metric | Entire snapshot |
|---|---:|
| Records | 3,000 |
| Revenue | 1,827,702.01 |
| Spend | 463,281.75 |
| Conversions | 24,869 |
| CTR | 2.69% |
| CVR | 3.26% |
| Paid revenue | 662,536.19 |
| Paid ROAS | 1.43x |
| Organic revenue share | 63.75% |
| Zero-return spend | 18,609.40 |
| Zero-return spend / paid spend | 4.02% |
| Source CVR mismatch records | 442 |

These totals describe the supplied snapshot. They are not targets or forecasts.
