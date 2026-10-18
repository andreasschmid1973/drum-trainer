import json, glob, re, os, numpy as np
from PIL import Image
from lay import render, systems
CH=json.load(open('../real/ch.json'))
src=glob.glob('/root/.claude/uploads/72854ad5-2428-5137-b45d-fab1076e08d6/*.pdf')+['/mnt/user-data/uploads/BlackRockForest/charts/29 JOKER AND THE THIEF Wolfmother .pdf']
def nr_of(f):
    b=os.path.basename(f); m=re.match(r'[0-9a-f]{8}-(\d+)_',b) or re.match(r'(\d+) ',b); return int(m.group(1))
def slot(c,x):
    v=x-1
    for a,n in c.get('mr',[]):
        if x>=a+n: v-=(n-1)
        elif x>a: v-=(x-a)*(1-1/n)
    return v
LAY={}; report=[]
for f in sorted(src,key=nr_of):
    nr=nr_of(f); c=CH[str(nr)]; tag='s%02d'%nr
    for old in glob.glob(tag+'-*.png'): os.remove(old)
    pages=render(f,tag); P=c['pg']; ok=True; pl=[]
    # Takt-Slots (Mehrtaktpausen = 1 Slot) in Reihenfolge
    slots=[]; b=1
    while b<=c['end']:
        n=1
        for a,m in c.get('mr',[]):
            if a==b: n=m
        slots.append((b,n)); b+=n
    si=0
    for p,png in enumerate(pages):
        S=systems(Image.open(png))
        first=P[p]; nxt=P[p+1] if p+1<len(P) else c['end']+1
        exp=sum(1 for s in slots if first<=s[0]<nxt)
        sysl=[]; det=0
        for s in S:
            xs=[]
            for x in s['bars']:
                if xs and x-xs[-1]<0.012: continue
                xs.append(x)
            if len(xs)<2: continue
            sysl.append({'y0':s['top'],'y1':s['bot'],'xs':xs}); det+=len(xs)-1
        if det!=exp: ok=False; report.append('#%d S.%d erwartet %d Takte, erkannt %d'%(nr,p+1,exp,det))
        rows=[]
        for s in sysl:
            for k in range(len(s['xs'])-1):
                if si>=len(slots): break
                b0,n=slots[si]; si+=1
                rows.append([b0,n,round(s['xs'][k],4),round(s['xs'][k+1],4),round(s['y0'],4),round(s['y1'],4)])
        pl.append(rows)
        si=sum(1 for s in slots if s[0]<nxt)  # bei Abweichung an der nächsten Seite neu aufsetzen
    LAY[nr]={'ok':ok,'pages':pl}
    print(nr,'ok' if ok else 'ABWEICHUNG',flush=True)
json.dump(LAY,open('layout.json','w'))
print('\n'.join(report))
