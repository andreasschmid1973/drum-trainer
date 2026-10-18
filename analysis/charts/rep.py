import json, glob, numpy as np
from PIL import Image
import lay
L=json.load(open('layout.json'))
lay.MODE,lay.FOUR,lay.FULL='none',True,0.95
res={}
for nr in sorted(L,key=int):
    pngs=sorted(glob.glob('s%02d-*.png'%int(nr)),key=lambda f:int(f.split('-')[-1].split('.')[0]))
    hits=[]
    for pi,png in enumerate(pngs):
        img=Image.open(png); g=np.array(img.convert('L')); a=g<160; H,W=a.shape
        for s in lay.systems(img):
            t=int(s['top']*H); b=int(s['bot']*H); sp=(b-t)/4
            full=a[t:b+1,:].mean(0)>0.95
            cols=np.where(full)[0]; grp=[]
            for c in cols:
                if grp and c-grp[-1][-1]<=1: grp[-1].append(c)
                else: grp.append([c])
            for G in grp:
                w=len(G)
                if w<3: continue
                c0,c1=G[0],G[-1]
                # Punkte in Zwischenräumen 2 und 3 links oder rechts
                ys=[int(t+1.5*sp),int(t+2.5*sp)]
                def dots(x0,x1):
                    x0=max(0,x0); x1=min(W,x1)
                    return all(a[y-2:y+3,x0:x1].mean()>0.25 for y in ys)
                L_=dots(c0-int(1.6*sp),c0-int(0.5*sp)); R_=dots(c1+int(0.5*sp),c1+int(1.6*sp))
                xf=(c0+c1)/2/W
                # Takt bestimmen
                rows=[r for r in L[nr][pi] if abs(r[4]-s['top'])<0.01]
                bar=None
                for r in rows:
                    if r[2]-0.01<=xf<=r[3]+0.01: bar=r[0] if xf<(r[2]+r[3])/2 else r[0]+r[1]
                kind=('start' if R_ and not L_ else 'end' if L_ and not R_ else 'both' if L_ and R_ else 'thick')
                hits.append((pi+1,round(xf,3),kind,bar))
    res[nr]=hits
    print(nr,[h for h in hits if h[2]!='thick'] , 'thick:',len([h for h in hits if h[2]=='thick']))
json.dump(res,open('repeats.json','w'))
