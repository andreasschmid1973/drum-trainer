import numpy as np, json, sys, librosa, os
SR=11025; HOP=55; FR=SR/HOP
CH=json.loads(open('ch.json').read())
def envs(nr):
    fn='envs%02d.npz'%nr
    if os.path.exists(fn): d=np.load(fn); return d['p'],d['m'],d['k'],d['s']
    yp=np.fromfile('s%02d_perc.f32'%nr,dtype=np.float32); ym=np.fromfile('s%02d_mix.f32'%nr,dtype=np.float32)
    def oenv(y): o=librosa.onset.onset_strength(y=y,sr=SR,hop_length=HOP,n_fft=512,lag=1,max_size=1); return o/(o.std()+1e-9)
    S=np.abs(librosa.stft(yp,n_fft=512,hop_length=HOP)); f=librosa.fft_frequencies(sr=SR,n_fft=512); L=np.log1p(100*S)
    def flux(lo,hi):
        m=(f>=lo)&(f<hi); d=np.diff(L[m],axis=1,prepend=L[m][:,:1]); d[d<0]=0; v=d.sum(0); v=v-np.convolve(v,np.ones(81)/81,'same'); v[v<0]=0; return v/(v.std()+1e-9)
    p,m,k,s=oenv(yp),oenv(ym),flux(30,150),flux(1500,5500)
    np.savez(fn,p=p,m=m,k=k,s=s); return p,m,k,s
BIAS=0.010  # Messfehler der librosa-Hüllkurve (kalibriert)
def drumbar(nr,bar):
    c=CH.get(str(nr))
    if not c: return True
    if bar<c['g']: return False
    for a,n in c.get('mr',[]):
        if a<=bar<a+n: return False
    return True
def refine(nr,res,W=0.15,step=0.005,alpha=2500.0):
    p,m,k,s=envs(nr); bt=np.array(res['beats']); bar=np.array(res['bar'])
    N=len(bt); offs=np.arange(-W,W+1e-9,step); C=len(offs)
    dr=np.array([drumbar(nr,b) for b in bar])
    mm=np.load('mmact_%02d.npy'%nr); mb=mm[:,0]+mm[:,1]
    def em(i):
        t=bt[i]+offs+BIAS; idx=np.round(t*FR).astype(int); v=np.zeros(C); ok=(idx>=1)&(idx<len(p)-1)
        e=p if dr[i] else 0.6*m+0.4*p
        v[ok]=np.maximum(np.maximum(e[idx[ok]-1],e[idx[ok]]),e[idx[ok]+1])
        j=np.round((bt[i]+offs)*100).astype(int); okb=(j>=0)&(j<len(mb)); w=np.zeros(C); w[okb]=mb[j[okb]]
        return v+4.0*w
    E=np.array([em(i) for i in range(N)])
    # erwarteter Schlagabstand: geglättete IOIs des Ausgangsrasters
    ioi=np.diff(bt); ioi_s=np.array([np.median(ioi[max(0,i-4):i+5]) for i in range(len(ioi))])
    score=E[0].copy(); back=np.zeros((N,C),dtype=int)
    for i in range(1,N):
        prev=bt[i-1]+offs; cur=bt[i]+offs
        d=cur[None,:]-prev[:,None]; d=np.maximum(d,1e-3)
        pen=alpha*np.log(d/ioi_s[i-1])**2
        tot=score[:,None]-pen
        back[i]=np.argmax(tot,0); score=tot[back[i],np.arange(C)]+E[i]
    path=np.zeros(N,dtype=int); path[-1]=np.argmax(score)
    for i in range(N-1,0,-1): path[i-1]=back[i,path[i]]
    nb=bt+offs[path]
    return nb, offs[path], dr
if __name__=='__main__':
    which=sys.argv[1]; R=json.load(open('res_%s.json'%which)); out={}
    for nr in range(1,30):
        r=R[str(nr)]; nb,sh,dr=refine(nr,r)
        r2=dict(r); r2['beats']=[round(float(x),4) for x in nb]; out[nr]=r2
        print(nr,'shift med %+.0f ms  range %+.0f..%+.0f'%(1000*np.median(sh[dr]),1000*sh.min(),1000*sh.max()), 'at limit',int(np.sum(np.abs(sh)>=0.145)))
    json.dump(out,open('ref_%s.json'%which,'w'))
