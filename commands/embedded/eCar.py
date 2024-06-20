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
        except:
            self.emergencyStop()

    def setDirection(self, value):
        self.ser.write(f"srv/{value}\n".encode('utf-8'))

    def emergencyStop(self):
        self.setVelocity(0)

    def closeSerial(self):
        self.emergencyStop()
        self.setDirection(0)
        self.ser.close()
        print("Serial Closed")

    def setSteering(self, slope):
        position = round(self.calculateSteeringPositionFromSlope(slope))
        
        if position != self.lastPosition:
            self.lastPosition = position
            self.setDirection(position)

    def calculateSteeringPositionFromSlope(self, slope):
        angle_from_horizontal = np.arctan(slope)

        angle_from_vertical = np.pi/2 - abs(angle_from_horizontal)
        
        if slope < 0:
            angle_from_vertical = -angle_from_vertical

        max_angle = np.pi/6
        position = (angle_from_vertical / max_angle) * 50

        position = np.clip(position, -50, 50)

        return position


