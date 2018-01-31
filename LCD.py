# 1 : GND
# 2 : 5V
# 3 : Contrast      (0-5V) (GND)
# 4 : RS            (GPIO-PIN) (Register Select)
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



# lcdString("Hier je string (max 16 breed", LCD_LINE_1 voor lijn 1
#                               LCD_LINE_2 voor lijn 2

import RPi.GPIO as GPIO
import time

scoreDisplay = None
status = None
counter = 0
counter1 = 1
# Define device constants
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)  # Use BCM GPIO numbers
LCD_WIDTH = 16
LCD_CHR = True  # RS Character
LCD_CMD = False  # RS Command

LCD_LINE_1 = 0x80  # Ram Locations  (First Icon on Line)    0x80-0x96
LCD_LINE_2 = 0xC0  # Ram Locations  (First Icon on Line)    0xC0-0xD6

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005



#Define GPIO to LCS mapping
#PIN Setup
GPIO.setmode(GPIO.BCM)  # Use BCM GPIO numbers
LCD_RS = 26
LCD_E = 19
LCD_D4 = 13
LCD_D5 = 6
LCD_D6 = 5
LCD_D7 = 20

GPIOoutLST = [LCD_RS, LCD_E, LCD_D4, LCD_D5, LCD_D6, LCD_D7]

def initLCD():

    time.sleep(0.020)
    for pin in GPIOoutLST:
        GPIO.setup(pin, GPIO.OUT)
    lcd_byte(0x33, LCD_CMD)
    lcd_byte(0x32, LCD_CMD)
    lcd_byte(0x06, LCD_CMD)  # 00000110 Cursor move direction
    lcd_byte(0x0C, LCD_CMD)  # 00001100 Display On,Cursor Off, Blink Off
    lcd_byte(0x28, LCD_CMD)  # 00101000 Data length, number of lines, font size
    lcd_byte(0x01, LCD_CMD)  # 00000001 Clear display
    time.sleep(E_DELAY)
    start()

def lcd_byte(bits, mode):   #bits = bytes to send   mode LCD_CHR or LCD_CMD
    GPIO.output(LCD_RS, mode)

    #High bits
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    if bits & 0x10 == 0x10:
        GPIO.output(LCD_D4, True)
    if bits & 0x20 == 0x20:
        GPIO.output(LCD_D5, True)
    if bits & 0x40 == 0x40:
        GPIO.output(LCD_D6, True)
    if bits & 0x80 == 0x80:
        GPIO.output(LCD_D7, True)

    lcdToggleEnable()

    # Low bits
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    if bits & 0x01 == 0x01:
        GPIO.output(LCD_D4, True)
    if bits & 0x02 == 0x02:
        GPIO.output(LCD_D5, True)
    if bits & 0x04 == 0x04:
        GPIO.output(LCD_D6, True)
    if bits & 0x08 == 0x08:
        GPIO.output(LCD_D7, True)

    lcdToggleEnable()

def cleanDisplay():
    lcd_byte(0x01, LCD_CMD)  # 00000001 Clean display


    

def lcdToggleEnable():
    #Pulse the `enable` flag to process data
    GPIO.output(LCD_E, 0)
    time.sleep(E_DELAY)
    GPIO.output(LCD_E, 1)
    time.sleep(E_PULSE)
    GPIO.output(LCD_E, 0)
    time.sleep(E_DELAY)# commands need > 37us to settle

def lcdString(string, line):
    #Sends string to LCD
    string = string.ljust(LCD_WIDTH, " ")
    lcd_byte(line, LCD_CMD)

    for char in range(LCD_WIDTH):
        lcd_byte(ord(string[char]), LCD_CHR)

def stop():
    cleanDisplay()
    lcdString("      Bye!", LCD_LINE_1)
    time.sleep(1)
    cleanDisplay()
    GPIO.cleanup()

def start():
    lcdString("-    GALAXY    -", LCD_LINE_1)
    time.sleep(0.2)
    lcdString(" -   GALAXY   - ", LCD_LINE_1)
    time.sleep(0.2)
    lcdString("  -  GALAXY  -  ", LCD_LINE_1)
    time.sleep(0.2)
    lcdString("   - GALAXY -   ", LCD_LINE_1)
    time.sleep(0.2)
    lcdString("    -GALAXY-    ", LCD_LINE_1)
    time.sleep(0.2)
    lcdString("     GALAXY     ", LCD_LINE_1)
    time.sleep(0.2)
    cleanDisplay()
    scoreDisplay = 0

def gameOver(scoreDisplay):
    cleanDisplay():
    lcdString("    GAME OVER   ", LCD_LINE_1)
    lcdstring(" Score  :"+str(scoreDisplay), LCD_LINE_2)

def score(scoreDisplay):
    cleanDisplay():
    lcdString("     GO! ", LCD_LINE_1)
    lcdString("Score   :" + str(scoreDisplay), LCD_LINE_2)
    gameOver(scoreDisplay)


    



initLCD()
start()
score(scoreDisplay)
