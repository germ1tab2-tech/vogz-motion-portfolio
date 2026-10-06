"""TikTok 02: original before/after typography concept, 15 seconds.
Usage: python3 render-tiktok-02.py supplied-music.mp3
Requires Pillow and ffmpeg. Uses the supplied music at 22–37 seconds.
"""
from pathlib import Path
import math,subprocess,sys
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parent
if len(sys.argv)!=2:raise SystemExit('Provide the music file path.')
W,H,FPS,DURATION=1080,1920,30,15
fonts={s:ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',s) for s in (20,24,28,32,36,42,48,60,68,78,88,96,110,140)}
regular=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',36)
BG=(17,12,31);WHITE='#f1e9ff';PURPLE='#b391ff';GOLD='#f2cc89';CX=485
frames_to_check={30,90,180,315,410}
def text(d,x,y,s,size,c):d.text((x,y),s,font=fonts[size],fill=c)
def center(d,y,s,size,c,cx=CX):text(d,cx-fonts[size].getlength(s)/2,y,s,size,c)
def ease(t,start,d=.48):
 x=max(0,min(1,(t-start)/d));return 1-(1-x)**3
def blend(a,b,p):return tuple(int(x+(y-x)*p) for x,y in zip(a,b))
def decorated_demo(im,box,u,small=False):
 # Original animated typography scene, drawn at its final display dimensions.
 d=ImageDraw.Draw(im);x,y,w,h=box;cx=x+w/2;cy=y+h/2
 d.rounded_rectangle((x,y,x+w,y+h),radius=12,fill='#241535',outline='#72589b',width=2)
 # Orbital arcs and gold accent create a different visual identity.
 r=min(w,h)*.36;phase=u*.6
 for k in range(3):
  rr=r+18*k;d.arc((cx-rr,cy-rr,cx+rr,cy+rr),start=(phase*55+k*110)%360,end=(phase*55+k*110)%360+165,fill=('#76569f','#57406f','#9878c5')[k],width=2)
 px=cx+rr*math.cos(phase);py=cy+rr*math.sin(phase);d.ellipse((px-4,py-4,px+4,py+4),fill=GOLD)
 if small:
  center(d,y+105,'NOUVELLE',24,WHITE,cx);center(d,y+151,'VIDÉO.',36,GOLD,cx)
 else:
  a=ease(u,0);b=ease(u,.245)
  center(d,y+185+int(45*(1-a)),'NOUVELLE',68,WHITE,cx)
  center(d,y+285+int(45*(1-b)),'VIDÉO.',96,GOLD,cx)
  linew=int(170*ease(u,.74));d.rectangle((cx-linew/2,y+420,cx+linew/2,y+423),fill=PURPLE)
  if u>.986:center(d,y+475,'UNE IDÉE. TON UNIVERS.',20,PURPLE,cx)
proc=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1920','-r','30','-i','-','-ss','22','-i',sys.argv[1],'-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-af','volume=0.8,afade=t=in:st=0:d=0.04,afade=t=out:st=14.4:d=0.6','-t','15','-movflags','+faststart',str(ROOT/'vogz-tiktok-02-avant-apres.mp4')],stdin=subprocess.PIPE)
for i in range(FPS*DURATION):
 t=i/FPS;im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
 # Restricted visual safe area, preserving the right-side TikTok controls.
 for k in range(26):
  x=80+(k*173)%800;y=260+(k*137)%1190
  v=int(50+15*math.sin(t*.5+k));d.ellipse((x,y,x+2,y+2),fill=(v,v-8,v+15))
 d.line((70,180,70,224),fill=GOLD,width=3);text(d,95,186,'VOGZ MOTION STUDIO',28,WHITE)
 text(d,70,1530,'DÉMONSTRATION / MOTION DESIGN',20,'#9e8aae')
 if t<2:
  center(d,490,'MÊME TEXTE.',68,WHITE)
  a=ease(t,.25);center(d,605+int(45*(1-a)),'AUTRE',88,PURPLE)
  center(d,715+int(45*(1-a)),'IMPACT.',96,GOLD)
  center(d,1020,'Regarde la différence.',36,WHITE)
 elif t<4:
  text(d,90,370,'01 / AVANT',32,'#b8a8c7')
  d.rectangle((80,550,890,1160),fill='#16151b',outline='#48434e',width=2)
  label='Nouvelle vidéo';d.text((CX-regular.getlength(label)/2,815),label,font=regular,fill='#b5b1b8')
  center(d,1240,'Un titre simple.',32,'#b8a8c7')
 elif t<9:
  u=t-4;text(d,90,370,'02 / APRÈS',32,GOLD)
  decorated_demo(im,(80,550,810,610),u)
  d=ImageDraw.Draw(im)
  center(d,1230,'Du rythme. Une identité.',32,WHITE)
  center(d,1300,'Un style créé sur mesure.',28,PURPLE)
 elif t<12:
  u=t-9;center(d,410,'LA DIFFÉRENCE ?',60,WHITE)
  d.rounded_rectangle((70,610,465,1020),radius=10,fill='#16151b',outline='#48434e',width=2)
  center(d,775,'Nouvelle vidéo',24,'#aaa4b0',267)
  decorated_demo(im,(495,610,395,410),u,True);d=ImageDraw.Draw(im)
  center(d,1090,'AVANT',28,'#b8a8c7',267);center(d,1090,'APRÈS',28,GOLD,692)
  center(d,1260,'Le même message.',32,WHITE)
  center(d,1330,'Une autre façon de le montrer.',28,PURPLE)
 else:
  u=t-12;center(d,435,'TON UNIVERS.',68,WHITE)
  center(d,545,'EN MOUVEMENT.',68,GOLD)
  center(d,790,'Intros · Logos · Outros',28,WHITE)
  center(d,850,'Titres · Overlays · Clips',28,PURPLE)
  a=ease(u,.15);y=1050+int(30*(1-a));d.rounded_rectangle((180,y,790,y+115),radius=8,fill=GOLD)
  center(d,y+30,'ENVOIE TON IDÉE EN DM',32,BG)
  center(d,1250,'Tous les styles, à la demande.',28,WHITE)
  center(d,1350,'@vogzmotionstudio',24,PURPLE)
 # Brief soft scene transitions, with no strobing.
 for boundary in (2,4,9,12):
  delta=abs(t-boundary)
  if delta<.08:im=Image.blend(im,Image.new('RGB',(W,H),BG),.30*(1-delta/.08))
 if i in frames_to_check:im.save('/tmp/vogz-tiktok-02-frame-'+str(i)+'.jpg',quality=88)
 if i==180:im.save(ROOT/'vogz-tiktok-02-cover.jpg',quality=92)
 proc.stdin.write(im.tobytes())
proc.stdin.close();assert proc.wait()==0
print('Vidéo 02 exportée : 15 s, 1080×1920, Astra 22–37 s, sans prix.')
