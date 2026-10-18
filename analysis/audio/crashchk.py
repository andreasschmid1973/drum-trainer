import json, numpy as np
R=json.load(open('final5.json')); SEC=json.load(open('sec.json'))
for nr in range(1,30):
    if str(nr) not in SEC: continue
    r=R[str(nr)]; t=np.array(r['beats']); bar=np.array(r['bar']); bi=np.array(r['bi']); e=np.load('hf_%02d.npy'%nr)
    dt={int(b):t[i] for i,(b,k) in enumerate(zip(bar,bi)) if k==0}
    def cr(b):
        if b not in dt: return None
        f=int(dt[b]*100)
        if f<30 or f+50>=len(e): return None
        return np.median(e[f+10:f+40])-np.median(e[f-25:f-3])
    tot={k:0.0 for k in range(-2,3)}; n=0
    for S,_ in SEC[str(nr)]:
        if S<=2: continue
        v={k:cr(S+k) for k in range(-2,3)}
        if any(x is None for x in v.values()): continue
        for k in v: tot[k]+=v[k]
        n+=1
    best=max(tot,key=tot.get)
    print('#%2d n=%2d Becken-Anstieg je Versatz: %s  -> %+d'%(nr,n,' '.join('%+d:%5.1f'%(k,tot[k]/max(1,n)) for k in range(-2,3)),best))
