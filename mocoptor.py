# import libs
import RPi.GPIO as IO

# set board mode
IO.setmode(IO.BOARD)

class Motor:
    def __init__(self, in1, in2, in3, in4):
        """
            This class is capable of using with 2-Wheel drive dc motors
            params
                in1, in2, in3, in4: signal pins of the motor driver
        """
        self.in1 = in1
        self.in2 = in2
        self.in3 = in3
        self.in4 = in4
        
        # setup pin
        IO.setup(self.in1, IO.OUT)
        IO.setup(self.in2, IO.OUT)
        IO.setup(self.in3, IO.OUT)
        IO.setup(self.in4, IO.OUT)

        # create pwm object
        self.in1 = IO.PWM(self.in1, 1000)
        self.in2 = IO.PWM(self.in2, 1000)
        self.in3 = IO.PWM(self.in3, 1000)
        self.in4 = IO.PWM(self.in4, 1000)
        
        # zero volt outputs
        self.in1.start(0)
        self.in2.start(0)
        self.in3.start(0)
        self.in4.start(0)


    def drive(self, wheel, direction, speed):
        """
            Drive a wheel
            params
                wheel: string of "l" or "r" for left and right respectively
                direction: string of "cw" or "ccw"
                speed: pwm duty cycle ranges from 0 to 100
            returns
                0 for success operation or -1 for invalid argument
        """
        temp_wheel = 0
        temp_dir   = 0
        
        if wheel.lower() == "l" and direction.lower() == "cw":
            temp_wheel = self.in1
        elif wheel.lower() == "l" and direction.lower() == "ccw":
            temp_wheel = self.in2
        elif wheel.lower() == "r" and direction.lower() == "cw":
            temp_wheel = self.in4
        elif wheel.lower() == "r" and direction.lower() == "ccw":
            temp_wheel = self.in3
        else:
            print("Invalid wheel or direction arguments");
            return -1
        
        if speed > 100 or speed < 0:
            print("Invalid speed argument.")
            return -1
        
        temp_wheel.ChangeDutyCycle(speed)
        
        return 0
    
    
    def fwd_drive(self, speed):
        """
            Forward Drive
            params
                speed: duty cycle ranging from 0 to 100
        """
        if speed > 100 or speed < 0:
            print("Invalid speed argument.")
            return -1
        
        self.drive("l", "ccw", speed)
        self.drive("r", "cw", speed)
        
        return 0
    
    
    def rev_drive(self, speed):
        """
            Reverse Drive
            params
                speed: duty cycle ranging from 0 to 100
        """
        if speed > 100 or speed < 0:
            print("Invalid speed argument.")
            return -1
        
        self.drive("l", "cw", speed)
        self.drive("r", "ccw", speed)
        
        return 0
    
        
    def turn_ccw(self, speed):
        """
            Turn CCW. Motors will spin in the same CW direction
            params
                speed: duty cycle ranging from 0 to 100
        """
        if speed > 100 or speed < 0:
            print("Invalid speed argument.")
            return -1
        
        self.drive("l", "cw", speed)
        self.drive("r", "cw", speed)
        
        return 0
    
    
    def turn_cw(self, speed):
        """
            Turn CCW. Motors will spin in the same CCW direction
            params
                speed: duty cycle ranging from 0 to 100
        """
        if speed > 100 or speed < 0:
            print("Invalid speed argument.")
            return -1
        
        self.drive("l", "ccw", speed)
        self.drive("r", "ccw", speed)
        
        return 0
    
    
    def brake(self):
        """
            Stop motors immediately
        """
        self.drive("l", "cw", 0)
        self.drive("l", "ccw", 0)
        self.drive("r", "cw", 0)
        self.drive("r", "ccw", 0)
        
    
#motors = Motor(38, 40, 35, 37)
