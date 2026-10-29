"""Check portable data, model references, relationships and report bounds. Stdlib only."""
from pathlib import Path
import base64,collections,csv,datetime,decimal,json,re,zlib

ROOT=Path(__file__).resolve().parents[1]
D=decimal.Decimal

def main():
    model=json.loads((ROOT/'powerbi/Marketing.SemanticModel/model.bim').read_text(encoding='utf-8'))
    tables={t['name']:t for t in model['model']['tables']}
    fields={n:{'Measure':{m['name'] for m in t.get('measures',[])},'Column':{c['name'] for c in t['columns']}} for n,t in tables.items()}
    with (ROOT/'data/marketing_snapshot.csv').open(encoding='utf-8',newline='') as f:
        rd=csv.DictReader(f);columns=rd.fieldnames;rows=list(rd)
    source='\n'.join(tables['Marketing']['partitions'][0]['source']['expression'])
    payload=re.search(r'Binary.FromText\("([A-Za-z0-9+/=]+)"',source).group(1)
    embedded=json.loads(zlib.decompress(base64.b64decode(payload),-15))
    assert len(rows)==len(embedded), 'CSV and model row counts differ.'
    numeric={'year','month_num','is_weekend','impressions','clicks','conversions','ctr','cpc','spend','conversion_rate','revenue','cost_per_conversion','roas','revenue_per_click','bounce_rate','avg_session_duration_sec','pages_per_session','engagement_score'}
    for row,values in zip(rows,embedded):
        for c,v in zip(columns,values):
            assert D(row[c])==D(str(v)) if c in numeric else row[c]==v, f'Data mismatch: {c}'
    assert 'Table.FromRows(Rows, {' in source, 'M column list must use braces.'
    rel=model['model']['relationships']
    assert any(r['fromTable']=='Marketing' and r['fromColumn']=='date' and r['toTable']=='Calendar' and r['toColumn']=='Date' and r['isActive'] and r['crossFilteringBehavior']=='oneDirection' for r in rel)
    for t in tables.values():
        for m in t.get('measures',[]):
            for ref in re.findall(r'\[([^\]]+)\]',m['expression']):
                assert ref in fields['Marketing']['Measure']|fields['Marketing']['Column'],f'Unknown DAX reference: {ref}'
    def check_fields(x):
        if isinstance(x,dict):
            for kind in ['Measure','Column']:
                if kind in x and isinstance(x[kind],dict) and 'Property' in x[kind]:
                    f=x[kind];entity=f.get('Expression',{}).get('SourceRef',{}).get('Entity')
                    if entity:assert f['Property'] in fields[entity][kind],f'Unknown visual field: {entity}.{f["Property"]}'
            for v in x.values():check_fields(v)
        elif isinstance(x,list):
            for v in x:check_fields(v)
    pages=ROOT/'powerbi/Marketing.Report/definition/pages'
    metadata=json.loads((pages/'pages.json').read_text())
    count=0
    for page_id in metadata['pageOrder']:
        pg=json.loads((pages/page_id/'page.json').read_text())
        for f in (pages/page_id/'visuals').glob('*/visual.json'):
            v=json.loads(f.read_text());p=v['position'];count+=1
            assert p['x']>=0 and p['y']>=0 and p['x']+p['width']<=pg['width'] and p['y']+p['height']<=pg['height'],f'Off-canvas visual: {f.name}'
            check_fields(v)
    # Public package must not retain original host names, user paths or bindings.
    forbidden=[r'[A-Z]:\\Users\\',r'\bDESKTOP-[A-Z0-9]{5,}',r'password\s*=',r'AccountKey\s*=']
    for f in ROOT.rglob('*'):
        if f.is_file() and f.suffix.lower() in {'.json','.bim','.pbip','.pbir','.pbism','.md','.sql','.csv','.py'} and f!=Path(__file__).resolve():
            text=f.read_text(encoding='utf-8')
            assert not any(re.search(v,text,re.I) for v in forbidden),f'Local/private string in {f.name}'
    total=lambda c,subset=rows:sum((D(r[c]) for r in subset),D(0))
    paid=[r for r in rows if r['channel_type']=='Paid']
    mismatches=sum(int(r['clicks'])>0 and abs(D(r['conversions'])/D(r['clicks'])-D(r['conversion_rate']))>D('.01') for r in rows)
    zero=[r for r in rows if D(r['spend'])>0 and D(r['revenue'])==0]
    summary={'records':len(rows),'date_start':min(r['date'] for r in rows),'date_end':max(r['date'] for r in rows),'total_revenue':str(total('revenue')),'total_spend':str(total('spend')),'paid_revenue':str(total('revenue',paid)),'paid_roas':str(total('revenue',paid)/total('spend',paid)),'ctr':str(total('clicks')/total('impressions')),'cvr':str(total('conversions')/total('clicks')),'cvr_mismatch_rows':mismatches,'zero_return_spend':str(total('spend',zero)),'exact_duplicate_rows':len(rows)-len({tuple(r.values()) for r in rows}),'category_counts':dict(collections.Counter(r['roas_category_fixed'] for r in rows)),'report_pages':len(metadata['pageOrder']),'report_visuals':count,'measures':len(fields['Marketing']['Measure']),'validation':'PASS: snapshot equivalence, field references, date relationship, canvas bounds, local-string scan','desktop_rendering':'Not tested: Power BI Desktop unavailable','sql_execution':'Not tested: SQL Server unavailable'}
    report=ROOT/'docs/validation.json';report.write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
