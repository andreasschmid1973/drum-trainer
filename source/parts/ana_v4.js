/*ANA-START*/
/* ===== Chart-Daten aus den Drum-Charts =====
   m: [Takt, Zähler, Nenner, Viertel-BPM] ab diesem Takt
   g: Takt, in dem der Drum-Groove mit einem Schlag auf der Eins einsetzt
   end: letzter Takt · mr: Pausen über mehrere Takte [Takt, Anzahl] · pg: erster Takt jeder PDF-Seite */
var CH={
1:{m:[[1,4,4,161]],g:1,end:208,pg:[1,50,94,145,189]},
2:{m:[[1,4,4,167]],g:5,end:200,mr:[[1,3],[197,4]],pg:[1,37,73,114,153,183]},
3:{m:[[1,4,4,164]],g:5,end:112,mr:[[1,3]],pg:[1,43,91]},
4:{m:[[1,12,8,112],[17,4,4,88]],g:1,end:175,pg:[1,32,63,90,122,147,167]},
5:{m:[[1,4,4,130]],g:1,end:65,pg:[1,44]},
6:{m:[[1,4,4,74],[62,2,4,74],[63,4,4,74],[90,4,4,66],[91,4,4,48]],g:3,end:93,mr:[[1,2],[15,7]],pg:[1,40,62,84]},
7:{m:[[1,4,4,128],[9,4,4,130],[13,4,4,131],[15,4,4,132],[17,4,4,133],[21,4,4,134],[25,4,4,135],[29,4,4,137],[30,4,4,139],[31,4,4,142],[32,4,4,144],[33,4,4,146],[44,4,4,147],[45,4,4,148],[65,4,4,150],[79,4,4,153],[80,4,4,155],[81,4,4,151],[90,4,4,153],[104,4,4,155],[105,4,4,158],[106,4,4,162],[121,5,4,150],[122,4,4,150]],g:1,end:123,pg:[1,51,99]},
8:{m:[[1,4,4,134]],g:6,end:141,mr:[[1,4]],pg:[1,49,97,141]},
9:{m:[[1,4,4,106]],g:3,end:122,pg:[1,62,109]},
10:{m:[[1,4,4,99]],g:5,end:89,mr:[[1,4]],pg:[1,48]},
11:{m:[[1,12,8,184],[68,6,8,184],[69,12,8,184]],g:1,end:164,mr:[[113,3]],pg:[1,37,73,116,149]},
12:{m:[[1,4,4,114],[100,4,4,93],[101,4,4,70]],g:9,end:102,mr:[[1,7],[101,2]],pg:[1,44,85]},
13:{m:[[1,4,4,110],[31,4,4,115],[32,4,4,138],[65,4,4,140],[73,4,4,142],[89,4,4,145],[154,9,8,130],[155,4,4,135]],g:25,end:161,mr:[[1,24]],pg:[1,61,98,143]},
14:{m:[[1,4,4,128]],g:1,end:147,pg:[1,41,89,132]},
15:{m:[[1,4,4,89],[15,4,4,91],[16,4,4,92],[25,4,4,93],[26,4,4,94],[31,4,4,92],[33,4,4,90],[34,4,4,88],[37,4,4,87],[49,4,4,88],[52,4,4,89],[60,4,4,88],[64,4,4,87],[77,4,4,88],[78,4,4,89],[79,4,4,90],[80,4,4,91],[81,4,4,92],[100,4,4,88],[101,4,4,92],[105,4,4,93],[116,4,4,95]],g:14,end:124,mr:[[2,4],[6,7],[91,5],[98,2]],pg:[1,42,71,109]},
16:{m:[[1,4,4,130],[104,2,4,130],[105,4,4,130]],g:1,end:112,mr:[[68,2],[110,2]],pg:[1,45,101]},
17:{m:[[1,4,4,133]],g:2,end:167,pg:[1,33,69,109,145]},
18:{m:[[1,4,4,140]],g:3,end:96,mr:[[1,2]],pg:[1,30,68]},
19:{m:[[1,4,4,132]],g:1,end:156,pg:[1,37,81,121]},
20:{m:[[1,15,16,72],[4,4,4,72],[7,15,16,72],[8,4,4,72],[11,15,16,72],[12,4,4,72],[20,5,4,72],[21,4,4,72],[68,3,4,72],[69,4,4,72],[94,2,4,72],[95,4,4,72]],g:21,end:101,mr:[[1,3],[5,2],[8,3],[13,7]],pg:[1,50,90]},
21:{m:[[1,4,4,79]],g:12,end:78,mr:[[1,11]],pg:[1,44]},
22:{m:[[1,4,4,191],[195,4,4,140]],g:1,end:198,mr:[[196,3]],pg:[1,41,96,145]},
23:{m:[[1,4,4,117]],g:6,end:101,mr:[[1,4],[82,3]],pg:[1,40,89]},
24:{m:[[1,4,4,150]],g:1,end:179,pg:[1,33,69,105,139,175]},
25:{m:[[1,4,4,96]],g:4,end:94,pg:[1,27,57,87]},
26:{m:[[1,4,4,129]],g:5,end:133,mr:[[1,3],[101,3]],pg:[1,40,80,125]},
27:{m:[[1,4,4,138],[127,2,4,138],[128,2,4,111],[129,4,4,111]],g:8,end:132,mr:[[1,6]],pg:[1,43,87,125]},
29:{m:[[1,4,4,155]],g:5,end:178,mr:[[1,4],[176,3]],pg:[1,42,78,113,149]}
};

