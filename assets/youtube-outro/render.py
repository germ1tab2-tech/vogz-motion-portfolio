"""Render the 10-second Vogz outro. Requires Pillow and ffmpeg.
Usage: python3 render.py /path/to/user-supplied-music.mp3
The full music file is not distributed with the source.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math,subprocess,json,sys
ROOT=Path(__file__).resolve().parent
selection=json.loads((ROOT/'selection.json').read_text())
if len(sys.argv)!=2:raise SystemExit('Usage: python3 render.py music.mp3')
music=Path(sys.argv[1]).resolve()
if not music.is_file():raise SystemExit('Music file not found')
W,H,FPS=1920,1080,30
bold='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
reg='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
fonts={n:ImageFont.truetype(bold,n) for n in (20,24,28,32,40,66,82)}
small=ImageFont.truetype(reg,26)
def ease(t,start,d=.65):
 x=max(0,min(1,(t-start)/d));return 1-(1-x)**3
def txt(d,x,y,s,size,color):d.text((x,y),s,font=fonts[size],fill=color)
def center(d,cx,y,s,size,color):txt(d,cx-fonts[size].getlength(s)/2,y,s,size,color)
proc=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pixel_format','rgb24','-video_size','1920x1080','-framerate','30','-i','-','-ss',str(selection['source_start']),'-i',str(music),'-map','0:v:0','-map','1:a:0','-t','10','-af','afade=t=in:st=0:d=0.035,afade=t=out:st=9.4:d=0.6,volume=0.8','-c:a','aac','-b:a','192k','-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(ROOT/'demo.mp4')],stdin=subprocess.PIPE)
for i in range(300):
 t=i/FPS;im=Image.new('RGB',(W,H),'#0f1923');d=ImageDraw.Draw(im)
 for x in range(0,W,100):d.line((x,0,x,H),fill='#14212b')
 for y in range(0,H,100):d.line((0,y,W,y),fill='#14212b')
 drift=15*math.sin(t*.5);d.polygon([(1620+drift,0),(1840+drift,0),(1520+drift,H),(1300+drift,H)],fill='#1b2732')
 d.rectangle((100,100,110,145),fill='#ff4655');txt(d,132,103,'VOGZ / MOTION STUDIO',24,'#a7bdc9')
 layer=Image.new('RGBA',(W,H));ld=ImageDraw.Draw(layer)
 a=ease(t,0,.48);txt(ld,110,180+int(28*(1-a)),'MERCI D’AVOIR REGARDÉ.',82,(238,234,226,int(255*a)))
 im=Image.alpha_composite(im.convert('RGBA'),layer).convert('RGB');d=ImageDraw.Draw(im)
 # End-screen subscription target, held steady after its entrance.
 a=ease(t,.499,.46);cx,cy=350,590;r=int(120*a)
 if r:
  pulse=max((math.exp(-max(0,t-onset)*14) for onset in selection['onsets'] if onset<=t),default=0)
  rr=r+12+int(4*pulse)
  d.ellipse((cx-rr,cy-rr,cx+rr,cy+rr),outline='#80e5dc',width=2)
  d.ellipse((cx-r,cy-r,cx+r,cy+r),fill='#ff4655')
 if a>.95:center(d,cx,cy-48,'V.',82,'#ffffff')
 if t>.986:
  center(d,cx,760,'ABONNE-TOI',32,'#ece8e1')
  center(d,cx,815,'LA SUITE ARRIVE.',20,'#80e5dc')
 # Two clean video slots, suitable for YouTube Studio end-screen overlays.
 for k,x in enumerate((750,1280)):
  a=ease(t,.987+k*.487,.44);y=int(480+30*(1-a));ww,hh=470,264
  if a>0:
   d.rectangle((x,y,x+ww,y+hh),fill='#1b2b37',outline='#4a6878',width=2)
   # Corner accents keep the video slots recognizable and unobstructed.
   d.line((x,y+32,x,y,x+32,y),fill='#80e5dc',width=3)
   d.line((x+ww-32,y+hh,x+ww,y+hh,x+ww,y+hh-32),fill='#ff4655',width=3)
  if a>.95:
   center(d,x+ww/2,y+100,'TA VIDÉO ICI',28,'#688797')
   center(d,x+ww/2,795,('À VOIR ENSUITE','À DÉCOUVRIR')[k],24,'#ece8e1')
 if t>1.974:txt(d,750,390,'ON SE RETROUVE DANS LA PROCHAINE.',28,'#80e5dc')
 d.line((110,945,1810,945),fill='#344653',width=1)
 txt(d,110,975,'TON UNIVERS. TON STYLE.',20,'#90a8b8')
 txt(d,1530,975,'VOGZ GAMING',20,'#90a8b8')
 if i==120:im.save(ROOT/'preview.jpg',quality=92)
 proc.stdin.write(im.tobytes())
proc.stdin.close();assert proc.wait()==0
print('Outro exportée : 10 s, 1920×1080, 30 fps, avec la musique fournie.')
