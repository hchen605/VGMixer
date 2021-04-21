'''
    Usage  : python processing.py
    
    Input  : An input WAV file for processing
    Output : A processed WAV audio sample
    
    Note   : Please change the code below to fit your needs.
'''
import numpy as np
from scipy.io.wavfile import read,write
from AudioLib.AudioProcessing import AudioProcessing

#parameters
input_file = 'vocal.wav'
output_file = 'hh_pitch.wav'
sample_freq = 44100
echo_en = 1 
reverb_en = 0
low_pass_en = 0
high_pass_en = 0
mix_level = 1
pitch_shift = 4

sound1 = AudioProcessing(input_file)

if echo_en: 
    sound1.set_echo(0.1)
    
if low_pass_en:
    sound1.set_lowpass(250) #cut off hz
    
if high_pass_en:
    sound1.set_highpass(250)    

if mix_level != 0:
    sound1.set_volume(mix_level)

if pitch_shift > 0:
    sound1.set_audio_pitch(pitch_shift)

#sound1.save_to_file('hh.wav')
write(output_file, sample_freq, sound1.audio_data.astype(np.int16))