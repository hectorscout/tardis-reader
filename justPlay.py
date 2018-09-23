import pyaudio
import wave
import time

CHUNK = 256
WAVE_OUTPUT_FILENAME = 'output.wav'

pa = pyaudio.PyAudio()
wf = wave.open(WAVE_OUTPUT_FILENAME, 'rb')

def playingCallback(in_data, frame_count, time_info, status):
    data = wf.readframes(frame_count)
    return (data, pyaudio.paContinue)

stream = pa.open(format=pa.get_format_from_width(wf.getsampwidth()),
                 channels=wf.getnchannels(),
                 rate=wf.getframerate(),
                 output=True,
                 frames_per_buffer=CHUNK,
                 output_device_index=2,
                 stream_callback=playingCallback)

stream.start_stream()

while stream.is_active():
    time.sleep(1.0)

stream.stop_stream()
stream.close()
wf.close()

pa.terminate()
