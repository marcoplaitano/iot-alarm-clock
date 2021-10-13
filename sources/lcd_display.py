# @file lcd_display.py
# @author marco
# @date 06 Oct 2021


import i2c


EN = 0b00000100

LCD_FUNCTION_SET = 0x20
LCD_8BIT_MODE = 0x10
LCD_4BIT_MODE = 0x00
LCD_2LINES = 0x08
LCD_1LINE = 0x00
LCD_58DOTS = 0x00
LCD_DISPLAY_SET = 0x08
LCD_DISPLAY_ON = 0x04
LCD_DISPLAY_OFF = 0x00
LCD_CURSOR_ON = 0x02
LCD_CURSOR_OFF = 0x00
LCD_BLINK_ON = 0x01
LCD_BLINK_OFF = 0x00
LCD_ENTRY_MODE_SET = 0x04
LCD_ENTRY_LEFT = 0x02
LCD_SHIFT_DECREMENT = 0x00

LCD_CMD_MODE = 0
LCD_DATA_MODE = 1

LCD_BACKLIGHT_ON = 0x08
LCD_BACKLIGHT_OFF = 0x00

LCD_CLEAR = 0x01
LCD_HOME = 0x02
LCD_NEXT_LINE = 0xC0



class LcdDisplay():
    """This class lets the user work with an LCD 1602 I2C display."""
    def __init__(self, i2cdrv, width=16, two_lines=True, addr=0x27, clk=400000):
        self.port = i2c.I2C(i2cdrv, addr, clk)
        self.port.start()
        self._num_lines = 2 if two_lines else 1
        self._width = width
        self._cursor = 0
        self._backlight = LCD_BACKLIGHT_OFF

        self.backlight_off()

        # puts the display into 4 bits mode
        self._4bit_mode()

        # specifies the mode, the number of lines and size of each character
        num_lines = LCD_2LINES if self._num_lines == 2 else LCD_1LINE
        self._function_control = LCD_4BIT_MODE | num_lines | LCD_58DOTS
        self._command(LCD_FUNCTION_SET | self._function_control)

        # starts by default with display turned on, cursor and blink off
        self._display_control = LCD_DISPLAY_ON | LCD_CURSOR_OFF | LCD_BLINK_OFF
        self._command(LCD_DISPLAY_SET | self._display_control)

        self.clear()

        # sets the text direction
        self._command(LCD_ENTRY_MODE_SET | LCD_ENTRY_LEFT | LCD_SHIFT_DECREMENT)

        self.backlight_on()


    def show(self, data):
        """Clear the screen and show first 2 items of the list on the lines."""
        self.clear()
        self.print_str(data[0])
        if len(data) > 1:
            self.next_line()
            self.print_str(data[1])


    def print_str(self, data):
        """Print the given string on the display. If the string is too long stop
        at the last available cursor position."""
        string = str(data)
        for c in string:
            self.print_char(c)


    def print_char(self, c):
        """Print the character on the display, if there is enough space."""
        if self._next():
            self._data(int(ord(c)))
            self._cursor += 1


    def clear(self):
        """Clear the display and move the cursor back to the beginning."""
        self._command(LCD_CLEAR)
        sleep(2)
        self.home()


    def home(self):
        """Move the cursor back to the beginning of the display."""
        self._cursor = 0
        self._command(LCD_HOME)
        sleep(2)


    def next_line(self):
        """Go to the second line of the screen."""
        if self._num_lines == 1:
            return
        self._command(LCD_NEXT_LINE)
        self._cursor = 17


    def cursor_pos(self, pos, line=1):
        """Let the user pick a new position for the cursor."""
        # the count starts from position 0 on line 1
        rows = [0x00, 0x40, 0x14, 0x54]
        if pos > self._width * self._num_lines:
            return
        if pos > self._width:
            line = 2
            pos -= self._width
        if line > self._num_lines or line < 1:
            line = self._num_lines
        self._command(0x80 | pos + rows[line-1])


    def backlight_on(self):
        """Turn the backlight on."""
        self._backlight = LCD_BACKLIGHT_ON
        self._write_bytes(0)


    def backlight_off(self):
        """Turn the backlight off."""
        self._backlight = LCD_BACKLIGHT_OFF
        self._write_bytes(0)


    def cursor_on(self):
        """Turn the cursor on."""
        self._display_control |= LCD_CURSOR_ON
        self._command(LCD_DISPLAY_SET | self._display_control)


    def cursor_off(self):
        """Turn the cursor off."""
        self._display_control &= ~LCD_CURSOR_ON
        self._command(LCD_DISPLAY_SET | self._display_control)


    def blink_on(self):
        """Turn the cursor's blink on."""
        self._display_control |= LCD_BLINK_ON
        self._command(LCD_DISPLAY_SET | self._display_control)


    def blink_off(self):
        """Turn the cursor's blink off."""
        self._display_control &= ~LCD_BLINK_ON
        self._command(LCD_DISPLAY_SET | self._display_control)


    def _next(self):
        """Return whether another character can be written. It goes to a new
        line when possible."""
        if self._num_lines == 2 and self._cursor == self._width * 2:
            return False
        if self._cursor == self._width:
            if self._num_lines == 2:
                self.next_line()
            else:
                return False
        return True


    def _command(self, value):
        self._send(value, LCD_CMD_MODE)


    def _data(self, value):
        self._send(value, LCD_DATA_MODE)


    def _send(self, data, mode):
        highnib = data & 0xf0
        lownib = (data << 4) & 0xf0
        self._write((highnib) | mode)
        self._write((lownib) | mode)


    def _write(self, data):
        self._write_bytes(data)
        self._pulse_enable(data)


    def _write_bytes(self, values):
        self.port.write(values | self._backlight)


    def _pulse_enable(self, data):
        self._write_bytes(data | EN)
        sleep(1)
        self._write_bytes(data & ~EN)
        sleep(1)


    def _4bit_mode(self):
        self._write(0x03 << 4)
        sleep(5)
        self._write(0x03 << 4)
        sleep(5)
        self._write(0x03 << 4)
        sleep(5)
        self._write(0x02 << 4)
