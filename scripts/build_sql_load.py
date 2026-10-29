"""Generate a path-free SQL Server insert script from the checked-in CSV."""
from pathlib import Path
import csv
ROOT=Path(__file__).resolve().parents[1]
TEXT={'date','quarter','month','day_of_week','channel','campaign','region','device','age_group','gender','spend_tier','channel_type','roas_category_fixed'}
def main():
    with (ROOT/'data/marketing_snapshot.csv').open(encoding='utf-8',newline='') as f:
        rd=csv.DictReader(f);cols=rd.fieldnames;rows=list(rd)
    def value(c,v):return "N'"+v.replace("'","''")+"'" if c in TEXT else v
    out=['-- Generated from data/marketing_snapshot.csv. No file-system paths required.','-- Run after 01_create_table.sql; refuses to load into a nonempty table.','USE MarketingDB;','GO','SET XACT_ABORT ON;','BEGIN TRY','    BEGIN TRANSACTION;',"    IF EXISTS (SELECT 1 FROM dbo.marketing_snapshot) THROW 50001, 'Snapshot table must be empty before loading. No rows inserted.', 1;"]
    for start in range(0,len(rows),500):
        out.append('    INSERT INTO dbo.marketing_snapshot ('+', '.join('['+c+']' for c in cols)+') VALUES')
        batch=rows[start:start+500]
        for i,row in enumerate(batch):
            out.append('    ('+', '.join(value(c,row[c]) for c in cols)+(');' if i==len(batch)-1 else '),'))
    out+=['    COMMIT TRANSACTION;','END TRY','BEGIN CATCH','    IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;','    THROW;','END CATCH;','GO','SELECT COUNT(*) AS rows_loaded FROM dbo.marketing_snapshot;','']
    (ROOT/'sql/02_load_snapshot.sql').write_text('\n'.join(out),encoding='utf-8')
    print(f'Generated {len(rows):,} inserts in batches of at most 500 rows.')
if __name__=='__main__':main()
