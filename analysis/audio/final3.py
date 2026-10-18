import json, numpy as np
import remap as RM
CHO=json.load(open('intro_choice.json'))
def smooth(x,t,W=8):
    out=np.empty_like(t)
    for i in range(len(t)):
        lo=max(0,i-W); hi=min(len(t),i+W+1); xs=x[lo:hi]; ys=t[lo:hi]
        p=np.polyfit(xs-x[i],ys,1); out[i]=p[1]
    return out
res={}
for nr in range(1,30):
    o=RM.remap(nr); r=dict(RM.R[str(nr)])
    if o is None: res[nr]=r; continue
    new,rel,x,st=o; old=np.array(r['beats'])
    f=np.where(rel)[0][0]
    if CHO.get(str(nr))=='old' and f>=4:
        seg=np.arange(0,f); live=seg[old[seg]>0.3]
        if len(live)>=4:
            sm=smooth(x[live],old[live],W=8)
            # Anschluss: Tempo und Lage am Anker stetig machen
            spq_a=np.polyfit(x[f:f+12],new[f:f+12],1)[0]
            k=live[-1]; target=new[f]-spq_a*(x[f]-x[k])
            corr=target-sm[-1]
            # Korrektur über die letzten 8 Schläge einblenden
            ramp=np.clip((np.arange(len(live))-(len(live)-8))/8.0,0,1)
            sm=sm+corr*ramp
            new[live]=sm
            # Vorlauf vor dem ersten hörbaren Schlag: mit Intro-Tempo extrapolieren
            pre=seg[old[seg]<=0.3]
            if len(pre):
                s0=np.polyfit(x[live[:8]],sm[:8],1)
                new[pre]=s0[0]*x[pre]+s0[1]
    r['beats']=[round(float(v),4) for v in new]; res[nr]=r
    io=np.diff(new[:f+1]); 
    print('#%2d intro %s: Tempo-Schwankung im Intro %.1f%%'%(nr,CHO.get(str(nr),'-'),100*np.std(io[io>0])/np.mean(io[io>0]) if f>2 else 0))
json.dump(res,open('final3.json','w'))
