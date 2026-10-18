import json, numpy as np
from chartbeats import chart_labels
from refine import refine
R=json.load(open('ref_fix.json')); CH=json.load(open('ch.json'))
def idx_of(r,b,k=0):
    bar=np.array(r['bar']); bi=np.array(r['bi']); w=np.where((bar==b)&(bi==k))[0]; return int(w[0]) if len(w) else None
def set_from(r,i0,times,labels):
    r['beats']=r['beats'][:i0]+list(map(float,times)); r['bar']=r['bar'][:i0]+[l[0] for l in labels]; r['bi']=r['bi'][:i0]+[l[1] for l in labels]; r['bn']=r['bn'][:i0]+[l[2] for l in labels]
def labels_back(nr,g,n):
    # n Labels vor Takt g (rückwärts), in zeitlicher Reihenfolge
    out=[]; b=g-1
    while len(out)<n:
        L=chart_labels(nr,b,64); L=[l for l in L if l[0]==b]; out=L+out; b-=1
    return out[-n:]
def rebuild_from_madmom(nr,A_bar,at):
    r=R[str(nr)]; mb=np.load('mmdb_%02d.npy'%nr)[:,0]; k=int(np.argmin(abs(mb-at)))
    i0=next(i for i,t in enumerate(r['beats']) if t>=mb[k]-0.05)
    set_from(r,i0,mb[k:],chart_labels(nr,A_bar,len(mb)-k))
# 1) Wanted Dead: Takt 3 = unsere bisherige Takt-1-Eins
# (Wanted Dead: Taktzählung bleibt, 2/4-Takt bestätigt)
# 2) War Pigs Intro: 16 Takte 12/8 (64 Puls-Schläge) gleichmäßig zwischen Takt 1 und Takt 17
r=R['4']; t17=r['beats'][idx_of(r,17)]; t1=r['beats'][idx_of(r,1,1)]
pul=np.linspace(t1,t17,65)[:-1]; i17=idx_of(r,17)
tail_t=r['beats'][i17:]; tail_l=list(zip(r['bar'][i17:],r['bi'][i17:],r['bn'][i17:]))
labs=chart_labels(4,1,64)
pre_n=4; pre_t=list(t1-(np.arange(pre_n,0,-1))*(pul[1]-pul[0])); pre_l=labels_back(4,1,pre_n)
r['beats']=pre_t+list(pul)+tail_t; r['bar']=[l[0] for l in pre_l+labs]+[l[0] for l in tail_l]; r['bi']=[l[1] for l in pre_l+labs]+[l[1] for l in tail_l]; r['bn']=[l[2] for l in pre_l+labs]+[l[2] for l in tail_l]
# 3) Intro: madmom-Schläge statt hochgerechnetem Raster, wenn die Schlagebene passt
for nr in range(1,30):
    if nr==4: continue
    r=R[str(nr)]; c=CH.get(str(nr)); g=c['g'] if c else 1
    ig=idx_of(r,g)
    if ig is None or ig<2: continue
    tg=r['beats'][ig]; mb=np.load('mmdb_%02d.npy'%nr)[:,0]
    ioi_ours=np.median(np.diff(r['beats'][max(0,ig-8):ig+1]))
    pre=mb[mb<tg-0.5*ioi_ours]
    if len(pre)<4: continue
    ioi_mm=np.median(np.diff(pre))
    if abs(np.log(ioi_mm/ioi_ours))>0.12: print(nr,'intro: madmom-Ebene passt nicht (%.2f vs %.2f s) -> Chart-Raster'%(ioi_mm,ioi_ours)); continue
    # Lücke zwischen letztem madmom-Schlag und Groove-Eins muss ~1 Schlag sein
    gap=tg-pre[-1]
    if abs(gap/ioi_ours-1)>0.25: print(nr,'intro: Anschluss passt nicht (gap %.2f)'%gap); continue
    labs=labels_back(nr,g,len(pre))
    tail=list(zip(r['beats'][ig:],r['bar'][ig:],r['bi'][ig:],r['bn'][ig:]))
    r['beats']=list(map(float,pre))+[x[0] for x in tail]; r['bar']=[l[0] for l in labs]+[x[1] for x in tail]
    r['bi']=[l[1] for l in labs]+[x[2] for x in tail]; r['bn']=[l[2] for l in labs]+[x[3] for x in tail]
    print(nr,'intro: %d madmom-Schläge übernommen'%len(pre))
# 4) Feinabgleich auf die Drum-Transienten (±30 ms)
for nr in range(1,30):
    r=R[str(nr)]; nb,sh,dr=refine(nr,r,W=0.03,step=0.0025,alpha=4000.0)
    r['beats']=[round(float(x),4) for x in nb]
json.dump(R,open('final.json','w'))