function meterBeats(num,den){
  var a=[],i;
  if(den===4){ for(i=0;i<num;i++) a.push(1); }
  else if(den===2){ for(i=0;i<num;i++) a.push(2); }
  else if(den===8){ if(num%3===0){ for(i=0;i<num/3;i++) a.push(1.5); } else { for(i=0;i<num;i++) a.push(0.5); } }
  else if(den===16){ for(i=0;i<Math.floor(num/4);i++) a.push(1); if(num%4) a.push((num%4)/4); }
  else { for(i=0;i<num;i++) a.push(4/den); }
  return a;
}
function buildChartBeats(ch){
  function seg(bar){ var s=ch.m[0]; for(var k=0;k<ch.m.length;k++){ if(ch.m[k][0]<=bar) s=ch.m[k]; } return s; }
  var T=[],D=[],B=[],I=[],N=[],t=0,bar,k,s,q,sp;
  var s0=ch.m[0], q0=meterBeats(s0[1],s0[2]), sp0=60/s0[3], pre=[], tt=0;
  for(bar=0;bar>=(ch.pre||-24);bar--){ for(k=q0.length-1;k>=0;k--){ tt-=q0[k]*sp0; pre.push([tt,q0[k]*sp0,bar,k,q0.length]); } }
  pre.reverse(); pre.forEach(function(p){ T.push(p[0]); D.push(p[1]); B.push(p[2]); I.push(p[3]); N.push(p[4]); });
  for(bar=1;bar<=(ch.end||400)+(ch.post||48);bar++){ s=seg(bar); q=meterBeats(s[1],s[2]); sp=60/s[3];
    for(k=0;k<q.length;k++){ T.push(t); D.push(q[k]*sp); B.push(bar); I.push(k); N.push(q.length); t+=q[k]*sp; } }
  return {t:T,d:D,b:B,i:I,n:N};
}

/* ----- FFT ----- */
var FFT_N=256, fRev=null, fCos=null, fSin=null;
function fftInit(N){ var lg=Math.round(Math.log(N)/Math.LN2),i,b,r; fRev=new Uint16Array(N); for(i=0;i<N;i++){ r=0; for(b=0;b<lg;b++) if(i&(1<<b)) r|=1<<(lg-1-b); fRev[i]=r; }
  fCos=new Float32Array(N/2); fSin=new Float32Array(N/2); for(i=0;i<N/2;i++){ fCos[i]=Math.cos(2*Math.PI*i/N); fSin[i]=-Math.sin(2*Math.PI*i/N); } }
