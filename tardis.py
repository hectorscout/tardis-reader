## arecord -D plughw:1,0 test.wav
## aplay -D plughw:1,0 test.wav
##

from Tkinter import *
from AudioHandler import AudioHandler
import threading

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
        
        self.quitButton = Button(frame, text="Quit", command=self.quitButtonPressed, height=buttonHeight, width=buttonWidth)

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
        threading.Thread(target=self.audioHandler.playRecording, args=(), kwargs={}).start()
#        self.audioHandler.playRecording()
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

    def quitButtonPressed(self):
        self.audioHandler.stopRecording()
        #self.audioHandler.stopPlaying()
        frame.quit


root = Tk()
#root.attributes("-fullscreen", True)

app = App(root)

root.mainloop()
root.destroy()
