import json, numpy as np, sys
from refine import drumbar, envs, FR, BIAS
R=json.load(open(sys.argv[1] if len(sys.argv)>1 else 'ref_perc.json'))
def peak(v,t,w=3):
    i=int(round((t+BIAS)*FR)); return v[max(0,i-w):i+w+1].max() if 0<i<len(v)-1 else 0
for nr in range(1,30):
    r=R[str(nr)]; p,m,k,s=envs(nr); bt=np.array(r['beats']); bar=np.array(r['bar']); bi=np.array(r['bi']); bn=np.array(r['bn'])
    acc={}
    for i in range(len(bt)-1):
        if not drumbar(nr,bar[i]) or bt[i]<0: continue
        n=bn[i]; d=bt[i+1]-bt[i]
        for half in (0,0.5):
            key=(n,bi[i]+half)
            a=acc.setdefault(key,[0,0,0]); a[0]+=peak(k,bt[i]+half*d); a[1]+=peak(s,bt[i]+half*d); a[2]+=1
    ns=sorted(set(kk[0] for kk in acc)); 
    main=max(ns,key=lambda n: sum(v[2] for kk,v in acc.items() if kk[0]==n))
    pos=sorted(kk[1] for kk in acc if kk[0]==main)
    kl=' '.join('%4.1f'%(acc[(main,q)][0]/acc[(main,q)][2]) for q in pos)
    sl=' '.join('%4.1f'%(acc[(main,q)][1]/acc[(main,q)][2]) for q in pos)
    print('%2d n=%d pos %s\n    kick  %s\n    snare %s'%(nr,main,' '.join('%4s'%q for q in pos),kl,sl))
