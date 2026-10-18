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
def detect_page(png,mode):
    lay.MODE,lay.FOUR,lay.FULL=mode
    sy=[]
    for s in lay.systems(Image.open(png)):
        xs=[]
        for x in s['bars']:
            if xs and x-xs[-1]<0.012: continue
            xs.append(x)
        if len(xs)>=2: sy.append({'y0':s['top'],'y1':s['bot'],'xs':xs})
    return sy
MODES=[(m,f,u) for m in ('none','blob') for f in (True,False) for u in (0.95,0.90)]
LAYOUT={}; REP=[]
for nr in range(1,30):
    c=CH.get(str(nr))
    if not c: continue
    sl=slots(c); P=c['pg']; pngs=sorted(glob.glob('s%02d-*.png'%nr),key=lambda f:int(f.split('-')[-1].split('.')[0]))
    pages=[]
    for pi,png in enumerate(pngs):
        first=P[pi]; nxt=P[pi+1] if pi+1<len(P) else c['end']+1
        psl=[s for s in sl if first<=s[0]<nxt]; exp=len(psl)
        best=None
        for mode in MODES:
            S=detect_page(png,mode); det=sum(len(s['xs'])-1 for s in S)
            if best is None or abs(det-exp)<abs(best[1]-exp): best=(S,det,mode)
            if det==exp: break
        S,det,mode=best; diff=det-exp
        if diff: REP.append('#%d S.%d: %+d'%(nr,pi+1,-diff))
        while diff<0 and S:
            bw=None
            for s in S:
                w=np.diff(s['xs']); med=np.median(w); k=int(np.argmax(w))
                if bw is None or w[k]/med>bw[0]: bw=(w[k]/med,s,k)
            _,s,k=bw; s['xs'].insert(k+1,(s['xs'][k]+s['xs'][k+1])/2); diff+=1
        while diff>0:
            bw=None
            for s in S:
                w=np.diff(s['xs'])
                for k in range(len(w)-1):
                    if bw is None or w[k]+w[k+1]<bw[0]: bw=(w[k]+w[k+1],s,k)
            if bw is None: break
            _,s,k=bw; del s['xs'][k+1]; diff-=1
        rows=[]; si=0
        for s in S:
            for k in range(len(s['xs'])-1):
                if si>=len(psl): break
                b0,n=psl[si]; si+=1
                rows.append([b0,n,round(s['xs'][k],4),round(s['xs'][k+1],4),round(s['y0'],4),round(s['y1'],4)])
        pages.append(rows)
    LAYOUT[nr]=pages
json.dump(LAYOUT,open('layout.json','w'))
print('\n'.join(REP)); print(len(REP),'Seiten korrigiert')
