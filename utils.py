# -*- coding: utf-8 -*-
"""
Created on Apr 16 16:28:20 2021

@author: Hsin with references
"""
import numpy as np
import pretty_midi
from scipy.io.wavfile import write


def load_midi(midi_path):
    #read MIDI notes
    note, dur = [], []
    midi_data = pretty_midi.PrettyMIDI(midi_path)
    for instrument in midi_data.instruments:
        for n in instrument.notes:
            # note.velocity 
            note.append(pretty_midi.note_number_to_hz(n.pitch))
            dur.append(int((n.end-n.start)*220))

    audio = np.empty(1)

    return note, dur


def write_audio(oup_path, samplerate, audio):
    write(oup_path, samplerate, audio)