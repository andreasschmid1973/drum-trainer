import json, numpy as np, sys
from refine import drumbar
import sys as _s; R=json.load(open(_s.argv[1] if _s.argv[1].endswith('.json') else 'ref_fix.json'))
for nr in [int(x) for x in sys.argv[1:] if not x.endswith('.json')]:
    r=R[str(nr)]; bt=np.array(r['beats']); bar=np.array(r['bar']); bi=np.array(r['bi']); bn=np.array(r['bn'])
    b=np.load('mmdb_%02d.npy'%nr); mb=b[:,0]
    line=[]
    for t,br in zip(bt[(bi==0)],bar[(bi==0)]):
        if t<0: continue
        k=np.argmin(abs(mb-t)); d=mb[k]-t
        c='.' if abs(d)>0.06 else str(int(b[k,1]))
        if not drumbar(nr,br): c=c if c=='.' else c.lower()
        line.append(c)
    s=''.join(line); print('#%d (Takt 1 ab links, 1 Zeichen pro Takt; Zahl = madmom-Schlag auf unserer Eins)'%nr)
    for i in range(0,len(s),50): print('  %4d %s'%(bar[(bi==0)&(bt>=0)][i],s[i:i+50]))
