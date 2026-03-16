#!/usr/bin/env python3

# Import the necessary libraries
import time
import math
from ev3dev2.motor import *
from ev3dev2.sound import Sound
from ev3dev2.button import Button
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *
from ev3dev2.sensor.virtual import *

# Create the sensors and motors objects
motorA = LargeMotor(OUTPUT_A)
motorB = LargeMotor(OUTPUT_B)
tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)

ultrasonic_sensor_in2 = UltrasonicSensor(INPUT_2)


SP = 10 # CM

integral = 0
last_time = time.time()
last_error = ultrasonic_sensor_in2.distance_centimeters - SP

def pidCalc(Kp, Ki, Kd, error) -> float:
    global integral, last_error, last_time
    
    dt = time.time() - last_time
    derivative = (error - last_error) / dt if dt != 0 else 0
    
    integral += error
    last_error = error
    
    return Kp * error + Ki * integral + Kd * derivative

# tank_drive.on(100, 100)
error = ultrasonic_sensor_in2.distance_centimeters - SP
while abs(error) > 1:
    speed = pidCalc(1, 0, 0, (error))
    print(f"Distance: {ultrasonic_sensor_in2.distance_centimeters}")
    
    if speed > 100:
        speed = 100
    elif speed < -100:
        speed = -100
        
    tank_drive.on(speed, speed)
    error = ultrasonic_sensor_in2.distance_centimeters - SP
    
print(f"Arrived! distance: {ultrasonic_sensor_in2.distance_centimeters}")
    
