from pyfirmata2 import Arduino
import time

# Auto-detect the Arduino board
PORT = Arduino.AUTODETECT
board = Arduino(PORT)

led_1 = board.get_pin('d:6:o')
led_2 = board.get_pin('d:5:o')
led_3 = board.get_pin('d:4:o')
led_4 = board.get_pin('d:3:o')
led_5 = board.get_pin('d:2:o')

leds = [led_1, led_2, led_3, led_4, led_5]

def LED(fingers): 
    for i in range(5):
        if fingers[i] == 1:
            leds[i].write(1)
        else:
            leds[i].write(0)