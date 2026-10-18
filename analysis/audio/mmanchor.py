import json, numpy as np, sys
R=json.load(open('ref_fix.json')); over=json.load(open('over.json')); CH=json.load(open('ch.json'))
for nr in sys.argv[1:]:
    r=R[nr]; bt=np.array(r['beats']); bar=np.array(r['bar']); bi=np.array(r['bi']); g=CH[nr]['g']
    j=int(np.where((bar==g)&(bi==0))[0][0]); t=bt[j]
    b=np.load('mmdb_%02d.npy'%int(nr)); md=b[b[:,1]==1][:,0]
    # erste madmom-Takt-Eins der folgenden 8 Takte, die zur Rasterlage passt
    m=md[np.argmin(abs(md-t))]
    print(nr,'our g at',round(t,3),'madmom downbeat',round(m,3))
    over[nr]={'gT':float(m)-0.0116,'s':r['scale']}
json.dump(over,open('over.json','w'))
