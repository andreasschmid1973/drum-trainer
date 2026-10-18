import json, numpy as np, sys
import sys as _s; R=json.load(open(_s.argv[1])); CH=json.load(open('ch.json'))
for nr in [int(x) for x in sys.argv[2:]] or range(1,30):
    if str(nr) not in CH: continue
    g=CH[str(nr)]['g']; r=R[str(nr)]; bt=np.array(r['beats']); bar=np.array(r['bar']); bi=np.array(r['bi'])
    d=np.load('b22_%02d.npz'%nr); fr=float(d['fr']); e=np.load('hf_%02d.npy'%nr)
    act=d['kick']+d['hat']
    row=[]
    for b in range(g-3,g+3):
        idx=np.where(bar==b)[0]
        if not len(idx): row.append('  –  '); continue
        cells=[]
        for i in idx:
            t=bt[i]; 
            if t<0: cells.append(' . '); continue
            a=act[int(t*fr)-2:int(t*fr)+3].max() if t*fr>2 else 0
            f=int(t*100); cr=(np.median(e[f+15:f+50])-np.median(e[f-25:f-3])) if f>25 else 0
            cells.append(('C' if cr>9 else ('*' if a>8 else ('+' if a>4 else '.'))))
        row.append('%d:%s'%(b,''.join(cells)))
    print('%2d g=%-3d %s   t(g)=%.2f'%(nr,g,'  '.join(row),bt[np.where((bar==g)&(bi==0))[0][0]]))
