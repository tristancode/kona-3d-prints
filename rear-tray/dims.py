import importlib.util, math, numpy as np, trimesh, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
D=''
spec=importlib.util.spec_from_file_location('k',D+'kona_organiser.py'); k=importlib.util.module_from_spec(spec); spec.loader.exec_module(k)
m=trimesh.load(D+'kona_organiser.stl')
xb,xf,xt=k.xb,k.xf,k.x_taper; hw=k.half_w
ixf=xf-k.WALL_T; pitch=k.ch_d+k.CRADLE_WALL; zone_x0=ixf-2*pitch
iy0=-hw(zone_x0)+k.WALL_T; cy=iy0+k.END_GAP+k.ch_len/2; y_end=cy+k.ch_len/2
px0=ixf-k.POCKET_L; ystr=hw(px0)-k.WALL_T
fig,ax=plt.subplots(figsize=(15,11))
sec=m.section(plane_origin=[0,0,6],plane_normal=[0,0,1])
p2,T=sec.to_2D(to_2D=np.eye(4))
for poly in p2.polygons_full:
    ax.add_patch(Polygon(np.array(poly.exterior.coords),closed=True,fc='#4682c8',ec='#1b3a5c',lw=0.8))
    for h in poly.interiors: ax.add_patch(Polygon(np.array(h.coords),closed=True,fc='white',ec='#1b3a5c',lw=0.8))
def dim(p1,p2,txt,off=8,col='#c0392b',fs=10):
    p1,p2=np.array(p1,float),np.array(p2,float); d=p2-p1; u=np.array([-d[1],d[0]])/np.linalg.norm(d); n=u*off
    a,b=p1+n,p2+n
    ax.annotate('',xy=b,xytext=a,arrowprops=dict(arrowstyle='<->',color=col,lw=1.2,shrinkA=0,shrinkB=0))
    if off: 
        for p,q in ((p1,a),(p2,b)): ax.plot([p[0],q[0]+u[0]*2*np.sign(off)],[p[1],q[1]+u[1]*2*np.sign(off)],color=col,lw=0.6)
    mid=(a+b)/2+u*(4 if off>=0 else -4); ang=math.degrees(math.atan2(d[1],d[0]))
    if ang>90: ang-=180
    if ang<=-90: ang+=180
    ax.text(mid[0],mid[1],txt,color=col,fontsize=fs,ha='center',va='center',rotation=ang,bbox=dict(fc='white',ec='none',pad=1,alpha=0.85))
hb,hf,ht=hw(xb),hw(xf),hw(xt)
dim((xb,-hb),(xb,hb),f"back {2*hb:.1f}",off=12)
dim((xf,-hf),(xf,hf),f"front {2*hf:.1f}",off=-12)
dim((xb,-hb),(xt,-ht),f"{xt-xb:.1f}",off=-12)
dim((xb,hb),(xt,ht),f"{xt-xb:.1f}",off=12)
sl=math.hypot(xf-xt,hf-ht)
dim((xt,-ht),(xf,-hf),f"taper {sl:.1f}",off=-12)
dim((xt,ht),(xf,hf),f"taper {sl:.1f}",off=12)
dim((xb,-hf),(xf,-hf),f"overall length {xf-xb:.1f}",off=-28,col='#555')
G='#1e7b3a'
dim((zone_x0,iy0+3),(ixf,iy0+3),f"{ixf-zone_x0:.1f}",off=0,col=G,fs=9)
dim((zone_x0-9,cy-k.ch_len/2),(zone_x0-9,y_end),f"balm channel {k.ch_len:.1f}",off=0,col=G,fs=9)
dim((px0+8,y_end+k.CRADLE_WALL),(px0+8,ystr),f"{ystr-y_end-k.CRADLE_WALL:.1f}",off=0,col=G,fs=9)
dim((px0,ystr-8),(ixf,ystr-8),f"fob pocket {k.POCKET_L:.1f}",off=0,col=G,fs=9)
bx0=xb+k.WALL_T; bx1=zone_x0-k.DIV_T
dim((bx0,-10),(bx1,-10),f"main bay {bx1-bx0:.1f} long",off=0,col=G,fs=9)
dim((-40,-hb+k.WALL_T),(-40,hb-k.WALL_T),f"{2*(hb-k.WALL_T):.1f} wide (back)",off=0,col=G,fs=9)
ax.text((xb+xf)/2,-hf-48,f"All sizes in mm. Red = outer edges, green = inside. Height {k.HEIGHT:.0f} mm, walls {k.WALL_T} mm, base {k.FLOOR_T} mm. Front (lip balm end) is on the right. Section cut 6 mm above the base.",ha='center',fontsize=10)
ax.set_title("Kona console organiser - top view with measurements",fontsize=13)
ax.set_aspect('equal'); ax.set_xlim(xb-30,xf+30); ax.set_ylim(-hf-55,hf+25); ax.axis('off')
plt.tight_layout(); plt.savefig(D+'kona_organiser_dimensions.png',dpi=110)
