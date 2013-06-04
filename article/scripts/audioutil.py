# coding: utf-8

import wave, struct
import numpy as n

# def wavwrite(seq, file, fa):
#     smin = min(seq)
#     smax = max(seq)
#     if smin-smax > 0:
#         seq = [(-.5 + (i-smin)/(smax-smin)) for i in seq]
#     sound = wave.open(file, 'w')
#     sound.setframerate(fa)
#     sound.setsampwidth(2)
#     sound.setnchannels(1)
#     sonic_vector = [i*(2**15-1) for i in seq]
#     sound.writeframes(struct.pack('h' *len(sonic_vector), \
#                                   *[int(i) for i in sonic_vector]))
#     sound.close()

def wavwrite(seq, filename, sr):
    noise_output = wave.open(filename, 'w')
    noise_output.setparams((1, 2, sr, 0, 'NONE', 'not compressed'))
    values = []
    percent = 0
    for i in range(len(seq)):
        if (i*100)/len(seq) > percent:
            percent = (i*100)/len(seq)
        lvalue = seq[i] * (32767)
        lpacked_value = struct.pack('h', lvalue)
        values.append(lpacked_value)

    value_str = ''.join(values)
    noise_output.writeframes(value_str)

    noise_output.close()

def wavread(file):
    wav = wave.open(file, "r")
    nchans, sampwidth, framerate, nframes, comptype, compname = wav.getparams()
    frames = wav.readframes(nframes * nchans)
    out = struct.unpack_from("%dh" % nframes * nchans, frames)
    return n.array(out), framerate
