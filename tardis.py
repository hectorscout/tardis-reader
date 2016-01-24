## arecord -D plughw:1,0 test.wav
## aplay -D plughw:1,0 test.wav
##

from Tkinter import *
import pyaudio
import wave
import time
import threading

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
            # data = self.stream.readframes(frame_count)
            print 'in callback'
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
        self.stream = self.pa.open(format=self.pa.get_format_from_width(wf.getsampwidth()),
                                   channels=wf.getnchannels(),
                                   rate=wf.getframerate(),
                                   output=True,
                                   output_device_index=2)
        data = wf.readframes(self.CHUNK)

        while data != '':
            self.stream.write(data)
            data = wf.readframes(self.CHUNK)

        self.stream.stop_stream()
        self.stream.close()

        self.pa.terminate()

    def pausePlayback(self):
        self.stream.stop_stream()

    def resumePlayback(self):
        self.stream.start_steam() #TODO: pretty sure this is wrong...
        
class App:
    def __init__(self, master):

        buttonHeight = 10
        buttonWidth = 20

        self.buttons = []
        
        frame = Frame(master)
        frame.pack()

        # Initial State (ready to record)
        self.recordButton = Button(frame, text="Record", fg="red", command=self.recordButtonPressed, height=buttonHeight, width=buttonWidth)

        # Recording State
        self.stopRecordButton = Button(frame, text="Stop Recording", fg="red", command=self.stopRecordButtonPressed, height=buttonHeight, width=buttonWidth)

        # Ready To Play State
        self.playButton = Button(frame, text="Play", command=self.playButtonPressed, height=buttonHeight, width=buttonWidth)
        self.deleteRecordButton = Button(frame, text="Delete Recording", fg="red", command=self.deleteRecordButtonPressed, height=buttonHeight, width=buttonWidth)

        # Playing State
        self.stopPlayingButton = Button(frame, text="Stop", fg="red", command=self.stopPlayingButtonPressed, height=buttonHeight, width=buttonWidth)
        self.pauseButton = Button(frame, text="Pause", command=self.pauseButtonPressed, height=buttonHeight, width=buttonWidth)

        # paused State
        self.resumeButton = Button(frame, text="Play", command=self.resumeButtonPressed, height=buttonHeight, width=buttonWidth)
        
        self.buttons = [self.recordButton, self.stopRecordButton, self.playButton, self.deleteRecordButton, self.stopPlayingButton, self.pauseButton, self.resumeButton]
        
        self.quitButton = Button(frame, text="Quit", command=frame.quit, height=buttonHeight, width=buttonWidth)

        self.quitButton.grid(row=1)

        self.setInitialState()

        self.audioHandler = AudioHandler()
        
    def clearButtons(self):
        for button in self.buttons:
            button.grid_forget()

    def setInitialState(self):
        self.clearButtons()
        self.recordButton.grid(row=0, column=0)

    def setRecordingState(self):
        self.clearButtons()
        self.stopRecordButton.grid(row=0, column=0)
            
    def setReadyToPlayState(self):
        self.clearButtons()
        self.playButton.grid(row=0, column=0)
        self.deleteRecordButton.grid(row=0, column=1)

    def setPlayingState(self):
        self.clearButtons()
        self.pauseButton.grid(row=0, column=0)
        self.stopPlayingButton.grid(row=0, column=1)

    def setPausedState(self):
        self.clearButtons()
        self.resumeButton.grid(row=0, column=0)
        self.stopPlayingButton.grid(row=0, column=1)
        
    def recordButtonPressed(self):
        print 'start recording stuff'
        threading.Thread(target=self.audioHandler.record, args=(), kwargs={}).start()
        self.setRecordingState()

    def stopRecordButtonPressed(self):
        print 'stop recording stuff'
        print 'save the file'
        print 'display the play and delete buttons'
        self.audioHandler.stopRecording()
        self.setReadyToPlayState()

    def playButtonPressed(self):
        print 'start playing the recorded audio'
        self.audioHandler.playRecording()
        print 'show the pause and stop buttons'
        self.setPlayingState()

    def deleteRecordButtonPressed(self):
        print 'Delete the recorded audio'
        print 'display the record audio button'
        self.setInitialState()
        
    def stopPlayingButtonPressed(self):
        print 'Stop playing the recorded audio'
        print 'Display the play and delete buttons'
        self.setReadyToPlayState()

    def pauseButtonPressed(self):
        print 'Pause the recorded audio'
        print 'display the play and stop buttons'
        self.setPausedState()

    def resumeButtonPressed(self):
        print 'Resume playing the audio'
        print 'display the play and stop buttons'
        self.setPlayingState()


root = Tk()
#root.attributes("-fullscreen", True)

app = App(root)

root.mainloop()
root.destroy()
