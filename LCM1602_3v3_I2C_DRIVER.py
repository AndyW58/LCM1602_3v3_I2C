#!/usr/bin/env python
#
# LCM1602-14 3v3 I2C Serial Character LCD Driver
#
# Author: Andy Whitt
#
# Last Revised: March 2021
#

import time
import smbus

# Instruction set

CLEAR_DISPLAY         = 0x01

ENTRY_MODE_SET        = 0x04
ENTRY_LEFT            = 0x02
ENTRY_RIGHT           = 0x00
ENTRY_SHIFT_INCREMENT = 0x01
ENTRY_SHIFT_DECREMENT = 0x00

DISPLAY_CONTROL       = 0x08
DISPLAY_ON            = 0x04
DISPLAY_OFF           = 0x00
CURSOR_ON             = 0x02
CURSOR_OFF            = 0x00
BLINK_ON              = 0x01
BLINK_OFF             = 0x00

FUNCTION_SET          = 0x20
_5x10DOTS             = 0x04
_5x8DOTS              = 0x00
_1LINE                = 0x00
_2LINE                = 0x08
_8BITMODE             = 0x10
_4BITMODE             = 0x00

_DISPLAY_LOGS = True

_i2cDev = smbus.SMBus(1)

_LCD_ADDR = 0x3E

_COLUMNS = 16
_ROWS    = 2

_COMMAND = 0X80
_DISPLAY = 0X40

class LCM1602_LCD_I2C:

    def __init__(self):
        
        self.currentColumn  = 0
        self.currentRow     = 0

        if _DISPLAY_LOGS == True : print('*** Initializing LCD\n')

        try:
        
            _i2cDev.read_byte(_LCD_ADDR)

            if _DISPLAY_LOGS == True : print('*** LCD device found at address : %X' % (_LCD_ADDR), '\n')

            self._lcdCommand(FUNCTION_SET    | _2LINE )
            self._lcdCommand(ENTRY_MODE_SET  | ENTRY_LEFT | ENTRY_SHIFT_DECREMENT )
            self._lcdCommand(DISPLAY_CONTROL | DISPLAY_ON | CURSOR_ON | BLINK_OFF )
            self._lcdCommand(CLEAR_DISPLAY )

            self._positionCursor(0,0)
        
            if _DISPLAY_LOGS == True : print('*** LCD Initialization Complete\n')

        except Exception as reason:

            print('*** LCD Initialization Failed,', _LCD_ADDR, '-', reason)

            raise SystemExit


    def _lcdCommand(self, instruction):

        if _DISPLAY_LOGS == True : print('*** Sending LCD Instruction : %X' % (instruction), '\n')

        try:
        
            _i2cDev.write_byte_data(_LCD_ADDR, _COMMAND, instruction)
            time.sleep(.01)

        except Exception as reason:

            print('!!! LCD command failed,', reason, '\n')

            raise SystemExit


    def _positionCursor(self, newRow, newColumn):
    
        if _DISPLAY_LOGS == True : print('*** Positioning Cursor to row:%d column:%d' % (newRow, newColumn),'\n')

        try:

            column = newColumn % _COLUMNS
            row = newRow % _ROWS

            if row == 0:

                instruction = column | 0x80

            else:

                instruction = column | 0xC0

            self.currentRow = row
            self.currentColumn = column

            self._lcdCommand(instruction)

        except Exception as reason:

            print('!!! Failed to position cursor,', reason, '\n')

            raise SystemExit


    def displayString(self, string):

        if _DISPLAY_LOGS == True : print('*** Displaying string: %s' % (string), '\n')

        try:

            for i in range(len(string)):

                time.sleep(.03)

                if _DISPLAY_LOGS == True :
                    
                    print('writing chars[%d]: %X to row:%d, column:%d\n' % (i, ord(string[i]), self.currentRow, self.currentColumn))

                _i2cDev.write_byte_data(_LCD_ADDR, _DISPLAY, ord(string[i]))
            
                self.currentColumn = self.currentColumn + 1
            
                if self.currentColumn >= _COLUMNS:
                
                    self._positionCursor(self.currentRow + 1, 0)

        except Exception as reason:

            print('!!! Failed to display string,', reason, '\n')

            raise SystemExit