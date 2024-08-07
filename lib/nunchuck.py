# source: https://github.com/kfricke/micropython-nunchuck

# The MIT License (MIT)

# Copyright (c) 2015 Kai Fricke

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
virtual = True

print("virtual: ", virtual)

if virtual:
    import timeE as time
else:
    import machine
    import time

class Nunchuck(object):
    """The Nunchuk object presents the sensor readings in a polling way.
    Based on the fact that the controller does communicate using I2C we
    cannot make it push sensor changes by using interrupts or similar
    facilities. Instead a polling mechanism is implemented, which updates
    the sensor readings based on "intent-driven" regular updates.

    If the "polling" way of updating the sensor readings is not sufficient
    a timer interrupt could be used to poll the controller. The
    corresponding update() method does not allocate memory and thereby
    could directly be used as an callback method for a timer interrupt."""

    """supports virtualisation with HyperVisor"""

    def __init__(self, i2c, poll=True):
        """Initialize the Nunchuk controller. If no polling is desired it
        can be disabled. Only one controller is possible on one I2C bus,
        because the address of the controller is fixed.
        The maximum stable I2C bus rate is 100kHz (200kHz seem to work on
        mine as well, 400kHz does not)."""

        
        self.i2c = i2c
        self.address = 0x52
        self.buffer = bytearray(b'\x00\x00\x00\x00\x00\x00')
        # There are two initialization sequences documented.
        #self.i2c.writeto(self.address, b'\x40\x00')
        #self.i2c.writeto(self.address, b'\x00')
        if virtual:
            from gigacube import HyperVisor
            self.h = HyperVisor.instance()
            return

        self.i2c.writeto(self.address, b'\xf0\x55')
        self.i2c.writeto(self.address, b'\xfb\x00')
        self.last_poll = time.ticks_ms()
        if poll:
            # Only poll every 50 milliseconds
            self.polling_threshold = 50
        else:
            # If no polling is desired we disable it completely
            self.polling_threshold = -1

    def update(self):
        """Requests a sensor readout from the controller and receives the
        six data bits afterwards."""
        if virtual:
            time.sleep_ms(10)
            return
        
        self.i2c.writeto(self.address, b'\x00')
        
        time.sleep_ms(10)
        
        self.i2c.readfrom_into(self.address, self.buffer)

    def __poll(self):
        """Poll the sensor readouts if necessary."""
        if virtual:
            self.update()
            return
        
        if time.ticks_diff(time.ticks_ms(), self.last_poll) > self.polling_threshold:
            self.update()

    def accelerator(self):
        """Retrieve the three axis of the last accelerometer reading.
        Returns a tuple of three elements: The x, y and z axis"""
        if virtual:
            raise NotImplementedError

        self.__poll()
        return ((self.buffer[2] << 2) + ((self.buffer[5] << 4) >> 6),
            (self.buffer[3] << 2) + ((self.buffer[5] << 2 ) >> 6),
            (self.buffer[4] << 2) + (self.buffer[5] >> 6))

    def buttons(self):
        """Returns a tuple representing the states of the button C and Z
        (in this order). The values are True if the corresponding button
        is being pressed and False otherwise."""
        if virtual:
            self.__poll()
            return self.h.getButtons()
        self.__poll()
        return (not (self.buffer[5] & 2 == 2), not (self.buffer[5] & 1 == 1))

    def joystick(self):
        """Get the X and Y positions of the thumb joystick. For both axis
        a value of 0 means left, ~136 center and 255 right position."""
        if virtual:
            raise NotImplementedError
        self.__poll()
        return (self.buffer[0], self.buffer[1])

    def joystick_left(self):
        """Returns True if the joystick is being held to the left side."""
        if virtual:
            self.__poll()
            return self.h.isLeft()
        
        self.__poll()
        return self.buffer[0] < 55

    def joystick_right(self):
        """Returns True if the joystick is being held to the right side."""
        if virtual:
            self.__poll()
            return self.h.isRight()
        self.__poll()
        return self.buffer[0] > 200

    def joystick_up(self):
        """Returns True if the joystick is being held to the upper side."""
        if virtual:
            self.__poll()
            return self.h.isUp()
        self.__poll()
        return self.buffer[1] > 200

    def joystick_down(self):
        """Returns True if the joystick is being held to the lower side."""
        if virtual:
            self.__poll()
            return self.h.isDown()
        self.__poll()
        return self.buffer[1] < 55

    def joystick_center(self):
        """Returns True if the joystick is not moved away fromthe center
        position."""
        if virtual:
            self.__poll()
            return self.h.isCenter()
        self.__poll()
        return self.buffer[0] > 100 and self.buffer[0] < 155 and self.buffer[1] > 100 and self.buffer[1] < 155

    def joystick_x(self):
        # Returns "normalized" x axis values
        if virtual:
            raise NotImplementedError
        self.__poll()
        return (self.buffer[0] >> 2) - 34

    def joystick_y(self):
        # Returns "normalized" x axis values
        if virtual:
            raise NotImplementedError
        self.__poll()
        return (self.buffer[1] >> 2) - 34
