import json, numpy as np, sys
from refine import drumbar
R=json.load(open('ref_perc.json')); CH=json.load(open('ch.json'))
def B(nr):
    d=np.load('b22_%02d.npz'%nr); return d['kick'],0.5*(d['snb']+d['snh']),d['hat'],float(d['fr'])
def pk(v,t,fr,w=2):
    i=int(round(t*fr)); return v[max(0,i-w):i+w+1].max() if 0<i<len(v)-1 else 0
res={}
for nr in range(1,30):
    r=R[str(nr)]; k,s,h,fr=B(nr); bt=np.array(r['beats']); bar=np.array(r['bar']); bi=np.array(r['bi']); bn=np.array(r['bn'])
    g=CH[str(nr)]['g'] if str(nr) in CH else None
    idx=[i for i in range(len(bt)) if drumbar(nr,bar[i]) and bt[i]>0 and bn[i]==4]
    sc=[]
    for kk in range(4):
        pos=[(bi[i]-kk)%4 for i in idx]
        sn=np.array([pk(s,bt[i],fr)+pk(h,bt[i],fr) for i in idx]); ki=np.array([pk(k,bt[i],fr) for i in idx]); pos=np.array(pos)
        back=sn[(pos==1)|(pos==3)].mean()-sn[(pos==0)|(pos==2)].mean()
        kick=ki[(pos==0)].mean()-ki[(pos==1)|(pos==3)].mean()
        sc.append((back,kick))
    # Einsatz: Becken+Kick am Groove-Beginn für Verschiebung kk
    gi=[i for i in range(len(bt)) if g and bar[i]==g and bi[i]==0]
    ent=[]
    for kk in range(4):
        if not gi: ent.append(0); continue
        j=gi[0]+kk; ent.append(pk(h,bt[j],fr,3)+pk(k,bt[j],fr,3) if j<len(bt) else 0)
    res[nr]=dict(sc=sc,ent=ent)
    print('%2d '%nr+'  '.join('k%d: back %+.1f kick %+.1f ent %.1f'%(kk,sc[kk][0],sc[kk][1],ent[kk]) for kk in range(4)))
json.dump(res,open('down.json','w'))
