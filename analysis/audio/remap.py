import json, numpy as np, sys
from chartbeats import meter
CH=json.load(open('ch.json')); R=json.load(open('final.json'))
BPM={1:159,2:160,3:163,4:91,5:130,6:150,7:148,8:134,9:106,10:99,11:184,12:114,13:150,14:128,15:90,16:129,17:133,18:140,19:132,20:70,21:79,22:191,23:117,24:151,25:97,26:129,27:139,28:128,29:155}
def chart_times(nr,bars):
    c=CH.get(str(nr)) or {'m':[[1,4,4,BPM[nr]]],'end':999}
    def seg(b):
        s=c['m'][0]
        for x in c['m']:
            if x[0]<=b: s=x
        return s
    T={}; t=0.0; lo=min(bars); hi=max(bars)
    for b in range(1,hi+2):
        s=seg(b); q=meter(s[1],s[2]); sp=60/s[3]
        for k,d in enumerate(q): T[(b,k)]=t; t+=d*sp
    s=seg(1); q=meter(s[1],s[2]); sp=60/s[3]; L=sum(q)*sp
    for b in range(0,lo-1,-1):
        for k in range(len(q)): T[(b,k)]=T[(1,k)]-(1-b)*L
    return T
def drumbar(nr,b):
    c=CH.get(str(nr))
    if not c: return True
    if b<c['g'] or b>c['end']: return False
    for a,n in c.get('mr',[]):
        if a<=b<a+n: return False
    return True
def beatdur(nr,b,k):
    c=CH.get(str(nr)) or {'m':[[1,4,4,120]]}
    seg=c['m'][0]
    for x in c['m']:
        if x[0]<=b: seg=x
    q=meter(seg[1],seg[2]); return q[k] if k<len(q) else q[-1]
def remap(nr,W=6):
    r=R[str(nr)]; bt=np.array(r['beats']); bar=np.array(r['bar']); bi=np.array(r['bi'])
    x=np.zeros(len(bt))
    for i in range(1,len(bt)): x[i]=x[i-1]+beatdur(nr,int(bar[i-1]),int(bi[i-1]))
    d=np.load('b22_%02d.npz'%nr); fr=float(d['fr']); env=d['kick']+0.6*(d['snb']+d['snh'])+0.4*d['hat']
    def pk(t):
        i=int(round(t*fr)); return env[max(0,i-3):i+4].max() if 0<i<len(env)-4 else 0
    strength=np.array([pk(t) for t in bt])
    rel=np.array([drumbar(nr,int(b)) for b in bar])&(strength>2.0)&(bt>0)
    # Takte mit wenigen kräftigen Schlägen gelten als unsicher
    for b in set(bar):
        m=bar==b
        if rel[m].mean()<0.5: rel[m]=False
    idx=np.where(rel)[0]
    if len(idx)<16: return None
    out=bt.copy()
    def fit(sel,xi):
        xs=x[sel]; ys=bt[sel]; w=1/(1+np.abs(xs-xi)/8.0)
        A=np.vstack([xs-xi,np.ones_like(xs)]).T*w[:,None]
        return np.linalg.lstsq(A,ys*w,rcond=None)[0]
    for i in range(len(bt)):
        j=np.searchsorted(idx,i)
        if rel[i]:
            sel=idx[max(0,j-W):j+W+1]; f=fit(sel,x[i])[1]
            out[i]=0.5*(f+bt[i]) if abs(f-bt[i])<0.03 else bt[i]
        else:
            L=idx[max(0,j-2*W):j]; Rr=idx[j:j+2*W]
            if len(L) and len(Rr):
                # linear zwischen den letzten/nächsten Ankern, Tempo konstant über die Lücke
                a_,b_=L[-1],Rr[0]
                out[i]=bt[a_]+(bt[b_]-bt[a_])*(x[i]-x[a_])/(x[b_]-x[a_])
            else:
                sel=Rr[:16] if len(L)==0 else L[-16:]
                out[i]=sum(fit(sel,x[i])*np.array([0,1]))
    return out,rel,x,strength
if __name__=='__main__':
    res={}
    for nr in range(1,30):
        o=remap(nr)
        if o is None: print(nr,'zu wenig'); continue
        new,rel,x,st=o; old=np.array(R[str(nr)]['beats'])
        d=np.load('b22_%02d.npz'%nr); fr=float(d['fr']); env=d['kick']+0.6*(d['snb']+d['snh'])+0.4*d['hat']
        def hit(ts): 
            return np.mean([env[max(0,int(round(t*fr))-2):int(round(t*fr))+3].max()>2.0 for t in ts if 0<t*fr<len(env)-3])
        ioi=np.diff(new)/np.maximum(np.diff(x),1e-6); nd=~rel[1:]; jit=np.std(np.diff(ioi[nd])/np.median(ioi)) if nd.sum()>3 else 0
        print('%2d hit old %.0f%% new %.0f%%  shift max %.0f ms  non-drum beats %d  ioi-jitter non-drum %.3f'%(nr,100*hit(old[rel]),100*hit(new[rel]),1000*np.abs(new-old).max(),(~rel).sum(),jit))
        r=dict(R[str(nr)]); r['beats']=[round(float(v),4) for v in new]; res[nr]=r
    json.dump(res,open('final2.json','w'))
