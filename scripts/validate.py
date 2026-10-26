import json, urllib.parse
from pathlib import Path
p=Path(__file__).resolve().parents[1]
data=json.loads((p/'_data/companies.json').read_text())
ids=set()
for c in data:
 assert c['id'] not in ids,c['id'];ids.add(c['id'])
 for field in ['name','website','location','region','sector','description','tech','remote','points','service','signal','rationale','pitch','people','sources','checked']:assert field in c,(c['id'],field)
 for k,maximum in [('tech',35),('need',25),('remote',25),('commercial',15)]:assert isinstance(c['points'][k],int) and 0<=c['points'][k]<=maximum
 for url in [c['website']]+[s['url'] for s in c['sources']]+[person[k] for person in c['people'] for k in ['source','photo','linkedin'] if person.get(k)]:assert urllib.parse.urlparse(url).scheme=='https',url
 assert c['sources'],c['id']
 assert len(c['signal'])<700
print(f'Validated {len(data)} companies, scores, unique IDs and source URLs.')
