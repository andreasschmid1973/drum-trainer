import json, numpy as np, sys
from chartbeats import chart_labels
R=json.load(open('ref_fix.json'))
def build(nr,A_bar,shift_beats=0,at=None):
    r=R[str(nr)]; bt=np.array(r['beats']); bar=np.array(r['bar']); bi=np.array(r['bi'])
    mb=np.load('mmdb_%02d.npy'%nr)[:,0]
    if at is None:
        i=int(np.where((bar==A_bar)&(bi==0))[0][0]); t=bt[i]
    else: t=at
    k=int(np.argmin(abs(mb-t)))+shift_beats
    keep=[q for q in range(len(bt)) if bt[q]<mb[k]-0.05]
    labs=chart_labels(nr,A_bar,len(mb)-k)
    r['beats']=[float(bt[q]) for q in keep]+[float(x) for x in mb[k:]]
    r['bar']=[int(bar[q]) for q in keep]+[l[0] for l in labs]
    r['bi']=[int(bi[q]) for q in keep]+[l[1] for l in labs]
    r['bn']=[int(r['bn'][q]) for q in keep]+[l[2] for l in labs]
    R[str(nr)]=r
    print(nr,'from bar',A_bar,'at',round(mb[k],3),'(ours',round(t,3),')')
if __name__=='__main__':
    for spec in json.loads(sys.argv[1]): build(*spec)
    json.dump(R,open('ref_fix.json','w'))
