'''
    Usage  : python processing.py
    
    Input  : An input WAV file for processing
    Output : A processed WAV audio sample
    
    Note   : Please change the code below to fit your needs.
'''

from AudioLib.AudioProcessing import AudioProcessing

echo_en = 1 
reverb_en = 0
low_pass_en = 0
high_pass_en = 0

sound1 = AudioProcessing('vocal.wav')

if echo_en: 
    sound1.set_echo(0.1)
    
if low_pass_en:
    sound1.set_lowpass(250) #cut off hz
    
if high_pass_en:
    sound1.set_highpass(250)    

sound1.save_to_file('hh.wav')
