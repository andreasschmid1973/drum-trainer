import json, numpy as np, subprocess, glob, os, re, librosa
from refine import drumbar
R=json.load(open('ref_perc.json'))
SRC='/mnt/user-data/uploads/BlackRockForest/mp3/'
def hf(nr):
    fn='hf_%02d.npy'%nr
    if os.path.exists(fn): return np.load(fn)
    f=[x for x in glob.glob(SRC+'*') if int(re.match(r'(\d+)',os.path.basename(x)).group(1))==nr][0]
    raw=subprocess.run(['ffmpeg','-v','error','-i',f,'-ac','1','-ar','44100','-af','highpass=f=7000,highpass=f=7000','-f','f32le','-'],capture_output=True,check=True).stdout
    y=np.frombuffer(raw,dtype=np.float32); n=len(y)//441
    e=np.sqrt((y[:n*441].reshape(n,441)**2).mean(1)); e=20*np.log10(e+1e-6); np.save(fn,e); return e
out={}
for nr in range(1,30):
    r=R[str(nr)]; e=hf(nr); bt=np.array(r['beats']); bar=np.array(r['bar']); bi=np.array(r['bi']); bn=np.array(r['bn'])
    acc=np.zeros(4); cnt=np.zeros(4)
    for i in range(len(bt)):
        if bn[i]!=4 or not drumbar(nr,bar[i]) or bt[i]<0.5: continue
        f=int(round(bt[i]*100))
        if f+60>=len(e): continue
        before=np.median(e[f-25:f-3]); after=np.median(e[f+15:f+50])   # Becken klingt nach
        acc[bi[i]]+= (after-before)>6; cnt[bi[i]]+=1
    out[nr]=list(acc/np.maximum(cnt,1))
    print('%2d crash-rate by beat 1..4: '%nr+' '.join('%.2f'%x for x in out[nr]))
