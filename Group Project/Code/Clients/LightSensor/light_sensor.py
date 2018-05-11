# -*- coding: utf-8 -*-
import json
import socket
import time

import mraa


class VoltageInput(object):

    def __init__(self, analog_pin):
        """Setting up the analog pin please"""
        self.aio = mraa.Aio(analog_pin)
        self.aio.setBit(12)

    @property
    def voltage(self):
        """Get the voltage value from the analog port"""
        raw_value = self.aio.read()
        return raw_value / 4095.0 * 5.0


class DarknessSensor(object):
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
    my_socket = socket.socket()
    host = "192.168.1.100"  # The ip of the master board
    port = 5001  # The port that will be used for sending the data of the sensor
    my_socket.connect((host, port))  # connecting to the master board
    my_data = {"source": "light", "room_no": 1, "value": 0}
    my_socket.send(json.dumps(my_data))
    received_server = my_socket.recv(1024)
    while True:
        if received_server == 'start':
            darkness_sensor.measure_light()  # getting the voltage values from the sensor
            new_ambient_light = darkness_sensor.ambient_light
            if new_ambient_light == 'extremely_dark':
                # Sending Data to the Master
                send_values = {'pin13': 0, 'pin11': 0, 'value': new_ambient_light}
                print('The Client Sending', send_values)
                my_socket.send(json.dumps(send_values))
                received_value = my_socket.recv(1024)
                if received_value == 'close':
                    my_socket.close()
                    break
            elif new_ambient_light == 'very_dark':
                # Send the needed pings
                send_values = {'pin13': 0, 'pin11': 0, 'value': new_ambient_light}
                print('The Client Sending', send_values)
                my_socket.send(json.dumps(send_values))
                received_value = my_socket.recv(1024)
                if received_value == 'close':
                    my_socket.close()
                    break
            elif new_ambient_light == 'almost_dark':
                # Send the needed pings
                send_values = {'pin13': 1, 'pin11': 0, 'value': new_ambient_light}
                print('The Client Sending', send_values)
                my_socket.send(json.dumps(send_values))
                received_value = my_socket.recv(1024)
                if received_value == 'close':
                    my_socket.close()
                    break
            elif new_ambient_light == 'normal':
                # Send the needed pings
                send_values = {'pin13': 1, 'pin11': 1, 'value': new_ambient_light}
                print('The Client Sending', send_values)
                my_socket.send(json.dumps(send_values))
                received_value = my_socket.recv(1024)
                if received_value == 'close':
                    my_socket.close()
                    break
            time.sleep(1)
