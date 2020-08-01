#!/usr/bin/env python3
from rak811 import Mode, Rak811
import bme680
import time
 
lora = Rak811()
lora.hard_reset()
lora.mode = Mode.LoRaWan
lora.band = 'EU868'
lora.set_config(app_eui='xxxxxxxxxxxxx',
                app_key='xxxxxxxxxxxxxxxxxxxxxx')
lora.join_otaa()
lora.dr = 5
 
sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)
 
while True:
    if sensor.get_sensor_data():
        temp = int(sensor.data.temperature * 100)
        humidity = int(sensor.data.humidity * 100)
        foo = "{0:04x}{1:04x}".format(temp,humidity)
        lora.send(bytes.fromhex(foo))
        time.sleep(20)
 
lora.close()