function fft(re,im,N){
  var i,j,t,size,half,step,st,k,wr,wi,a,b,tr,ti;
  for(i=0;i<N;i++){ j=fRev[i]; if(j>i){ t=re[i]; re[i]=re[j]; re[j]=t; t=im[i]; im[i]=im[j]; im[j]=t; } }
  for(size=2;size<=N;size<<=1){ half=size>>1; step=N/size;
    for(st=0;st<N;st+=size){ for(k=0;k<half;k++){ wr=fCos[k*step]; wi=fSin[k*step]; a=st+k; b=a+half;
      tr=re[b]*wr-im[b]*wi; ti=re[b]*wi+im[b]*wr; re[b]=re[a]-tr; im[b]=im[a]-ti; re[a]+=tr; im[a]+=ti; } } }
}

/* ----- Onset-Hüllkurven: Bass (Kick), Mitten (Snare/Gitarre), Höhen (Becken/Snare) ----- */
function onsetBands(ab){
  var sr=ab.sampleRate, n=ab.length, x, i, k;
  if(ab.numberOfChannels>1){ var c0=ab.getChannelData(0),c1=ab.getChannelData(1); x=new Float32Array(n); for(i=0;i<n;i++) x[i]=(c0[i]+c1[i])*0.5; } else x=ab.getChannelData(0);
  var ss=0; for(i=0;i<n;i+=7) ss+=x[i]*x[i]; var gain=0.1/Math.sqrt(ss/(n/7)+1e-12);
  var N=FFT_N; if(!fRev) fftInit(N);
  var hop=Math.max(1,Math.round(sr/100)), fr=sr/hop, F=Math.max(0,Math.floor((n-N)/hop)+1);
  var win=new Float32Array(N); for(i=0;i<N;i++) win[i]=0.5-0.5*Math.cos(2*Math.PI*i/N);
  var b1=Math.max(1,Math.round(40*N/sr)), b2=Math.round(150*N/sr), b3=Math.round(2000*N/sr), b4=Math.min(N/2-1,Math.round(5500*N/sr));
  var re=new Float32Array(N), im=new Float32Array(N), prev=new Float32Array(N/2), cur=new Float32Array(N/2);
  var L=new Float32Array(F), M=new Float32Array(F), H=new Float32Array(F), E=new Float32Array(F);
  var c1=Math.max(1,Math.round(80*N/sr)), c2=Math.round(1000*N/sr), NC=c2-c1, SPC=new Float64Array((F+1)*NC);
  for(var f=0;f<F;f++){
    var o=f*hop; for(i=0;i<N;i++){ re[i]=x[o+i]*win[i]*gain; im[i]=0; }
    fft(re,im,N);
    var sl=0,sm=0,sh=0,en=0;
    for(k=b1;k<=b4;k++){ var mg=Math.sqrt(re[k]*re[k]+im[k]*im[k]), lv=Math.log(1+100*mg); cur[k]=lv; en+=mg*mg; var d=lv-prev[k]; if(d>0){ if(k<b2) sl+=d; else if(k<b3) sm+=d; else sh+=d; } }
    L[f]=sl/(b2-b1); M[f]=sm/(b3-b2); H[f]=sh/(b4-b3); E[f]=en;
    for(k=0;k<NC;k++) SPC[(f+1)*NC+k]=SPC[f*NC+k]+cur[c1+k];
    var tmp=prev; prev=cur; cur=tmp;
  }
  function norm(a){ var Wn=Math.round(0.35*fr), cs=new Float64Array(F+1), out=new Float32Array(F), s2=0, c=0;
    for(i=0;i<F;i++) cs[i+1]=cs[i]+a[i];
    for(i=0;i<F;i++){ var lo=Math.max(0,i-Wn),hi=Math.min(F,i+Wn+1),v=a[i]-(cs[hi]-cs[lo])/(hi-lo); out[i]=v>0?v:0; s2+=out[i]*out[i]; c++; }
    var sd=Math.sqrt(s2/Math.max(1,c))+1e-9; for(i=0;i<F;i++) out[i]/=sd; return out; }
  function smooth(a){ var out=new Float32Array(F), g=[0.11,0.24,0.3,0.24,0.11]; for(i=0;i<F;i++){ var s=0; for(k=-2;k<=2;k++){ var ii=i+k; if(ii>=0&&ii<F) s+=a[ii]*g[k+2]; } out[i]=s; } return out; }
  var l=norm(L), m=norm(M), h=norm(H), env=new Float32Array(F), hi=new Float32Array(F);
  for(i=0;i<F;i++){ env[i]=l[i]+m[i]+h[i]; hi[i]=m[i]+h[i]; }
  return {lag:N/2/sr,fr:fr,F:F,dur:n/sr,env:smooth(env),low:smooth(l),hi:smooth(hi),en:E,spc:SPC,nc:NC};
}

