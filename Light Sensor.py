# -*- coding: utf-8 -*-
import json
import socket

import mraa
import time

my_socket = socket.socket()
host = "192.168.1.100"  # The ip of the master board
port = 5009  # The port that will be used for sending the data of the sensor
my_socket.connect((host, port))  # connecting to the master board


class VoltageInput:

    def __init__(self, analog_pin):
        """Setting up the analog pin please"""
        self.aio = mraa.Aio(analog_pin)
        self.aio.setBit(12)

    @property
    def voltage(self):
        """Get the voltage value from the analog port"""
        raw_value = self.aio.read()
        return raw_value / 4095.0 * 5.0


class DarknessSensor:
    # Light level descriptions
    light_extremely_dark = "extremely_dark"
    light_very_dark = "very_dark"
    light_dark = "almost_dark"
    light_normal = "normal"
    # voltage levels
    extremely_dark_max_voltage = 2.0
    very_dark_max_voltage = 3.0
    dark_max_voltage = 4.0

    def __init__(self, analog_pin):
        """Setting up the default values of the sensor reading"""
        self.voltage_input = VoltageInput(analog_pin)
        self.voltage = 0.0
        self.ambient_light = self.light_extremely_dark
        self.measure_light()

    def measure_light(self):
        """Measuring the values of the light needed based on the voltage"""
        self.voltage = self.voltage_input.voltage
        if self.voltage < self.extremely_dark_max_voltage:
            self.ambient_light = self.light_extremely_dark
        elif self.voltage < self.very_dark_max_voltage:
            self.ambient_light = self.light_very_dark
        elif self.voltage < self.dark_max_voltage:
            self.ambient_light = self.light_dark
        else:
            self.ambient_light = self.light_normal


if __name__ == "__main__":
    darkness_sensor = DarknessSensor(0)  # object with default value
    last_ambient_light = ""
    while True:
        # Definig the pins gpio
        pin13 = mraa.Gpio(13)
        pin12 = mraa.Gpio(12)
        pin11 = mraa.Gpio(11)
        pin10 = mraa.Gpio(10)
        pin13.dir(mraa.DIR_OUT)
        pin12.dir(mraa.DIR_OUT)
        pin11.dir(mraa.DIR_OUT)
        pin10.dir(mraa.DIR_OUT)

        darkness_sensor.measure_light()  # getting the voltage values from the sensor
        new_ambient_light = darkness_sensor.ambient_light

        if new_ambient_light == 'extremely_dark':
            # Sending Data to the Master
            my_socket.send(json.dumps({'room_no': 1, 'light': 1}))
            # Led up the leds based on the light status
            pin13.write(1)
            pin12.write(0)
            pin11.write(0)
            pin10.write(0)
        elif new_ambient_light == 'very_dark':
            my_socket.send(json.dumps({'room_no': 1, 'light': 1}))
            pin12.write(1)
            pin11.write(0)
            pin10.write(0)
            pin13.write(0)
        elif new_ambient_light == 'almost_dark':
            my_socket.send(json.dumps({'room_no': 1, 'light': 1}))
            pin11.write(1)
            pin13.write(0)
            pin12.write(0)
            pin10.write(0)
        elif new_ambient_light == 'normal':
            my_socket.send(json.dumps({'room_no': 1, 'light': 0}))
            pin10.write(1)
            pin13.write(0)
            pin12.write(0)
            pin11.write(0)
        else:
            print("Other Values")
        # Sleep 1 second to give the master board to sync with other boards
        time.sleep(1)
