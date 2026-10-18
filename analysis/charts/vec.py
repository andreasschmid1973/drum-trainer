import pymupdf, numpy as np, json, glob, os, re, sys
from lay import longest_run
def sys_images(pdf):
    doc=pymupdf.open(pdf); out=[]
    for pno,p in enumerate(doc):
        W,H=p.rect.width,p.rect.height; items=[]
        for info in p.get_image_info(xrefs=True):
            x0,y0,x1,y1=info['bbox']
            if (x1-x0)<0.3*W: continue
            pix=pymupdf.Pixmap(doc,info['xref'])
            if pix.n-pix.alpha>=3: pix=pymupdf.Pixmap(pymupdf.csGRAY,pix)
            arr=np.frombuffer(pix.samples,dtype=np.uint8).reshape(pix.height,pix.width,pix.n)[:,:,0]
            items.append({'bbox':(x0/W,y0/H,x1/W,y1/H),'img':arr})
        items.sort(key=lambda d:d['bbox'][1]); out.append(items)
    return out
def analyse(arr):
    a=arr<200; H,W=a.shape
    rows=[(r,)+tuple(longest_run(a[r])) for r in range(H)]
    cand=[(r,L,x0,x1) for r,L,x0,x1 in rows if L>0.10*W]
    lines=[]
    for r,L,x0,x1 in cand:
        if lines and r-lines[-1]['r'][-1]<=1 and len(lines[-1]['r'])<4: lines[-1]['r'].append(r)
        else: lines.append({'r':[r],'x0':x0,'x1':x1,'L':L})
    for l in lines: l['y']=np.mean(l['r'])
    best=None
    for i in range(len(lines)):
        for j in range(i+1,min(len(lines),i+6)):
            sp=lines[j]['y']-lines[i]['y']
            if sp<6: continue
            grp=[i,j]
            for k in range(3):
                s2=(lines[grp[-1]]['y']-lines[grp[0]]['y'])/(len(grp)-1); want=lines[grp[-1]]['y']+s2; hit=None
                for q in range(grp[-1]+1,min(len(lines),grp[-1]+6)):
                    if abs(lines[q]['y']-want)<=max(2.0,0.12*s2) and min(lines[q]['L'],lines[i]['L'])>0.8*max(lines[q]['L'],lines[i]['L']): hit=q; break
                if hit is None: break
                grp.append(hit)
            if len(grp)==5 and (best is None or lines[grp[0]]['L']>lines[best[0]]['L']): best=grp
    if not best: return None
    g=best; t=int(round(lines[g[0]]['y'])); b=int(round(lines[g[4]]['y'])); x0=lines[g[0]]['x0']; x1=lines[g[0]]['x1']
    sp=(b-t)/4
    full=a[t:b+1,:].mean(0)>0.96
    pad=max(2,int(sp*0.35))
    above=a[max(0,t-pad):t-1,:].any(0); below=a[b+2:b+pad+1,:].any(0)
    cols=[c for c in np.where(full&~above&~below)[0] if x0-3<=c<=x1+3]
    bl=[]
    for c in cols:
        if bl and c-bl[-1][-1]<=2: bl[-1].append(c)
        else: bl.append([c])
    xs=[]
    for grp in bl:
        c=(min(grp)+max(grp))/2
        if xs and c-xs[-1]<0.012*W: continue
        xs.append(c)
    if not xs or xs[0]-x0>0.02*W: xs=[x0]+xs
    if x1-xs[-1]>0.02*W: xs=xs+[x1]
    return {'t':t/H,'b':b/H,'xs':[x/W for x in xs]}
if __name__=='__main__':
    CH=json.load(open('../real/ch.json'))
    src=glob.glob('/root/.claude/uploads/72854ad5-2428-5137-b45d-fab1076e08d6/*.pdf')+['/mnt/user-data/uploads/BlackRockForest/charts/29 JOKER AND THE THIEF Wolfmother .pdf']
    def nr_of(f):
        b=os.path.basename(f); m=re.match(r'[0-9a-f]{8}-(\d+)_',b) or re.match(r'(\d+) ',b); return int(m.group(1))
    def nslots(c):
        n=0; b=1
        while b<=c['end']:
            m=1
            for a,k in c.get('mr',[]):
                if a==b: m=k
            n+=1; b+=m
        return n
    RES={}
    for f in sorted(src,key=nr_of):
        nr=nr_of(f); pages=sys_images(f); P=[]
        for items in pages:
            row=[]
            for it in items:
                r=analyse(it['img'])
                x0,y0,x1,y1=it['bbox']
                if r is None: row.append({'bbox':it['bbox'],'xs':None}); continue
                row.append({'bbox':it['bbox'],'t':y0+r['t']*(y1-y0),'b':y0+r['b']*(y1-y0),'xs':[x0+x*(x1-x0) for x in r['xs']]})
            P.append(row)
        det=sum(len(s['xs'])-1 for p in P for s in p if s['xs']); miss=sum(1 for p in P for s in p if not s['xs'])
        exp=nslots(CH[str(nr)]); RES[nr]=P
        print('#%2d erkannt %3d erwartet %3d %s  (Systeme ohne Notenlinien: %d)  pro Seite %s'%(nr,det,exp,'OK' if det==exp else 'diff %+d'%(det-exp),miss,[sum(len(s['xs'])-1 for s in p if s['xs']) for p in P]),flush=True)
    json.dump(RES,open('vec.json','w'))
