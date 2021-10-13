# @file alarm.py
# @author marco
# @date 05 Oct 2021


import sources.buzzer as _buzzer
import sources.time_data as _timedata


class Alarm:
    def __init__(self, buzzer_pin, hour=8, minutes=0):
        self._time = _timedata.Time(hour=hour, minutes=minutes)
        self._buzzer = _buzzer.Buzzer(buzzer_pin)
        self._is_on = False
        self._dismissed = False
        self._num_repetitions = 0
        self._days_off = []
        self._message = "Wake up!"


    def set_time(self, hour, minutes):
        """Set time in which the alarm has to go off."""
        self._time.set(_timedata.Time(hour=hour, minutes=minutes))


    def set_message(self, message):
        """Set the message to display when the alarm goes off."""
        self._message = message


    def set_days_off(self, days):
        """Add days to the list of days off."""
        for day in days:
            if day not in self._days_off:
                self._days_off.append(day)


    def remove_days_off(self, days):
        """Remove days from the list of days off."""
        for day in days:
            if day in self._days_off:
                self._days_off.remove(day)


    def is_day_off(self, time):
        """Return whether the current day is a day off."""
        return time.day() in self._days_off


    def time(self):
        """Return alarm time."""
        return self._time


    def message(self):
        """Return alarm message."""
        return self._message


    def is_on(self):
        """Return whether alarm is currently on."""
        return self._is_on


    def is_dismissed(self):
        """Return whether alarm has been dismissed."""
        return self._dismissed


    def on(self):
        """Turn alarm on."""
        if self._is_on:
            return
        self._is_on = True
        self._dismissed = False
        self._buzzer.play_melody()


    def repeat(self):
        """Repeat alarm and increase melody's tonality."""
        if not self._is_on:
            return

        self._num_repetitions += 1
        # Can't go too high with the tonality.
        if self._num_repetitions > 3:
            self._num_repetitions = 0
            self._buzzer.restore_tone()
        else:
            self._buzzer.increase_tone()
        self._buzzer.play_melody()


    def dismiss(self):
        """Dismiss the alarm."""
        if not self._is_on:
            return
        self._is_on = False
        self._dismissed = True
        self._buzzer.stop()


    def reset(self):
        """Reset alarm's parameters for next usage."""
        self._is_on = False
        self._dismissed = False
        self._num_repetitions = 0
