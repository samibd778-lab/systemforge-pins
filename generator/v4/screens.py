"""Build 1440x900 laptop screens from consecutive 1440x582 shots + zoom crops.
Usage: python3 generator/v4/screens.py <p>   (reads 'screens' and 'zooms' from products/<p>.json)
screens: {name: [shot, shot, ...] or [shot, {"crop":[x0,y0,x1,y1]}...]}
zooms: {name: [shot, [x0,y0,x1,y1]] or [[shot,[box]],[shot,[box]]] for side-by-side}
"""
import sys, json, pathlib
import numpy as np
from PIL import Image
ROOT = pathlib.Path(__file__).resolve().parents[2]
P = sys.argv[1]
CFG = json.load(open(ROOT/f'generator/v4/products/{P}.json'))
D = ROOT/f'generator/v4/scr/{P}'; D.mkdir(parents=True, exist_ok=True)
def shot(n): return Image.open(ROOT/f'shots/hd/{n}.jpg').convert('RGB')
def overlap(a,b):
    A=np.asarray(a.convert('L'),dtype=np.int16); B=np.asarray(b.convert('L'),dtype=np.int16)
    best=(1e9,None)
    for k in range(40,A.shape[0]-60):
        d=np.abs(A[k:k+60]-B[:60]).mean()
        if d<best[0]: best=(d,k)
    return best
def stack(names,h=900):
    out=None
    for n in names:
        if isinstance(n,dict):  # explicit piece: {"shot":..., "y0":..} appended without overlap search
            b=shot(n['shot']).crop((0,n.get('y0',0),1440,582)); start=out.height if out else 0
        else:
            b=shot(n)
            if out is None: out=b; continue
            d,k=overlap(out.crop((0,out.height-582,1440,out.height)),b)
            start=out.height-582+k if d<1.5 else out.height
        new=Image.new('RGB',(1440,start+b.height),'white'); new.paste(out,(0,0)); new.paste(b,(0,start)); out=new
    c=Image.new('RGB',(1440,h),'white'); c.paste(out.crop((0,0,1440,min(h,out.height))),(0,0)); return c
def no_cta(im):
    a=np.asarray(im).astype(int)
    g=(abs(a[:,:,0]-232)<6)&(abs(a[:,:,1]-241)<6)&(abs(a[:,:,2]-236)<6)
    rows=np.where(g[:,300:1300].mean(1)>0.6)[0]
    if len(rows): a[rows.min()-4:rows.max()+5,90:1440]=255
    return Image.fromarray(a.astype('uint8'))
for k,v in CFG['screens'].items():
    no_cta(stack(v)).save(D/f'{k}.png'); print('screen',k)
for k,v in CFG['zooms'].items():
    parts = v if isinstance(v[0],list) else [v]
    ims=[shot(s).crop(tuple(b)) for s,b in parts]
    z=Image.new('RGB',(sum(i.width for i in ims),max(i.height for i in ims)),'white'); x=0
    for i in ims: z.paste(i,(x,0)); x+=i.width
    z.save(D/f'z-{k}.png'); print('zoom',k)
