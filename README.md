# This repo includes the code of the final project for MUSI-6202

## Scripts description
- main.py: start the pipeline via some input parameters
- vgmixer.py: set the effect of both guitar and vocals and mix them together
- guitar_ks.py: input midi file and generate guitar sound
- utils.py: some basic function, such as loading and writing
- AudioProcessing.py: seting effect, like lowpass, highpass, echo, etc.

## Parameters description
#### IO parameters
- --midi_path: input midi path (default is assets/hb.mid)
- --vocals_path: input vocal sound path (default is assets/vocal.wav)
- --mixing_en: enable guitar and vocal mixing (default is False)
- --guitar_oup_path: path to save the synthesized guitar output (default is output/hb_guitar.wav)
- --vocal_oup_path: path to save the vocal audio output (default is output/hb_vocal.wav)
- --mix_oup_path: path to save the mixing output (default is output/hb_mix.wav)

#### Vocal effect parameters
- --flanger_en: enable flanger effect or not when synthesizing guitar (default is False)
- --chorus_en: enable chorus effect or not when synthesizing guitar (default is False)
- --sr: sampling rate when synthesizing guitar (default is 44100)
- --vc_echo_en: enable echo on vocal audio (default is False)
- --vc_reverb_en: enable reverb on vocal audio (default is False)
- --vc_lowpass_en: enable lowpass filter on vocal audio (default is False)
- --vc_highpass_en: enable highpass filter on vocal audio (default is False)
- --vc_echo: echo rate on vocal audio (default is 0.1)
- --vc_dry: dry rate for reverb on vocal audio (default is 1)
- --vc_wet: wet rate for reverb on vocal audio (default is 1)
- --vc_reverb_gain: gain for reverb on vocal audio (default is 0.1)
- --vc_lowpass_hz: cutoff frequency for lowpass filter on vocal audio (default is 250)
- --vc_highpass_hz: cutoff frequency for highpass filter on vocal audio (default is 250)
- --vc_volume: mixing volume for vocal audio (default is 1)

#### Guitar effect parameters
- --gtr_echo_en: enable echo on guitar audio (default is False)
- --gtr_reverb_en: enable reverb on guitar audio (default is False)
- --gtr_lowpass_en: enable lowpass filter on guitar audio (default is False)
- --gtr_highpass_en: enable highpass filter on guitar audio (default is False)
- --gtr_echo: echo rate on guitar audio (default is 0.1)
- --gtr_dry: dry rate for reverb on guitar audio (default is 1)
- --gtr_wet: wet rate for reverb on guitar audio (default is 1)
- --gtr_reverb_gain: gain for reverb on guitar audio (default is 0.1)
- --gtr_lowpass_hz: cutoff frequency for lowpass filter on guitar audio (default is 250)
- --gtr_highpass_hz: cutoff frequency for highpass filter on guitar audio (default is 250)
- --gtr_volume: mixing volume for guitar audio (default is 1)

## Basic usage 
1. install requirement
` pip install -r requirements.txt`
2. run the script
`python main.py ` or `python main.py --gtr_echo_en True --gtr_echo 0.5`