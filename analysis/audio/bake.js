const fs=require('fs');
const src=fs.readFileSync('/home/claude/ana_v4.js','utf8')+fs.readFileSync('maps2.js','utf8')+fs.readFileSync('/home/claude/mapalign.js','utf8');
const M=new Function(src+'; return {MAPS:MAPS,decodeMap:decodeMap,mapOffset:mapOffset};')();
for(let nr=1;nr<=29;nr++){
  const b=fs.readFileSync('s'+String(nr).padStart(2,'0')+'_mix.f32'); const x=new Float32Array(b.buffer,b.byteOffset,b.length/4);
  const ab={sampleRate:11025,length:x.length,numberOfChannels:1,getChannelData:()=>x};
  const D=M.decodeMap(M.MAPS[nr]); const o=M.mapOffset(ab,D.beats); M.MAPS[nr].o=Math.round(o.d*10000)/10000;
  // Test: künstlich um 37 ms verschoben → muss erkannt werden
  const sh=Math.round(0.037*11025), y=new Float32Array(x.length); y.set(x.subarray(0,x.length-sh),sh);
  const o2=M.mapOffset({sampleRate:11025,length:y.length,numberOfChannels:1,getChannelData:()=>y},D.beats);
  process.stdout.write(nr+': o '+(o.d*1000).toFixed(1)+'ms, shifted-test '+((o2.d-o.d)*1000).toFixed(1)+'ms | ');
}
fs.writeFileSync('maps2.js','var MAPS='+JSON.stringify(M.MAPS)+';');
