import sys, glob, os, re, numpy as np, subprocess
import madmom
from madmom.features.downbeats import RNNDownBeatProcessor
SRC='/mnt/user-data/uploads/BlackRockForest/mp3/'
proc=RNNDownBeatProcessor()
for f in sorted(glob.glob(SRC+'*')):
    nr=int(re.match(r'(\d+)',os.path.basename(f)).group(1))
    if nr%2!=int(sys.argv[1]): continue
    fn='mmact_%02d.npy'%nr
    if os.path.exists(fn): continue
    raw=subprocess.run(['ffmpeg','-v','error','-i',f,'-ac','1','-ar','44100','-f','s16le','-'],capture_output=True,check=True).stdout
    sig=madmom.audio.signal.Signal(np.frombuffer(raw,dtype=np.int16).copy(),sample_rate=44100)
    act=proc(sig); np.save(fn,act); print(nr,act.shape,flush=True)
