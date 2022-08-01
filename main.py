import pydub
from pydub import AudioSegment
from pydub.playback import play

sound1 = AudioSegment.from_file(r"ΑΓΙΑ ΣΚΕΠΗ.mp3")
sound1_channels = sound1.split_to_mono()
sound1 = sound1_channels[0].overlay(sound1_channels[1])
sound1 = sound1 - 30 # make sound1 quiter 30dB

sound2 = AudioSegment.from_file(r"ΑΓΙΑ ΚΥΡΙΑΚΗ.mp3")
sound2_channels = sound2.split_to_mono()
sound2 = sound2_channels[0].overlay(sound2_channels[1])
sound2 = sound2 - 30 # make sound2 quiter 30dB

import pyaudio

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

p = pyaudio.PyAudio()
player = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True,frames_per_buffer=CHUNK)
mic_stream = p.open(format=FORMAT, channels=CHANNELS,rate=RATE, input=True,frames_per_buffer=CHUNK)

#chunk_time_in_seconds = int(RATE/CHUNK)
chunk_number = 0

while(True):
    mic_data = mic_stream.read(CHUNK)
    mic_sound = AudioSegment(mic_data, sample_width=2, channels=1, frame_rate=RATE)
    mic_sound_duration = len(mic_sound)
    
    sound1_part = sound1[chunk_number*mic_sound_duration:(chunk_number+1)*mic_sound_duration]
    sound2_part = sound2[chunk_number*mic_sound_duration:(chunk_number+1)*mic_sound_duration]
    
    
    
    #player.write(mic_sound.raw_data) works well
    mix_sound = sound1_part.overlay(sound2_part).overlay(mic_sound)
    player.write(mix_sound.raw_data) # low microphone quality
    
    chunk_number = chunk_number+1