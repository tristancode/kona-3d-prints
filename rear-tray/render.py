import trimesh, numpy as np, sys
from PIL import Image, ImageDraw
m=trimesh.load('kona_organiser.stl').subdivide_to_size(3.0)
def render(el,az,W=900,H=650,crop=None):
    a,e=np.radians(az),np.radians(el)
    Rz=np.array([[np.cos(a),-np.sin(a),0],[np.sin(a),np.cos(a),0],[0,0,1]])
    Rx=np.array([[1,0,0],[0,np.cos(e),-np.sin(e)],[0,np.sin(e),np.cos(e)]])
    R=Rx@Rz; v=m.vertices@R.T; n=m.face_normals@R.T
    if crop is None: lo,hi=v.min(0),v.max(0)
    else:
        cc=np.array([[x,y,z] for x in (crop[0][0],crop[1][0]) for y in (crop[0][1],crop[1][1]) for z in (crop[0][2],crop[1][2])])@R.T
        lo,hi=cc.min(0),cc.max(0)
    s=0.85*min(W/(hi[0]-lo[0]),H/(hi[1]-lo[1])); c=(lo+hi)/2
    px=(v[:,0]-c[0])*s+W/2; py=H/2-(v[:,1]-c[1])*s; pz=v[:,2]
    L=np.array([-0.4,0.6,0.7]);L/=np.linalg.norm(L)
    shade=np.clip(n@L,0,1)*0.6+0.3
    zb=np.full((H,W),-1e9); img=np.full((H,W,3),245.0); base=np.array([70,130,200])
    for f,sh in zip(m.faces,shade):
        x,y,z=px[f],py[f],pz[f]
        x0,x1=int(max(0,np.floor(x.min()))),int(min(W-1,np.ceil(x.max())))
        y0,y1=int(max(0,np.floor(y.min()))),int(min(H-1,np.ceil(y.max())))
        if x1<x0 or y1<y0: continue
        gx,gy=np.meshgrid(np.arange(x0,x1+1)+.5,np.arange(y0,y1+1)+.5)
        d=(y[1]-y[2])*(x[0]-x[2])+(x[2]-x[1])*(y[0]-y[2])
        if abs(d)<1e-9: continue
        w0=((y[1]-y[2])*(gx-x[2])+(x[2]-x[1])*(gy-y[2]))/d
        w1=((y[2]-y[0])*(gx-x[2])+(x[0]-x[2])*(gy-y[2]))/d; w2=1-w0-w1
        ins=(w0>=-1e-6)&(w1>=-1e-6)&(w2>=-1e-6); zz=w0*z[0]+w1*z[1]+w2*z[2]
        sub=zb[y0:y1+1,x0:x1+1]; upd=ins&(zz>sub); sub[upd]=zz[upd]; img[y0:y1+1,x0:x1+1][upd]=base*sh
    return Image.fromarray(img.astype(np.uint8))
iso=render(-55,200)
close=render(-60,90,crop=(np.array([20,-67,0]),np.array([94,67,20])))
out=Image.new('RGB',(1800,720),(245,245,245)); out.paste(iso,(0,40)); out.paste(close,(900,40))
d=ImageDraw.Draw(out)
d.text((20,10),"Overview (front = left end)",fill=(0,0,0)); d.text((920,10),"From the main bay: half-pencil lift ridges either side of the U finger notch",fill=(0,0,0))
d.text((20,695),(sys.argv[1] if len(sys.argv)>1 else "Kona console organiser v8 - 187 long x 118.5-133 wide x 20 mm - PLA/PETG, no supports"),fill=(0,0,0))
out.save('kona_organiser_preview.png')
