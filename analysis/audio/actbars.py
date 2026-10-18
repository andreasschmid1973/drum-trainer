import json, numpy as np, sys
R=json.load(open('ref_fix.json'))
nr=int(sys.argv[1]); b0,b1=int(sys.argv[2]),int(sys.argv[3])
r=R[str(nr)]; bt=np.array(r['beats']); bar=np.array(r['bar']); bi=np.array(r['bi'])
d=np.load('b22_%02d.npz'%nr); fr=float(d['fr'])
for b in range(b0,b1+1):
    idx=np.where(bar==b)[0]
    if not len(idx) or bt[idx[0]]<0: continue
    t0=bt[idx[0]]; t1=bt[idx[-1]]+(bt[idx[-1]]-bt[idx[-2]] if len(idx)>1 else 1)
    seg=lambda v: v[int(t0*fr):int(t1*fr)]
    k=np.sort(seg(d['kick']))[-6:].mean(); s=np.sort(seg(d['snb']))[-6:].mean(); h=np.sort(seg(d['hat']))[-6:].mean()
    print('#%d bar %3d %6.1fs  kick %4.1f %s  snare %4.1f %s  hat %4.1f %s'%(nr,b,t0,k,'#'*int(k),s,'#'*int(s),h,'#'*int(h)))
