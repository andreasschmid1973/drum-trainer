import numpy as np, json, sys, librosa
from PIL import Image, ImageDraw
SR=11025
def bands(nr):
    y=np.fromfile('s%02d_perc.f32'%nr,dtype=np.float32)
    S=np.abs(librosa.stft(y,n_fft=512,hop_length=55))  # 5ms
    fr=SR/55; f=librosa.fft_frequencies(sr=SR,n_fft=512)
    L=np.log1p(100*S)
    def flux(lo,hi):
        m=(f>=lo)&(f<hi); d=np.diff(L[m],axis=1); d[d<0]=0; v=d.sum(0); v=np.concatenate([[0],v]); 
        v=v-np.convolve(v,np.ones(81)/81,'same'); v[v<0]=0; return v/(v.std()+1e-9)
    lag=256/2/SR
    return flux(30,150),flux(150,1500),flux(1500,5500),fr,lag
def heat(nr,res,cols=96):
    k,s,h,fr,lag=bands(nr)
    bt=np.array(res['beats']); bar=np.array(res['bar']); bi=np.array(res['bi']); bn=np.array(res['bn'])
    db=np.where(bi==0)[0]
    rows=[];labels=[]
    for q in range(len(db)-1):
        a=db[q]; b=db[q+1]; t0=bt[a]; t1=bt[b]
        if t0<0: continue
        L=t1-t0; ts=np.linspace(t0-0.12*L,t1+0.0*L,cols,endpoint=False)
        # sample max in each column bin
        def samp(v):
            idx=((ts-lag)*fr).astype(int); idx2=(((ts+L*1.12/cols)-lag)*fr).astype(int)
            return np.array([v[max(0,i):max(max(0,i)+1,j)].max() if 0<=i<len(v)-1 else 0 for i,j in zip(idx,idx2)])
        rows.append(np.stack([samp(k),samp(s),samp(h)],-1)); labels.append(bar[a])
    A=np.array(rows); A=np.clip(A/3.0,0,1)
    img=(A*255).astype(np.uint8)
    im=Image.fromarray(img).resize((cols*4,len(rows)*4),Image.NEAREST)
    d=ImageDraw.Draw(im)
    # beat markers: downbeat at col 0.12/1.12 position
    x0=int(cols*4*0.12/1.12); d.line([(x0,0),(x0,im.size[1])],fill=(255,255,255),width=1)
    for r,lb in enumerate(labels):
        if lb%8==1: d.text((2,r*4-3),str(lb),fill=(255,255,0))
    return im
if __name__=='__main__':
    which=sys.argv[1]; R=json.load(open('res_%s.json'%which)); nrs=[int(x) for x in sys.argv[2:]]
    ims=[heat(n,R[str(n)]) for n in nrs]
    H=max(i.size[1] for i in ims); W=sum(i.size[0]+20 for i in ims)
    out=Image.new('RGB',(W,H+20),(40,40,40)); x=0; d=ImageDraw.Draw(out)
    for n,i in zip(nrs,ims): out.paste(i,(x,20)); d.text((x+4,4),'#%d'%n,fill=(255,255,255)); x+=i.size[0]+20
    out.save('heat_%s_%s.png'%(which,'_'.join(map(str,nrs))))
