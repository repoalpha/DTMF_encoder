import os
import wave
with wave.open('/Users/stephenlilley/dtmf.wav') as w:
    framerate = w.getframerate()
    frames = w.getnframes()
    channels = w.getnchannels()
    width = w.getsampwidth()
    filesize = os.stat('/Users/stephenlilley/dtmf.wav')
    time = frames / framerate
    print('sampling rate:', framerate, 'Hz')
    print('length:', frames, 'samples')
    print('channels:', channels)
    print('sample width:', width, 'bytes')
    print('file size:', filesize.st_size, 'bytes', filesize.st_size/1000, 'kB' )
    print('Duration:', time, 'seconds')
    data = w.readframes(frames)
