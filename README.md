# pyfx
project to learn an impulse response with a neural network

# Overview
- `./app` contains the (GUI) app to load an IR and convolve in realtime, eventually could be replaces with an NN 
- `./training` contains scripts related to label generation and training
- `./examples` contains example scripts for various libs (pysounddevice etc.)

# Setup + requirements
1. Guitar dataset "GuitarSet" downloadable [here](https://zenodo.org/record/3371780)
    - Put the data from `audio_mono-mic.zip` into `./training/data` 
    - other links: (github repo)[https://github.com/marl/guitarset] (website)[https://guitarset.weebly.com/]
1. Guitar amp impulse responses from God's Cab [here](https://wilkinsonaudio.com/products/gods-cab)
    - GuitarSet is 44.1kHz so using an IR from `./Gods_Cab_1.4/44.1`
    - `57_1_inch_cap_pres_1.wav` -> Shure SM57, 1 inch from speaker cap, presence knob at 2. See God's Cab manual for more.

TODO:
 - make app input/output device selection actually work (uses OS defaults right now)
   - allow selecting input channel(s) for the device
 - handle resampling according to device selection (librosa?)


