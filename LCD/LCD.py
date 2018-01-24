# 1 : GND
# 2 : 5V
# 3 : Contrast      (0-5V) (GND)
# 4 : RS            (GPIO-PIN)
# 5 : Read Write      !Ground!
# 6 : Enable          (GPIO-PIN)
# 7 : Data Bit 0      Not Used
# 8 : Data Bit 1      Not Used
# 9 : Data Bit 2      Not Used
# 10 : Data Bit 3     Not Used
# 11 : Data Bit 4     GPIO-PIN
# 12 : Data Bit 5     GPIO-PIN
# 13 : Data Bit 6     GPIO-PIN
# 14 : Data Bit 7     GPIO-PIN
# 15 : Anode LCD      5V (1K Ohm?)
# 16 : Cathode LCD    GND

import RPi.GPIO as GPIO
import time

# Define GPIO to LCS mapping
LCD_RS  = 26
LCD_E   = 19
LCD_D4  = 13
LCD_D5  = 6
LCD_D6  = 5
LCD_D7  = 11
GPIOoutLST = [LCD_RS, LCD_E, LCD_D4, LCD_D5, LCD_D6, LCD_D7]

#Define device constants
LCD_WIDTH   = 16
LCD_CHR     = True
LCD_CMD     = False

LCD_LINE_1  = 0x80
LCD_LINE_2  = 0xC0

# Timing constants
E_PULSE = 0.00005
E_DELAY = 0.00005

def __init__(self):
    GPIO.setmode(GPIO.BCM)          # Use BCM GPIO numbers
    GPIO.setup(GPIOoutLST, GPIO.OUT)
