"""Render the original Vogz YouTube demo. Requires Python, Pillow, NumPy and ffmpeg.
Run: python3 render.py. Output: demo.mp4 (1080p, 30 fps, 5 seconds).
"""
from pathlib import Path
import math, subprocess, wave
from PIL import Image, ImageDraw, ImageFont
import numpy as np
ROOT=Path(__file__).resolve().parent
W,H,FPS,DURATION=1920,1080,30,5
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
REG='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
fonts={s:ImageFont.truetype(FONT,s) for s in (22,26,32,38,46,64,106,116)}
regular=ImageFont.truetype(REG,30)
def ease(t,start,duration=.65):
 x=max(0,min(1,(t-start)/duration));return 1-(1-x)**3
def text(draw,pos,label,size,color):draw.text(pos,label,font=fonts[size],fill=color)
def width(label,size):return fonts[size].getlength(label)
# Original synthesized sound: quiet transition sweeps and a two-note accent.
sr=48000;ts=np.arange(sr*DURATION)/sr;rng=np.random.default_rng(8);sound=np.zeros_like(ts)
for start in (.18,1.15,2.8):
 u=ts-start;mask=(u>=0)&(u<.3);sound[mask]+=rng.normal(0,.055,mask.sum())*np.sin(np.pi*u[mask]/.3)**2
for start,freq in ((2.95,660),(3.08,880)):
 u=ts-start;mask=(u>=0)&(u<.3);sound[mask]+=.10*np.sin(2*np.pi*freq*u[mask])*np.exp(-u[mask]*14)*np.minimum(u[mask]/.012,1)
wav=ROOT/'sound.wav'
with wave.open(str(wav),'wb') as f:
 f.setnchannels(1);f.setsampwidth(2);f.setframerate(sr);f.writeframes((np.clip(sound,-1,1)*32767).astype('<i2').tobytes())
cmd=['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pixel_format','rgb24','-video_size',f'{W}x{H}','-framerate',str(FPS),'-i','-','-i',str(wav),'-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart','-shortest',str(ROOT/'demo.mp4')]
proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
for frame in range(FPS*DURATION):
 t=frame/FPS;im=Image.new('RGB',(W,H),'#101922');d=ImageDraw.Draw(im)
 for x in range(0,W,80):d.line((x,0,x,H),fill='#17232d')
 for y in range(0,H,80):d.line((0,y,W,y),fill='#17232d')
 # A gently sliding diagonal and the studio corner marks.
 drift=int(20*math.sin(t*.8));d.polygon([(1400+drift,0),(1700+drift,0),(1300+drift,H),(1000+drift,H)],fill='#1e2933')
 d.line((96,130,96,82,144,82),fill='#ff4655',width=3);d.line((1776,998,1824,998,1824,950),fill='#80e5dc',width=3)
 text(d,(140,89),'VOGZ / MOTION STUDIO',26,'#bcc9d1');text(d,(140,942),'CONCEPT YOUTUBE  /  16:9',22,'#8d9eab')
 text(d,(1580,942),'DEMO / 01',22,'#8d9eab')
 # Intro: clean kinetic typography, staged line entrances.
 a=ease(t,.12);x=int(140-140*(1-a));y=252
 layer=Image.new('RGBA',(W,H));ld=ImageDraw.Draw(layer)
 text(ld,(x,y),'TON CONTENU.',106,(238,238,231,int(255*a)))
 b=ease(t,.48);text(ld,(int(140-140*(1-b)),382),'PLUS D’IMPACT.',116,(255,70,85,int(255*b)))
 c=ease(t,1.05);ld.rectangle((140,559,140+int(125*c),565),fill=(128,229,220,255))
 ld.text((140,int(611+20*(1-c))),'Une identité qui se remarque. Dès la première seconde.',font=regular,fill=(176,192,203,int(255*c)))
 im=Image.alpha_composite(im.convert('RGBA'),layer).convert('RGB');d=ImageDraw.Draw(im)
 # A custom play symbol, drawn as geometry rather than a borrowed logo.
 p=ease(t,.28);cx,cy=1510,380;size=int(95*p)
 d.rounded_rectangle((cx-size,cy-size*.7,cx+size,cy+size*.7),radius=22,fill='#ff4655')
 if size:d.polygon([(cx-20*p,cy-31*p),(cx-20*p,cy+31*p),(cx+34*p,cy)],fill='#ffffff')
 # CTA enters after the title has time to read.
 q=ease(t,2.65,.5);by=int(765+65*(1-q));bw=int(360*q)
 if bw>0:
  d.rounded_rectangle((140,by,140+bw,by+86),radius=8,fill='#eeeae3')
  if q>.95:
   text(d,(163,by+21),'ABONNE-TOI',32,'#101922');text(d,(440,by+15),'+',38,'#ff4655')
 if t>3.5:
  r=ease(t,3.5,.4);text(d,(int(552+18*(1-r)),by+25),'LA SUITE ARRIVE.',26,'#80e5dc')
 d.rectangle((140,898,1780,901),fill='#2a3a46');d.rectangle((140,898,140+int(1640*t/DURATION),901),fill='#ff4655')
 if frame==100:im.save(ROOT/'preview.jpg',quality=90)
 proc.stdin.write(im.tobytes())
proc.stdin.close()
if proc.wait()!=0:raise RuntimeError('ffmpeg failed')
wav.unlink()
print(ROOT/'demo.mp4')
