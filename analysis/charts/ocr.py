import numpy as np, subprocess, glob, json, sys, os, re
from PIL import Image
from lay import systems
def band_numbers(img,s):
    W,H=img.size; t=s['top']*H; sp=(s['bot']-s['top'])*H/4
    y0=int(t-2.6*sp); y1=int(t-0.15*sp); x0=int(max(0,s['x0']*W-15)); x1=int(min(W,s['x1']*W+5))
    crop=img.convert('L').crop((x0,y0,x1,y1)).resize(((x1-x0)*3,(y1-y0)*3),Image.LANCZOS)
    fn='/tmp/_band.png'; crop.save(fn)
    out=subprocess.run(['tesseract',fn,'-','--psm','11','-c','tessedit_char_whitelist=0123456789','tsv'],capture_output=True,text=True).stdout
    res=[]
    for line in out.splitlines()[1:]:
        p=line.split('\t')
        if len(p)<12 or not p[11].strip().isdigit(): continue
        conf=float(p[10]); 
        if conf<30: continue
        left=int(p[6])/3+x0; h=int(p[9])/3
        if h>sp*1.6: continue   # zu groß: kein Taktnummer-Ziffer (z. B. Mehrtaktpause)
        res.append((int(p[11]),left/W,conf))
    return res
if __name__=='__main__':
    png=sys.argv[1]; img=Image.open(png)
    for s in systems(img):
        print(round(s['top'],3),[ (n,round(x,3)) for n,x,c in band_numbers(img,s)], [round(x,3) for x in s['bars']])
