# Data dictionary

The checked-in CSV has 3,000 observations and 31 fields. The exact observation grain was not documented; one row is treated as one source record. No exact duplicate rows were found.

| Field | SQL type | Meaning |
|---|---|---|
| `date` | `DATE` | Observation date; report filters through Calendar. |
| `year` | `SMALLINT` | Source year, hidden in report fields. |
| `quarter` | `NVARCHAR(100)` | Source quarter label. |
| `month` | `NVARCHAR(100)` | Source abbreviated month; Calendar supplies report months. |
| `month_num` | `TINYINT` | Source month number. |
| `day_of_week` | `NVARCHAR(100)` | Source weekday label. |
| `is_weekend` | `BIT` | Source weekend flag: 0 or 1; retained without redefining local weekends. |
| `channel` | `NVARCHAR(100)` | Marketing channel. |
| `campaign` | `NVARCHAR(100)` | Source campaign label; same labels may occur across channels. |
| `region` | `NVARCHAR(100)` | Broad geographic region. |
| `device` | `NVARCHAR(100)` | Device group. |
| `age_group` | `NVARCHAR(100)` | Age band. |
| `gender` | `NVARCHAR(100)` | Source gender group. |
| `impressions` | `INT` | Reported impressions. |
| `clicks` | `INT` | Reported clicks. |
| `ctr` | `DECIMAL(18,6)` | Supplied row CTR; audit only. |
| `cpc` | `DECIMAL(18,4)` | Supplied row CPC; audit only. |
| `spend` | `DECIMAL(18,4)` | Advertising spend in unspecified source currency. |
| `conversions` | `INT` | Reported conversions. |
| `conversion_rate` | `DECIMAL(18,6)` | Supplied row CVR; audit only. |
| `revenue` | `DECIMAL(18,4)` | Reported attributed revenue in unspecified source currency. |
| `cost_per_conversion` | `DECIMAL(18,4)` | Supplied row CPA; audit only. |
| `roas` | `DECIMAL(18,6)` | Supplied row ROAS; audit only. |
| `revenue_per_click` | `DECIMAL(18,4)` | Supplied row revenue per click; audit only. |
| `bounce_rate` | `DECIMAL(18,6)` | Supplied bounce rate; not aggregated in the report. |
| `avg_session_duration_sec` | `DECIMAL(18,6)` | Supplied session-duration statistic; not aggregated in the report. |
| `pages_per_session` | `DECIMAL(18,6)` | Supplied session-depth statistic; not aggregated in the report. |
| `engagement_score` | `DECIMAL(18,6)` | Supplied score; calculation was not supplied. |
| `spend_tier` | `NVARCHAR(100)` | Source spend segment; original thresholds were not supplied. |
| `channel_type` | `NVARCHAR(100)` | Source heuristic: Email and SEO = Organic, all others = Paid. |
| `roas_category_fixed` | `NVARCHAR(100)` | Cleaned source category; nonzero-spend category thresholds were not supplied. |

Calendar contains a unique Date key, Year, Month Number, Month, Year-Month and Year-Month Sort. The active one-to-many relationship filters Marketing from Calendar. Month labels sort by Month Number; Year-Month sorts by Year-Month Sort.
