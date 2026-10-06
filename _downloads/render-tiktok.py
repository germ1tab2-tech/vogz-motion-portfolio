"""Original Vogz promotional TikTok: 1080x1920, 15 s, 30 fps.
Requires Pillow, NumPy and ffmpeg. Run from repository root.
Pass a music-file path to use a 15-second excerpt starting at the optional second argument instead of synthesized audio.
"""
from pathlib import Path
import subprocess,math,wave,sys
import numpy as np
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parent;W,H,FPS,DURATION=1080,1920,30,15
fonts={s:ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',s) for s in (20,24,28,32,36,42,48,60,72,82,96,110,140,180)}
BG='#0f1923';WHITE='#ece8e1';RED='#ff4655';CYAN='#80e5dc'
def text(d,x,y,s,size,c):d.text((x,y),s,font=fonts[size],fill=c)
def center(d,y,s,size,c):text(d,480-fonts[size].getlength(s)/2,y,s,size,c)
def ease(t,start,d=.45):
 x=max(0,min(1,(t-start)/d));return 1-(1-x)**3
# Fresh original 96 BPM electronic bed, synthesized without external audio.
sr=48000;ts=np.arange(DURATION*sr)/sr;audio=np.zeros_like(ts);rng=np.random.default_rng(30)
def freq(n):return 440*2**((n-69)/12)
for beat in range(24):
 u=ts-beat*.625;mask=(u>=0)&(u<.4);v=u[mask]
 audio[mask]+=.20*np.sin(2*np.pi*(48*v+80*.022*(1-np.exp(-v/.022))))*np.exp(-v*13)
 if beat%2:
  mask=(u>=0)&(u<.15);v=u[mask];audio[mask]+=.035*rng.normal(0,1,len(v))*np.exp(-v*30)*np.minimum(v/.006,1)
for step in range(48):
 u=ts-step*.3125;mask=(u>=0)&(u<.055);v=u[mask];noise=rng.normal(0,1,len(v));audio[mask]+=.009*(noise-np.roll(noise,1))*np.exp(-v*70)
for k in range(12):
 chord=((57,60,64),(53,57,60),(55,60,64),(55,59,62))[k%4]
 u=ts-k*1.25;mask=(u>=0)&(u<1.25);v=u[mask];env=np.minimum(v/.05,1)*np.minimum((1.25-v)/.15,1)
 for n in chord:audio[mask]+=.027*np.sin(2*np.pi*freq(n)*v)*env
 audio[mask]+=.08*np.sin(2*np.pi*freq(chord[0]-12)*v)*env
for k in range(48):
 n=(76,79,81,79,77,76,72,76,79,84,83,79,74,79,83,81)[k%16]
 u=ts-k*.3125;mask=(u>=0)&(u<.29);v=u[mask];audio[mask]+=.035*np.sin(2*np.pi*freq(n)*v)*np.minimum(v/.01,1)*np.exp(-v*12)
audio*=np.minimum(ts/.04,1)*np.clip((15-ts)/.6,0,1)
wav=ROOT/'tiktok-temp.wav'
with wave.open(str(wav),'wb') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(sr);f.writeframes((audio*32767).astype('<i2').tobytes())
# Optional user-supplied music, matching the currently delivered version.
if len(sys.argv)>1:
 subprocess.run(['ffmpeg','-y','-v','error','-ss',sys.argv[2] if len(sys.argv)>2 else '21.514' ,'-i',sys.argv[1],'-t','15','-ac','1','-ar','48000','-af','volume=0.8,afade=t=in:st=0:d=0.04,afade=t=out:st=14.4:d=0.6',str(wav)],check=True)
proc=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1920','-r','30','-i','-','-i',str(wav),'-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart','-t','15',str(ROOT/'vogz-offres-tiktok.mp4')],stdin=subprocess.PIPE)
for i in range(450):
 t=i/FPS;im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
 for x in range(0,W,90):d.line((x,0,x,H),fill='#14222e')
 for y in range(0,H,90):d.line((0,y,W,y),fill='#14222e')
 drift=15*math.sin(t);d.polygon([(870+drift,0),(1080,0),(780+drift,1920),(570+drift,1920)],fill='#1a2834')
 d.rectangle((70,190,76,225),fill=RED);text(d,95,189,'VOGZ MOTION STUDIO',28,WHITE)
 text(d,70,1560,'MOTION DESIGN SUR MESURE',20,CYAN)
 if t<2.5:
  center(d,470,'TON CONTENU',60,WHITE)
  a=ease(t,.18);center(d,580+int(50*(1-a)),'MÉRITE',96,WHITE)
  b=ease(t,.55);center(d,710+int(50*(1-b)),'DU MOUVEMENT.',72,RED)
  d.line((190,910,770,910),fill=CYAN,width=3)
  center(d,990,'Créateurs · Streamers · Marques',32,'#adbfcc')
  center(d,1070,'Voilà ce que je peux créer pour toi.',28,'#adbfcc')
 elif t<5.5:
  u=t-2.5;text(d,70,330,'01 / INTROS & LOGOS',36,CYAN)
  a=ease(u,.12);shift=int(100*(1-a))
  d.rectangle((80,560,890,1070),fill='#152631',outline='#456171',width=2)
  center(d,660+shift,'VOGZ',140,WHITE)
  center(d,840,'TON IDENTITÉ EN MOUVEMENT.',24,CYAN)
  ww=int(420*ease(u,.5));d.rectangle((270,930,270+ww,937),fill=RED)
  center(d,1180,'Une signature dès la première seconde.',28,WHITE)
 elif t<8.5:
  u=t-5.5;text(d,70,330,'02 / OUTROS',36,CYAN)
  # A compact original end screen, rendered and animated here.
  x0,y0=80,560;d.rectangle((x0,y0,890,1080),fill='#152631',outline='#456171',width=2)
  text(d,115,605,'MERCI D’AVOIR REGARDÉ.',32,WHITE)
  r=int(63*ease(u,.08));d.ellipse((230-r,845-r,230+r,845+r),fill=RED)
  if u>.4:text(d,195,805,'V.',60,WHITE)
  for k,x in enumerate((390,640)):
   a=ease(u,.45+k*.35);y=760+int(35*(1-a));d.rectangle((x,y,x+210,y+125),fill='#223845',outline=CYAN,width=2)
  text(d,154,950,'ABONNE-TOI',20,WHITE)
  center(d,1180,'Une fin propre. Une raison de revenir.',28,WHITE)
 elif t<11.5:
  u=t-8.5;text(d,70,330,'03 / TITRES & OVERLAYS',36,CYAN)
  d.rectangle((80,560,890,1080),fill='#152631',outline='#456171',width=2)
  a=ease(u,.1);x=int(120-850*(1-a));d.rectangle((x,650,x+600,765),fill=RED)
  text(d,x+30,665,'TON IDÉE, EN GRAND.',42,WHITE)
  a=ease(u,.6);x=int(120-850*(1-a));d.rectangle((x,860,x+530,950),fill=WHITE)
  text(d,x+25,881,'@TONPSEUDO',32,BG)
  center(d,1180,'Tes infos visibles. Ton style reconnaissable.',28,WHITE)
 else:
  u=t-11.5;center(d,410,'TON STYLE.',72,WHITE);center(d,515,'À LA DEMANDE.',72,RED)
  center(d,705,'Gaming · Clean · Pro · Créatif',28,CYAN)
  center(d,860,'INTROS · LOGOS · OUTROS',28,'#adbfcc');center(d,940,'TON PROJET.',60,WHITE)
  a=ease(u,.45);y=int(1140+40*(1-a));d.rectangle((190,y,770,y+110),fill=RED)
  center(d,y+25,'ÉCRIS-MOI EN DM',36,WHITE)
  center(d,1320,'Envoie ton idée ou une référence.',28,'#adbfcc')
 # Subtle fade between scenes, keeping the pacing calm and legible.
 for boundary in (2.5,5.5,8.5,11.5):
  if abs(t-boundary)<.10:
   alpha=int(95*(1-abs(t-boundary)/.10));im=Image.blend(im,Image.new('RGB',(W,H),BG),alpha/255)
 if i==400:im.save(ROOT/'vogz-tiktok-cover.jpg',quality=92)
 proc.stdin.write(im.tobytes())
proc.stdin.close();assert proc.wait()==0;wav.unlink();print('TikTok exporté : 15 s, 1080×1920.')
