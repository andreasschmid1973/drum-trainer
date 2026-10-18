import numpy as np, librosa, json, sys
def env(nr):
    x=np.fromfile('s%02d_perc.f32'%nr,dtype=np.float32); sr=11025
    o=librosa.onset.onset_strength(y=x,sr=sr,hop_length=55); return o/np.percentile(o,99), sr/55
def locoff(nr,beats,win=8,rng=0.25):
    o,fr=env(nr); out=[]
    for s in range(0,len(beats)-win,win):
        b=np.array(beats[s:s+win])
        if b[0]<0: continue
        best=(-1,0)
        for d in np.arange(-rng,rng+1e-9,0.005):
            f=np.round((b+d)*fr).astype(int); f=f[(f>1)&(f<len(o)-2)]
            v=sum(o[j-1:j+2].max() for j in f)/max(1,len(f))
            best=max(best,(v,d))
        f=np.round(b*fr).astype(int); f=f[(f>1)&(f<len(o)-2)]; v0=sum(o[j-1:j+2].max() for j in f)/max(1,len(f))
        out.append((b[0],best[1],best[0],v0))
    return out
if __name__=='__main__':
    nr=int(sys.argv[1]); R=json.load(open(sys.argv[2] if len(sys.argv)>2 else 'final5.json'))[str(nr)]
    for b0,d,v,v0 in locoff(nr,R['beats']): print('%7.2f %+6.3f  %.2f vs %.2f'%(b0,d,v,v0))
