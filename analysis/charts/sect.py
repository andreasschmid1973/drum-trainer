import json, glob, subprocess, re
from PIL import Image
L=json.load(open('layout.json'))
VOC=['intro','verse','chorus','pre-chorus','prechorus','bridge','solo','outro','break','interlude','intelude','theme','main','riff','harmonica','fade','out','guitar','pre-verse','pre-solo','pre','instrumental','breakdown','coda','ending','end','interlude','post-chorus']
OUT={}
for nr in sorted(L,key=int):
    pages=L[nr]; secs=[]
    pngs=sorted(glob.glob('s%02d-*.png'%int(nr)),key=lambda f:int(f.split('-')[-1].split('.')[0]))
    for pi,png in enumerate(pngs):
        if pi>=len(pages): break
        im=Image.open(png); W,H=im.size
        tsv=subprocess.run(['tesseract',png,'-','--psm','11','tsv'],capture_output=True,text=True).stdout
        words=[]
        for line in tsv.splitlines()[1:]:
            p=line.split('\t')
            if len(p)<12 or not p[11].strip(): continue
            w=p[11].strip(); 
            words.append((int(p[6])/W,int(p[7])/H,int(p[8])/W,int(p[9])/H,w,float(p[10])))
        # Zeilen bilden
        words.sort(key=lambda w:(round(w[1]*200),w[0]))
        used=set()
        for i,w in enumerate(words):
            if i in used: continue
            base=re.sub(r'[^a-z\-]','',w[4].lower())
            if base not in VOC or w[5]<40: continue
            if w[1]<0.06: continue  # Kopfzeile
            label=[w[4]]; x1=w[0]+w[2]; used.add(i)
            for j,v in enumerate(words):
                if j in used or j==i: continue
                if abs(v[1]-w[1])<0.008 and 0<=v[0]-x1<0.03:
                    t=v[4]
                    if re.fullmatch(r'[A-Za-z\-]+|\d',t): label.append(t); x1=v[0]+v[2]; used.add(j)
            lab=' '.join(label); lab=re.sub(r'(?i)intelude','Interlude',lab)
            cx=w[0]; cy=w[1]+w[3]
            # Takt: System direkt unter dem Label, Takt mit x0 <= cx+0.02
            rows=[r for r in pages[pi] if r[4]>cy-0.005 and r[4]-cy<0.06]
            if not rows: continue
            y=min(r[4] for r in rows); rows=[r for r in rows if abs(r[4]-y)<0.003]
            mid=(cx+x1)/2; r=min(rows,key=lambda r:abs(r[2]-mid))
            secs.append((r[0],lab))
    secs=sorted(set(secs))
    OUT[nr]=secs; print(nr,secs)
json.dump(OUT,open('sections.json','w'))
