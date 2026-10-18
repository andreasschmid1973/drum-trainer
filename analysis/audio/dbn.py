import json, numpy as np, os, sys
from madmom.features.downbeats import DBNDownBeatTrackingProcessor
from refine import drumbar
R=json.load(open(sys.argv[1] if len(sys.argv)>1 else 'ref_fix.json'))
for nr in range(1,30):
    r=R[str(nr)]; bt=np.array(r['beats']); bar=np.array(r['bar']); bi=np.array(r['bi']); bn=np.array(r['bn'])
    fn='mmdb_%02d.npy'%nr
    ioi=np.median(np.diff(bt[bt>0])); bpm=60/ioi
    if not os.path.exists(fn):
        a=np.load('mmact_%02d.npy'%nr)
        b=DBNDownBeatTrackingProcessor(beats_per_bar=[4],fps=100,min_bpm=bpm*0.8,max_bpm=bpm*1.25)(a); np.save(fn,b)
    b=np.load(fn); mb=b[:,0]; md=b[b[:,1]==1][:,0]
    # Schlag-Ebene: Abstand unserer Drum-Schläge zum nächsten madmom-Schlag
    sel=np.array([drumbar(nr,x) for x in bar])&(bt>0.5)
    d=np.array([mb[np.argmin(abs(mb-t))]-t for t in bt[sel]])
    within=np.mean(np.abs(d)<0.04)
    # Takt-Ebene: unsere Takt-Eins relativ zu madmoms Takt-Eins (in Schlägen, mod 4)
    od=bt[(bi==0)&sel&(bn==4)]
    rel=[]
    for t in od:
        k=np.argmin(abs(mb-t)); 
        if abs(mb[k]-t)>0.06: continue
        # Position dieses madmom-Schlags im madmom-Takt
        pos=int(b[k,1])-1; rel.append(pos)
    h=np.bincount(rel,minlength=4)/max(1,len(rel))
    print('%2d bpm %.0f  beat-agree %.0f%%  our-downbeat = madmom beat#: %s'%(nr,bpm,100*within,' '.join('%.2f'%x for x in h)))
