# coding:utf-8
import pyaudio
import wave

# To use PyAudio, first instantiate PyAudio using pyaudio.PyAudio() (1), which
# sets up the portaudio system.

# To record or play audio, open a stream on the desired device with the desired 
# audio parameters using pyaudio.PyAudio.open() (2). This sets up a pyaudio.
# Stream to play or record audio.

# Play audio by writing audio data to the stream using pyaudio.Stream.write(), 
# or read audio data from the stream using pyaudio.Stream.read(). (3)

# Note that in “blocking mode”, each pyaudio.Stream.write() or pyaudio.Stream.read() 
# blocks until all the given/requested frames have been 
# played/recorded. Alternatively, to generate audio data on the fly or immediately
# process recorded audio data, use the “callback mode” outlined below.

# Use pyaudio.Stream.stop_stream() to pause playing/recording, and pyaudio.Stream.close() 
# to terminate the stream. (4)

# Finally, terminate the portaudio session using pyaudio.PyAudio.terminate() (5)
RESPEAKER_RATE = 16000
RESPEAKER_CHANNELS = 8
RESPEAKER_WIDTH = 2
# run getDeviceInfo.py to get index
RESPEAKER_INDEX = 2
CHUNK = 1024
RECORD_SECONDS = 6
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()

stream = p.open(
            rate=RESPEAKER_RATE,
            format=p.get_format_from_width(RESPEAKER_WIDTH),
            channels=RESPEAKER_CHANNELS,
            input=True,
            input_device_index=RESPEAKER_INDEX,)

print("* recording")

frames = []

for i in range(0, int(RESPEAKER_RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(RESPEAKER_CHANNELS)
wf.setsampwidth(p.get_sample_size(p.get_format_from_width(RESPEAKER_WIDTH)))
wf.setframerate(RESPEAKER_RATE)
wf.writeframes(b''.join(frames))
wf.close()

