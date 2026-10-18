const fs=require('fs'); const src=fs.readFileSync('/home/claude/ana_v4.js','utf8');
const M=new Function(src+'; return {analyzeSong:analyzeSong};')();
const BPM={1:159,2:160,3:163,4:91,5:130,6:150,7:148,8:134,9:106,10:99,11:184,12:114,13:150,14:128,15:90,16:129,17:133,18:140,19:132,20:70,21:79,22:191,23:117,24:151,25:97,26:129,27:139,28:128,29:155};
const over=JSON.parse(fs.readFileSync('over.json')); const base=JSON.parse(fs.readFileSync('res_perc.json'));
for(const nr of Object.keys(over)){
  const b=fs.readFileSync('s'+String(nr).padStart(2,'0')+'_perc.f32'); const x=new Float32Array(b.buffer,b.byteOffset,b.length/4);
  base[nr]=M.analyzeSong({sampleRate:11025,length:x.length,numberOfChannels:1,getChannelData:()=>x},+nr,BPM[nr],over[nr]);
  console.log(nr,'new gT',base[nr].gTime.toFixed(3));
}
fs.writeFileSync('res_fix.json',JSON.stringify(base));
