import json, numpy as np
import remap as RM
for nr in range(1,30):
    o=RM.remap(nr)
    if o is None: continue
    new,rel,x,st=o; r=RM.R[str(nr)]; bt=np.array(r['beats']); bar=np.array(r['bar']); bi=np.array(r['bi'])
    idx=np.where(rel)[0]
    # Tempo der Anker (s pro Viertel) lokal
    for a,b in zip(idx[:-1],idx[1:]):
        if b-a<4: continue
        q=x[b]-x[a]; dt=bt[b]-bt[a]
        L=idx[(idx<=a)][-8:]; Rr=idx[(idx>=b)][:8]
        spq=[]
        for S in (L,Rr):
            if len(S)>2: spq.append(np.polyfit(x[S],bt[S],1)[0])
        if not spq: continue
        exp=np.mean(spq); ratio=dt/(q*exp)
        flag='  <-- passt nicht' if abs(ratio-1)>0.04 else ''
        print('#%2d Lücke Takt %d.%d – %d.%d (%.1f Viertel, %.2fs): Verhältnis %.3f  ~%+.2f Takte%s'%(nr,bar[a],bi[a]+1,bar[b],bi[b]+1,q,dt,ratio,(dt/exp-q)/4,flag))
