# Based heavily on https://blog.bartbania.com/raspberry_pi/temperature-log-howto/

import sys

from subprocess import PIPE, Popen
from envirophat import light, weather, leds
from Adafruit_IO import *

FACTOR = 1.3

with open('keyfile.txt', 'r') as f:
    api_key = f.read().strip()

aio = Client(api_key)

def get_environment():
    data = {'pi-zero-temp-board': weather.temperature(), 'pi-zero-pressure': weather.pressure(), 'pi-zero-light': light.light()}
    data['pi-zero-temp-cpu'] = get_cpu_temperature()
    data['pi-zero-temp-actual'] = data['pi-zero-temp-board'] - ((data['pi-zero-temp-cpu'] - data['pi-zero-temp-board'])/FACTOR)

    return data

def get_cpu_temperature():
    process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
    output, _error = process.communicate()

    return float(output[output.index('=') + 1:output.rindex("'")])

def send_data(data):
    for feed,value in data.iteritems():
        aio.send(feed, value)

if __name__ == '__main__':
    data = get_environment()
    send_data(data)

    sys.exit()

