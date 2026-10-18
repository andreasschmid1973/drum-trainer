import numpy as np, json, sys, librosa, pickle, os
SR=11025
def env(nr):
    fn='env%02d.npy'%nr
    if os.path.exists(fn): return np.load(fn)
    y=np.fromfile('s%02d_perc.f32'%nr,dtype=np.float32)
    o=librosa.onset.onset_strength(y=y,sr=SR,hop_length=55,n_fft=512,lag=1,max_size=1)
    o=o/(o.std()+1e-9); np.save(fn,o); return o
FR=SR/55; LAG=0  # onset_strength frames are centered
def quality(nr,res):
    o=env(nr); bt=np.array(res['beats']); bar=np.array(res['bar']); bi=np.array(res['bi'])
    def val(t): 
        i=np.round(t*FR).astype(int); i=i[(i>=0)&(i<len(o))]
        return o[i]
    def mx(t,w=4):
        i=np.round(t*FR).astype(int); r=[]
        for q in i:
            if 0<=q<len(o): r.append(o[max(0,q-w):q+w+1].max())
        return np.array(r)
    # per 2-bar window: best shift
    db=np.where(bi==0)[0]; shifts=[]; bars=[]
    for q in range(0,len(db)-2,2):
        a,b=db[q],db[q+2]; ts=bt[a:b]
        if ts[0]<0: continue
        best=None
        for d in np.arange(-0.12,0.1201,0.005):
            v=mx(ts+d,1).mean()
            if best is None or v>best[0]: best=(v,d)
        base=mx(ts,1).mean(); off=mx(ts+0.5*np.median(np.diff(ts)),1).mean()
        shifts.append((bar[a],best[1],base,off))
    S=np.array(shifts)
    good=np.mean(np.abs(S[:,1])<=0.02); onb=np.mean(S[:,2]); offb=np.mean(S[:,3])
    return good,onb,offb,S
if __name__=='__main__':
    which=sys.argv[1]; R=json.load(open('res_%s.json'%which))
    for nr in range(1,30):
        g,on,off,S=quality(nr,R[str(nr)])
        bad=[ (int(b),round(d*1000)) for b,d,_,_ in S if abs(d)>0.02]
        print('%2d good %.0f%% on %.2f off %.2f'%(nr,100*g,on,off), 'bad bars:',bad[:12], '...' if len(bad)>12 else '')
