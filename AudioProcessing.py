'''
	File: AudioProcessing.py
	Description: A python class to perform low level DSP processing on a given input audio data
	Version: 1 (Tested to work with WAV files)

	How to use:

	from AudioLib.AudioProcessing import AudioProcessing

	# Read in WAV file into Python Class
	sound1 = AudioProcessing('input.wav')

	# Add an echo to the audio
	sound1.set_echo(1)

	# Set audio volume
	sound1.set_volume(1)

	# Set lowpass filter
	sound1.set_lowpass(250)

	# Set highpass filter
	sound1.set_highpass(250)

	# Set reverb 
	sound1.set_reverb()
'''

import sys, wave
import numpy as np
from numpy import array, int16
from scipy.signal import lfilter, butter
from scipy.io.wavfile import read, write
from scipy import signal
from scipy.signal import convolve
import librosa


class AudioProcessing(object):

	__slots__ = ('audio_data', 'sample_freq')

	def __init__(self, input_audio=None, sr=48000):
		if type(input_audio) is str:
			self.audio_data, self.sample_freq = librosa.load(input_audio, sr=sr)
		elif type(input_audio) is list:
			self.sample_freq, self.audio_data = input_audio
		else:
			raise "Please pass either input audio or audio path for this function."
		
		if len(self.audio_data.shape) == 2:
			self.audio_data = AudioProcessing.convert_to_mono_audio(self.audio_data)

	def set_echo(self, delay):
		print('set echo')
		'''Applies an echo that is 0...<input audio duration in seconds> seconds from the beginning'''
		output_audio = np.zeros(len(self.audio_data))
		output_delay = delay * self.sample_freq

		for count, e in enumerate(self.audio_data):
			output_audio[count] = e + self.audio_data[count - int(output_delay)]

		self.audio_data = output_audio

	def set_volume(self, level):
		print('set volume')
		'''Sets the overall volume of the data via floating-point factor'''
		output_audio = np.zeros(len(self.audio_data))

		for count, e in enumerate(self.audio_data):
			output_audio[count] = (e * level)

		self.audio_data = output_audio

	def set_lowpass(self, cutoff_low, order=5):
		print('set lowpass')
		'''Applies a low pass filter'''
		nyquist = self.sample_freq / 2.0
		cutoff = cutoff_low / nyquist
		x, y = signal.butter(order, cutoff, btype='lowpass', analog=False)
		self.audio_data = signal.filtfilt(x, y, self.audio_data)

	def set_highpass(self, cutoff_high, order=5):
		print('set highpass')
		'''Applies a high pass filter'''
		nyquist = self.sample_freq / 2.0
		cutoff = cutoff_high / nyquist
		x, y = signal.butter(order, cutoff, btype='highpass', analog=False)
		self.audio_data = signal.filtfilt(x, y, self.audio_data)

	def set_reverb(self, reverb_in='assets/Conic Long Echo Hall.wav', gain_dry=1, gain_wet=1, output_gain=0.05):
		print('set reverb')
		reverb = librosa.load(reverb_in, sr=self.sample_freq)[0]
		total_samples_sample = self.audio_data.shape[-1]
		reverb_out = np.zeros([np.shape(self.audio_data)[0] + np.shape(reverb)[0] - 1], dtype = np.float64)
		self.audio_data = output_gain * (convolve(self.audio_data * gain_dry, reverb * gain_wet, method = 'fft'))
	
	@staticmethod
	def convert_to_mono_audio(input_audio):
		'''Returns a numpy array that represents the mono version of a stereo input'''
		output_audio = []
		temp_audio = input_audio.astype(float)

		for e in temp_audio:
			output_audio.append((e[0] / 2) + (e[1] / 2))

		return np.array(output_audio)

	def set_audio_speed(self, speed_factor):
		'''Sets the speed of the audio by a floating-point factor'''
		sound_index = np.round(np.arange(0, len(self.audio_data), speed_factor))
		self.audio_data = self.audio_data[sound_index[sound_index < len(self.audio_data)].astype(int)]
		
		
	def set_audio_pitch(self, n, window_size=2**13, h=2**11):
		'''Sets the pitch of the audio to a certain threshold'''
		factor = 2 ** (1.0 * n / 12.0)
		self._set_stretch(1.0 / factor, window_size, h)
		self.audio_data = self.audio_data[window_size:]
		self.set_audio_speed(factor)

	def _set_stretch(self, factor, window_size, h):
		phase = np.zeros(window_size)
		hanning_window = np.hanning(window_size)
		result = np.zeros(int(len(self.audio_data) / factor + window_size))

		for i in np.arange(0, len(self.audio_data) - (window_size + h), h*factor):
			# Two potentially overlapping subarrays
			a1 = self.audio_data[int(i): int(i + window_size)]
			a2 = self.audio_data[int(i + h): int(i + window_size + h)]

			# The spectra of these arrays
			s1 = np.fft.fft(hanning_window * a1)
			s2 = np.fft.fft(hanning_window * a2)

			# Rephase all frequencies
			phase = (phase + np.angle(s2/s1)) % 2*np.pi

			a2_rephased = np.fft.ifft(np.abs(s2)*np.exp(1j*phase))
			i2 = int(i / factor)
			result[i2: i2 + window_size] += hanning_window*a2_rephased.real

		# normalize (16bit)
		result = ((2 ** (16 - 4)) * result/result.max())
		self.audio_data = result.astype('int16')	   