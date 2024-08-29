// Boot the server.
s.boot


(
~cwd = thisProcess.nowExecutingPath.dirname;
~seismo_relpath = "data/seismogram_export_processed.wav";
~seismo_path = ~cwd +/+ ~seismo_relpath;
)

~seismo_path.postln;

~seismo = Buffer.read(s, ~seismo_path);

(
{ PlayBuf.ar(numChannels: 1,
	bufnum: ~seismo,
	loop: 0,
	doneAction: 2)}.play
)

(
a = {
	arg speed = 1, direction = 1;

	var sig;
	//speed = LFNoise0.kr(1) * 0.2 + 1;
	//direction = LFClipNoise.kr(1);

	sig = PlayBuf.ar(numChannels: 1,
		bufnum: ~seismo,
		rate: speed * direction,
		loop: 1);
	sig = Mix.new(sig).dup(2) * 0.5;
}.play;
)

a.set(\speed, 4);
a.set(\direction, 1);

a.free;



// Synthdef
(
SynthDef.new(\seismoPlayer, {
	arg speed = 0.1, direction = 1;

	var sig;
	//speed = LFNoise0.kr(1) * 0.2 + 1;
	//direction = LFClipNoise.kr(1);

	sig = PlayBuf.ar(numChannels: 1,
		bufnum: ~seismo,
		rate: speed * direction,
		loop: 1);
	Out.ar(0, sig);
	Out.ar(1, sig);
}).add;
)

b = Synth.new(\seismoPlayer, [\speed, 0.5]);
b.set(\speed, 0.05);
b.free;


