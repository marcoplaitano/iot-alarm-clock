# @file main.py
# @author marco
# @date 04 Oct 2021

import requests
import sources.alarm as _alarm
import sources.time_data as _timedata
import sources.wifi_connection as _wifi
import sources.lcd_display as _lcd_display
import sources.motion_sensor as _motion_sensor



#########################################
#            global variables           #
#########################################

CURRENT_TIME = _timedata.Time()

alarm = _alarm.Alarm(D14.PWM)

display = _lcd_display.LcdDisplay(I2C0)

motion_sensor = _motion_sensor.MotionSensor(D27)



#########################################
#               functions               #
#########################################

def error(msg=None):
    """Display given message or default error string. Enter endless loop."""
    while True:
        display.show([msg if msg else "ERROR!"])
        sleep(1000)
        display.clear()
        sleep(500)


def start_wifi():
    """Start a new WIFI connection if none is found."""
    if not _wifi.is_connected():
        display.show(["Connecting wifi."])
        if not _wifi.connect():
            error("NO INTERNET!")


def show_info(minutes):
    """Show current time and time to next alarm on display."""
    h = int(minutes/60)
    m = minutes - h * 60
    t = _timedata.Time(hour=h, minutes=m)
    display.show([CURRENT_TIME, "Alarm in " + t.format()])


def show_alarm():
    """Show alarm info on display while it rings."""
    display.show([alarm.time(), alarm.message()])


def retrieve_time():
    """Get current day and time from the internet."""
    start_wifi()
    display.show(["Retrieving time."])
    for _ in range(5):
        try:
            data = requests.get("http://worldclockapi.com/api/json/utc/now")
            date_time = str(data.json()["currentDateTime"]) # YYYY-MM-DDTHH:MMZ
            day_of_week = str(data.json()["dayOfTheWeek"])
        except Exception:
            continue
        time = _timedata.Time()
        time.set_day(day_of_week)
        time.set_hour((int(date_time[11:13]) + 2) % 24) # +2 because of timezone
        time.set_minutes(int(date_time[14:16]))
        return time
    else:
        error("CAN'T GET TIME!")


def sleep_to_next_day():
    """Sleep for the amount of seconds needed to get to the next day."""
    seconds = CURRENT_TIME.seconds_to(_timedata.Time(hour=23, minutes=59))
    # Sleep for some more just to make sure it reaches the following day.
    seconds += 90
    my_sleep(seconds)


def determine_time(prev_time, sleep_seconds):
    """Determine how much time has passed since the device has gone to sleep."""
    # Time for which the device has slept.
    sleep_hours = int(sleep_seconds/3600)
    sleep_minutes = int(sleep_seconds/60) - sleep_hours * 60

    new_day = prev_time.day()
    new_hour = prev_time.hour() + sleep_hours
    new_minutes = prev_time.minutes() + sleep_minutes

    while new_minutes > 59:
        new_minutes -= 60
        new_hour += 1
    while new_hour > 23:
        new_hour -= 24
        new_day = _timedata.next_day(new_day)

    CURRENT_TIME.update(new_day, new_hour, new_minutes)


def my_sleep(seconds=0):
    """Sleep for the given amount of seconds."""
    minutes = int(seconds / 60)
    remaining = seconds - minutes * 60

    for n in range(0, minutes):
        show_info(minutes - n)
        sleep(60 * 1000)
        determine_time(CURRENT_TIME, 60)

    sleep(remaining * 1000)
    determine_time(CURRENT_TIME, 60)
    show_info(0)



#########################################
#                 setup                 #
#########################################

alarm.set_time(7, 30)
alarm.set_message("Good morning!")
alarm.set_days_off(["Saturday", "Sunday"])



#########################################
#          program starts here          #
#########################################

while True:
    # Retrieving current time from the internet.
    CURRENT_TIME = retrieve_time()
    display.show([CURRENT_TIME])

    # Keep sleeping if today is day off.
    if alarm.is_day_off(CURRENT_TIME):
        sleep_to_next_day()
        continue

    # How long it has to sleep to reach next alarm time.
    wait_time = CURRENT_TIME.seconds_to(alarm.time())
    my_sleep(wait_time)

    show_alarm()
    alarm.on()
    while not motion_sensor.movement_detected():
        sleep(1200)
        alarm.repeat()
    alarm.dismiss()
    # Sleep 90 seconds to reach next minute and avoid alarm going off again,
    # immediately after it has been dismissed.
    my_sleep(90)
    alarm.reset()
