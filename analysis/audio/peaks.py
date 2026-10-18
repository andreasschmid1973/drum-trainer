import numpy as np,sys
def peaks(nr,band,t0,t1,thr=None,rel=0.35):
    z=np.load('b22_%02d.npz'%nr); e=z[band]; fr=float(z['fr']); lag=float(z['lag'])
    a,b=int(t0*fr),int(t1*fr); s=e[a:b]
    if thr is None: thr=rel*np.percentile(e[int(len(e)*0.2):int(len(e)*0.8)],99)
    out=[]
    for i in range(2,len(s)-2):
        if s[i]>thr and s[i]==s[i-2:i+3].max(): out.append(((a+i)/fr+lag, s[i]/thr))
    return out
if __name__=='__main__':
    nr=int(sys.argv[1]);t0=float(sys.argv[2]);t1=float(sys.argv[3])
    for band in sys.argv[4].split(','):
        print(band,' '.join('%.2f(%.1f)'%p for p in peaks(nr,band,t0,t1)))
