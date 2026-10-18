import numpy as np, subprocess, glob, os, re, json, sys
from PIL import Image, ImageDraw
DPI=150
MODE='blob'
FOUR=True
FULL=0.90
def render(pdf,tag):
    subprocess.run(['pdftoppm','-r',str(DPI),'-gray','-png',pdf,tag],check=True)
    return sorted(glob.glob(tag+'-*.png'))
def longest_run(row):
    if not row.any(): return 0,0,0
    d=np.diff(np.concatenate([[0],row.astype(np.int8),[0]])); st=np.where(d==1)[0]; en=np.where(d==-1)[0]
    k=np.argmax(en-st); return en[k]-st[k],st[k],en[k]
def systems(img):
    g=np.array(img.convert('L')); a=g<190; H,W=a.shape
    al=g<235
    cand=[]
    for r in range(H):
        L,x0,x1=longest_run(al[r])
        if L>0.05*W: cand.append((r,x0,x1))
    lines=[]
    for r,x0,x1 in cand:
        if lines and r-lines[-1]['r'][-1]<=1 and len(lines[-1]['r'])<3: lines[-1]['r'].append(r); lines[-1]['x0']=min(lines[-1]['x0'],x0); lines[-1]['x1']=max(lines[-1]['x1'],x1)
        else: lines.append({'r':[r],'x0':x0,'x1':x1})
    for l in lines: l['y']=np.mean(l['r'])
    used=set(); staves=[]
    for i in range(len(lines)):
        if i in used: continue
        for j in range(i+1,min(len(lines),i+6)):
            sp=lines[j]['y']-lines[i]['y']
            if sp<5 or sp>18: continue
            grp=[i,j]; 
            for k in range(3):
                sp2=(lines[grp[-1]]['y']-lines[grp[0]]['y'])/(len(grp)-1); want=lines[grp[-1]]['y']+sp2; hit=None
                for q in range(grp[-1]+1,min(len(lines),grp[-1]+6)):
                    Lq=lines[q]['x1']-lines[q]['x0']; Li=lines[i]['x1']-lines[i]['x0']
                    if abs(lines[q]['y']-want)<=2.6 and abs(lines[q]['x0']-lines[i]['x0'])<0.06*W and min(Lq,Li)>0.75*max(Lq,Li): hit=q; break
                if hit is None: break
                grp.append(hit)
            if len(grp)==5:
                staves.append(grp); used.update(grp); break
            if len(grp)==4 and FOUR:
                # Bildstreifen-Grenze kann eine Notenlinie verschlucken: fünfte Linie ergänzen
                sp4=(lines[grp[3]]['y']-lines[grp[0]]['y'])/3
                fake={'r':[int(round(lines[grp[3]]['y']+sp4))],'x0':lines[grp[0]]['x0'],'x1':lines[grp[0]]['x1'],'y':lines[grp[3]]['y']+sp4}
                lines.append(fake); grp.append(len(lines)-1)
                staves.append(grp); used.update(grp); break
    out=[]
    for g in staves:
        t=int(round(lines[g[0]]['y'])); b=int(round(lines[g[4]]['y'])); x0=lines[g[0]]['x0']; x1=lines[g[0]]['x1']
        staffrows=set()
        for q in g: staffrows.update(lines[q]['r'])
        inner=[r for r in range(t+1,b) if r not in staffrows and r-1 not in staffrows and r+1 not in staffrows]
        seg=a[t:b+1,:]; full=seg.mean(0)>FULL
        above=a[t-4:t-1,:].any(0); below=a[b+2:b+5,:].any(0)
        cols=[c for c in np.where(full&~above&~below)[0] if x0-3<=c<=x1+3]
        bl=[]
        for c in cols:
            if bl and c-bl[-1][-1]<=2: bl[-1].append(c)
            else: bl.append([c])
        bx=[]
        for grp in bl:
            c0,c1=min(grp),max(grp)
            if c1-c0>8: continue
            # Nachbarschaft: neben einem Taktstrich ist es (bis auf Notenlinien) weitgehend leer
            # An den Enden eines Notenhalses sitzt ein Notenkopf; an einem Taktstrich nur die Notenlinie
            sp=(b-t)/4.0
            ends=[r for r in list(range(t+2,int(t+sp*0.8)))+list(range(int(b-sp*0.8),b-1)) if r not in staffrows]
            if ends and MODE=='blob':
                cols_n=list(range(max(0,c0-7),max(0,c0-2)))+list(range(c1+3,min(a.shape[1],c1+8)))
                blob=a[np.ix_(ends,cols_n)].mean()
                if blob>0.18: continue
            bx.append((c0+c1)/2)
        # Systemanfang/-ende ergänzen, falls nicht erkannt
        if not bx or bx[0]-x0>0.02*W: bx=[x0]+bx
        if x1-bx[-1]>0.02*W: bx=bx+[x1]
        out.append({'top':t/H,'bot':b/H,'x0':x0/W,'x1':x1/W,'bars':[x/W for x in bx],'w':[]})
    out.sort(key=lambda s:s['top'])
    return out
if __name__=='__main__':
    pdf=sys.argv[1]; tag=sys.argv[2]
    pages=render(pdf,tag)
    for p in pages[:1]:
        im=Image.open(p); S=systems(im); W,H=im.size
        d=ImageDraw.Draw(im.convert('RGB')); im2=im.convert('RGB'); d=ImageDraw.Draw(im2)
        for s in S:
            d.rectangle([s['x0']*W,s['top']*H,s['x1']*W,s['bot']*H],outline=(0,160,255))
            for x in s['bars']: d.line([x*W,s['top']*H-6,x*W,s['bot']*H+6],fill=(255,0,0),width=2)
            print(len(s['bars']),[round(x,3) for x in s['bars']], s['w'])
        im2.save(tag+'_dbg.png')
