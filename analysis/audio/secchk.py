import json, numpy as np
R=json.load(open('final5.json')); SEC=json.load(open('sec.json'))
for nr in range(1,30):
    if str(nr) not in SEC: continue
    r=R[str(nr)]; t=np.array(r['beats']); bar=np.array(r['bar']); bi=np.array(r['bi'])
    C=np.load('chr_%02d.npy'%nr); fr=11025/110; e=np.load('hf_%02d.npy'%nr)
    dt={int(b):t[i] for i,(b,k) in enumerate(zip(bar,bi)) if k==0}
    def nov(b):
        if b-2 not in dt or b+2 not in dt: return None
        a0,a1,a2=[int(dt[x]*fr) for x in (b-2,b,b+2)]
        if a2>=C.shape[1] or a0<0: return None
        x=C[:,a0:a1].mean(1); y=C[:,a1:a2].mean(1); x/=np.linalg.norm(x)+1e-9; y/=np.linalg.norm(y)+1e-9
        f=int(dt[b]*100); cr=np.median(e[f+15:f+50])-np.median(e[f-25:f-3]) if f>30 and f+50<len(e) else 0
        return (1-x@y)*10+max(0,cr)/6
    tot={k:0 for k in range(-2,3)}; n=0
    for S,name in SEC[str(nr)]:
        if S<=2: continue
        v={k:nov(S+k) for k in range(-2,3)}
        if any(x is None for x in v.values()): continue
        best=max(v,key=v.get); tot[best]+=1; n+=1
    print('#%2d Abschnitte %2d  bester Versatz: %s'%(nr,n,' '.join('%+d:%d'%(k,tot[k]) for k in range(-2,3))))
