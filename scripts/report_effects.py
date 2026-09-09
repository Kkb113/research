"""Post-hoc descriptive four-volume bootstrap; not a population guarantee."""
import argparse,itertools,json
from pathlib import Path
import numpy as np
p=argparse.ArgumentParser();p.add_argument('timings',type=Path);a=p.parse_args();rows=json.loads(a.timings.read_text());out={}
for other in ['upstream','sparse']:
 grouped=[]
 for name in sorted(set(x['scroll'] for x in rows)):
  grouped.append(float(np.mean([np.log(x['methods'][other]['median_seconds']/x['methods']['block']['median_seconds']) for x in rows if x['scroll']==name])))
 n=len(grouped);boot=[np.exp(np.mean([grouped[j] for j in combo])) for combo in itertools.product(range(n),repeat=n)]
 out[other]={'equal_scroll_geometric_speedup':float(np.exp(np.mean(grouped))),'conditional_bootstrap_95':[float(x) for x in np.quantile(boot,[.025,.975])],'wins':sum(x['methods'][other]['median_seconds']>x['methods']['block']['median_seconds'] for x in rows)}
print(json.dumps(out,indent=2))
