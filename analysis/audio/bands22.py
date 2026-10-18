import subprocess, glob, os, re, numpy as np, librosa
from concurrent.futures import ProcessPoolExecutor
SRC='/mnt/user-data/uploads/BlackRockForest/mp3/'
SR=22050; HOP=110
def one(f):
    nr=int(re.match(r'(\d+)',os.path.basename(f)).group(1)); fn='b22_%02d.npz'%nr
    if os.path.exists(fn): return nr
    raw=subprocess.run(['ffmpeg','-v','error','-i',f,'-ac','1','-ar',str(SR),'-f','f32le','-'],capture_output=True,check=True).stdout
    y=np.frombuffer(raw,dtype=np.float32).copy()
    D=librosa.stft(y,n_fft=1024,hop_length=HOP); H,P=librosa.decompose.hpss(D,margin=2.0)
    S=np.abs(P); fq=librosa.fft_frequencies(sr=SR,n_fft=1024); L=np.log1p(100*S)
    def flux(lo,hi):
        m=(fq>=lo)&(fq<hi); d=np.diff(L[m],axis=1,prepend=L[m][:,:1]); d[d<0]=0; v=d.mean(0)
        v=v-np.convolve(v,np.ones(41)/41,'same'); v[v<0]=0; return (v/(v.std()+1e-9)).astype(np.float32)
    np.savez(fn,kick=flux(35,110),snb=flux(160,320),snh=flux(1000,4000),hat=flux(6500,11000),lag=np.float32(1024/2/SR),fr=np.float32(SR/HOP))
    return nr
with ProcessPoolExecutor(2) as ex:
    for nr in ex.map(one,sorted(glob.glob(SRC+'*'))): print(nr,end=' ',flush=True)
