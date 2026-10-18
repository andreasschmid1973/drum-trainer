import json, glob, subprocess, sys, os
from PIL import Image, ImageOps
from concurrent.futures import ThreadPoolExecutor
L=json.load(open('layout.json'))
def ocr(img,tag):
    fn='/tmp/_bn_%s.png'%tag; img.save(fn)
    o=subprocess.run(['tesseract',fn,'-','--psm','7','-c','tessedit_char_whitelist=0123456789'],capture_output=True,text=True).stdout.strip()
    return o
def song(nr):
    pages=L[str(nr)]; res=[]
    for pi,rows in enumerate(pages):
        hi=Image.open('r250/s%02d-%d.png'%(nr,pi+1)).convert('L'); W,H=hi.size
        prev_y=None
        for k,r in enumerate(rows):
            if prev_y is None or abs(r[4]-prev_y)>0.003: prev_y=r[4]; continue  # erster Takt im System: Nummer abgeschnitten
            b0,n,x0,x1,y0,y1=r; sp=(y1-y0)*H/4
            box=(int(x0*W-0.2*sp),int(y0*H-2.4*sp),int(x0*W+2.6*sp),int(y0*H-0.25*sp))
            c=hi.crop(box); c=c.resize((c.size[0]*4,c.size[1]*4),Image.LANCZOS).point(lambda p:255 if p>150 else 0)
            c=ImageOps.expand(c,20,255)
            o=ocr(c,'%d_%d_%d'%(nr,pi,k))
            res.append((pi+1,b0,o))
    return nr,res
out={}
with ThreadPoolExecutor(4) as ex:
    for nr,res in ex.map(song,[int(x) for x in (sys.argv[1:] or sorted(L,key=int))]):
        ok=sum(1 for p,b,o in res if o==str(b)); bad=[(p,b,o) for p,b,o in res if o and o.isdigit() and o!=str(b)]
        out[nr]=res; print('#%d  lesbar %d/%d korrekt %d  Abweichungen %s'%(nr,sum(1 for x in res if x[2]),len(res),ok,bad[:14]),flush=True)
json.dump(out,open('barnum.json','w'))
