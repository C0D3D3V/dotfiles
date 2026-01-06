#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import os
import time
import notify2
from playsound import playsound


def notify_warning(title, battery_name, text, icon_path):
    notify2.init(title)
    notification = notify2.Notification(title, text, icon=icon_path)
    notification.show()


def audio_warning(path):
    playsound(path)


if __name__ == "__main__":
    power_path = "/sys/class/power_supply/"
    battery = "BAT0"
    audio = True
    notify = True
    audio_path = os.path.expanduser("~") + "/.config/i3/audio/"
    icon_path = os.path.expanduser("~") + "/.config/i3/low-battery.png"
    warning_threshold = [20, 15, 5]
    time_cycle = 1

    test_audio = False
    test_notify = False

    if test_audio:
        print("Audio test")
        print("Warning audio")
        audio_warning(audio_path + "warning.wav")
        print("Plug-in audio")
        audio_warning(audio_path + "plug-in.wav")
        print("Plug-out audio")
        audio_warning(audio_path + "plug-out.wav")

    if test_notify:
        print("Notify test")
        notify_warning("Notification Test", "NO_BATTERY", "Test", icon_path)

    if test_audio or test_notify:
        exit()

    warning_threshold = sorted(warning_threshold, reverse=False)
    battery_path = power_path + battery

    adapter = glob.glob(power_path + "ADP*")[0]

    has_alerted = [False, False, False]


    power_supply_online = (
        True if float(open(adapter + "/online", "r").read()) == 1 else False
    )

    has_alerted_full = False
    old_power_supply_online = power_supply_online

    threshold = 2

    while True:
        power_supply_online = (
            True if int(open(adapter + "/online", "r").read()) == 1 else False
        )
        capacity = float(open(battery_path + "/capacity", "r").read())
        print("Power: {}%".format(capacity))
        print(
            "Status: {}".format(
                "Discharging" if not power_supply_online else "Charging"
            )
        )

        if not power_supply_online:
            # Steckt nicht am Netzteil
            if old_power_supply_online:
                # War vorher am Netzteil
                if notify:
                    notify_warning("Battery warning", battery, "discharging", icon_path)
                if audio:
                    audio_warning(audio_path + "plug-out.wav")
                # Reset alerts
                has_alerted_full = False

            if capacity < warning_threshold[threshold] and not has_alerted[threshold]:
                has_alerted[threshold] = True
                print(f"Warning battery below threshold {warning_threshold[threshold]}")
                if notify:
                    notify_warning(
                        "Battery warning",
                        battery,
                        f"battery capacity is below {int(capacity)}",
                        icon_path,
                    )
                if audio:
                    audio_warning(audio_path + "warning.wav")
                if threshold > 0:
                    threshold -= 1
        else:
            # Steckt am Netzteil
            if not old_power_supply_online:
                # War vorher nicht am Netzteil
                if notify:
                    notify_warning("Battery notice", battery, "charging", icon_path)
                if audio:
                    audio_warning(audio_path + "plug-in.wav")
                # Reset alerts
                has_alerted = [False, False, False]
                threshold = 2

            if capacity >= 98:
                if not has_alerted_full:
                    has_alerted_full = True
                    if notify:
                        notify_warning("Battery notice", battery, "full", icon_path)

        old_power_supply_online = power_supply_online

        print("-" * 79)
        time.sleep(time_cycle)
