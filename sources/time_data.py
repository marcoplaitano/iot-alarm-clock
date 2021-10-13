# @file time_data.py
# @author marco
# @date 04 Oct 2021


class Time:
    def __init__(self, day="Monday", hour=0, minutes=0):
        self._day = day
        self._hour = hour
        self._minutes = minutes


    def format(self):
        """Return string in format 'HH:MM'."""
        h = "0" + str(self._hour) if self._hour < 10 else str(self._hour)
        m = "0" + str(self._minutes) if self._minutes < 10 else str(self._minutes)
        return h + ":" + m


    def __str__(self):
        return self._day + ", " + self.format()


    def __eq__(self, other):
        if type(other) != type(self):
            return False
        if self._day != other.day():
            return False
        return self._hour == other.hour() and self._minutes == other.minutes()


    def __ne__(self, other):
        return not self == other


    # This function exists because apparently zerynth version of Python does not
    # call __eq__ method when using '==' and explicitly calling __eq__ is not
    # elegant.
    def equals(self, other):
        """Return whether other time object is equal to self."""
        return self.__eq__(other)


    def set(self, time):
        """Copy time info from argument object."""
        self._day = time.day()
        self._hour = time.hour()
        self._minutes = time.minutes()


    def update(self, day, hour, minutes):
        """Set new values for all fields."""
        self._day = day
        self._hour = hour
        self._minutes = minutes


    def set_day(self, day):
        """Set day of the week."""
        self._day = day


    def set_hour(self, hour):
        """Set hour."""
        self._hour = hour


    def set_minutes(self, minutes):
        """Set minutes."""
        self._minutes = minutes


    def day(self):
        """Return day of the week."""
        return self._day


    def hour(self):
        """Return hour."""
        return self._hour


    def minutes(self):
        """Return minutes."""
        return self._minutes


    def seconds_to(self, other):
        """Calculate number of seconds needed to reach other time. Day of the
        week is not taken into account."""
        if self.equals(other):
            return 0

        sh = self._hour
        sm = self._minutes
        oh = other.hour()
        om = other.minutes()

        if sh == oh:
            # Same hour but self is some minutes behind.
            if sm <= om:
                return (om - sm) * 60
            # Same hour but other_time has already passed, it is now 23:XX hours
            # and minutes away.
            # REMAINING MINUTES is: 60 - SM + OM
            # If SM > OM it still works but the result will be > 60. It is fine
            # since what matters is the number of seconds and saying
            #  (75min * 60)  or  (1h * 3600 + 15min * 60)  has the same effect.
            else:
                return 23 * 3600 + (60 - sm + om) * 60
        # Self is hours behind. It adds (OH - SH - 1) complete hours and then
        # the remaining minutes.
        # e.g. self = 2:30, other = 5:15. It considers (5-2-1)=2 complete hours
        #      to get to 4:30 and then (60-30+15)=45 minutes left to get from
        #      4:30 to 5:15.
        # It also works if other is just 1 hour away, in that case:
        # (OH - SH - 1) = (OH - (OH - 1) - 1) = 0
        # and it only considers the remaining minutes.
        elif sh < oh - 1:
            return 3600 * (oh - sh - 1) + (60 - sm + om) * 60
        # Self is hours ahead.
        else:
            return 3600 * (24 - sh + oh - 1) + (60 - sm + om) * 60



days_of_the_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
                    "Saturday", "Sunday"]


def next_day(day):
    """Return next day of the week"""
    index = days_of_the_week.index(day)
    return days_of_the_week[(index + 1) % 7]
