import serial
import struct
import csv
import _thread


class KillSwitch:
    _list = []

    @staticmethod
    def input_thread(list_):
        input()
        list_.append(None)

    @classmethod
    def setup(cls):
        _thread.start_new_thread(cls.input_thread, (cls._list,))

    @classmethod
    def is_off(cls):
        return not cls._list

KillSwitch.setup()

ser = serial.Serial('COM3')

while KillSwitch.is_off():
    ser.read(11)
    value = 0
    for i in [10, 1, 0.1, 0.01]:
        value += struct.unpack('B', ser.read(1))[0] * i
    print(value)
