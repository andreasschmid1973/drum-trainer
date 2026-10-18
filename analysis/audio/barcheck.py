import json, numpy as np, sys
R=json.load(open('ref_fix.json')); CH=json.load(open('ch.json'))
def expected(nr,b):
    c=CH[str(nr)]
    if b<c['g']-1 or b>c['end']: return 0
    if b==c['g']-1: return 0.5
    for a,n in c.get('mr',[]):
        if a<=b<a+n: return 0
    return 1
for nr in range(1,30):
    if str(nr) not in CH: continue
    r=R[str(nr)]; bt=np.array(r['beats']); bar=np.array(r['bar']); bi=np.array(r['bi'])
    d=np.load('b22_%02d.npz'%nr); fr=float(d['fr']); act=d['kick']+d['hat']+0.5*(d['snb']+d['snh'])
    bars=sorted(set(bar[(bi==0)&(bt>=0)])); obs={}
    for b in bars:
        i=np.where((bar==b)&(bi==0))[0][0]; j=np.where(bar==b)[0][-1]
        t0=bt[i]; t1=bt[j+1] if j+1<len(bt) else t0+2
        obs[b]=act[int(t0*fr):int(t1*fr)].mean()
    best=[]
    for D in range(-3,4):
        xs=[];ys=[]
        for b in bars:
            e=expected(nr,b+D)
            xs.append(e); ys.append(obs[b])
        xs=np.array(xs); ys=np.array(ys)
        c=np.corrcoef(xs,ys)[0,1] if xs.std()>0 else 0
        best.append((c,D))
    best.sort(reverse=True)
    print('%2d best bar offset %+d (corr %.2f), offset 0 corr %.2f'%(nr,best[0][1],best[0][0],[c for c,D in best if D==0][0]))
