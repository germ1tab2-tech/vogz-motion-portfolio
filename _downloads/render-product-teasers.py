"""Two original illustrated product teasers, not real product demonstrations.
Requires Pillow and ffmpeg. Run from repository root.
"""
from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import math,subprocess
ROOT=Path(__file__).resolve().parent;W,H=1080,1920;FPS=30;D=10
fonts={n:ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',n) for n in (22,26,30,34,40,48,58,68,82)}
BG='#f2eee6';INK='#263c35';GREEN='#557969';CX=480
music=ROOT.parent/'assets/youtube-demo/demo.mp4'
def center(d,y,s,n,c=INK):d.text((CX-fonts[n].getlength(s)/2,y),s,font=fonts[n],fill=c)
def ease(u):p=max(0,min(1,u/.45));return 1-(1-p)**3
for product in ('bac','crochets'):
 output=ROOT/f'tiktok-{product}-apercu.mp4'
 proc=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1920','-r','30','-i','-','-stream_loop','-1','-i',str(music),'-map','0:v:0','-map','1:a:0','-t','10','-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-c:a','aac','-af','volume=0.45,afade=t=out:st=9.5:d=0.5','-movflags','+faststart',str(output)],stdin=subprocess.PIPE)
 for i in range(D*FPS):
  t=i/FPS;im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
  d.text((80,195),'MAISON / UNE IDÉE À TESTER',font=fonts[26],fill=GREEN)
  d.line((80,275,880,275),fill='#d2d7ca',width=2)
  # Original flat illustrations: neither supplier footage nor a simulated test.
  if product=='bac':
   if t<3:
    center(d,365,'LE FILTRE',68);center(d,450,'À NETTOYER ?',68)
    center(d,1220,'Et l’eau à récupérer…',34,GREEN)
   elif t<7:
    center(d,365,'UNE PISTE :',58);center(d,455,'UN BAC DE VIDANGE.',48)
    center(d,1220,'À placer sous l’ouverture du filtre.',30,GREEN)
   else:
    center(d,365,'JE LE TESTE',68);center(d,455,'À RÉCEPTION.',68)
    center(d,1220,'Dimensions, passage, récupération.',30,GREEN)
   yy=695+int(14*math.sin(t*1.5));d.rounded_rectangle((135,yy,825,yy+400),radius=35,fill='#d7dfd5',outline='#6f8b7b',width=5)
   d.rounded_rectangle((172,yy+36,788,yy+335),radius=24,fill='#f9faf5',outline='#a1b4a6',width=3)
   d.line((180,yy+350,780,yy+350),fill='#9fb29f',width=3)
   # A stylized notch, not a claim of a precise compatible model.
   d.rectangle((383,yy-5,575,yy+43),fill=BG);d.line((383,yy+43,575,yy+43),fill='#6f8b7b',width=4)
  else:
   if t<3:
    center(d,365,'PETITE SALLE',68);center(d,455,'DE BAIN ?',68)
    center(d,1220,'Une place pour suspendre ?',34,GREEN)
   elif t<7:
    center(d,365,'DES CROCHETS',68);center(d,455,'POUR LE RAIL.',58)
    center(d,1220,'Ouverture annoncée : 25 mm.',30,GREEN)
   else:
    center(d,365,'JE VÉRIFIE',68);center(d,455,'LA TENUE.',68)
    center(d,1220,'Compatibilité et usage, à réception.',30,GREEN)
   # Graphic representation of hook and rail; no loaded towel or fake result.
   yy=760+int(12*math.sin(t*1.5));d.rounded_rectangle((160,yy,810,yy+65),radius=30,fill='#bcc7c0',outline='#7c9283',width=3)
   for x in (315,590):
    d.arc((x-62,yy-65,x+62,yy+90),180,360,fill=GREEN,width=32)
    d.line((x+62,yy+12,x+62,yy+220),fill=GREEN,width=32)
    d.arc((x-22,yy+170,x+62,yy+255),0,180,fill=GREEN,width=32)
  center(d,1370,'Tu veux voir le test ?',34)
  d.text((80,1540),'ILLUSTRATION / TEST À VENIR',font=fonts[26],fill=GREEN)
  d.text((80,1600),'Les performances restent à vérifier.',font=fonts[22],fill='#738679')
  if i==160:im.save(ROOT/f'tiktok-{product}-cover.jpg',quality=90)
  proc.stdin.write(im.tobytes())
 proc.stdin.close();assert proc.wait()==0
 print(output.name)
