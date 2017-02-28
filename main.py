import serial
import struct
import csv
import _thread
import datetime


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


class Anemometer:
    def __init__(self, file, port):
        self.file = file
        self.ser = serial.Serial(port, timeout=1.2)
        self.port = port
        self.wind_velocities = []
        self.temperatures = []

    def dump(self, no_of_bytes=11):
        return self.ser.read(no_of_bytes)

    def read_value(self):
        value = 0.
        for i in [10, 1, 0.1, 0.01]:
            value += struct.unpack('B', self.ser.read(1))[0] * i
        return round(value, 2)

    def save_values(self):
        print('saving data for {}'.format(self.port))

        wind_velocity_file = self.file + '_wind.csv'
        with open(wind_velocity_file, 'w') as f:
            writer = csv.writer(f, delimiter='\r')
            writer.writerow(self.wind_velocities)

        temperature_file = self.file + '_temp.csv'
        with open(temperature_file, 'w') as f:
            writer = csv.writer(f, delimiter='\r')
            writer.writerow(self.temperatures)


KillSwitch.setup()
now = datetime.datetime.now()
prefix = '{}{:02d}{:02d}_{:02d}{:02d}{:02d}'.format(now.year, now.month, now.day, now.hour, now.minute, now.second)

# Need to check the port name
adam = Anemometer(file='data/{}_adam'.format(prefix), port='COM15')
brian = Anemometer(file='data/{}_brian'.format(prefix), port='COM17')
camilla = Anemometer(file='data/{}_camilla'.format(prefix), port='COM16')

wind_speakers = [
    adam,
    camilla,
    brian
]

second = 0

while KillSwitch.is_off() and second < 2000:
    for speaker in wind_speakers:
        if second % 30 == 0:
            if speaker.dump(7):
                temperature = speaker.read_value()
                speaker.temperatures.append(temperature)

                velocity = speaker.read_value()
                speaker.wind_velocities.append(velocity)

                print('{}>> vel:{} temp:{}'.format(speaker.port, velocity, temperature))

        else:
            if speaker.dump(11):
                velocity = speaker.read_value()
                speaker.wind_velocities.append(velocity)
                print('{}>> vel:{}'.format(speaker.port, velocity))

    print(second)
    second += 1

# Save values
for speaker in wind_speakers:
    speaker.save_values()
