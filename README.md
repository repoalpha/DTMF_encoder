# DTMF_encoder

The original intent of this project was to create a DTMF (Dual Tone Multi Frequency) tone generator and metadata file to create audio samples for deep learning. Why DTMF? My reasoning is, its more complex than straight single tones, less complex than voice or music samples, and it perhaps has other uses as well given its orginal use was as a telephony dialer format.

On the surface a DTMF audio tone generator would seem a trivial execise, but a number of significant challanges arose using pyaudio as an audio source to create samples for deeplearning. This DTMF encoder modifies a simple encoder created by Noah Spurrier. In particular it adds some special features to make it useful I think for deeplearning. I have provided a jupyter notebook of the 3 python scripts for easy viewing.

1. The DTMF tone generator saves all the tones as one long numpy array to be used to save all the captured audio as a single wave file.
2. There is talk on stack overflow etc. that the 'wave module' won't support 32 bit samples as float32 and only 16 bit or 24 bit samples. Clearly this is no longer the case.
3. The DTMF tones are saved as a audio wave file which can be played back by play_wave.py.
4. The generated DTMF digits used in the .wav sample are stored also as a .csv metafile for supervised learning.
5. A script is provided to print out details of the .wav file generated.
6. Lastly, and the most difficult challange, removing the annoying pops from each tone samples transition.

I could not find any example on the net of how to save a sythesized waveform using the pyaudio module into a .wav file. There were plenty of examples using microphone generated audio samples but not systhesized audio like DTMF tones into a .wav file and as one contiguous float32 bit sample. This solution is provided in my dtmf.py script. In addition the annoying pops between audio samples proved to be a challange to using tones generated by pyaudio (and by extension 'port audio' which pyaudio uses)for deeplearning. The 'pops' are caused by differing finishing and starting phase angles of the samples. Typically the solutions offered on stack overflow are complicated and after testing didn't produce the needed results including 'pydub' which when constructing very longer sequences of samples would be impractical. The solution is to fade in and out between samples with a 'fader' which smooths out these transitions at the array level. The fader multiplies numpy arrays to the tone samples arrays to fade the amplitude of the sample start or finish. Lastly the actual notes or digits used to set the tone frequencies are stored in a .csv metafile so it could be used in supervised deeplearning training.

## Dependencies 

pyaudio 
wave 
numpy

## Installation of pyaudio
### Ubuntu:

sudo apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0
sudo apt-get install ffmpeg libav-tools
pip install pyaudio

**pip install pyaudio don’t use sudo in virtual env**

### Mac OSX

brew install portaudio
pip install pyaudio

## Installation of wave and numpy
on both Ubuntu and Mac OSX

pip install wave
pip install numpy



