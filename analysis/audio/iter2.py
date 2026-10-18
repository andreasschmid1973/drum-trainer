import json, numpy as np, sys
from refine import refine, drumbar, envs, FR, BIAS
R=json.load(open('res_fix.json')); out={}
for nr in range(1,30):
    r=dict(R[str(nr)])
    for it in range(4):
        nb,sh,dr=refine(nr,r); r['beats']=[float(x) for x in nb]
        if np.sum(np.abs(sh)>=0.145)==0: break
    # Qualität nur in Drum-Takten: Anteil Schläge mit Onset-Spitze innerhalb ±15 ms
    p,m,k,s=envs(nr); bt=np.array(r['beats']); bar=np.array(r['bar'])
    dmask=np.array([drumbar(nr,b) for b in bar])&(bt>0)
    def peak(t,w):
        i=int(round((t+BIAS)*FR)); return p[max(0,i-w):i+w+1].max() if 0<i<len(p) else 0
    on=np.array([peak(t,3) for t in bt[dmask]])
    ib=np.median(np.diff(bt)); off=np.array([peak(t+ib/2,3) for t in bt[dmask]])
    hit=np.mean(on>1.0)
    r['beats']=[round(x,4) for x in r['beats']]; out[nr]=r
    print('%2d iters %d  drum-beats %4d  onset-at-beat %.0f%%  mean on %.2f off %.2f'%(nr,it+1,dmask.sum(),100*hit,on.mean(),off.mean()))
json.dump(out,open('ref_fix.json','w'))
