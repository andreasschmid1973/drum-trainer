import json, numpy as np, subprocess
from refine import drumbar
R=json.load(open('ref_perc.json')); CH=json.load(open('ch.json'))
def pk(v,t,w=2):
    i=int(round(t*100)); return v[max(0,i-w):i+w+1].max() if 0<=i<len(v) else 0
plan={}
for nr in range(1,30):
    a=np.load('mmact_%02d.npy'%nr); beat=a[:,0]+a[:,1]; down=a[:,1]
    r=R[str(nr)]; bt=np.array(r['beats']); bar=np.array(r['bar']); bi=np.array(r['bi']); bn=np.array(r['bn'])
    sel=[i for i in range(len(bt)-1) if bt[i]>0.3]
    on=np.mean([pk(beat,bt[i]) for i in sel]); off=np.mean([pk(beat,bt[i]+(bt[i+1]-bt[i])/2) for i in sel])
    half=0.5 if off>on*1.3 else 0.0
    # Downbeat-Profil auf dem (ggf. halb verschobenen) Raster
    dp=np.zeros(4); cnt=np.zeros(4)
    for i in sel:
        if bn[i]!=4: continue
        t=bt[i]+half*(bt[i+1]-bt[i]); dp[bi[i]]+=pk(down,t); cnt[bi[i]]+=1
    dp/=np.maximum(cnt,1); k=int(np.argmax(dp)); srt=np.sort(dp)
    conf=srt[-1]/(srt[-2]+1e-3)
    if conf<1.6: k=0
    d=k+half
    if d>2.01: d-=4
    if abs(d-2)<0.01:
        d=2.0  # später nach Intro-Lage entscheiden
    plan[nr]={'shift':d,'conf':round(float(conf),2),'on':round(float(on),2),'off':round(float(off),2),'prof':[round(float(x),2) for x in dp]}
    print(nr,plan[nr])
json.dump(plan,open('plan.json','w'))
