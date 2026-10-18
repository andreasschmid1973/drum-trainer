import json, numpy as np, sys
R=json.load(open('ref_fix.json')); CH=json.load(open('ch.json'))
def strip(nr,band='kick'):
    r=R[str(nr)]; bt=np.array(r['beats']); bar=np.array(r['bar'])
    d=np.load('b22_%02d.npz'%nr); fr=float(d['fr']); v=d[band] if band!='snare' else 0.5*(d['snb']+d['snh'])
    vals={}
    for b in sorted(set(bar)):
        idx=np.where(bar==b)[0]
        if bt[idx[0]]<0 or len(idx)<2: continue
        t0=bt[idx[0]]; t1=bt[idx[-1]]+(bt[idx[-1]]-bt[idx[-2]])
        seg=v[int(t0*fr):int(t1*fr)]; vals[b]=np.sort(seg)[-6:].mean() if len(seg)>6 else 0
    return vals
for nr in [int(x) for x in sys.argv[1:]]:
    c=CH.get(str(nr)); vk=strip(nr); 
    ref=np.median(list(vk.values()))
    bars=sorted(vk); line=''; exp=''
    for b in bars:
        x=vk[b]/ref; line+=str(min(9,int(round(x*5))))
        e='?'
        if c:
            e='-' if b<c['g']-1 else ('p' if b==c['g']-1 else 'X')
            for a,n in c.get('mr',[]):
                if a<=b<a+n: e='-'
            if b>c['end']: e=' '
        exp+=e
    print('#%d  first bar %d'%(nr,bars[0]))
    for i in range(0,len(line),60): print('   bar %4d  kick %s\n              chart %s'%(bars[i],line[i:i+60],exp[i:i+60]))
