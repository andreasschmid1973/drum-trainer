import json, numpy as np, sys, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
R=json.load(open(sys.argv[1]))
specs=[a.split(':') for a in sys.argv[2:]]  # nr:bar_from:bar_to
fig,axs=plt.subplots(len(specs),1,figsize=(16,2.6*len(specs)))
if len(specs)==1: axs=[axs]
for ax,(nr,b0,b1) in zip(axs,specs):
    nr=int(nr); b0=int(b0); b1=int(b1); r=R[str(nr)]; d=np.load('b22_%02d.npz'%nr); fr=float(d['fr'])
    bt=np.array(r['beats']); bar=np.array(r['bar']); bi=np.array(r['bi'])
    sel=np.where((bar>=b0)&(bar<=b1))[0]; t0=bt[sel[0]]-0.1; t1=bt[sel[-1]]+0.6
    tt=np.arange(int(t0*fr),int(t1*fr))/fr
    for j,(nm,c,off) in enumerate([('kick','tab:red',0),('snb','tab:blue',1),('snh','tab:cyan',2),('hat','tab:green',3)]):
        v=d[nm][int(t0*fr):int(t1*fr)]; ax.plot(tt,np.clip(v,0,8)/8+off,c,lw=0.8)
    for i in sel:
        ax.axvline(bt[i],color='k' if bi[i]==0 else '0.6',lw=1.6 if bi[i]==0 else 0.6)
        if bi[i]==0: ax.text(bt[i],4.05,str(bar[i]),fontsize=8)
    ax.set_yticks([0.5,1.5,2.5,3.5]); ax.set_yticklabels(['kick','snare tief','snare hoch','hat/becken']); ax.set_xlim(t0,t1); ax.set_title('#%d Takt %d-%d'%(nr,b0,b1),fontsize=9)
plt.tight_layout(); plt.savefig('roll.png',dpi=80)
