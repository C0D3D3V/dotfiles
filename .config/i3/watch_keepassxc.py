#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
import time

import dbus
import dbus.mainloop.glib
from gi.repository import GLib

# Evolution bugs if the wallet is not open, so we pause it if the wallet closes

def on_properties_changed(*args, **kwargs):
    session_bus = dbus.SessionBus()
    secrets_service = session_bus.get_object(
        "org.freedesktop.secrets", "/org/freedesktop/secrets/aliases/default"
    )

    properties_interface = dbus.Interface(
        secrets_service, "org.freedesktop.DBus.Properties"
    )

    properties = properties_interface.GetAll("org.freedesktop.Secret.Collection")

    # Do not use "is True" here. We need == comparator
    locked = properties["Locked"] == True
    if locked:
        print("🔒 KeePassXC has been locked!")

        subprocess.run(
            ["killall", "evolution", "-s", "STOP"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

    else:
        print("🔓 KeePassXC has been unlocked!")
        time.sleep(0.1)
        subprocess.run(
            ["killall", "evolution", "-s", "CONT"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )


def listen_for_keepassxc_lock_events():
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    session_bus = dbus.SessionBus()

    session_bus.add_signal_receiver(
        on_properties_changed,
        dbus_interface="org.freedesktop.Secret.Service",
        signal_name="CollectionChanged",
        path="/org/freedesktop/secrets",
    )

    print("🔄 Listening for KeePassXC lock/unlock events...")
    loop = GLib.MainLoop()
    loop.run()


listen_for_keepassxc_lock_events()
