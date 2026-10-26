"""Refresh public job-board evidence. No credentials and no LinkedIn scraping.
A hiring signal is never treated as an intention to purchase B2B services.
"""
import concurrent.futures, datetime, json, re, urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
TODAY=datetime.date.today().isoformat()
PATTERNS={'PostgreSQL':r'\b(postgres(?:ql)?)\b','SQL Server':r'\b(sql server|mssql)\b','MongoDB':r'\bmongodb\b','MariaDB':r'\bmariadb\b','MySQL':r'\bmysql\b','AWS':r'\b(aws|amazon web services)\b','Azure':r'\bazure\b'}
def fetch(url):
 req=urllib.request.Request(url,headers={'User-Agent':'PacificProspect/1.0 (public hiring research)'})
 with urllib.request.urlopen(req,timeout=25) as r:return json.load(r)
def scan(board):
 try:
  payload=fetch('https://api.ashbyhq.com/posting-api/job-board/'+board['board'])
  if not isinstance(payload.get('jobs'),list):raise ValueError('Invalid API response')
  found=[]
  for j in payload['jobs']:
   text=j.get('descriptionPlain','');title=j.get('title','')
   tech=[k for k,v in PATTERNS.items() if re.search(v,text,re.I)]
   if not tech or not re.search(r'engineer|database|devops|architect|infrastructure|developer|platform|SRE',title,re.I):continue
   found.append((j,tech))
  return board,found,None
 except Exception as e:return board,[],type(e).__name__
def main():
 curated=json.loads((ROOT/'_data/curated.json').read_text());boards=json.loads((ROOT/'_data/boards.json').read_text())
 previous=json.loads((ROOT/'_data/companies.json').read_text()) if (ROOT/'_data/companies.json').exists() else []
 records={c['id']:c for c in previous if c.get('origin')=='feed'}
 records.update({c['id']:c for c in curated});failures=[];success=0
 with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
  for b,jobs,error in pool.map(scan,boards):
   if error:
    failures.append({'source':b['board'],'error':error});continue
   success+=1;id=b['board']
   if not jobs:
    if id in records and records[id].get('origin')=='feed':del records[id]
    if id in records and records[id].get('origin')=='curated':records[id]['sourceStatus']='Fonte editoriale; nessun annuncio pertinente nel feed corrente'
    continue
   tech=sorted(set(t for _,ts in jobs for t in ts));best=sorted(jobs,key=lambda x:(bool(x[0].get('isRemote')),len(x[1])),reverse=True)
   j=best[0][0];text=' '.join(x[0].get('descriptionPlain','') for x in jobs);loc=j.get('location') or 'Da verificare'
   remote_jobs=[x[0] for x in jobs if x[0].get('isRemote')]
   global_remote=any(re.search(r'europe|EMEA|worldwide|anywhere|global',x.get('location',''),re.I) for x in remote_jobs)
   remote=25 if global_remote else 15 if remote_jobs else 5 if any(x[0].get('workplaceType')=='Hybrid' for x in jobs) else 0
   technical=35 if any(t not in ('AWS','Azure') for t in tech) else 20
   need=25 if re.search(r'database (administrator|engineer)|\bDBA\b|database migration|query optimization|postgres.{0,30}(scal|migrat)',text,re.I) else 15
   contract=8 if any(x[0].get('employmentType')=='Contract' for x in jobs) else 0
   old=records.get(id,{})
   records[id]={**old,'id':id,'name':b['name'],'website':b['website'],'location':loc,'region':'Europa' if re.search(r'europe|EMEA|london|paris|berlin|amsterdam|dublin|lisbon|prague',loc,re.I) else 'Mondo','sector':old.get('sector','Tecnologia'),'description':old.get('description','Azienda con posizioni tecniche pubbliche pertinenti ai servizi Pacific IT. Attività e dimensioni da approfondire.'),'tech':tech,'remote':'Remoto · Europa / globale' if remote==25 else 'Remoto · vincoli da verificare' if remote==15 else 'Ibrido' if remote==5 else 'Remoto non documentato','points':dict(tech=technical,need=need,remote=remote,commercial=contract),'service':'Health check & Remote DBA' if technical==35 else 'Cloud & automazione','signal':f"{len(jobs)} annunci tecnici pertinenti. Esempio: {j['title']}.",'rationale':f"Tecnologie citate negli annunci: {', '.join(tech)}. La ricerca di dipendenti non dimostra apertura a servizi B2B.",'pitch':old.get('pitch','Proporre un assessment mirato alle tecnologie citate, verificando prima se valutano un supporto esterno.'),'people':old.get('people',[]),'sources':[dict(label=x[0]['title'],url=x[0]['jobUrl']) for x in best[:5]],'checked':TODAY,'sourceStatus':'Feed pubblico consultato; annunci presenti alla verifica','origin':old.get('origin','feed')}
 for c in records.values():
  if (datetime.date.today()-datetime.date.fromisoformat(c['checked'])).days>30:
   c['sourceStatus']='Evidenza oltre 30 giorni: da riconfermare';c['points']['need']=min(c['points']['need'],5);c['points']['commercial']=0
 result=sorted(records.values(),key=lambda c:(-sum(c['points'].values()),c['name']))
 (ROOT/'_data/companies.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 (ROOT/'_data/meta.json').write_text(json.dumps(dict(updated=TODAY,sourceCount=len(boards),successfulFeeds=success,failedFeeds=failures,companies=len(result),coverage='Catalogo editoriale e aziende con job board configurata; non esaustivo.'),ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(dict(companies=len(result),successfulFeeds=success,failedFeeds=len(failures))))
 if success==0:print('WARNING: no live feeds available; previous and curated evidence preserved')
if __name__=='__main__':main()
