import json, glob, numpy as np
from PIL import Image
L=json.load(open('layout.json')); INK={}
for nr,pages in L.items():
    vals={}
    for pi,rows in enumerate(pages):
        g=np.array(Image.open('s%02d-%d.png'%(int(nr),pi+1)).convert('L'))<150; H,W=g.shape
        for b0,n,x0,x1,y0,y1 in rows:
            sp=(y1-y0)*H/4; ya=int(y0*H-2.2*sp); yb=int(y1*H+1.8*sp); xa=int(x0*W+0.4*sp); xb=int(x1*W-0.4*sp)
            box=g[ya:yb,xa:xb].copy()
            # Notenlinien entfernen: Zeilen, die fast komplett dunkel sind
            rowfull=box.mean(1)>0.6; box[rowfull,:]=False
            # Taktstrich-Spalten entfernen
            colfull=box.mean(0)>0.5; box[:,colfull]=False
            v=box.sum()/max(1,(xb-xa))/sp
            for k in range(n): vals[b0+k]=v/ (1 if n==1 else 1)
    INK[nr]=vals
json.dump(INK,open('ink.json','w'))
v=INK['26']; med=np.median(list(v.values()))
print('Jump',' '.join('%d:%.2f'%(b,v[b]/med) for b in list(range(1,13))+list(range(97,112))))
v=INK['3']; med=np.median(list(v.values()))
print('Paranoid',' '.join('%d:%.2f'%(b,v[b]/med) for b in range(1,25)))
