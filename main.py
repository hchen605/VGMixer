# -*- coding: utf-8 -*-
"""
Created on Apr 16 16:28:20 2021

@author: Hsin with references
"""
import argparse
from utils import load_midi, write_audio
from guitar_ks import synthesize_notes
import numpy as np
from vgmixer import set_effect, mixing, vocal_synth


def main(args):
    if args.bit == 64:
        input_bit = 'DOUBLE'
    elif args.bit == 32:
        input_bit = 'PCM_32'
    elif args.bit == 24:
        input_bit = 'PCM_24'
    elif args.bit == 16:
        input_bit = 'PCM_16'
    elif args.bit == 8:
        input_bit = 'PCM_U8'
    else:
        raise 'Please enter either 24, 16 or 8 bit rate.'
    # midi synthesized branch
    note, dur, pitch = load_midi(args.midi_path)
    guitar_sound = synthesize_notes(note, dur, args.flanger_en, args.chorus_en, args.sr, args.flanger_freq, args.chorus_freq)
    guitar_sound = set_effect([args.sr, guitar_sound.astype(np.float32, order='C') / 32768.0], \
                               args.gtr_echo_en, args.gtr_reverb_en, args.gtr_lowpass_en, args.gtr_highpass_en, \
                               args.gtr_echo, args.gtr_dry, args.gtr_wet, args.gtr_reverb_gain, args.gtr_lowpass_hz, args.gtr_highpass_hz,\
                               args.gtr_volume, args.sr, args.gtr_lowpass_order, args.gtr_lowpass_order
                               ).audio_data
                              

    write_audio(args.guitar_oup_path, args.sr, guitar_sound, input_bit)

    # vocals branch
    if args.vc_use_midi:
        vocal_sound = vocal_synth('assets/c_2.wav', args.midi_path, args.sr)
    else:
        vocal_sound = args.vocals_path
    vocal_sound = set_effect(vocal_sound,\
                             args.vc_echo_en, args.vc_reverb_en, args.vc_lowpass_en, args.vc_highpass_en, \
                             args.vc_echo, args.vc_dry, args.vc_wet, args.vc_reverb_gain, args.vc_lowpass_hz, args.vc_highpass_hz, \
                             args.vc_volume, args.sr, args.vc_lowpass_order, args.vc_lowpass_order
                             ).audio_data
    write_audio(args.vocal_oup_path, args.sr, vocal_sound, input_bit)

    # mixing vocal and guitar
    if args.mixing_en:
        mix_sound = mixing(vocal_sound, guitar_sound)
        write_audio(args.mix_oup_path, args.sr, mix_sound, input_bit)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script to do the prediction with all kinds of network for the speech and music detection task.")

    # input features
    parser.add_argument('--midi_path', type=str, default="assets/hb.mid", help='path to the input midi')
    parser.add_argument('--vocals_path', type=str, default="assets/vocal.wav", help='path to the input vocals')
    parser.add_argument("--sr", type=int, default=48000, help="Synthesized sampling rate")
    parser.add_argument("--bit", type=int, default=24, help="Bit rate for output ")

    # guitar synthesis
    parser.add_argument('--flanger_en', default=False, type=lambda x: (str(x).lower() == 'true'), help="Enable flanger")
    parser.add_argument('--chorus_en', default=False, type=lambda x: (str(x).lower() == 'true'), help="Enable chorus")
    parser.add_argument("--flanger_freq", type=float, default=2, help="flanger freq")
    parser.add_argument("--chorus_freq", type=float, default=3, help="chorus freq")

    # vocal effect
    parser.add_argument('--vc_use_midi', default=False, type=lambda x: (str(x).lower() == 'true'), help="Use midi to synth vocal. Default is directly using input vocal audio")
    parser.add_argument('--vc_echo_en', default=False, type=lambda x: (str(x).lower() == 'true'), help="Enable echo")
    parser.add_argument('--vc_reverb_en', default=False, type=lambda x: (str(x).lower() == 'true'), help="Enable reverb")
    parser.add_argument('--vc_lowpass_en', default=False, type=lambda x: (str(x).lower() == 'true'), help="Enable lowpass filter")
    parser.add_argument('--vc_highpass_en', default=False, type=lambda x: (str(x).lower() == 'true'), help="Enable highpass filter")
    parser.add_argument("--vc_echo", type=float, default=0.1, help="echo rate")
    parser.add_argument("--vc_dry", type=float, default=1.0, help="reverb dry")
    parser.add_argument("--vc_wet", type=float, default=1.0, help="reverb wet")
    parser.add_argument("--vc_reverb_gain", type=float, default=0.1, help="reverb gain")
    parser.add_argument("--vc_lowpass_hz", type=float, default=250.0, help="cut off hz for lowpass filter")
    parser.add_argument("--vc_lowpass_order", type=int, default=5, help="order of lowpass filter")
    parser.add_argument("--vc_highpass_hz", type=float, default=250.0, help="cut off hz for highpass filter")
    parser.add_argument("--vc_highpass_order", type=int, default=5, help="order of highpass filter")
    parser.add_argument("--vc_volume", type=float, default=1.0, help="set mixing volume")

    # guitar effect
    parser.add_argument('--gtr_echo_en', default=False, type=lambda x: (str(x).lower() == 'true'), help="Enable echo")
    parser.add_argument('--gtr_reverb_en', default=False, type=lambda x: (str(x).lower() == 'true'), help="Enable reverb")
    parser.add_argument('--gtr_lowpass_en', default=False, type=lambda x: (str(x).lower() == 'true'), help="Enable lowpass filter")
    parser.add_argument('--gtr_highpass_en', default=False, type=lambda x: (str(x).lower() == 'true'), help="Enable highpass filter")
    parser.add_argument("--gtr_echo", type=float, default=0.1, help="echo rate")
    parser.add_argument("--gtr_dry", type=float, default=1, help="reverb dry")
    parser.add_argument("--gtr_wet", type=float, default=1, help="reverb wet")
    parser.add_argument("--gtr_reverb_gain", type=float, default=0.1, help="reverb gain")
    parser.add_argument("--gtr_lowpass_hz", type=float, default=250, help="cut off hz for lowpass filter")
    parser.add_argument("--gtr_lowpass_order", type=int, default=5, help="order of lowpass filter")
    parser.add_argument("--gtr_highpass_hz", type=float, default=250, help="cut off hz for highpass filter")
    parser.add_argument("--gtr_highpass_order", type=int, default=5, help="order of highpass filter")
    parser.add_argument("--gtr_volume", type=float, default=1, help="set mixing volume")

    # vocal and guitar mixing
    parser.add_argument('--mixing_en', default=False, type=lambda x: (str(x).lower() == 'true'), help="Enable vocal and guitar mixing")

    # output file
    parser.add_argument('--guitar_oup_path', type=str, default="output/hb_guitar.wav", help='path to the output synthesized guitar wav')
    parser.add_argument('--vocal_oup_path', type=str, default="output/hb_vocal.wav", help='path to the output vocal wav')
    parser.add_argument('--mix_oup_path', type=str, default="output/hb_mix.wav", help='path to the output mixing wav')
    args = parser.parse_args()

    main(args)
    