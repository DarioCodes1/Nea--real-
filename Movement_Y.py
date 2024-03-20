import time
#from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_StepperMotor

# Create a default object for the motor hat.
#mh = Adafruit_MotorHAT(i2c_bus=1)  # Specify I2C bus 1

def move_up(speed, steps):
    speed = float(speed)
    steps = int(steps)
    # Select the stepper motor port and set the number of steps per revolution.
    myStepper = mh.getStepper(200, 2)  # 200 steps/rev, port #2 (for the 2nd motor)
    # Move the stepper motor at any speed inputted
    myStepper.setSpeed(speed)
    
    for i in range(steps):
        myStepper.oneStep(Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.MICROSTEP)
        time.sleep(0.01)  # Adjust the sleep time as needed

def move_down(speed, steps):
    speed = float(speed)
    steps = int(steps)
    # Select the stepper motor port and set the number of steps per revolution.
    myStepper = mh.getStepper(200, 2)  # 200 steps/rev, port #1
    # Move the stepper motor at any speed inputted
    myStepper.setSpeed(speed)
    
    # Move the stepper motor at any speed inputted
    for i in range(steps):
        myStepper.oneStep(Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.MICROSTEP)
        time.sleep(0.01)  # Adjust the sleep time as needed
