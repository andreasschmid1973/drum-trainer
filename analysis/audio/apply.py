import json, numpy as np, subprocess, sys
plan=json.load(open('plan.json')); R=json.load(open('ref_perc.json')); CH=json.load(open('ch.json'))
over={}
for nr in range(1,30):
    sh=plan[str(nr)]['shift']; r=R[str(nr)]
    if sh==0: continue
    bt=np.array(r['beats']); bar=np.array(r['bar']); bi=np.array(r['bi'])
    g=CH[str(nr)]['g'] if str(nr) in CH else 1
    j=int(np.where((bar==g)&(bi==0))[0][0])
    whole=int(np.floor(sh)); frac=sh-whole
    t=bt[j+whole]+frac*(bt[j+whole+1]-bt[j+whole])
    over[nr]={'gT':float(t)-0.0116,'s':r['scale']}  # Analyse rechnet intern ohne Fensterversatz
    print(nr,'shift',sh,'gT',round(r['gTime'],3),'->',round(t,3))
json.dump(over,open('over.json','w'))
