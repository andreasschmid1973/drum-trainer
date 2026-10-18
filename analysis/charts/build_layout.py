import json, glob, numpy as np
from PIL import Image
import lay
CH=json.load(open('../real/ch.json'))
def slots(c):
    out=[]; b=1
    while b<=c['end']:
        n=1
        for a,m in c.get('mr',[]):
            if a==b: n=m
        out.append((b,n)); b+=n
    return out
def detect(nr,mode):
    lay.MODE,lay.FOUR,lay.FULL=mode
    pngs=sorted(glob.glob('s%02d-*.png'%nr),key=lambda f:int(f.split('-')[-1].split('.')[0]))
    pages=[]
    for png in pngs:
        sy=[]
        for s in lay.systems(Image.open(png)):
            xs=[]
            for x in s['bars']:
                if xs and x-xs[-1]<0.012: continue
                xs.append(x)
            if len(xs)>=2: sy.append({'y0':s['top'],'y1':s['bot'],'xs':xs})
        pages.append(sy)
    return pages
LAYOUT={}
for nr in range(1,30):
    if str(nr) not in CH: continue
    sl=slots(CH[str(nr)]); exp=len(sl); best=None
    for mode in [(m,f,u) for m in ('none','blob') for f in (False,True) for u in (0.95,0.90)]:
        P=detect(nr,mode); det=sum(len(s['xs'])-1 for p in P for s in p)
        if best is None or abs(det-exp)<abs(best[1]-exp): best=(P,det,mode)
    P,det,mode=best; diff=det-exp
    allsys=[s for p in P for s in p]
    # Korrektur: fehlende Taktstriche im breitesten Takt ergänzen, überzählige am schmalsten Paar entfernen
    while diff<0:
        bw=None
        for s in allsys:
            w=np.diff(s['xs']); med=np.median(w)
            k=int(np.argmax(w)); r=w[k]/med
            if bw is None or r>bw[0]: bw=(r,s,k)
        _,s,k=bw; s['xs'].insert(k+1,(s['xs'][k]+s['xs'][k+1])/2); diff+=1
    while diff>0:
        bw=None
        for s in allsys:
            w=np.diff(s['xs'])
            if len(w)<2: continue
            for k in range(len(w)-1):
                v=w[k]+w[k+1]
                if bw is None or v<bw[0]: bw=(v,s,k)
        _,s,k=bw; del s['xs'][k+1]; diff-=1
    pages=[]; si=0
    for p in P:
        rows=[]
        for s in p:
            for k in range(len(s['xs'])-1):
                b0,n=sl[si]; si+=1
                rows.append([b0,n,round(s['xs'][k],4),round(s['xs'][k+1],4),round(s['y0'],4),round(s['y1'],4)])
        pages.append(rows)
    LAYOUT[nr]=pages
    print('#%d mode %s det %d exp %d -> korrigiert um %+d'%(nr,mode,det,exp,exp-det),flush=True)
json.dump(LAYOUT,open('layout.json','w'))
