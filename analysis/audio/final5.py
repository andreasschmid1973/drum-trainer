import json, numpy as np
import remap as RM
INK=json.load(open('../lay/ink.json')); R4=json.load(open('final4.json')); R0=json.load(open('final.json'))
out={}; log=[]
def act_score(ts,act):
    v=[act[max(0,int(round(t*100))-2):int(round(t*100))+3].max() for t in ts if 0.3<t and t*100<len(act)-3]
    return np.mean(v) if v else 0
for nr in range(1,30):
    r=dict(R4[str(nr)]); t=np.array(r['beats']); bar=np.array(r['bar']); bi=np.array(r['bi'])
    x=np.zeros(len(t))
    for i in range(1,len(t)): x[i]=x[i-1]+RM.beatdur(nr,int(bar[i-1]),int(bi[i-1]))
    ink=INK.get(str(nr),{}); med=np.median(list(ink.values())) if ink else 1
    def sparse(b):
        if not RM.drumbar(nr,b): return True
        v=ink.get(str(b)); return v is not None and v<0.7*med
    sp=np.array([sparse(int(b)) for b in bar])
    strong=np.where(~sp&(t>0.3))[0]
    if len(strong)<16: out[nr]=r; continue
    new=t.copy(); i=0; nspan=0
    first=strong[0]
    while i<len(t):
        if sp[i] and i>first:
            j=i
            while j<len(t) and sp[j]: j+=1
            L=strong[strong<i]; Rr=strong[strong>=j]
            if len(L) and len(Rr):
                a_,b_=L[-1],Rr[0]
                ratio=((t[b_]-t[a_])/(x[b_]-x[a_]))/np.polyfit(x[L[-8:]],t[L[-8:]],1)[0]
                if abs(ratio-1)<0.06:
                    for k in range(a_+1,b_): new[k]=t[a_]+(t[b_]-t[a_])*(x[k]-x[a_])/(x[b_]-x[a_])
                    nspan+=1
                else: log.append('#%d Takt %d-%d: Länge passt nicht (%.3f), bleibt wie erkannt'%(nr,bar[i],bar[j-1] if j<=len(bar) else 0,ratio))
            i=j
        else: i+=1
    # Intro (alles vor dem ersten kräftigen Takt): konstantes Tempo
    a=np.load('mmact_%02d.npy'%nr); act=a[:,0]+a[:,1]
    if first>=4:
        S=strong[:16]; spq=np.polyfit(x[S],t[S],1)[0]
        ext=t[first]+spq*(x[:first]-x[first])
        live=np.where(t[:first]>0.3)[0]
        if len(live)>=4:
            p=np.polyfit(x[live],t[live],1)  # gleichmäßige Gerade durch die erkannten Intro-Schläge
            lin=p[0]*x[:first]+p[1]; lin+= (t[first]-spq*(x[first]-x[first-1])) - lin[-1] - (p[0]*(x[first]-x[first-1])-spq*(x[first]-x[first-1]))*0
            # Anschluss an den Anker: Gerade so verschieben, dass der Schritt zum Anker passt
            lin=lin-(lin[-1]-(t[first]-p[0]*(x[first]-x[first-1])))
            se=act_score(ext[live],act); sl=act_score(lin[live],act); dev=abs(p[0]/spq-1)
            choice='konstant' if se>=sl-0.02 else 'eigenes Intro-Tempo'
            new[:first]=ext if choice=='konstant' else lin
            log.append('#%d Intro bis Takt %d: %s (Intro %.1f vs. Song %.1f BPM, Treffer %.2f/%.2f)'%(nr,bar[first],choice,60/p[0],60/spq,se,sl))
        else: new[:first]=ext
    r['beats']=[round(float(v),4) for v in new]; out[nr]=r
json.dump(out,open('final5.json','w'))
print('\n'.join(log))
r=out[26]; bt=np.array(r['beats']); bar=np.array(r['bar'])
print('Jump',' '.join('%d:%.1f'%(b,240/(bt[np.where(bar==b+1)[0][0]]-bt[np.where(bar==b)[0][0]])) for b in list(range(1,11))+list(range(98,110))))
