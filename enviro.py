# Based heavily on https://blog.bartbania.com/raspberry_pi/temperature-log-howto/

import time
import sys

from subprocess import PIPE, Popen
from envirophat import light, weather, leds

from ISStreamer.Streamer import Streamer

FACTOR = 1.3

with open('/home/shearna/repos/iot-enviropi/keyfile.txt', 'r') as f:
    api_key = f.read().strip()

streamer = Streamer(bucket_name="Pi Zero", bucket_key="shearn89-pizero", access_key=api_key)

def get_environment():
    data = {
        'board_temp': round(weather.temperature(),2),
        'pressure': round(weather.pressure(),0),
        'light': round(light.light(),2)
    }
    data['cpu_temp'] = get_cpu_temperature()
    data['est_temp'] = round(data['board_temp'] - ((data['cpu_temp'] - data['board_temp'])/FACTOR),2)

    return data

def get_cpu_temperature():
    process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
    output, _error = process.communicate()

    return round(float(output[output.index('=') + 1:output.rindex("'")]),2)

def send_data(data):
    for feed,value in data.iteritems():
        streamer.log(feed,value)

if __name__ == '__main__':
    print ("Starting temp logger...")
    streamer.log("messages", "pi zero stream starting")
    while True:
        data = get_environment()
        send_data(data)
        time.sleep(60)