function median(a){ var s=a.slice().sort(function(x,y){return x-y;}); return s.length?s[Math.floor(s.length/2)]:0; }

/* ----- Hauptanalyse ----- */
function analyzeSong(ab,nr,listBpm,opt){
  var O=onsetBands(ab), fr=O.fr, F=O.F, env=O.env, low=O.low, hi=O.hi, i, j, k;
  if(F<300) throw new Error('kurz');
  function at(a,t){ var f=Math.round(t*fr); return (f>=0&&f<F)?a[f]:0; }
  // Musikbeginn (erste hörbare Stelle) und Drum-Einsatz (dauerhaft Kick + Becken)
  var en=O.en, pk=0; for(i=0;i<F;i++) if(en[i]>pk) pk=en[i];
  var tStart=0; for(i=0;i<F;i++){ if(en[i]>pk*0.002){ tStart=i/fr; break; } }
  var W=Math.round(1.5*fr), cs=new Float64Array(F+1); for(i=0;i<F;i++) cs[i+1]=cs[i]+low[i]+hi[i];
  var act=new Float32Array(F); for(i=0;i<F;i++){ var lo=Math.max(0,i-W),h2=Math.min(F,i+W+1); act[i]=(cs[h2]-cs[lo])/(h2-lo); }
  var ref=act.slice().sort()[Math.floor(F*0.8)]||1, tD=tStart;
  for(i=0;i<F;i++){ if(act[i]>0.45*ref){ var ok=true; for(k=i;k<Math.min(F,i+2*fr);k+=10){ if(act[k]<0.3*ref){ ok=false; break; } } if(ok){ tD=Math.max(tStart,i/fr-1.5); break; } } }

  var ch=CH[nr]||null, nochart=!ch;
  if(nochart){
    // Ohne Chart: 4/4 im Setlist-Tempo, Oktave über Autokorrelation prüfen
    var bpm=listBpm||120, f0=Math.round(tD*fr), f1=Math.min(F,f0+Math.round(60*fr)), best=-1, bestB=bpm;
    [0.5,1,2].forEach(function(mul){ var b=bpm*mul; if(b<55||b>210) return; var Lg=Math.round(60*fr/b), s=0, c=0; for(var q=f0;q+Lg<f1;q++){ s+=env[q]*env[q+Lg]; c++; } s=c?s/c:0; var z=Math.log(b/120)/Math.LN2; s*=Math.exp(-0.5*z*z/0.8); if(s>best){ best=s; bestB=b; } });
    ch={m:[[1,4,4,bestB]],g:1,end:Math.ceil(O.dur*bestB/240)+8,pre:-Math.ceil(tD*bestB/240)-12};
  }
  var C=buildChartBeats(ch), NB=C.t.length, jg=-1;
  for(j=0;j<NB;j++){ if(C.b[j]===ch.g&&C.i[j]===0){ jg=j; break; } }
  var Cg=C.t[jg], j1=jg; for(j=0;j<NB;j++){ if(C.b[j]===1&&C.i[j]===0){ j1=j; break; } }
  var barG=0; for(j=jg;j<NB&&C.b[j]===ch.g;j++) barG+=C.d[j];

  function wgt(jj,t){ var f=Math.round(t*fr); if(f<0||f>=F) return 0; var v=env[f];
    if(C.i[jj]===0) v+=0.7*low[f]; else if(C.n[jj]===4&&(C.i[jj]&1)) v+=0.5*hi[f]; return v; }

  // (a) Beat-Raster: Tempofaktor und Phase gegenüber dem Chart, nur aus den Schlägen (ohne Takt-Eins)
  var K=0; while(jg+K<NB&&K<96&&C.t[jg+K]-Cg<32) K++;
  // Suchfenster: (1) Musikbeginn + Intro-Länge laut Chart, (2) erkannter Drum-Einsatz
  var intro=nochart?0:(Cg-C.t[j1]), Tprior=nochart?tD:(tStart+intro), wd=Math.min(20,2.5*barG+0.12*intro);
  var WIN=[[Tprior-wd,Tprior+wd],[tD-1.5*barG,tD+3*barG]].map(function(w){ return [Math.max(-0.5,w[0]),Math.min(O.dur-5,w[1])]; }).filter(function(w){ return w[1]>w[0]; });
  if(!WIN.length) WIN=[[0,Math.min(10,O.dur/2)]];
  function inWin(t){ for(var q=0;q<WIN.length;q++){ if(t>=WIN[q][0]-0.3&&t<=WIN[q][1]+0.3) return true; } return false; }
  var offs=new Float32Array(K), gS=-1e9, gT=Math.max(0,tD), gSc=1, s, Tg, sc;
  function gridScore(T0,sv){ var v=0; for(var q=0;q<K;q++){ var f=Math.round((T0+sv*(C.t[jg+q]-Cg))*fr); if(f>=0&&f<F) v+=env[f]; } return v; }
  for(s=0.85;s<=1.1501;s+=0.004){
    for(k=0;k<K;k++) offs[k]=s*(C.t[jg+k]-Cg);
    for(var wi=0;wi<WIN.length;wi++) for(Tg=WIN[wi][0];Tg<=WIN[wi][1];Tg+=1/fr){ sc=0; for(k=0;k<K;k++){ var ff=Math.round((Tg+offs[k])*fr); if(ff>=0&&ff<F) sc+=env[ff]; } if(sc>gS){ gS=sc; gT=Tg; gSc=s; } }
  }
  for(s=gSc-0.004;s<=gSc+0.0041;s+=0.0005){ for(Tg=gT-0.03;Tg<=gT+0.0301;Tg+=0.5/fr){ sc=gridScore(Tg,s); if(sc>=gS){ gS=sc; gT=Tg; gSc=s; } } }

  // (b) Welcher Schlag ist die Eins des Groove-Takts? Kandidaten = Rasterschläge im Suchfenster
  var NC=O.nc, SPC=O.spc;
  // Klangwechsel (Akkord/Bass) zwischen dem Takt vor und nach t; Fenster = ein Takt, damit sich das Drum-Pattern heraushebt
  function nov(t,Lbar){ var f=Math.round(t*fr), w=Math.max(3,Math.round(Lbar*fr)); if(f-w<0||f+w>F) return 0; var v=0;
    for(var q=0;q<NC;q++){ var A1=(SPC[(f+w)*NC+q]-SPC[f*NC+q])/w, B1=(SPC[f*NC+q]-SPC[(f-w)*NC+q])/w, d=A1-B1; v+=d*d; } return v/NC; }
  function actMean(t0,t1){ var f0=Math.max(0,Math.round(t0*fr)), f1=Math.min(F,Math.round(t1*fr)); if(f1<=f0) return 0; var v=0; for(var q=f0;q<f1;q++) v+=act[q]; return v/(f1-f0)/ref; }
  var cands=[];
  for(var m=-400;m<=400;m++){ var jj=jg+m; if(jj<0||jj>=NB) continue; var Tc=gT+gSc*(C.t[jj]-Cg); if(!inWin(Tc)) continue;
    // Takt-Eins-Merkmale über die ersten ~24 Takte des Grooves
    var dbv=0, obv=0, nd=0, no=0, q;
    for(q=0;q<K;q++){ var tq=Tc+gSc*(C.t[jg+q]-Cg), Lb=gSc*C.d[jg+q]*C.n[jg+q], f=Math.round(tq*fr); if(f<0||f>=F) continue;
      var hv=nov(tq,Lb);
      if(C.i[jg+q]===0){ dbv+=hv; nd++; } else { obv+=hv; no++; } }
    var lab=(nd?dbv/nd:0)-(no?obv/no:0);
    var ent=actMean(Tc,Tc+2*barG*gSc)-actMean(Tc-2.75*barG*gSc,Tc-0.8*barG*gSc);
    var bt0=gSc*C.d[jg], dz=nochart?0:(Tc-Tprior-(gSc-1)*(Cg-C.t[j1]))/(0.75*bt0), pri=dz<-1?-Math.min(8,0.5*dz*dz):-Math.min(2.5,0.5*dz*dz);
    var hit=0, fh=Math.round(Tc*fr); for(q=fh-2;q<=fh+2;q++){ if(q>=0&&q<F&&low[q]+hi[q]>hit) hit=low[q]+hi[q]; }
    // Passt das ganze Raster (inkl. späterer Takt- und Tempowechsel) mit diesem Anker?
    // Lage und Tempo pro Kandidat leicht nachoptimieren (Tempowechsel im Chart verschieben sonst die Phase)
    var full=-1, bT=Tc, bSs=gSc, qEnd=jg; while(qEnd<NB&&C.t[qEnd]-Cg<240) qEnd++;
    for(var ds=-0.006;ds<=0.00601;ds+=0.002){ var sv=gSc+ds; for(var dT=-0.04;dT<=0.0401;dT+=0.01){ var fv=0;
      for(q=jg;q<qEnd;q+=1){ var fq=Math.round((Tc+dT+sv*(C.t[q]-Cg))*fr); if(fq>=0&&fq<F) fv+=env[fq]; }
      if(fv>full){ full=fv; bT=Tc+dT; bSs=sv; } } }
    cands.push({T:bT,s:bSs,lab:lab,ent:ent,pri:pri,hit:hit,full:full});
  }
  function zs(key){ var mu=0,sd=0; cands.forEach(function(c){ mu+=c[key]; }); mu/=cands.length; cands.forEach(function(c){ sd+=(c[key]-mu)*(c[key]-mu); }); sd=Math.sqrt(sd/cands.length)+1e-9; cands.forEach(function(c){ c['z'+key]=(c[key]-mu)/sd; }); }
  var bTg=gT, bS=gSc;
  if(cands.length){ ['lab','ent','hit'].forEach(zs);
    var fmax=0; cands.forEach(function(c){ if(c.full>fmax) fmax=c.full; });
    var bestC=null; cands.forEach(function(c){ c.zfull=fmax?10*(c.full/fmax-1):0; c.tot=1.0*c.zlab+1.2*c.zent+0.6*c.zhit+c.pri+c.zfull; if(!bestC||c.tot>bestC.tot) bestC=c; });
    bTg=bestC.T; bS=bestC.s; }
  if(opt&&opt.gT!=null){ bTg=opt.gT; if(opt.s) bS=opt.s; }
  if(typeof DBG!=="undefined") console.log("grid",gT.toFixed(2),gSc.toFixed(3),"cands",cands.map(function(c){return c.T.toFixed(2)+" L"+c.zlab.toFixed(1)+" E"+c.zent.toFixed(1)+" H"+c.zhit.toFixed(1)+" P"+c.pri.toFixed(1)+" G"+c.zfull.toFixed(1)+" ="+c.tot.toFixed(1);}).join("\n"));

  // Taktweises Nachführen ab dem Groove-Einsatz (Phase ±50 ms, Tempo ±3 % pro Takt)
  var BT=new Float64Array(NB); for(j=0;j<NB;j++) BT[j]=NaN;
  var wide={}; (ch.mr||[]).forEach(function(r){ wide[r[0]+r[1]]=1; });
  for(k=1;k<ch.m.length;k++){ var pb=ch.m[k-1][3], nb=ch.m[k][3]; if(Math.abs(nb/pb-1)>0.04) wide[ch.m[k][0]]=0.5; }
  var t=bTg, r=bS; j=jg; var rSum=0, rCnt=0;
  while(j<NB&&t<O.dur+2){
    var nb2=C.n[j]-C.i[j], Wb=Math.min(NB-j,Math.max(8,nb2+4)), wd=wide[C.b[j]]&&j!==jg, dR=wd?(wide[C.b[j]]===1?0.4:0.2)*C.d[j]*r:0.05, dSt=wd?0.008:0.004;
    var bD=0, bR=r, bV=-1e9;
    for(var dd=-dR;dd<=dR+1e-9;dd+=dSt){
      for(var rr=r*0.97;rr<=r*1.0301;rr+=r*0.005){
        var cu=0, v=0; for(k=0;k<Wb;k++){ v+=wgt(j+k,t+dd+rr*cu); cu+=C.d[j+k]; }
        v-=(wd?0.5:3)*(dd/0.06)*(dd/0.06)+2*((rr/r-1)/0.025)*((rr/r-1)/0.025);
        if(v>bV){ bV=v; bD=dd; bR=rr; }
      }
    }
    var cu2=0; for(k=0;k<nb2;k++){ BT[j+k]=t+bD+bR*cu2; cu2+=C.d[j+k]; }
    t=t+bD+bR*cu2; r=0.7*r+0.3*bR; j+=nb2; if(rCnt<8){ rSum+=bR; rCnt++; }
  }
  // Vor dem Groove: aus dem Chart zurückrechnen (Intro wird nicht zur Erkennung benutzt)
  var rIn=rCnt?rSum/rCnt:bS; for(j=jg-1;j>=0;j--) BT[j]=BT[jg]+rIn*(C.t[j]-Cg);

  var bt=[],bb=[],bi=[],bn=[];
  for(j=0;j<NB;j++){ if(!isFinite(BT[j])) break; if(BT[j]<-3) continue; if(BT[j]>O.dur+1) break;
    bt.push(Math.round((BT[j]+O.lag)*1000)/1000); bb.push(C.b[j]); bi.push(C.i[j]); bn.push(C.n[j]); }
  var io=[]; for(j=1;j<bt.length;j++){ if(bt[j-1]>=bTg) io.push(bt[j]-bt[j-1]); }
  var tEnd=O.dur; if(!nochart){ for(j=0;j<bt.length;j++){ if(bb[j]>ch.end){ tEnd=Math.min(O.dur,bt[j]); break; } } }
  var t1=bTg; for(j=0;j<bt.length;j++){ if(bb[j]>=1){ t1=bt[j]; break; } }
  return {v:4,chart:!nochart,start:Math.max(0,nochart?bTg:t1),end:tEnd,duration:O.dur,beats:bt,bar:bb,bi:bi,bn:bn,
          bpm:io.length?60/median(io):(ch.m[0][3]),gTime:bTg+O.lag,scale:bS,tracked:true};
}
/*ANA-END*/
