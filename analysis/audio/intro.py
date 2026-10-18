import json, numpy as np
import remap as RM
def score(ts,act):
    v=[act[max(0,int(round(t*100))-2):int(round(t*100))+3].max() for t in ts if 0<t*100<len(act)-3]
    return np.mean(v) if v else 0
out={}
for nr in range(1,30):
    o=RM.remap(nr)
    if o is None: continue
    new,rel,x,st=o; r=RM.R[str(nr)]; old=np.array(r['beats']); bar=np.array(r['bar'])
    a=np.load('mmact_%02d.npy'%nr); act=a[:,0]+a[:,1]
    first=np.where(rel)[0][0]
    if first<4: continue
    seg=slice(0,first); sel=old[seg]>0.2
    so=score(old[seg][sel],act); sn=score(new[seg][sel],act)
    io=np.diff(old[seg]); jit=np.std(io)/np.mean(io)
    sh=np.abs(new[seg]-old[seg]).max()
    out[nr]='old' if so>sn+0.03 else 'new'
    print('#%2d Intro %d Schläge bis Takt %d: madmom-Treffer alt %.2f neu %.2f  Gleichmaß alt %.3f  max Abw %.2fs -> %s'%(nr,first,bar[first],so,sn,jit,sh,out[nr]))
json.dump(out,open('intro_choice.json','w'))
