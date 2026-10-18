import json, numpy as np, sys
from refine import drumbar
R=json.load(open('ref_fix.json'))
def pk(v,t,fr,w=2):
    i=int(round(t*fr)); return v[max(0,i-w):i+w+1].max() if 0<i<len(v)-1 else 0
for nr in [int(x) for x in sys.argv[1:]]:
    r=R[str(nr)]; bt=np.array(r['beats']); bar=np.array(r['bar']); bi=np.array(r['bi']); bn=np.array(r['bn'])
    d=np.load('b22_%02d.npz'%nr); fr=float(d['fr']); sn=0.5*(d['snb']+d['snh'])+d['hat']; kk=d['kick']
    a=np.load('mmact_%02d.npy'%nr); down=a[:,1]
    out=[]
    for b0 in range(int(bar.min()),int(bar.max())+1,8):
        idx=[i for i in range(len(bt)) if b0<=bar[i]<b0+8 and bn[i]==4 and bt[i]>0 and drumbar(nr,bar[i])]
        if len(idx)<12: out.append('   ·  '); continue
        pos=bi[idx]; s=np.array([pk(sn,bt[i],fr) for i in idx]); dd=np.array([pk(down,bt[i],100) for i in idx])
        back=s[(pos%2)==1].mean()-s[(pos%2)==0].mean()
        dpos=int(np.argmax([dd[pos==q].mean() if np.any(pos==q) else 0 for q in range(4)]))
        out.append('%+4.1f/%d'%(back,dpos))
    print('#%d  Takt-8er-Blöcke: Backbeat(+ = Snare auf 2&4) / madmom-Eins-Position'%nr)
    print('   '+' '.join(out))
