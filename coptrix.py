from time import sleep
import spidev
import RPi.GPIO as IO

LEDMAT_BRIGHTNESS_ADDR = 0x0A
LEDMAT_DECODEMODE_ADDR = 0x09
LEDMAT_SHUTDOWNREG_ADDR = 0x0C
LEDMAT_TESTLAMP_CMD = 0x0F
LEDMAT_SCAN_LIMIT_ADDR = 0x0B
LEDMAT_DIGITS_ADDR = (0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08)

# MOODS
MOOD_SMILEY = (0x00, 0x68, 0x64, 0x04, 0x04, 0x64, 0x68, 0x00)
MOOD_SAD = (0x00, 0x24, 0x68, 0x08, 0x08, 0x68, 0x24, 0x00)
MOOD_SLEEP = (0x00, 0x20, 0x24, 0x04, 0x04, 0x24, 0x20, 0x00)
MOOD_ANGRY = (0x00, 0x64, 0x28, 0x08, 0x08, 0x28, 0x64, 0x00)
MOOD_KUY = (0x0C, 0x12, 0x11, 0xE1, 0xE1, 0x19, 0x12, 0x0C)

# set board mode
IO.setmode(IO.BOARD)

class LEDMatrix:
    def __init__(self, pin_CS):
        self.spi = None
        self.cs = pin_CS
        
        ### PIN CONFIGS ###
        # setup CS pin
        IO.setup(self.cs, IO.OUT)
        IO.output(self.cs, IO.HIGH) # must be high due to spi config
        
        # spi config and init
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0) # open SPI connection
        self.spi.max_speed_hz = 500000
        self.spi.mode = 0
        
        ### STARTUP ROUTINE ###

        # turn on chip
        IO.output(self.cs, IO.LOW)
        self.spi.xfer([LEDMAT_SHUTDOWNREG_ADDR])
        self.spi.xfer([0x01])
        IO.output(self.cs, IO.HIGH)
        
        # turning off lamp
        IO.output(self.cs, IO.LOW)
        self.spi.xfer([LEDMAT_TESTLAMP_CMD])
        self.spi.xfer([0x00])
        IO.output(self.cs, IO.HIGH)
        
        # turn off decode mode
        IO.output(self.cs, IO.LOW)
        self.spi.xfer([LEDMAT_DECODEMODE_ADDR])
        self.spi.xfer([0x00])
        IO.output(self.cs, IO.HIGH)
        
        # scan limit to display all digits
        IO.output(self.cs, IO.LOW)
        self.spi.xfer([LEDMAT_SCAN_LIMIT_ADDR])
        self.spi.xfer([0x07])
        IO.output(self.cs, IO.HIGH)
    
    def write(self, addr, value):
        """
            Low Level function used to write data to LED Matrix
            User can use this function to write to a specific line
        """
        if addr < 0 or value < 0:
            print("Bad write arguemnts. Return -1")
            return -1
        
        IO.output(self.cs, IO.LOW)
        self.spi.xfer([addr])
        self.spi.xfer([value])
        IO.output(self.cs, IO.HIGH)
    
    def wash(self):
        """
            Turn off all LEDs
        """
        for line in LEDMAT_DIGITS_ADDR:
            self.write(line, 0)
    
    def lamp(self):
        """
            Turn on all LEDs
        """
        for line in LEDMAT_DIGITS_ADDR:
            self.write(line, 0xff)
            
    
    def change_brightness(self, level):
        if level > 15:
            level = 15
        elif level < 0:
            level = 0
        
        self.write(LEDMAT_BRIGHTNESS_ADDR, level)
        
    def feel(self, mood="sleep"):
        if mood.lower() == "smiley":
            mood = MOOD_SMILEY
        elif mood.lower() == "sad":
            mood = MOOD_SAD
        elif mood.lower() == "angry":
            mood = MOOD_ANGRY
        elif mood.lower() == "kuy":
            mood = MOOD_KUY
        else:
            mood = MOOD_SLEEP
        
        # write mood
        for i, line in enumerate(LEDMAT_DIGITS_ADDR):
            self.write(line, mood[i])


