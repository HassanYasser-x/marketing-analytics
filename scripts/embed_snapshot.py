"""Refresh the portable model snapshot from data/marketing_snapshot.csv (stdlib only)."""
from pathlib import Path
import base64,csv,datetime,json,zlib

ROOT=Path(__file__).resolve().parents[1]
MODEL=ROOT/'powerbi/Marketing.SemanticModel/model.bim'
INT={'year','month_num','is_weekend','impressions','clicks','conversions'}
TEXT={'quarter','month','day_of_week','channel','campaign','region','device','age_group','gender','spend_tier','channel_type','roas_category_fixed'}

def read_snapshot():
    with (ROOT/'data/marketing_snapshot.csv').open(encoding='utf-8',newline='') as f:
        reader=csv.DictReader(f);columns=reader.fieldnames;rows=[]
        for row in reader:
            rows.append([row[c] if c in TEXT or c=='date' else int(row[c]) if c in INT else float(row[c]) for c in columns])
    return columns,rows

def main():
    columns,rows=read_snapshot()
    model=json.loads(MODEL.read_text(encoding='utf-8'))
    tables={t['name']:t for t in model['model']['tables']}
    assert columns==[c['sourceColumn'] for c in tables['Marketing']['columns']], 'CSV columns must match the model.'
    raw=json.dumps(rows,separators=(',',':'),ensure_ascii=False).encode()
    payload=base64.b64encode(zlib.compress(raw,9)[2:-4]).decode()
    collist='{'+', '.join(json.dumps(c) for c in columns)+'}'
    types=['{"'+c+'", '+('type date' if c=='date' else 'Int64.Type' if c in INT else 'type text' if c in TEXT else 'type number')+'}' for c in columns]
    tables['Marketing']['partitions'][0]['source']['expression']=['let',f'    Rows = Json.Document(Binary.Decompress(Binary.FromText("{payload}", BinaryEncoding.Base64), Compression.Deflate)),',f'    Source = Table.FromRows(Rows, {collist}),','    Typed = Table.TransformColumnTypes(Source, {'+', '.join(types)+'}, "en-US")','in','    Typed']
    years=[datetime.date.fromisoformat(r[0]).year for r in rows]
    expr=tables['Calendar']['partitions'][0]['source']['expression']
    expr[1]=f'    StartDate = #date({min(years)}, 1, 1),'
    expr[2]=f'    EndDate = #date({max(years)}, 12, 31),'
    MODEL.write_text(json.dumps(model,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(f'Embedded {len(rows):,} records; Calendar covers {min(years)}–{max(years)}.')

if __name__=='__main__': main()
