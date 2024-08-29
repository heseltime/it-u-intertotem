// Boot the server.
s.boot


~houston = Buffer.read(s, "/usr/share/SuperCollider/sounds/a11wlk01-44_1.aiff");
~chouston = Buffer.read(s, "/usr/share/SuperCollider/sounds/a11wlk01.wav");

// Single shot play of the sample.
(
{ PlayBuf.ar(numChannels: 1,
	bufnum: ~houston,
	loop: 0,
	doneAction: 2)}.play
)

{ PlayBuf.ar(1, ~chouston) }.play


// Speed and direction change.
(
{
	var speed;
	var direction;

	speed = LFNoise0.kr(1) * 0.2 + 1;
	direction = LFClipNoise.kr(1);

	PlayBuf.ar(numChannels: 1,
		bufnum: ~houston,
		rate: speed * direction,
		loop: 1);
}.play;
)

