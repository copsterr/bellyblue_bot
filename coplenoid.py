import RPi.GPIO as IO

# set board mode
IO.setmode(IO.BOARD)

class Solenoid:
    def __init__(self, en):
        self.en = en
        IO.setup(self.en, IO.OUT)
        
    def on(self):
        IO.output(self.en, IO.HIGH)
        
    def off(self):
        IO.output(self.en, IO.LOW)