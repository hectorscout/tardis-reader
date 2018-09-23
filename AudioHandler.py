import pyaudio
import wave
import time

class AudioHandler:
    def __init__(self):
        self.RECORD_SECONDS = 5
        self.FORMAT = pyaudio.paInt16
        self.CHUNK = 256
        self.CHANNELS = 1
        # self.RATE = 44100
        self.RATE = 8000
        self.WAVE_OUTPUT_FILENAME = 'output.wav'

        self.pa = pyaudio.PyAudio()

    def record(self):
        self.frames = []
        self.stopPressed = False

        def recordingCallback(in_data, frame_count, time_info, status):
            self.frames.append(in_data)
            if self.stopPressed:
                callbackFlag = pyaudio.paComplete
                self.stopPressed = False
            else:
                callbackFlag = pyaudio.paContinue
            return(in_data, callbackFlag)
        
        self.stream = self.pa.open(format=self.FORMAT,
                                   channels=self.CHANNELS,
                                   rate=self.RATE,
                                   input=True,
                                   frames_per_buffer=self.CHUNK,
                                   stream_callback=recordingCallback)

        print "* recording"

        self.stream.start_stream()

        while self.stream.is_active():
            time.sleep(0.1)
        # self.frames = []
        
        # for i in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
        #     data = self.stream.read(self.CHUNK)
        #     self.frames.append(data)

        print 'stopping it'
        self.stream.stop_stream()
        self.stream.close()
        self.pa.terminate()

        print self.frames[0]
        print len(self.frames)
        wf = wave.open(self.WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.pa.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close()

    def stopRecording(self):
        self.stopPressed = True
        
    def playRecording(self):
        self.pa = pyaudio.PyAudio()
        wf = wave.open(self.WAVE_OUTPUT_FILENAME, 'rb')

        def playingCallback(in_data, frame_count, time_info, status):
            data = wf.readframes(frame_count)
            #print 'in callback %s %s' % (frame_count, len(data))
            return (data, pyaudio.paContinue)# if data else pyaudio.paComplete)

        print 'channels: %s, rate: %s' % (wf.getnchannels(), wf.getframerate())
        self.stream = self.pa.open(format=self.pa.get_format_from_width(wf.getsampwidth()),
                                   channels=wf.getnchannels(),
                                   rate=wf.getframerate(),
                                   output=True,
                                   frames_per_buffer=self.CHUNK,
                                   output_device_index=2,
                                   stream_callback=playingCallback)

        self.stream.start_stream()

        while self.stream.is_active():
            time.sleep(0.5)

        self.stream.stop_stream()
        self.stream.close()
        wf.close()

        self.pa.terminate()

    def pausePlayback(self):
        self.stream.stop_stream()

    def resumePlayback(self):
        self.stream.start_steam() #TODO: pretty sure this is wrong...
