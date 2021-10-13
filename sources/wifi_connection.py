# @file wifi_connection.py
# @author marco
# @date 04 Oct 2021

from wireless import wifi
from espressif.esp32net import esp32wifi as wifi_driver


WIFI_NAME = "WIFI_NAME"
WIFI_PASSWORD = "WIFI_PASSWORD"


def connect():
    """Connect the board to the wifi."""
    if WIFI_PASSWORD == "WIFI_PASSWORD":
        return False

    wifi_driver.auto_init()

    try:
        wifi.link(WIFI_NAME, wifi.WIFI_WPA2, WIFI_PASSWORD)
        return True
    except Exception:
        return False


def disconnect():
    try:
        wifi.unlink()
        return True
    except Exception:
        return False


def get_ip_address():
    """Return the IP address associated to the device."""
    try:
        return wifi.link_info()[0]
    except Exception:
        return None


def is_connected():
    """Return whether the device is connected to wifi or not."""
    try:
        return wifi.is_linked()
    except Exception:
        return False
