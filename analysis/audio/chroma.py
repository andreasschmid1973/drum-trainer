import json, numpy as np, librosa, os
from refine import drumbar
R=json.load(open('ref_perc.json')); SR=11025
def chroma(nr):
    fn='chr_%02d.npy'%nr
    if os.path.exists(fn): return np.load(fn)
    ym=np.fromfile('s%02d_mix.f32'%nr,dtype=np.float32); yp=np.fromfile('s%02d_perc.f32'%nr,dtype=np.float32)
    yh=ym-yp[:len(ym)]
    C=librosa.feature.chroma_stft(y=yh,sr=SR,n_fft=2048,hop_length=110)  # 10ms
    np.save(fn,C); return C
out={}
for nr in range(1,30):
    r=R[str(nr)]; C=chroma(nr); bt=np.array(r['beats']); bar=np.array(r['bar']); bi=np.array(r['bi']); bn=np.array(r['bn'])
    fr=SR/110; nov=np.zeros(4); cnt=np.zeros(4)
    for i in range(1,len(bt)-1):
        if bn[i]!=4 or bt[i-1]<0: continue
        a=int(bt[i-1]*fr); b=int(bt[i]*fr); c=int(bt[i+1]*fr)
        if c>=C.shape[1] or b-a<3 or c-b<3: continue
        x=C[:,a:b].mean(1); y=C[:,b:c].mean(1)
        x/=np.linalg.norm(x)+1e-9; y/=np.linalg.norm(y)+1e-9
        nov[bi[i]]+=1-np.dot(x,y); cnt[bi[i]]+=1
    out[nr]=list(nov/np.maximum(cnt,1))
    v=np.array(out[nr]); print('%2d chord-change by beat 1..4: '%nr+' '.join('%.3f'%x for x in v),'  -> max at',int(np.argmax(v)))
json.dump(out,open('chroma_prof.json','w'))
