# -*- coding: utf-8 -*-
"""
Created on Apr 16 16:28:20 2021

@author: Hsin with references
"""
import argparse
from utils import load_midi, write_audio
from guitar_ks import synthesize_notes
import numpy as np
from vgmixer import set_effect, mixing


def main(args):
    # midi synthesized branch
    note, dur = load_midi(args.midi_path)
    guitar_sound = synthesize_notes(note, dur, args.flanger_en, args.chorus_en, args.sr)
    guitar_sound = set_effect([args.sr, guitar_sound.astype(np.float32, order='C') / 32768.0], \
                               args.gtr_echo_en, args.gtr_reverb_en, args.gtr_lowpass_en, args.gtr_highpass_en, \
                               args.gtr_echo, args.gtr_dry, args.gtr_wet, args.gtr_reverb_gain, args.gtr_lowpass_hz, args.gtr_highpass_hz,\
                               args.gtr_volume, args.gtr_pitch_shift,
                               ).audio_data
                              

    write_audio(args.guitar_oup_path, args.sr, guitar_sound)

    # vocals branch
    vocal_sound = set_effect(args.vocals_path,\
                             args.vc_echo_en, args.vc_reverb_en, args.vc_lowpass_en, args.vc_highpass_en, \
                             args.vc_echo, args.vc_dry, args.vc_wet, args.vc_reverb_gain, args.vc_lowpass_hz, args.vc_highpass_hz, \
                             args.vc_volume, args.vc_pitch_shift,
                             ).audio_data
    write_audio(args.vocal_oup_path, args.sr, vocal_sound)

    # mixing vocal and guitar
    mix_sound = mixing(vocal_sound, guitar_sound)
    write_audio(args.mix_oup_path, args.sr, mix_sound)


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
    parser.add_argument('--vc_echo_en', default=False, type=lambda x: (str(x).lower() == 'true'), help="Enable echo")
    parser.add_argument('--vc_reverb_en', default=False, type=lambda x: (str(x).lower() == 'true'), help="Enable reverb")
    parser.add_argument('--vc_lowpass_en', default=False, type=lambda x: (str(x).lower() == 'true'), help="Enable lowpass filter")
    parser.add_argument('--vc_highpass_en', default=False, type=lambda x: (str(x).lower() == 'true'), help="Enable highpass filter")
    parser.add_argument("--vc_echo", type=int, default=0.1, help="echo rate")
    parser.add_argument("--vc_dry", type=int, default=1, help="reverb dry")
    parser.add_argument("--vc_wet", type=int, default=1, help="reverb wet")
    parser.add_argument("--vc_reverb_gain", type=int, default=0.1, help="reverb gain")
    parser.add_argument("--vc_lowpass_hz", type=int, default=250, help="cut off hz for lowpass filter")
    parser.add_argument("--vc_highpass_hz", type=int, default=250, help="cut off hz for highpass filter")
    parser.add_argument("--vc_volume", type=int, default=1, help="set mixing volume")
    parser.add_argument("--vc_pitch_shift", type=int, default=0, help="set pitch shifting factor")

    # guitar effect
    parser.add_argument('--gtr_echo_en', default=False, type=lambda x: (str(x).lower() == 'true'), help="Enable echo")
    parser.add_argument('--gtr_reverb_en', default=False, type=lambda x: (str(x).lower() == 'true'), help="Enable reverb")
    parser.add_argument('--gtr_lowpass_en', default=False, type=lambda x: (str(x).lower() == 'true'), help="Enable lowpass filter")
    parser.add_argument('--gtr_highpass_en', default=False, type=lambda x: (str(x).lower() == 'true'), help="Enable highpass filter")
    parser.add_argument("--gtr_echo", type=int, default=0.1, help="echo rate")
    parser.add_argument("--gtr_dry", type=int, default=1, help="reverb dry")
    parser.add_argument("--gtr_wet", type=int, default=1, help="reverb wet")
    parser.add_argument("--gtr_reverb_gain", type=int, default=0.1, help="reverb gain")
    parser.add_argument("--gtr_lowpass_hz", type=int, default=250, help="cut off hz for lowpass filter")
    parser.add_argument("--gtr_highpass_hz", type=int, default=250, help="cut off hz for highpass filter")
    parser.add_argument("--gtr_volume", type=int, default=1, help="set mixing volume")
    parser.add_argument("--gtr_pitch_shift", type=int, default=0, help="set pitch shifting factor")

    # vocal and guitar mixing
    parser.add_argument('--mixing_en', default=False, type=lambda x: (str(x).lower() == 'true'), help="Enable vocal and guitar mixing")

    # output file
    parser.add_argument('--guitar_oup_path', type=str, default="output/hb_guitar.wav", help='path to the output synthesized guitar wav')
    parser.add_argument('--vocal_oup_path', type=str, default="output/hb_vocal.wav", help='path to the output vocal wav')
    parser.add_argument('--mix_oup_path', type=str, default="output/hb_mix.wav", help='path to the output mixing wav')
    args = parser.parse_args()

    main(args)
    