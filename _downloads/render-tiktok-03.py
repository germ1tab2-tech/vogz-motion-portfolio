"""Original kinetic typography exercise. Python + Pillow + ffmpeg.
Usage: python3 render-tiktok-03.py music.mp3
12 seconds, vertical Full HD. User-supplied soundtrack at 22–34 seconds.
"""
from pathlib import Path
import subprocess,sys,math
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parent;W,H=1080,1920
if len(sys.argv)!=2:raise SystemExit('Provide music file')
font='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
fonts={n:ImageFont.truetype(font,n) for n in (20,24,28,32,40,58,90,125,150,170,200)}
def txt(d,x,y,s,size,c):d.text((x,y),s,font=fonts[size],fill=c)
def center(d,y,s,size,c):txt(d,490-fonts[size].getlength(s)/2,y,s,size,c)
def ease(u,d=.45):v=max(0,min(1,u/d));return 1-(1-v)**3
proc=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1920','-r','30','-i','-','-ss','22','-i',sys.argv[1],'-map','0:v:0','-map','1:a:0','-t','12','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-af','volume=0.8,afade=t=in:st=0:d=0.03,afade=t=out:st=11.7:d=0.3','-movflags','+faststart',str(ROOT/'vogz-tiktok-03-motion.mp4')],stdin=subprocess.PIPE)
for i in range(360):
 t=i/30;stage=int(t/4);u=t-stage*4
 if stage==0:
  im=Image.new('RGB',(W,H),'#080f18');d=ImageDraw.Draw(im);c='#a5f0ed';label='01 / FOCUS'
  # Targeting brackets close in, then stay in a calm continuous movement.
  spread=140*(1-ease(u));x0=140-spread;x1=840+spread;y0=625-spread;y1=1125+spread
  for x,y,sx,sy in ((x0,y0,1,1),(x1,y0,-1,1),(x0,y1,1,-1),(x1,y1,-1,-1)):
   d.line((x+65*sx,y,x,y,x,y+65*sy),fill=c,width=4)
  center(d,755+int(95*(1-ease(u))),'FOCUS.',150,c)
  sweep=650+(u%2)/2*450;d.line((155,sweep,825,sweep),fill='#235957',width=2)
  d.line((490,520,490,565),fill=c,width=2);d.line((470,542,510,542),fill=c,width=2)
  center(d,1220,'CAPTER LE REGARD.',28,'#82a7b5')
 elif stage==1:
  im=Image.new('RGB',(W,H),'#eeeae0');d=ImageDraw.Draw(im);c='#151b20';label='02 / FLOW'
  # Smooth offset typography and a moving diagonal ribbon.
  a=ease(u);offset=int(650*(1-a));
  center(d,590-offset,'FLOW',170,c)
  center(d,805,'FLOW',170,'#9da3a0')
  center(d,1020+offset,'FLOW',170,c)
  for k in range(3):
   y=570+k*215;d.line((140,y,840,y),fill='#b8bdb7',width=1)
  d.ellipse((780,1280+int(15*math.sin(u*2)),825,1325+int(15*math.sin(u*2))),fill='#567168')
  center(d,1390,'TROUVER LE RYTHME.',28,'#567168')
 else:
  im=Image.new('RGB',(W,H),'#eb7146');d=ImageDraw.Draw(im);c='#171917';label='03 / MOVE'
  # Moving block, bold words and a drawn directional arrow.
  a=ease(u);xx=90+int(700*(1-a));d.rectangle((xx,610,xx+790,985),fill=c)
  center(d,695,'MOVE.',150,'#f2eedf')
  yy=1090+int(13*math.sin(u*2));d.line((195,yy+115,760,yy+115),fill=c,width=20)
  d.line((645,yy,760,yy+115,645,yy+230),fill=c,width=20)
  center(d,1420,'DONNER DU MOUVEMENT.',28,c)
 txt(d,85,205,'VOGZ / MOTION STUDY',24,c)
 txt(d,85,310,label,20,c)
 txt(d,85,1580,'ESSAI TYPO & ANIMATION',20,c)
 # A minimal segment indicator instead of promotional copy.
 for k in range(3):d.rectangle((85+k*65,1640,130+k*65,1644),fill=c if k<=stage else ('#536568' if stage==0 else '#bfb4a6' if stage==1 else '#bc633f'))
 # Slide between visual worlds without flashing.
 transition=ease(u,.22)
 if stage>0 and u<.22:
  previous='#080f18' if stage==1 else '#eeeae0'
  d.rectangle((int(1080*transition),0,1080,1920),fill=previous)
 if i in (60,180,300):im.save(f'/tmp/vogz-motion-03-{i}.jpg',quality=90)
 if i==60:im.save(ROOT/'vogz-tiktok-03-cover.jpg',quality=92)
 proc.stdin.write(im.tobytes())
proc.stdin.close();assert proc.wait()==0
print('Vidéo motion 03 exportée : 12 s, 1080×1920, sans discours commercial.')
