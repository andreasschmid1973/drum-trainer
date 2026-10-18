const fs=require('fs'); const src=fs.readFileSync('/home/claude/ana_v4.js','utf8');
const M=new Function(src+'; return {analyzeSong:analyzeSong,onsetBands:onsetBands,CH:CH};')();
const BPM={1:159,2:160,3:163,4:91,5:130,6:150,7:148,8:134,9:106,10:99,11:184,12:114,13:150,14:128,15:90,16:129,17:133,18:140,19:132,20:70,21:79,22:191,23:117,24:151,25:97,26:129,27:139,28:128,29:155};
const which=process.argv[2]||'perc'; const out={};
for(let nr=1;nr<=29;nr++){
  const f='s'+String(nr).padStart(2,'0')+'_'+which+'.f32'; const b=fs.readFileSync(f); const x=new Float32Array(b.buffer,b.byteOffset,b.length/4);
  const t0=Date.now(); const r=M.analyzeSong({sampleRate:11025,length:x.length,numberOfChannels:1,getChannelData:()=>x},nr,BPM[nr]);
  out[nr]=r; console.log(nr,'scale',r.scale.toFixed(3),'gT',r.gTime.toFixed(2),'bpm',r.bpm.toFixed(1),'beats',r.beats.length,(Date.now()-t0)+'ms');
}
fs.writeFileSync('res_'+which+'.json',JSON.stringify(out));
