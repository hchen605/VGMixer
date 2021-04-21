# -*- coding: utf-8 -*-
"""
Created on Apr 16 16:28:20 2021

@author: Hsin with references
"""
import argparse
from utils import load_midi, write_audio
from guitar_ks import synthesize_notes
import numpy as np
from vgmixer import vocal_effect, mixing


def main(args):
    # midi synthesized
    note, dur = load_midi(args.midi_path)
    guitar_sound = synthesize_notes(note, dur, args.flanger_en, args.chorus_en, args.sr)
    write_audio(args.guitar_oup_path, args.sr, guitar_sound.astype(np.int16))

    # vocals
    vocal_sound = vocal_effect(args.vocals_path).audio_data
    write_audio(args.vocal_oup_path, args.sr, vocal_sound.astype(np.int16))

    # mixing vocal and guitar
    mix_sound = mixing(vocal_sound, guitar_sound)
    write_audio(args.mix_oup_path, args.sr, mix_sound.astype(np.int16))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script to do the prediction with all kinds of network for the speech and music detection task.")

    # input features
    parser.add_argument('--midi_path', type=str, default="assets/hb.mid", help='path to the input midi')
    parser.add_argument('--vocals_path', type=str, default="assets/vocal.wav", help='path to the input vocals')

    # guitar synthesis
    parser.add_argument('--flanger_en', default=False, type=lambda x: (str(x).lower() == 'true'), help="Enable flanger")
    parser.add_argument('--chorus_en', default=False, type=lambda x: (str(x).lower() == 'true'), help="Enable chorus")
    parser.add_argument("--sr", type=int, default=44100, help="Synthesized sampling rate")

    # vocal effect
    parser.add_argument('--echo_en', default=False, type=lambda x: (str(x).lower() == 'true'), help="Enable echo")
    parser.add_argument('--lowpass_en', default=False, type=lambda x: (str(x).lower() == 'true'), help="Enable lowpass filter")
    parser.add_argument('--highpass_en', default=False, type=lambda x: (str(x).lower() == 'true'), help="Enable highpass filter")

    parser.add_argument("--echo", type=int, default=0.1, help="echo rate")
    parser.add_argument("--lowpass_hz", type=int, default=250, help="cut off hz for lowpass filter")
    parser.add_argument("--highpass_hz", type=int, default=250, help="cut off hz for highpass filter")
    parser.add_argument("--volume", type=int, default=1, help="set mixing volume")
    parser.add_argument("--pitch_shift", type=int, default=0, help="set pitch shifting factor")

    # vocal and guitar mixing
    parser.add_argument('--mixing_en', default=False, type=lambda x: (str(x).lower() == 'true'), help="Enable vocal and guitar mixing")

    # output file
    parser.add_argument('--guitar_oup_path', type=str, default="output/hb_guitar.wav", help='path to the output synthesized guitar wav')
    parser.add_argument('--vocal_oup_path', type=str, default="output/hb_vocal.wav", help='path to the output vocal wav')
    parser.add_argument('--mix_oup_path', type=str, default="output/hb_mix.wav", help='path to the output mixing wav')
    args = parser.parse_args()

    main(args)
    