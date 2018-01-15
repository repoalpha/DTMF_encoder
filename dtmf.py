'''

 DTMF
                1209 Hz 1336 Hz 1477 Hz 1633 Hz
        697 Hz  1       2       3       A
        770 Hz  4       5       6       B
        852 Hz  7       8       9       C
        941 Hz  *       0       #       D

2015
originally modified from Noah Spurrier noah@noah.org

2018 ***new sections***

Fader - fades samples to remove clicks between samples due to different phase angles
DTMF digit record save as csv file - use with deeplearning
record audio as a wave file for playback - use for deeplearning

'''

import math
import numpy as np
import pyaudio
import sys
import time
import wave
import csv

FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "dtmf.wav"
p = pyaudio.PyAudio()

def sine_wave(frequency, length, rate):
    length = int(length * rate)
    factor = float(frequency) * (math.pi * 2) / rate
    return np.sin(np.arange(length) * factor)

def sine_sine_wave(f1, f2, length, rate):
    s1=sine_wave(f1,length,rate)
    s2=sine_wave(f2,length,rate)
    ss=s1+s2
    sa=np.divide(ss, 2.0)
    return sa

def play_tone(stream, frequency=440, length=0.10, rate=44100):
    frames = []
    frames.append(sine_wave(frequency, length, rate))
    chunk = np.concatenate(frames) * 0.25
    stream.write(chunk.astype(numpy.float32).tostring())

def play_dtmf_tone(stream, digits, length=0.2, rate=44100):
    dtmf_freqs = {'1': (1209,697), '2': (1336, 697), '3': (1477, 697), 'A': (1633, 697),
                  '4': (1209,770), '5': (1336, 770), '6': (1477, 770), 'B': (1633, 770),
                  '7': (1209,852), '8': (1336, 852), '9': (1477, 852), 'C': (1633, 852),
                  '*': (1209,941), '0': (1336, 941), '#': (1477, 941), 'D': (1633, 941)}
    dtmf_digits = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '*', '0', '#', 'A', 'B', 'C', 'D']
    if type(digits) is not type(''):
        digits=str(digits)[0]
    digits = ''.join ([dd for dd in digits if dd in dtmf_digits])
    joined_chunks = []
    for digit in digits:
        digit=digit.upper()
        frames = []
        frames.append(sine_sine_wave(dtmf_freqs[digit][0], dtmf_freqs[digit][1], length, rate))
        chunk = np.concatenate(frames) * 0.25
        joined_chunks.append(chunk)
        
        # fader section
        fade = 200 # 200ms
        fade_in = np.arange(0., 1., 1/fade)
        fade_out = np.arange(1., 0., -1/fade)

        chunk[:fade] = np.multiply(chunk[:fade], fade_in) # fade sample wave in
        chunk[-fade:] = np.multiply(chunk[-fade:], fade_out) # fade sample wave out
        time.sleep(0.1)
        
    X = np.array(joined_chunks, dtype='float32') # creates an one long array of tone samples to record
    stream.write(X.astype(np.float32).tostring()) # to hear tones
    
        
        
    # record tone sequence float 32 array as a wave file section (works on python 3.6)
    for i in range(0, int(RECORD_SECONDS)):
        waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(p.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(X.astype(np.float32).tostring())
        waveFile.close()

if __name__ == '__main__':
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1, rate=44100, output=1,frames_per_buffer=CHUNK)
    

    # Dial a telephone number.
    if len(sys.argv) != 2:
        a = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '*', '0', '#', 'A', 'B', 'C', 'D']
        digits = str(np.random.choice(a, 20)) # set random length of numbers to pluck from list
        # below preps random list of numbers for inclusion into csv file
        digits=digits.replace("[",'') # replace characters with null
        digits=digits.replace("]",'')
        digits=digits.replace("'",'')
        digits=digits.replace(" ",'') # replace space with null
        # print(digits)
        
        # writes digits to csv file
        with open('metadata.csv', 'w') as csvfile:
            characters = csv.writer(csvfile, delimiter=' ')
            characters.writerows(digits)
    else:
        digits = sys.argv[1]
    play_dtmf_tone(stream, digits)
    
    stream.close()
    p.terminate()
