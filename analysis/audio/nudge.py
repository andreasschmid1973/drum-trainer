import json, numpy as np, sys
nr=sys.argv[1]; k=float(sys.argv[2])
R=json.load(open('ref_fix.json')); over=json.load(open('over.json')); CH=json.load(open('ch.json'))
r=R[nr]; bt=np.array(r['beats']); bar=np.array(r['bar']); bi=np.array(r['bi']); g=CH[nr]['g'] if nr in CH else 1
j=int(np.where((bar==g)&(bi==0))[0][0]); w=int(np.floor(k)); f=k-w
t=bt[j+w]+f*(bt[j+w+1]-bt[j+w]); over[nr]={'gT':float(t)-0.0116,'s':r['scale']}
json.dump(over,open('over.json','w')); print(nr,'gT',round(r['gTime'],3),'->',round(t,3))
