import glob, subprocess, json, sys
from PIL import Image, ImageOps
import lay
lay.MODE,lay.FOUR,lay.FULL='none',True,0.95
def nums(nr):
    out=[]
    los=sorted(glob.glob('s%02d-*.png'%nr),key=lambda f:int(f.split('-')[-1].split('.')[0]))
    for pi,lp in enumerate(los):
        lo=Image.open(lp); hi=Image.open('r250/'+lp.split('/')[-1]); W,H=hi.size
        for s in lay.systems(lo):
            t=s['top']*H; sp=(s['bot']-s['top'])*H/4; x0=s['x0']*W
            box=(max(0,int(x0-3.0*sp)),int(t-2.3*sp),int(x0+1.2*sp),int(t+0.2*sp))
            c=hi.crop(box).convert('L'); c=c.resize((c.size[0]*4,c.size[1]*4),Image.LANCZOS)
            c=c.point(lambda p:255 if p>150 else 0); c=ImageOps.expand(c,20,255); c.save('/tmp/_n.png')
            o=subprocess.run(['tesseract','/tmp/_n.png','-','--psm','7','-c','tessedit_char_whitelist=0123456789'],capture_output=True,text=True).stdout.strip()
            out.append((pi+1,round(s['top'],4),o))
    return out
if __name__=='__main__':
    for nr in map(int,sys.argv[1:]): print(nr,nums(nr))
