import json, numpy as np
import remap as RM
R3=json.load(open('final3.json')); out={}
def robust(x,t,W=6,c=0.04,it=4):
    w_all=np.ones(len(t)); fit=t.copy()
    for _ in range(it):
        for i in range(len(t)):
            lo=max(0,i-W); hi=min(len(t),i+W+1); xs=x[lo:hi]-x[i]; ys=t[lo:hi]; w=w_all[lo:hi]*(1-(np.abs(xs)/(np.abs(xs).max()+1e-9))**3)**3+1e-6
            A=np.vstack([xs,np.ones_like(xs)]).T*np.sqrt(w)[:,None]; p=np.linalg.lstsq(A,ys*np.sqrt(w),rcond=None)[0]; fit[i]=p[1]
        r=np.abs(t-fit); w_all=np.where(r<c,(1-(r/c)**2)**2,0.0)
    return fit
d_stats=[]
for nr in range(1,30):
    r=dict(R3[str(nr)]); t=np.array(r['beats']); bar=np.array(r['bar']); bi=np.array(r['bi'])
    x=np.zeros(len(t))
    for i in range(1,len(t)): x[i]=x[i-1]+RM.beatdur(nr,int(bar[i-1]),int(bi[i-1]))
    f=robust(x,t)
    d=np.load('b22_%02d.npz'%nr); fr=float(d['fr']); env=d['kick']+0.6*(d['snb']+d['snh'])+0.4*d['hat']
    strg=np.array([env[max(0,int(round(v*fr))-2):int(round(v*fr))+3].max() if 0<v*fr<len(env)-3 else 0 for v in t])
    dmb=np.array([RM.drumbar(nr,int(b)) for b in bar])
    dev=t-f; keep=(np.abs(dev)<0.012)&(strg>3.5)&dmb
    new=np.where(keep,t,np.where(np.abs(dev)<0.012,f+0.5*dev,f))
    dm=np.array([RM.drumbar(nr,int(b)) for b in bar])&(t>0.3)
    hit=lambda ts: np.mean([env[max(0,int(round(v*fr))-2):int(round(v*fr))+3].max()>2.0 for v in ts if 0<v*fr<len(env)-3])
    io=np.diff(new)/np.diff(x); jit=np.median(np.abs(np.diff(io))/io[1:])
    print('#%2d Treffer vorher %.0f%% nachher %.0f%%  Tempo-Unruhe Schlag-zu-Schlag %.2f%%  max Korrektur %.0f ms'%(nr,100*hit(t[dm]),100*hit(new[dm]),100*jit,1000*np.abs(new-t).max()))
    # Schwache Takte (kaum Schlagzeug, z. B. Keyboard allein): gleichmäßig zwischen kräftigen Nachbarn
    bars=sorted(set(bar.tolist())); act={}
    for b in bars:
        ii=np.where(bar==b)[0]; t0=new[ii[0]]; t1=new[ii[-1]]+(new[ii[-1]]-new[ii[-2]] if len(ii)>1 else 0.5)
        seg=env[max(0,int(t0*fr)):max(0,int(t1*fr))]; act[b]=np.sort(seg)[-8:].mean() if len(seg)>8 else 0
    med=np.median([act[b] for b in bars if RM.drumbar(nr,b)])
    weak=np.array([act[int(b)]<0.55*med for b in bar])
    strong=np.where(~weak&(new>0.3))[0]; spans=0
    i=0
    while i<len(new):
        if weak[i]:
            j=i
            while j<len(new) and weak[j]: j+=1
            L=strong[strong<i]; Rr=strong[strong>=j]
            if len(L) and len(Rr) and (j-i)>=4:
                a_,b_=L[-1],Rr[0]
                for k in range(a_+1,b_): new[k]=new[a_]+(new[b_]-new[a_])*(x[k]-x[a_])/(x[b_]-x[a_])
                spans+=1
            i=j
        else: i+=1
    r['beats']=[round(float(v),4) for v in new]; out[nr]=r
json.dump(out,open('final4.json','w'))
