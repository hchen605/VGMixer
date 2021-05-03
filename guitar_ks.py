# -*- coding: utf-8 -*-
"""
Created on Apr 16 16:28:20 2021

@author: Hsin with references
"""

import numpy as np
import scipy.signal as ss
import wave
from scipy.io.wavfile import read 
import pretty_midi


class ks(object):
  '''  Generate sound wave using Karplus-Strong Algorithm.
  
  Attributes:
    sample_rate:  Sample Rate for the sound wave.
    block:        The data that has been generated.
    total_len:    The number of the generated sample points.
    factor:       The factor used in K-S Algorithm. In a range between 0 and 1.
                  When set to 1, it sounds like a plucked-string. When 0.5, a drum like sound.
  '''


  def __init__(self, sample_rate=44100, freq=220):
    self.sample_rate = sample_rate
    self.period = int(sample_rate / freq)
    #  fill the start-up chunk with random data
    self.chunk = np.random.rand(self.period)
    #  eliminate DC component
    self.chunk = self.chunk - np.mean(self.chunk)
    #  initial the block of the entire sound wave
    self.block = self.chunk
    self.total_len = 0
    self.factor = 1


  def set_factor(self, f):
    self.factor = f

  def __buffer(self):
    '''  The core of the class. Implementing the K-S Algorithm.
    '''
    for i in range(self.period):
      prob = np.random.rand()
      if self.factor>=prob:
        self.chunk[i] = (self.chunk[i-1] + self.chunk[i])*0.5
      else:
        self.chunk[i] = -(self.chunk[i-1] + self.chunk[i])*0.5

  def generator(self, length=500):
    '''  call the __buffer() function for several times to build a complete waveform.
    
    Args:
      length: the number of chunks that build up a block
    '''
    #print('Generating...')
    self.block = self.chunk
    self.total_len = length * self.period + len(self.chunk)
    for i in range(length-1):
      self.__buffer()
      self.block = np.append(self.block, self.chunk)
    # convert the result from float to int
    self.__convert_to_int16()
    #print('Done. %s frames for total.' % self.total_len)
    return self.block

  def __convert_to_int16(self):
    self.block = self.block*(2**16-1)
    self.block = self.block.astype(np.int16)


def generate_wave_input(freq, length, rate=44100, phase=0.0):
    ''' Used by waveform generators to create frequency-scaled input array

        Courtesy of threepineapples:
          https://code.google.com/p/python-musical/issues/detail?id=2
    '''
    length = np.ceil(length * rate)
    t = np.arange(length) / float(rate)
    omega = float(freq) * 2 * np.pi
    phase *= 2 * np.pi  
    return omega * t + phase


def sine(freq, length, rate=44100, phase=0.0):
    ''' Generate sine wave for frequency of 'length' seconds long
        at a rate of 'rate'. The 'phase' of the wave is the percent (0.0 to 1.0)
        into the wave that it starts on.
    '''

    data = generate_wave_input(freq, length, rate, phase)

    return np.sin(data)

def modulated_delay(data, modwave, dry, wet):
    ''' Use LFO "modwave" as a delay modulator (no feedback)
    '''
    out = data.copy()
    for i in range(len(data)):
        index = int(i - modwave[i])
        if index >= 0 and index < len(data):
            out[i] = data[i] * dry + data[index] * wet
    return out


def feedback_modulated_delay(data, modwave, dry, wet):
    ''' Use LFO "modwave" as a delay modulator (with feedback)
    '''
    out = data.copy()
    for i in range(len(data)):
        index = int(i - modwave[i])
        if index >= 0 and index < len(data):
            out[i] = out[i] * dry + out[index] * wet
    return out

def chorus(data, freq, dry=0.5, wet=0.5, depth=1.0, delay=25.0, rate=44100):
    ''' Chorus effect
        http://en.wikipedia.org/wiki/Chorus_effect
    '''
    length = float(len(data)) / rate
    mil = float(rate) / 1000
    delay *= mil
    depth *= mil
    modwave = (sine(freq, length) / 2 + 0.5) * depth + delay
    return modulated_delay(data, modwave, dry, wet)


def flanger(data, freq, dry=0.5, wet=0.5, depth=20.0, delay=1.0, rate=44100):
    ''' Flanger effect
        http://en.wikipedia.org/wiki/Flanging
    '''
    length = float(len(data)) / rate
    mil = float(rate) / 1000
    delay *= mil
    depth *= mil
    modwave = (sine(freq, length) / 2 + 0.5) * depth + delay

    return feedback_modulated_delay(data, modwave, dry, wet)

def synthesize_notes(note, dur, flanger_en=True, chorus_en=True, samplerate=44100):
    audio = np.empty(1)
    for i in range(len(note)):
        k = ks(samplerate, note[i])

        k.set_factor(1)
        k.generator(dur[i]) 

        audio_tmp = k.block
    
        if flanger_en:
            audio_tmp = flanger(audio_tmp, note[i])
    
        if chorus_en:
            audio_tmp = chorus(audio_tmp, note[i])
    
        audio = np.append(audio, audio_tmp)
    return audio
    

