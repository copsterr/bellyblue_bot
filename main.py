import microgear.client as microgear
import logging
from time import sleep
import spidev
import RPi.GPIO as IO
from mocoptor import *
from coptrix import *
from coplenoid import *

### MICROGEAR ###
APPID = "bellybluegw"
GEARKEY = "cGK3ij44dENtsPV"
GEARSECRET = "BwLvRGd4Gro4S3cMZiIMbfh9H"

microgear.create(GEARKEY, GEARSECRET, APPID, {'debugmode': True})
 
def connection():
    logging.info("Now I am connected with netpie")
    
def subscription(topic, message):
    logging.info(topic + " " + message)

def disconnect():
    logging.info("disconnected")
    
microgear.setalias("bot")
microgear.on_connect = connection
microgear.on_message = subscription
microgear.on_disconnect = disconnect
microgear.subscribe("/botcmd")
microgear.connect()


### SETUP BOARD ###
IO.setmode(IO.BOARD)
solenoid_pin     = 32
ledMatrix_cs_pin = 8
proximity_pin    = 22
motor_pins       = [38, 40, 35, 37]


### SETUP PERIPHERALS ###
IO.setup(solenoid_pin, IO.OUT) # solenoid
IO.setup(proximity_pin, IO.IN) # proximity
mat = LEDMatrix(ledMatrix_cs_pin) # LED Matrix
mat.wash() # wash all leds on matrix
motor = Motor(motor_pins[0], motor_pins[1], motor_pins[2], motor_pins[3]) # motors


### LOOP ###
while True:
    

