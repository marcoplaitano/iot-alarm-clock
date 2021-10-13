# @file buzzer.py
# @author marco
# @date 06 Oct 2021

"""
The resistance used for the buzzer has been increased from recommended 1k to 10k
Ohm in order to decrease volume.
"""


import pwm


# names of the notes going from C3 to B4
notes_names = [
    "c3", "c#3", "d3", "d#3", "e3", "f3", "f#3", "g3", "g#3", "a3", "a#3", "b3",
    "c4", "c#4", "d4", "d#4", "e4", "f4", "f#4", "g4", "g#4", "a4", "a#4", "b4",
]

# frequences of the notes going from C3 to B4
notes_freqs = [
    130, 138, 146, 155, 164, 174, 185, 196, 208, 220, 233, 246,
    261, 277, 293, 311, 329, 349, 369, 392, 415, 440, 466, 493
]

# default melody used for the alarm
default_melody = ["g3", "a3", "b3", "c4", "d4", "d4", "g3"]



class Buzzer:
    def __init__(self, pwm_pin):
        self._pin = pwm_pin
        pinMode(self._pin, OUTPUT)
        self._melody = default_melody[:]


    def stop(self):
        """Disable PWM."""
        pwm.write(self._pin, 0, 0)


    def _play_note(self, note):
        """Play a single note."""
        period = 1000000 // note
        pwm.write(self._pin, period, period // 2, MICROS)


    def play_melody(self, melody=None):
        """Play a sequence of notes."""
        if not melody:
            melody = self._melody
        for note in melody:
            freq = notes_freqs[notes_names.index(note)]
            self._play_note(freq)
            sleep(500)
        self.stop()


    def increase_tone(self):
        """Increase default melody's tonality by a semitone."""
        i = 0
        for note in self._melody:
            self._melody[i] = notes_names[notes_names.index(note) + 1]
            i += 1


    def restore_tone(self):
        """Restore default melody's tonality."""
        self._melody = default_melody[:]
