#!/usr/bin/env python3
import json,sys
from collections import defaultdict
from pathlib import Path
p=Path(sys.argv[1] if len(sys.argv)>1 else 'logs/skill-usage.jsonl')
req={'run_id','task_id','skill','version','trigger','phase','result','score','evidence'}
stats=defaultdict(lambda:{'runs':0,'pass':0,'partial':0,'fail':0,'not_needed':0,'sum':0.0}); errors=[]
for n,line in enumerate(p.read_text().splitlines(),1):
 if not line.strip(): continue
 try:r=json.loads(line)
 except Exception as e: errors.append(f'line {n}: {e}'); continue
 m=req-r.keys()
 if m: errors.append(f'line {n}: missing {sorted(m)}'); continue
 s=stats[r['skill']]; s['runs']+=1; s['sum']+=float(r['score']); s[r['result'].lower()]+=1
out={'valid':not errors,'errors':errors,'skills':{k:{**{x:y for x,y in v.items() if x!='sum'},'average_score':round(v['sum']/v['runs'],1)} for k,v in stats.items()}}
print(json.dumps(out,indent=2)); raise SystemExit(1 if errors else 0)
