# IoT Alarm Clock

A simple project to implement an IoT-based alarm clock.

- - - - - -

## Description

The current time and the info about the upcoming alarm is written on an LCD
Display.<br>
When the alarm goes off a passive buzzer plays a sequence of notes through
PWM.<br>
An infrared motion sensor can capture any movement, such as a hand gesture, that
can be interpreted as a wish from the user to turn off the alarm.*

The firmware has been produced with a version of the Python language derived
from the [Zerynth SDK] for IoT platforms.

<br>

\* Having in mind a use case in which the user is asleep and the alarm plays
early in the morning, there should be no concerns of other movements being
mistaken for the intentional dismissing of the alarm.

- - - - - -

## Usage

In the [main.py] file the user can modify the following lines to specify:
+ the alarm time
+ the message to display when the alarm goes off
+ the days of the week in which the alarm should not be active.

```py
alarm.set_time(7, 30)
alarm.set_message("Good morning!")
alarm.set_days_off(["Saturday", "Sunday"])
```

- - - - - -

## Components

+ ESP32-DevKitC development board
+ I2C LCD Display
+ Infrared Motion Sensor
+ Breadboard
+ Passive buzzer
+ 10k Ohm resistor
+ NPN transistor
+ *6x* M/M jumper wires
+ *7x* M/F jumper wires

- - - - - -

## License

Distributed under the [MIT License].


<!-- Links -->

[Zerynth SDK]:
https://www.zerynth.com/zsdk

[main.py]:
main.py

[MIT License]:
LICENSE