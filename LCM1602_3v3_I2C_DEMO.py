#!/usr/bin/env python
#
# Demo Program using LCM1602-14 3v3 I2C Driver
#
# Author: Andy Whitt
#
# Last Revised: March 2021
#

from LCM1602_3v3_I2C_DRIVER import *

if __name__ == "__main__":

    print('3V3 1602 Serial Character LCD I2C Demo\n')

    try:

        lcdDisplay = LCM1602_LCD_I2C()

        print('Displaying two lines of text...\n')

        lcdDisplay.displayString('Line One________________Line Two')

    except Exception as reason:

        print('Terminated abnormally,', reason, '\n')

    print('program end')