/*MAP-START*/
function decodeMap(m){
  var t=[],s=0,i,bar=[],b=m.b0; for(i=0;i<m.t.length;i++){ s+=m.t[i]; t.push(s/1000); }
  var bi=[],bn=[]; for(i=0;i<m.i.length;i++){ bi.push(+m.i[i]); bn.push(+m.n[i]); }
  if(m.b) bar=m.b.slice(); else { for(i=0;i<bi.length;i++){ if(i>0&&bi[i]===0) b++; bar.push(b); } }
  return {beats:t,bar:bar,bi:bi,bn:bn};
}
// Versatz zwischen gespeicherter Taktkarte und der hier dekodierten Datei (Decoder-Unterschiede)
function mapOffset(ab,beats){
  var O=onsetBands(ab), env=O.env, fr=O.fr, best=-1, bd=0, sc0=0;
  for(var d=-0.12;d<=0.1201;d+=0.0025){ var v=0; for(var k=0;k<beats.length;k++){ var f=Math.round((beats[k]+d-O.lag)*fr); if(f>=1&&f<O.F-1) v+=Math.max(env[f-1],env[f],env[f+1]); } if(v>best){ best=v; bd=d; } if(Math.abs(d)<1e-6) sc0=v; }
  return {d:bd,gain:best/(sc0||1)};
}
function mapAnalysis(ab,nr,dur){
  var m=MAPS[nr]; if(!m||Math.abs(dur-m.d)>0.8) return null;
  var M=decodeMap(m), off=mapOffset(ab,M.beats), d=off.d-(m.o||0);
  if(Math.abs(d)>0.11) return null;
  var bt=M.beats.map(function(x){ return Math.round((x+d)*1000)/1000; });
  var c=CH[nr], io=[], j, g=c?c.g:1, gT=bt[0], t1=bt[0];
  for(j=1;j<bt.length;j++) io.push(bt[j]-bt[j-1]);
  for(j=0;j<bt.length;j++){ if(M.bar[j]===g&&M.bi[j]===0){ gT=bt[j]; break; } }
  for(j=0;j<bt.length;j++){ if(M.bar[j]>=1){ t1=bt[j]; break; } }
  var tEnd=dur; if(c){ for(j=0;j<bt.length;j++){ if(M.bar[j]>c.end){ tEnd=Math.min(dur,bt[j]); break; } } }
  return {v:5,chart:!!c,fromMap:true,offset:d,start:Math.max(0,t1),end:tEnd,duration:dur,beats:bt,bar:M.bar,bi:M.bi,bn:M.bn,
          bpm:io.length?60/median(io):120,gTime:gT,scale:1,tracked:true};
}
/*MAP-END*/
