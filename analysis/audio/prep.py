import subprocess, glob, os, re, numpy as np, librosa, sys
from concurrent.futures import ProcessPoolExecutor
SRC='/mnt/user-data/uploads/BlackRockForest/mp3/'
def one(f):
    nr=int(re.match(r'(\d+)',os.path.basename(f)).group(1))
    out='s%02d'%nr
    if os.path.exists(out+'_perc.f32'): return nr
    raw=subprocess.run(['ffmpeg','-v','error','-i',f,'-ac','1','-ar','22050','-f','f32le','-'],capture_output=True,check=True).stdout
    y=np.frombuffer(raw,dtype=np.float32).copy()
    y11=librosa.resample(y,orig_sr=22050,target_sr=11025).astype(np.float32); y11.tofile(out+'_mix.f32')
    D=librosa.stft(y,n_fft=2048,hop_length=512)
    H,P=librosa.decompose.hpss(D,margin=2.0)
    yp=librosa.istft(P,hop_length=512,length=len(y))
    yp11=librosa.resample(yp,orig_sr=22050,target_sr=11025).astype(np.float32); yp11.tofile(out+'_perc.f32')
    return nr
fs=sorted(glob.glob(SRC+'*'))
with ProcessPoolExecutor(4) as ex:
    for nr in ex.map(one,fs): print(nr,end=' ',flush=True)
