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

try:

    import RPi.GPIO as GPIO
    import time

    # Define GPIO to LCS mapping
    class LCD:
        #PIN Setup
        LCD_RS = 26
        LCD_E = 19
        LCD_D4 = 13
        LCD_D5 = 6
        LCD_D6 = 5
        LCD_D7 = 11

        GPIOoutLST = [LCD_RS, LCD_E, LCD_D4, LCD_D5, LCD_D6, LCD_D7]

        #Define device constants
        LCD_WIDTH   = 16
        LCD_CHR     = True      #RS Character
        LCD_CMD     = False     #RS Command

        LCD_LINE_1  = 0x80  #Ram Locations  (First Icon on Line)    0x80-0x96
        LCD_LINE_2  = 0xC0  #Ram Locations  (First Icon on Line)    0xC0-0xD6

        # Timing constants
        E_PULSE = 0.0005
        E_DELAY = 0.0005

        def __init__(self):
            GPIO.setwarnings(False)
            time.sleep(0.020)
            GPIO.setmode(GPIO.BCM)   # Use BCM GPIO numbers
            GPIO.setup(GPIOoutLST, GPIO.OUT)
            # lcd_byte(0x33, LCD_CMD)
            # lcd_byte(0x32, LCD_CMD)
            lcd_byte(0x06, LCD_CMD)  # 00000110 Cursor move direction
            lcd_byte(0x0C, LCD_CMD)  # 00001100 Display On,Cursor Off, Blink Off
            lcd_byte(0x28, LCD_CMD)  # 00101000 Data length, number of lines, font size
            lcd_byte(0x01, LCD_CMD)  # 00000001 Clear display
            time.sleep(E_DELAY)

        def lcd_byte(self, bits, mode):   #bits = bytes to send   mode LCD_CHR or LCD_CMD
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

            LCD.lcdToggleEnable(self)

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

            LCD.lcdToggleEnable(self)

        def cleanDisplay(self):
            lcd_byte(0x01, LCD_CMD)  # 00000001 Clean display

        def lcdToggleEnable(self):
            #Pulse the `enable` flag to process data
            GPIO.output(self.LCD_E, 0)
            time.sleep(LCD.E_DELAY)
            GPIO.output(self.LCD_E, 1)
            time.sleep(LCD.E_PULSE)
            GPIO.output(self.LCD_E, 0)
            time.sleep(LCD.E_DELAY)# commands need > 37us to settle

        def lcdString(self, string, line):
            #Sends string to LCD
            string = string.ljust(LCD.LCD_WIDTH, " ")
            LCD.lcd_byte(self, line, LCD.LCD_CMD)

            for char in range(LCD.LCD_WIDTH):
                LCD.lcd_byte(ord(string[i]), LCD.LCD_CHR)

except KeyboardInterrupt:
    GPIO.cleanup()
finally:
    GPIO.cleanup()

#https://www.raspberrypi-spy.co.uk/2012/07/16x2-lcd-module-control-using-python/
#https://www.openhacks.com/uploadsproductos/eone-1602a1.pdf
#http://oomlout.com/parts/LCDD-01-datasheet.pdf
#https://www.tutorialspoint.com/python/bitwise_operators_example.htm