import json, numpy as np
from chartbeats import CH, meter
import locoff
F=json.load(open('final5.json'))
def seg(nr,bar):
    m=CH[str(nr)]['m']; s=m[0]
    for x in m:
        if x[0]<=bar: s=x
    return s
def qlen(nr,bar):  # list of beat lengths (quarters) of a bar
    s=seg(nr,bar); return meter(s[1],s[2])
def labels(nr,bar0,n):
    out=[]; b=bar0
    while len(out)<n:
        q=qlen(nr,b)
        for k in range(len(q)): out.append((b,k,len(q)))
        b+=1
    return out[:n]
def synth(nr,bar_from,bar_to,t_from,t_to):
    """beats for bars [bar_from,bar_to) spread linearly (in quarters) between t_from and t_to"""
    pos=[];lab=[];acc=0
    for b in range(bar_from,bar_to):
        q=qlen(nr,b)
        for k,l in enumerate(q): pos.append(acc); lab.append((b,k,len(q))); acc+=l
    pos=np.array(pos); return list(t_from+(t_to-t_from)*pos/acc), lab
def pre(nr,t1,spq,bars=2):
    """pre-beats before bar 1 (bars 1-bars..0) using bar-1 meter"""
    q=qlen(nr,1); T=[];L=[]
    for b in range(1-bars,1):
        for k,l in enumerate(q): L.append((b,k,len(q)))
    tot=bars*sum(q); acc=0
    for b in range(bars):
        for l in q: T.append(t1-spq*(tot-acc)); acc+=l
    return T,L
def pack(nr,T,L):
    r=dict(F[str(nr)]); r['beats']=[round(float(x),4) for x in T]
    r['bar']=[l[0] for l in L]; r['bi']=[l[1] for l in L]; r['bn']=[l[2] for l in L]
    return r
out={}
# ---------- 4 War Pigs ----------
R=F['4']; t=np.array(R['beats']); w=np.load('wp_intro_beats.npy')
T=[];L=[]
for b in range(1,17):            # 12/8: 6 quarter-beats per bar (w index 2+6(b-1)), dotted beats at 0,1.5,3,4.5
    i=2+6*(b-1)
    for k,qp in enumerate([0,1.5,3,4.5]):
        a=int(qp); f=qp-a; T.append(w[i+a]+f*(w[i+a+1]-w[i+a])); L.append((b,k,4))
t17=w[98]; i19=int(np.argmin(abs(t-58.11)))
T2,L2=synth(4,17,19,t17,t[i19]); T+=T2; L+=L2
rest=t[i19:]; L+=labels(4,19,len(rest)); T+=list(rest)
spq=(w[8]-w[2])/6; P,PL=pre(4,T[0],spq*1.5/1.5); 
P,PL=pre(4,T[0],spq)   # meter() gives 1.5-quarter beats -> pre uses spq per quarter
out['4']=pack(4,P+T,PL+L)
# ---------- 6 Wanted Dead or Alive ----------
R=F['6']; t=np.array(R['beats']); a=int(np.argmin(abs(t-8.64)))
sp=np.median(np.diff(t[a:a+16]))
T=list(t[a]-sp*np.arange(16,0,-1))+list(t[a:])   # 2 bars before bar 3 (=bars 1,2) + 2 pre-bars
L=labels(6,-1,16)+labels(6,3,len(t)-a)
# fix: labels(6,-1,..) uses bar-1 meter, fine (4/4)
T=np.array(T)
# local timing correction 45-100 s (bars without kick were only interpolated)
o,fr=locoff.env(6)
def score(ts,d):
    f=np.round((ts+d)*fr).astype(int); f=f[(f>1)&(f<len(o)-2)]
    return np.mean([o[j-1:j+2].max() for j in f]) if len(f) else 0
ds=np.arange(-0.15,0.1501,0.005)
def best(ts): s=[score(ts,d) for d in ds]; return ds[int(np.argmax(s))], max(s), score(ts,0)
ref=np.median([best(T[k-4:k+4])[0] for k in range(20,len(T)-20,8) if T[k]>110 and T[k]<280])
corr=np.zeros(len(T))
idx=[k for k in range(4,len(T)-4) if 45<T[k]<100]
raw={k:best(T[k-4:k+5]) for k in idx}
for k in idx:
    d,v,v0=raw[k]
    if v>v0*1.15: corr[k]=d-ref
from scipy.ndimage import median_filter, uniform_filter1d
corr=uniform_filter1d(median_filter(corr,7),5)
T=T+corr
print('#6 ref %.3f, max corr %.3f'%(ref,abs(corr).max()))
out['6']=pack(6,T,L)
# ---------- 20 Silent Lucidity ----------
R=F['20']; t=np.array(R['beats']); i21=int(np.argmin(abs(t-68.61)))
t1=0.33; T,L=synth(20,1,21,t1,t[i21]); spq=(t[i21]-t1)/79.75
P,PL=pre(20,t1,spq)
# pre-bars in 4/4 for a clean count-in
PL=[(b,k,4) for b in (-1,0) for k in range(4)]; P=[t1-spq*(8-k) for k in range(8)]
rest=t[i21:]; T=P+T+list(rest); L=PL+L+labels(20,21,len(rest))
out['20']=pack(20,T,L)
print('#20 spq %.4f = %.1f BPM'%(spq,60/spq))
# ---------- 26 Jump ----------
R=F['26']; t=np.array(R['beats']); i9=int(np.argmin(abs(t-15.484)))
bars=[0.865,2.671,4.478,6.284,8.091,9.898,11.705,13.512,t[i9]]
T=[];L=[]
for b in range(1,9):
    for k in range(4): T.append(bars[b-1]+(bars[b]-bars[b-1])*k/4); L.append((b,k,4))
spq=(bars[4]-bars[0])/16
P=[bars[0]-spq*(8-k) for k in range(8)]; PL=[(b,k,4) for b in (-1,0) for k in range(4)]
rest=t[i9:]; T=P+T+list(rest); L=PL+L+labels(26,9,len(rest))
out['26']=pack(26,T,L)
for nr in out:
    r=out[nr]; t=np.array(r['beats']); bar=np.array(r['bar']); bi=np.array(r['bi'])
    assert np.all(np.diff(t)>0.1), nr
    c=CH[nr]; e=np.where((bar==c['end'])&(bi==0))[0]
    print(nr,'bar1 %.2f'%t[np.where((bar==1)&(bi==0))[0][0]],'end bar %d at %s, dur %.1f, last bar %d'%(c['end'],t[e[0]] if len(e) else '-',r['duration'],bar[-1]))
F2=dict(F); F2.update(out); json.dump(F2,open('final6.json','w'))
