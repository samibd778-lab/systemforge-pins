import numpy as np
from PIL import Image
def load(p): return Image.open(p).convert('RGB')
def overlap(a,b):
    A=np.asarray(a.convert('L'),dtype=np.int16); B=np.asarray(b.convert('L'),dtype=np.int16)
    best=(1e9,None)
    for k in range(40,A.shape[0]-40):
        n=A.shape[0]-k
        if n<60: break
        d=np.abs(A[k:k+60]-B[:60]).mean()
        if d<best[0]: best=(d,k)
    return best
def stack(paths,h=900):
    ims=[load(p) for p in paths]
    out=ims[0]
    for b in ims[1:]:
        d,k=overlap(out.crop((0,out.height-582,1440,out.height)),b)
        if d<3: start=out.height-582+k
        else: start=out.height
        new=Image.new('RGB',(1440,start+b.height),'white'); new.paste(out,(0,0)); new.paste(b,(0,start)); out=new
        if out.height>=h: break
    return out.crop((0,0,1440,h))
