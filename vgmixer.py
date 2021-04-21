# -*- coding: utf-8 -*-
"""
Created on Apr 16 16:28:20 2021

@author: Hsin with references
"""

from AudioLib.AudioProcessing import AudioProcessing
import numpy as np


# To Do: reverb?
def vocal_effect(input_file, echo_en=True, reverb_en=False, low_pass_en=False, high_pass_en=False, mix_level=1, pitch_shift=0):
    
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
    
    return sound1
    

def mixing(vocal, guitar):
    #mixing
    guitar_len = len(guitar)
    vocal_len = len(vocal)
    max_len = max(vocal_len, guitar_len)
    
    mix = np.zeros(max_len)
    mix = np.append(vocal, np.zeros(max_len - vocal_len +1)) + np.append(guitar, np.zeros(max_len - guitar_len+1))
    
    return mix
    
    