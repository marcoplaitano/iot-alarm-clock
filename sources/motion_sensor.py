# @file motion_sensor.py
# @author marco
# @date 07 Oct 2021


class MotionSensor:
    def __init__(self, pin):
        self._pin = pin
        pinMode(self._pin, INPUT)


    def movement_detected(self):
        """Return True if motion has been detected"""
        return digitalRead(self._pin) == 1


    def value(self):
        """Return value caught by sensor. 1 = movement, 0 = quietness."""
        return digitalRead(self._pin)
