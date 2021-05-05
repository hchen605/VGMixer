# -*- coding: utf-8 -*-
"""
Created on Apr 16 16:28:20 2021

@author: Hsin with references
"""

from AudioProcessing import AudioProcessing
import numpy as np
from utils import load_midi

def set_effect(input_file, echo_en=True, reverb_en=False, low_pass_en=False, high_pass_en=False, \
               echo_rate=0.1, dry=1, wet=1, reverb_gain=0.05, lowpass_cutoff=250.0, highpass_cutoff=250.0,\
               mix_level=1, sr=48000, lowpass_order=5, highpass_order=5):
    '''  Add sound effect for input audio.
  
    Attributes:
    input_file:  Input file, can be two format: input_file_path(str) or input_file_data(sampling rate, np.array).
    echo_en:     Enable echo effect (bool).
    reverb_en:   Enable reverb effect (bool).
    low_pass_en: Enable lowpass filter (bool).
    high_pass_en: Enable highpass filter (bool)
    echo_rate: Echo factor (float)
    lowpass_cutoff: lowpass cutoff frequency (float)
    highpass_cutoff: highpass cutoff freuqnecy (float)
    mix_level: volume of the data. Value should between 0 and 1. Disabled when setting to 0
    '''


    sound1 = AudioProcessing(input_file, sr=sr)
    
    if echo_en: 
        sound1.set_echo(echo_rate)
        
    if low_pass_en:
        sound1.set_lowpass(lowpass_cutoff, lowpass_order) #cut off hz
        
    if high_pass_en:
        sound1.set_highpass(highpass_cutoff, highpass_order)    
    
    if mix_level != 0:
        sound1.set_volume(mix_level)

    if reverb_en:
        sound1.set_reverb(gain_dry=dry, gain_wet=wet, output_gain=reverb_gain)
    
    return sound1
    

def mixing(vocal, guitar):
    #mixing
    guitar_len = len(guitar)
    vocal_len = len(vocal)
    max_len = max(vocal_len, guitar_len)
    
    mix = np.zeros(max_len)
    mix = np.append(vocal, np.zeros(max_len - vocal_len +1)) + np.append(guitar, np.zeros(max_len - guitar_len+1))
    
    return mix
    

def vocal_synth(vocal, midi, sr):
    note, dur, pitch = load_midi(midi)

    sound = np.empty(1)

    for i in range(len(pitch)):
        sound1 = AudioProcessing(vocal, sr=sr)
        sound1.set_audio_pitch(pitch[i]-60)
        synth = sound1.audio_data
        synth = synth[:dur[i]*200]
        #synth = np.append(np.zeros(dur[i]), synth)
        sound = np.append(sound, synth)

    return [sound1.sample_freq, sound.astype(np.float32, order='C') / 32768.0]