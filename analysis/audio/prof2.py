import json, numpy as np, sys
from refine import drumbar
R=json.load(open(sys.argv[1] if len(sys.argv)>1 else 'ref_perc.json'))
def B(nr):
    d=np.load('b22_%02d.npz'%nr); return d['kick'],0.5*(d['snb']+d['snh']),d['hat'],float(d['fr'])
def pk(v,t,fr,w=2):
    i=int(round(t*fr)); return v[max(0,i-w):i+w+1].max() if 0<i<len(v)-1 else 0
for nr in [int(x) for x in sys.argv[2:]] or range(1,30):
    r=R[str(nr)]; k,s,h,fr=B(nr); bt=np.array(r['beats']); bar=np.array(r['bar']); bi=np.array(r['bi']); bn=np.array(r['bn'])
    acc={}
    for i in range(len(bt)-1):
        if not drumbar(nr,bar[i]) or bt[i]<0: continue
        n=bn[i]; d=bt[i+1]-bt[i]
        for half in (0,0.5):
            a=acc.setdefault((n,bi[i]+half),np.zeros(4)); a+=[pk(k,bt[i]+half*d,fr),pk(s,bt[i]+half*d,fr),pk(h,bt[i]+half*d,fr),1]
    main=max(set(q[0] for q in acc),key=lambda n: sum(v[3] for q,v in acc.items() if q[0]==n))
    pos=sorted(q[1] for q in acc if q[0]==main)
    print('%2d n=%d '%(nr,main)+' '.join('%5s'%q for q in pos))
    for j,nm in enumerate(['kick','snare','hat']): print('   %-5s '%nm+' '.join('%5.1f'%(acc[(main,q)][j]/acc[(main,q)][3]) for q in pos))
