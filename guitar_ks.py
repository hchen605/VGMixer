# -*- coding: utf-8 -*-
"""
Created on Apr 16 16:28:20 2021

@author: Hsin with references
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as ss
import wave
#import pyaudio
from scipy.io.wavfile import write
from scipy.io.wavfile import read 

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

  def generate_sine(self):
    '''  used for test
    '''
    self.block = np.zeros(100000)
    self.total_len = 100000
    for i in range(100000):
      self.block[i] = np.sin(i*0.02*np.pi)*0.5
    self.__convert_to_int16()


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
    print('Generating...')
    self.block = self.chunk
    self.total_len = length * self.period + len(self.chunk)
    for i in range(length-1):
      self.__buffer()
      self.block = np.append(self.block, self.chunk)
    # convert the result from float to int
    self.__convert_to_int16()
    print('Done. %s frames for total.' % self.total_len)
    return self.block


  def __convert_to_int16(self):
    self.block = self.block*(2**16-1)
    self.block = self.block.astype(np.int16)


  def save_to_file(self, fname):
    '''  Save the generated waveform to a local file with the parameter fname.
    '''
    f = wave.open(fname, 'wb')
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(self.sample_rate)
    f.writeframes(self.block)
    f.close()


  def __counter(self):
    '''  A counter used in the audio callback function.
    '''
    c = 0
    while True:
      yield c
      c = c + 1


  def player_init(self):
    '''  Prepare the data and get ready to play the sound.
    '''
    print('Initializing player...')
    self.player_buffer = 1024
    self.__player_counter = self.__counter()
    align = self.total_len % self.player_buffer
    align_data = np.zeros(self.player_buffer - align).astype(np.int16)
    self.block = np.append(self.block, align_data)
    self.__player_nbuffers = int(len(self.block) / self.player_buffer) - 1
    self.__player_alldata = self.block.tobytes()
    print('Done.')


  def __scope_init(self):
    self.__scope_fft_disp_range = int(self.player_buffer/2)
    
    self.__scope_x = np.arange(self.player_buffer)
    self.__scope_fft_x = self.__scope_x[0:self.__scope_fft_disp_range]*(self.sample_rate/self.player_buffer)
    
    self.__scope_buffer = np.zeros(self.player_buffer)
    self.__scope_fft = np.ones(self.player_buffer)[0:self.__scope_fft_disp_range]
    
    self.__scope_fig = plt.figure()
    self.__scope_ax1 = plt.subplot(211)
    self.__scope_ax2 = plt.subplot(212)
    
    self.__scope_line1, = self.__scope_ax1.plot(self.__scope_x,self.__scope_buffer)
    self.__scope_line2, = self.__scope_ax2.plot(self.__scope_fft_x, self.__scope_fft)
    
    self.__scope_ax1.set_ylim(-(2**15), 2**15-1, auto=None)
    self.__scope_ax2.set_yscale('log')
    self.__scope_ax2.set_xscale('log')
    self.__scope_ax2.set_ylim(1, (65535*self.player_buffer/2), auto=None)
    
    self.__scope_refresh = 1
    
    self.__scope_window = ss.hann(self.player_buffer, sym=False)
    return 0


  def __scope_refresh_buffer(self, n):
    self.__scope_buffer = self.block[n*self.player_buffer:(n+1)*self.player_buffer]
    self.__scope_buffer = self.__scope_buffer * self.__scope_window
    self.__scope_fft = np.abs(np.fft.fft(self.__scope_buffer))[0:self.__scope_fft_disp_range]


  def __scope_draw(self):
    self.__scope_line1.set_ydata(self.__scope_buffer)
    self.__scope_line2.set_ydata(self.__scope_fft)
    self.__scope_fig.canvas.draw()
    self.__scope_fig.canvas.flush_events()

"""
  def __player_callback(self, in_data, frame_count, time_info, status):
    c = next(self.__player_counter)
    rdata = self.__player_alldata[2*c*self.player_buffer:2*(c+1)*self.player_buffer]
    
    self.__scope_refresh_buffer(c)

    if c<self.__player_nbuffers:
      return(rdata, pyaudio.paContinue)
    else:
      self.__scope_refresh=0
      return(rdata, pyaudio.paComplete)


  def play(self):
    self.player_init()
    self.__scope_init()
    p = pyaudio.PyAudio()
    s = p.open(format = p.get_format_from_width(2), channels=1, rate=self.sample_rate, output=True, stream_callback=self.__player_callback)
    s.start_stream()
    while self.__scope_refresh:
      self.__scope_draw()
    s.stop_stream()
    s.close()
    p.terminate()
    plt.close('all')
"""
def generate_wave_input(freq, length, rate=44100, phase=0.0):
    ''' Used by waveform generators to create frequency-scaled input array

        Courtesy of threepineapples:
          https://code.google.com/p/python-musical/issues/detail?id=2
    '''
    length = int(length * rate)
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

if __name__=='__main__':
    
    #parameters
    flanger_en = 1
    chorus_en = 1
    samplerate = 44100
    
    #read MIDI notes
    note = [220, 247, 261]
    dur = [330, 110, 500]
    audio = np.empty(1)
    
    
    for i in range(len(note)):
        k = ks(samplerate, note[i])

        k.set_factor(1)
        #  参数取值为0到1，产生不同音色。为0.5时为鼓音色，1时为拨弦音色
        k.generator(dur[i]) #110 ~ 60bpm 1/8
    
        audio_tmp = k.block
    
        if flanger_en:
            audio_tmp = flanger(audio_tmp, note[i])
    
        if chorus_en:
            audio_tmp = chorus(audio_tmp, note[i])
    
        audio = np.append(audio, audio_tmp)
    
    
    """    
    k = ks(44100, 247)

    k.generator(110)

    if flanger_en:
        audio = np.append(audio, flanger(k.block, 247))
    elif chorus_en:
        audio = np.append(audio, chorus(k.block, 247))
    else:
        audio= np.append(audio, k.block)
        
    #print(audio)
    k = ks(44100, 261)
    k.generator(500)

    if flanger_en:
        audio = np.append(audio, flanger(k.block, 261))
    elif chorus_en:
        audio = np.append(audio, chorus(k.block, 261))
    else:
        audio= np.append(audio, k.block)
    
    """ 
    
    write('hh.wav', samplerate, audio.astype(np.int16))
    
    #audio = flanger(audio, )
    
  
    