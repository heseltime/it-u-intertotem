# info

# 3 main functions: (see code template nb 01)

# get last 10 mins as catalog via get_events
# set min mag

# get_stations to get specific stations
# stations have distance, can get distance to the epi center
# different waves for differents tations
# e.g. get 4 stations, check channels, hard coded

# need to call get_waveforms with that info

# (nb 02)

# next step is stream from get_waveforms to next step (possible intermediate step of creating msd file)
# (for file obspy.read())

# can normalize

# st.write()

# e.g. st.write(out_filepath,
 #        format = 'WAV',
 #        framerate = sps,
 #        rescale = True)

# Q: can get to super collider directly? via buffer, e.g.?

# can potentially compress at this point, before WAV file

# pedalboard for compression of WAV, no super collider here prob better

# sound setup info: Idea: set up on separate device, realize http/other? pipeline of WAV to this new machine

# JACK audio kit running as daemon in bg

# TRAKTOR aido 6 external sound card for quality maybe

# SuperCollider IDE
# see 03_SC folder and scd files

# buffer -> SynthDef -> run Synth 