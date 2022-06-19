
import time
import board
import pwmio
from audiopwmio import PWMAudioOut
from audiomp3 import MP3Decoder
from random import randint

class Speaker: 
    def __init__(self, Aout = board.A0):
        # speaker defaults as off
        self.speaker = pwmio.PWMOut(Aout, duty_cycle = 0, variable_frequency = True)

    def _playtone(self, frequency):
        self.speaker.frequency = frequency

    def noise(self):
        # generate white noise
        # better for localisation than pure tones
        minf = 1000
        maxf = 20000
        for _ in range(5000):
            self._playtone(randint(minf, maxf))
            time.sleep(0.001)

    def _sweep(self, startf = 300, endf = 8100, step = 10, delay = 0.0025):
        for f in range(startf, endf, step):
            self._playtone(f)
            time.sleep(delay)

    def siren(self, cycles = 3):
        self.speaker.duty_cycle = 65535 // 2
        # cyclex sweep up and down
        for _ in range(cycles):
            self._sweep()
            self._sweep(startf = 8100, endf = 300, step = -10)

    def shutup(self):
        self._playtone(0)
        self.speaker.duty_cycle = 0
    
    def beep(self, n : int):
        for _ in range(0,n):
            self.speaker.duty_cycle = 65535 // 2
            self._playtone(4000)
            time.sleep(0.2)
            self.speaker.duty_cycle = 0

    def longBeep(self, n : int):
       for _ in range(0, n):
           self.speaker.duty_cycle = 65535 // 2
           self._playtone(4000)
           time.sleep(0.8)
           self.speaker.duty_cycle = 0

    def playsong(self, filename: str):
        with open(filename, "rb") as mp3:
            decoder = MP3Decoder(mp3)
            self.speaker.deinit()
            audio = PWMAudioOut(board.A0)
            audio.play(decoder)
            while audio.playing:
                pass
            audio.deinit()
            decoder.deinit()
            self.speaker = pwmio.PWMOut(board.A0, duty_cycle = 0, variable_frequency = True)
