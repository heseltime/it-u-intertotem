// Start this script by running
// sclang ./06_standalone_hello_world.scd
// in a linux terminal.

s.doWhenBooted({
	// A simple sine tone synth.
	SynthDef("one_tone_only", {
		var sig;
		var freq = 440;

		sig = SinOsc.ar(freq);
		Out.ar(0, sig);
	}).add;

	s.sync;

	a = Synth("one_tone_only");
});

s.boot;



