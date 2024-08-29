s.boot;

NetAddr.langPort

OSCFunc.trace(hideStatusMsg: true)

// Execute the following block to start listening for OSC messages
// with /hello/world path.
// Next run 04_02_osc_hello_world.py to send a hello world message.
// The received message is plotted in the Post window.
(
OSCFunc(
	{
		arg msg, time, addr, recvPort;
		\oneShot.postln;
		msg.postln;
	},
	'/hello/world').oneShot;
)


// Control Sample Playback with OSC

// Prepare the samples path and load the files into the buffers.
(
~cwd = thisProcess.nowExecutingPath.dirname;
~seismo_relpath = "data/seismogram_export_processed.wav";
~seismo_relpath_2 = "data/a11wlk01-44_1.aiff";
~seismo_path = ~cwd +/+ ~seismo_relpath;
~seismo_path_2 = ~cwd +/+ ~seismo_relpath_2;
~seismo = Buffer.read(s, ~seismo_path);
~seismo_2 = Buffer.read(s, ~seismo_path_2);
)

// Create a buffer playback synthdef.
(
SynthDef.new(\seismoPlayer, {
	arg bufnum, speed = 0.1, direction = 1;

	var sig;
	//speed = LFNoise0.kr(1) * 0.2 + 1;
	//direction = LFClipNoise.kr(1);

	sig = PlayBuf.ar(numChannels: 1,
		bufnum: bufnum,
		rate: speed * direction,
		loop: 1);
	Out.ar(0, sig);
	Out.ar(1, sig);
}).add;
)

// Run the synth.
b = Synth.new(\seismoPlayer, [\bufnum, ~seismo, \speed, 0.5]);

// Change paramerters manually
b.set(\speed, 0.05);
b.set(\bufnum, ~seismo);
b.set(\bufnum, ~seismo_2);

// Stop the synth.
b.free;



// Start the OSCFunc listener for speed changes.
(
~ctrl_sampler_speec = OSCFunc(
	{
		arg msg, time, addr, recvPort;
		"Setting speed".postln;
		msg.postln;
		msg[1].postln;
		b.set(\speed, msg[1]);
	},
	'/control/sampler/speed');
)

// Start the OSCFunc listener for source changes.
(
~ctrl_sampler_src = OSCFunc(
	{
		arg msg, time, addr, recvPort;
		"Setting frequency".postln;
		msg.postln;
		msg[1].postln;
		switch (msg[1],
			0, {b.set(\bufnum, ~seismo)},
			1, {b.set(\bufnum, ~seismo_2)},
			{b.set(\bufnum, ~seismo)}
		);
	},
	'/control/sampler/src');
)

// Control the running buffer playback synth using OSC messages sent from
// python scripts.
//
// Change speed.
// python 04_03_control_sampler_speed.py 3
//
// Change buffer.




// Stop the OSC listeners.
(
~ctrl_sampler_speed.free;
~ctrl_sampler_src.free;
)