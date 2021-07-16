import nidaqmx
import numpy as np

Fs = 20000
duration = 60 # in s
numSamples = duration * Fs


## setting up digital outputs on nidaq device
do_task = nidaqmx.Task()
do_task.do_channels.add_do_chan('/Dev1/port0/line0',name_to_assign_to_lines='trigger')
do_task.do_channels.add_do_chan('/Dev1/port0/line7',name_to_assign_to_lines='cameraTrigger')
do_task.timing.cfg_samp_clk_timing(Fs, source='/Dev1/PFI0', samps_per_chan=numSamples)


## building array

do_out = np.zeros([2,numSamples],dtype='bool')
do_out[0,1:-1] = Truetrigger # (tells the intan system when to record and the non-DO nidaq tasks when to start)
cameraRate = 45 # Hz
cameraOnsets = np.int32(np.arange(0.01,duration,1/cameraRate)*Fs) # the sample for camera trigger up
cameraOffsets = np.int32(cameraOnsets+0.005*Fs) # the sample for camera trigger down
for on_off in zip(cameraOnsets,cameraOffsets):
    do_out[1,on_off[0]:on_off[1]] = True

## writing daq outputs onto device
do_task.write(do_out)

# starting the task (if adding other tasks, make sure do_task is started last -- it triggers the others)
do_task.start()
do_task.wait_until_done()
do_task.stop()
