#! ../../.venv/bin python3.11

import serial
import time

class Car:
    def __init__(self, com, baud):
        self.ser = serial.Serial(f"/dev/{com}", baudrate= baud, timeout= 1.0)
        time.sleep(3)
        self.ser.reset_input_buffer()
        print("Serial started!")

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

    def readDistance(self):
        pass
