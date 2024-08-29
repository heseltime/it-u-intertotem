// Boot the server.
s.boot


// A simple sine tone synth.
(
SynthDef("one_tone_only", {
	var sig;
	var freq = 440;

	sig = SinOsc.ar(freq, mul:0.5);
	Out.ar(0, sig);
}).add
)

a = Synth("one_tone_only");
a.free


// A sine tone synth with selectable frequency.
(
SynthDef("multiple_tones", {
	arg freq;

	var sig;

	sig = SinOsc.ar(freq: [freq, freq], mul: 0.2);
	Out.ar(0, sig);
}).add
)

// Create three synths with different frequencies.
a = Synth("multiple_tones", [\freq, 550]);
b = Synth("multiple_tones", [\freq, 660]);
c = Synth("multiple_tones", [\freq, 880]);

// Set the frequency using midi notes.
a.set(\freq, 60.midicps)
b.set(\freq, 63.midicps)
c.set(\freq, 65.midicps)

// Stop the synths.
a.free
b.free
c.free

