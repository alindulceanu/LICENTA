#! ../../.venv/bin python3.11

import serial
import time
import numpy as np

class Car:
    def __init__(self, com, baud):
        self.ser = serial.Serial(f"/dev/{com}", baudrate= baud, timeout= 1.0)
        time.sleep(3)
        self.ser.reset_input_buffer()
        print("Serial started!")
        self.lastPosition = None

    def __del__(self):
        try:
            self.closeSerial()
        except Exception as e:
            print(e)

    def setVelocity(self, value):
        try:
            self.ser.write(f"dc/{value}\n".encode('utf-8'))
            print(f"Velocity set to {value}")
        except:
            self.emergencyStop()

    def setDirection(self, value):
        self.ser.write(f"srv/{value}\n".encode('utf-8'))
        print(f"Direction set to {value}")

    def emergencyStop(self):
        self.setVelocity(0)

    def closeSerial(self):
        self.emergencyStop()
        self.ser.close()
        print("Serial Closed")

    def setSteering(self, slope):
        # No need to round the position here as calculateSteeringPositionFromSlope already clamps it.
        position = round(self.calculateSteeringPositionFromSlope(slope))
        
        if position != self.lastPosition:
            print("Steering position:", position)
            self.lastPosition = position
            # Set the position
            self.setDirection(position)

    def calculateSteeringPositionFromSlope(self, slope):
        # Calculate the angle from the horizontal axis
        angle_from_horizontal = np.arctan(slope)

        # Calculate the angle from the vertical axis, adjusting for the sign of the slope
        angle_from_vertical = np.pi/2 - abs(angle_from_horizontal)
        if slope < 0:
            angle_from_vertical = -angle_from_vertical

        # Scale the angle to map it to the servo's range from -50 to +50
        # The servo's range corresponds to angles from -pi/6 to pi/6
        max_angle = np.pi/6  # Maximum steering angle in radians (30 degrees)
        position = (angle_from_vertical / max_angle) * 50

        # Clamp the position to make sure it doesn't exceed the servo's physical limits
        position = np.clip(position, -50, 50)

        return position


