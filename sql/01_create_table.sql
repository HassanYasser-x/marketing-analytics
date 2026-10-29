-- SQL Server. Creates objects only when absent; does not drop existing data.
IF DB_ID(N'MarketingDB') IS NULL EXEC(N'CREATE DATABASE MarketingDB');
GO
USE MarketingDB;
GO
IF OBJECT_ID(N'dbo.marketing_snapshot', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.marketing_snapshot (
        [date] DATE NOT NULL,
        [year] SMALLINT NOT NULL,
        [quarter] NVARCHAR(100) NOT NULL,
        [month] NVARCHAR(100) NOT NULL,
        [month_num] TINYINT NOT NULL,
        [day_of_week] NVARCHAR(100) NOT NULL,
        [is_weekend] BIT NOT NULL,
        [channel] NVARCHAR(100) NOT NULL,
        [campaign] NVARCHAR(100) NOT NULL,
        [region] NVARCHAR(100) NOT NULL,
        [device] NVARCHAR(100) NOT NULL,
        [age_group] NVARCHAR(100) NOT NULL,
        [gender] NVARCHAR(100) NOT NULL,
        [impressions] INT NOT NULL,
        [clicks] INT NOT NULL,
        [ctr] DECIMAL(18,6) NOT NULL,
        [cpc] DECIMAL(18,4) NOT NULL,
        [spend] DECIMAL(18,4) NOT NULL,
        [conversions] INT NOT NULL,
        [conversion_rate] DECIMAL(18,6) NOT NULL,
        [revenue] DECIMAL(18,4) NOT NULL,
        [cost_per_conversion] DECIMAL(18,4) NOT NULL,
        [roas] DECIMAL(18,6) NOT NULL,
        [revenue_per_click] DECIMAL(18,4) NOT NULL,
        [bounce_rate] DECIMAL(18,6) NOT NULL,
        [avg_session_duration_sec] DECIMAL(18,6) NOT NULL,
        [pages_per_session] DECIMAL(18,6) NOT NULL,
        [engagement_score] DECIMAL(18,6) NOT NULL,
        [spend_tier] NVARCHAR(100) NOT NULL,
        [channel_type] NVARCHAR(100) NOT NULL,
        [roas_category_fixed] NVARCHAR(100) NOT NULL
    );
END;
GO
