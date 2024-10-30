# SPDX-FileCopyrightText: 2024 Liz Clark for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Test interrupts for VCNL4200"""
import board
import digitalio
import time
from adafruit_vcnl4200 import Adafruit_VCNL4200, PS_INT, ALS_PERS, PS_PERS

i2c = board.I2C()
sensor = Adafruit_VCNL4200(i2c)

interrupt_pin = digitalio.DigitalInOut(board.D5)
interrupt_pin.direction = digitalio.Direction.INPUT
interrupt_pin.pull = digitalio.Pull.UP

sensor.als_low_threshold = 500
sensor.als_high_threshold = 1000
sensor.prox_int_threshold_low = 200
sensor.prox_int_threshold_high = 600

sensor.als_interrupt(enabled=True, white_channel=False)
sensor.prox_interrupt = PS_INT["BOTH"]
sensor.prox_interrupt_logic_mode = False
sensor.als_persistence = ALS_PERS["1"]
sensor.prox_persistence = PS_PERS["1"]

print("Monitoring interrupts...")

while True:
    if not interrupt_pin.value:  # Active low
        print("Interrupt triggered!")
        interrupt_flags = sensor.interrupt_flags
        print("Interrupt flags:", interrupt_flags)
        
        print("Proximity:", sensor.proximity)
        print("Ambient Light:", sensor.lux)
        if interrupt_flags["PROX_AWAY"]:
            print("Proximity: Object moved away")
        if interrupt_flags["PROX_CLOSE"]:
            print("Proximity: Object close")
        if interrupt_flags["ALS_HIGH"]:
            print("ALS: Light level too high")
        if interrupt_flags["ALS_LOW"]:
            print("ALS: Light level too low")
        time.sleep(0.5)
    else:
        print(f"Ambient: {sensor.lux}, Proximity: {sensor.proximity}")
    
    time.sleep(0.1)