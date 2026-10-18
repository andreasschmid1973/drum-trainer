import json, numpy as np, sys
R=json.load(open('ref_fix.json'))
def codes(nr):
    r=R[str(nr)]; bt=np.array(r['beats']); bar=np.array(r['bar']); bi=np.array(r['bi'])
    b=np.load('mmdb_%02d.npy'%nr); mb=b[:,0]; res=[]
    for t,br in zip(bt[bi==0],bar[bi==0]):
        k=np.argmin(abs(mb-t)); res.append((int(br),int(b[k,1]) if abs(mb[k]-t)<0.06 else 0))
    return res
def changepoint(nr,c,after=0):
    cs=codes(nr)
    for q in range(len(cs)-4):
        if cs[q][0]<after: continue
        if all(cs[q+z][1]==c for z in range(4)): return cs[q][0]
def apply(nr,frombar,k):
    r=R[str(nr)]; bt=r['beats']; bar=r['bar']; bi=r['bi']; bn=r['bn']
    i0=[i for i in range(len(bt)) if bar[i]==frombar and bi[i]==0][0]
    # ab dem Umschaltpunkt bekommt jeder Zeitpunkt das Label k Schläge weiter
    if k>0:
        for key in ('bar','bi','bn'): r[key]=r[key][:i0]+r[key][i0+k:]
        r['beats']=r['beats'][:len(r['bar'])]
    else:
        k=-k
        # k Schläge Label einfügen: Zeitpunkte ab i0 bekommen Labels von i0-k
        for key in ('bar','bi','bn'): r[key]=(r[key][:i0]+r[key][i0-k:i0]+r[key][i0:])[:len(r['beats'])]
        # doppelte Labels vermeiden: die eingefügten k Labels gehören zum Takt davor -> Zeit i0.. bekommt (bar,bi) des vorherigen Durchlaufs
    R[str(nr)]=r
if __name__=='__main__':
    todo=json.loads(sys.argv[1])   # [[nr,c,after,k],...]
    for nr,c,after,k in todo:
        cp=changepoint(nr,c,after); print(nr,'code',c,'from bar',cp,'k',k)
        if cp: apply(nr,cp,k)
    json.dump(R,open('ref_fix.json','w'))
