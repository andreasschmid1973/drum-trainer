import json, glob
from PIL import Image, ImageDraw
import lay
R=json.load(open('repeats.json'))
crops=[]
for nr,hits in sorted(R.items(),key=lambda x:int(x[0])):
    pngs=sorted(glob.glob('s%02d-*.png'%int(nr)),key=lambda f:int(f.split('-')[-1].split('.')[0]))
    sysc={}
    for pg,xf,kind,bar in hits:
        img=Image.open(pngs[pg-1]).convert('L'); W,H=img.size
        if pg not in sysc: sysc[pg]=lay.systems(img)
        # nehme System mit Strich: alle Systeme prüfen, crop um xf in jedem System wo dunkel
        for s in sysc[pg]:
            t=int(s['top']*H); b=int(s['bot']*H); x=int(xf*W)
            col=img.crop((x-1,t,x+2,b))
            if sum(1 for p in col.getdata() if p<160)/max(1,col.size[0]*col.size[1])<0.9: continue
            c=img.crop((x-60,t-25,x+60,b+25)).convert('RGB'); d=ImageDraw.Draw(c); d.text((2,0),'%s/%s b%s'%(nr,pg,bar),fill=(255,0,0))
            crops.append(c)
print(len(crops))
cols=16; w,h=120,crops[0].size[1]
for k in range(0,len(crops),cols*12):
    part=crops[k:k+cols*12]; rows=(len(part)+cols-1)//cols
    m=Image.new('RGB',(cols*w,rows*h),'white')
    for i,c in enumerate(part): m.paste(c.resize((w,h)),((i%cols)*w,(i//cols)*h))
    m.save('rsheet_%d.png'%(k//(cols*12)))
