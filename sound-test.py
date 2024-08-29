from subprocess import call
basecmd = ["mplayer", "-ao", "alsa:device=bluetooth"]
myfile = "/home/lab03/Desktop/intertotem/it-u-intertotem/sound/BabyElephantWalk60.wav"
call(basecmd + [myfile])
