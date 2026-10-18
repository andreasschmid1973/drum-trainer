import json, glob, numpy as np
from PIL import Image
from lay import systems
CH=json.load(open('../real/ch.json'))
def slots(c):
    out=[]; b=1
    while b<=c['end']:
        n=1
        for a,m in c.get('mr',[]):
            if a==b: n=m
        out.append((b,n)); b+=n
    return out
DET={}
for nr in range(1,30):
    if str(nr) not in CH: continue
    pngs=sorted(glob.glob('s%02d-*.png'%nr),key=lambda f:int(f.split('-')[1].split('.')[0]))
    pages=[]
    for png in pngs:
        sy=[]
        for s in systems(Image.open(png)):
            xs=[]
            for x in s['bars']:
                if xs and x-xs[-1]<0.012: continue
                xs.append(x)
            if len(xs)>=2: sy.append({'y0':s['top'],'y1':s['bot'],'xs':xs})
        pages.append(sy)
    det=sum(len(s['xs'])-1 for p in pages for s in p); exp=len(slots(CH[str(nr)]))
    DET[nr]=pages
    print('#%2d erkannt %3d  erwartet %3d  %s   pro Seite %s'%(nr,det,exp,'OK' if det==exp else 'diff %+d'%(det-exp),[sum(len(s['xs'])-1 for s in p) for p in pages]),flush=True)
json.dump(DET,open('det.json','w'))
