from subprocess import call
basecmd = ["mplayer", "-ao", "alsa:device=bluetooth"]
myfile = "/home/lab03/Desktop/intertotem/it-u-intertotem/sound/BabyElephantWalk60.wav"
call(basecmd + [myfile])

"""
lab03@raspberrypi:~/Desktop/intertotem/it-u-intertotem $ python sound-test.py
MPlayer 1.4 (Debian), built with gcc-10 (C) 2000-2019 MPlayer Team
do_connect: could not connect to socket
connect: No such file or directory
Failed to open LIRC support. You will not be able to use your remote control.

Playing /home/lab03/Desktop/intertotem/it-u-intertotem/sound/BabyElephantWalk60.wav.
libavformat version 58.45.100 (external)
Audio only file format detected.
Load subtitles in /home/lab03/Desktop/intertotem/it-u-intertotem/sound/
==========================================================================
Opening audio decoder: [pcm] Uncompressed PCM audio decoder
AUDIO: 22050 Hz, 1 ch, s16le, 352.8 kbit/100.00% (ratio: 44100->44100)
Selected audio codec: [pcm] afm: pcm (Uncompressed PCM)
==========================================================================
[AO_ALSA] alsa-lib: pcm.c:2660:(snd_pcm_open_noupdate) Unknown PCM bluetooth
[AO_ALSA] Playback open error: No such file or directory
Failed to initialize audio driver 'alsa:device=bluetooth'
Could not open/initialize audio device -> no sound.
Audio: no sound
Video: no video

"""
