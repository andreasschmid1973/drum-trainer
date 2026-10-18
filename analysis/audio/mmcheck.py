import json, numpy as np, sys
from refine import drumbar
R=json.load(open(sys.argv[1] if len(sys.argv)>1 else 'ref_perc.json'))
def pk(v,t,w=2):
    i=int(round(t*100)); return v[max(0,i-w):i+w+1].max() if 0<=i<len(v) else 0
for nr in range(1,30):
    a=np.load('mmact_%02d.npy'%nr); beat=a[:,0]+a[:,1]; down=a[:,1]
    r=R[str(nr)]; bt=np.array(r['beats']); bar=np.array(r['bar']); bi=np.array(r['bi']); bn=np.array(r['bn'])
    on=[];off=[]; dp={}
    for i in range(len(bt)-1):
        if bt[i]<0.3: continue
        d=bt[i+1]-bt[i]; on.append(pk(beat,bt[i])); off.append(pk(beat,bt[i]+d/2))
        key=(bn[i],bi[i]); dp.setdefault(key,[]).append(pk(down,bt[i]))
    main=max(set(k[0] for k in dp),key=lambda n: sum(len(v) for k,v in dp.items() if k[0]==n))
    prof=[np.mean(dp[(main,q)]) for q in range(main) if (main,q) in dp]
    print('%2d beat on %.2f off %.2f | downbeat-act by pos (n=%d): %s -> %d'%(nr,np.mean(on),np.mean(off),main,' '.join('%.2f'%x for x in prof),int(np.argmax(prof))))
