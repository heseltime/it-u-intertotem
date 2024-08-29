from subprocess import call
basecmd = ["mplayer", "-ao", "alsa:device=bluetooth"]
myfile = "/sound/BabyElephantWalk60.wav"
call(basecmd + [myfile])