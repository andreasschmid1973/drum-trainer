import json, numpy as np
R=json.load(open('ref_fix.json')); CH=json.load(open('ch.json'))
for nr in range(1,30):
    r=R[str(nr)]; bt=np.array(r['beats']); bar=np.array(r['bar']); bi=np.array(r['bi'])
    p=np.load('envs%02d.npz'%nr)['p']; fr=11025/55
    thr=np.percentile(p,99.0); idx=np.where(p>thr)[0]; t=idx[-1]/fr
    k=np.argmin(abs(bt-t)); 
    endbar=CH[str(nr)]['end'] if str(nr) in CH else None
    mr=[m for m in CH.get(str(nr),{}).get('mr',[]) if m[0]+m[1]-1>=(endbar or 0)]
    print('%2d last strong hit %.1fs -> our bar %d beat %d (+%.2fs)   chart end %s %s  audio len %.1f'%(nr,t,bar[k],bi[k]+1,t-bt[k],endbar,('(rest '+str(mr)+')') if mr else '',len(p)/fr))
