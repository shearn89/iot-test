# Based heavily on https://blog.bartbania.com/raspberry_pi/temperature-log-howto/

import time
import sys
import logging

from subprocess import PIPE, Popen
from envirophat import light, weather, leds

from ISStreamer.Streamer import Streamer

FACTOR = 1.3

logging.basicConfig(level=logging.INFO)

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
    data['est_temp'] = data['board_temp'] - ((data['cpu_temp'] - data['board_temp'])/FACTOR)

    return data

def get_cpu_temperature():
    process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
    output, _error = process.communicate()

    return round(float(output[output.index('=') + 1:output.rindex("'")]),2)

def send_data(data):
    logging.debug('sending data')
    for feed,value in data.iteritems():
        logging.debug("%s,%.2f" % (feed,value))
        streamer.log(feed,value)

if __name__ == '__main__':
    logging.info("Starting temp logger...")
    while True:
        data = get_environment()
        send_data(data)
        time.sleep(60)
