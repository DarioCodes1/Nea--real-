import time
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_StepperMotor

# Create a default object for the motor hat.
#mh = Adafruit_MotorHAT(i2c_bus=2)  # Specify I2C bus 2 as this is the motor that controls the x movement of the laser, currently commented out as I'm coding on PC not raspberry pi

def move_left(speed, steps):
    # Select the stepper motor port and set the number of steps per revolution.
    myStepper = mh.getStepper(200, 1)  # 200 steps/rev, port #1
    # Set the speed of the motor
    myStepper.setSpeed(speed)
    
    # Move the stepper motor very slowly by the smallest degree possible.
    for i in range(steps):
        myStepper.oneStep(Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.MICROSTEP)
        time.sleep(0.01)  # Adjust the sleep time as needed

def move_right(speed, steps):
    # Select the stepper motor port and set the number of steps per revolution.
    myStepper = mh.getStepper(200, 1)  # 200 steps/rev, port #1
    # Set the speed of the motor
    myStepper.setSpeed(speed)
    
    # Move the stepper motor very slowly by the smallest degree possible.
    for i in range(steps):
        myStepper.oneStep(Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.MICROSTEP)
        time.sleep(0.01)  # Adjust the sleep time as needed

