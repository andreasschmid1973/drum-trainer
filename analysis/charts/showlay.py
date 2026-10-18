import json, sys, glob
from PIL import Image, ImageDraw
L=json.load(open('layout.json')); ims=[]
for spec in sys.argv[1:]:
    nr,pg=map(int,spec.split(':'))
    png='s%02d-%d.png'%(nr,pg)
    if not glob.glob(png): png=sorted(glob.glob('s%02d-*.png'%nr))[pg-1]
    im=Image.open(png).convert('RGB'); W,H=im.size; d=ImageDraw.Draw(im)
    for b0,n,x0,x1,y0,y1 in L[str(nr)][pg-1]:
        d.rectangle([x0*W+2,y0*H-14,x1*W-2,y1*H+3],outline=(255,0,0),width=2); d.text((x0*W+5,y1*H+2),str(b0),fill=(255,0,0))
    ims.append(im.resize((W*2//3,H*2//3)))
W=sum(i.size[0] for i in ims); H=max(i.size[1] for i in ims); m=Image.new('RGB',(W,H),'gray'); x=0
for i in ims: m.paste(i,(x,0)); x+=i.size[0]
m.save('lay_check.png')
