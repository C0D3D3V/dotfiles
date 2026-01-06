#!/usr/bin/env python
# -*- coding: utf-8 -*-
import functools
import os
import subprocess

import psutil
from i3ipc import Connection


def is_process_running(process_name):
    """Check if there is any running process that contains the given name."""
    for proc in psutil.process_iter(attrs=["pid", "name"]):
        if process_name in proc.info["name"]:
            return True
    return False


def exp_usr(path):
    return os.path.expanduser(path)


def on_shutdown(conn, processes):
    for process in processes:
        process.terminate()

    # Ensure all subprocesses have terminated
    for process in processes:
        process.wait()
    conn.main_quit()


def main():
    # List of scripts to run as subprocesses
    cmds = [
        [exp_usr("~/.config/i3/lock.py")],  # screen lock
        [
            exp_usr("~/.config/i3/i3-workspace-names-daemon.py")
        ],  # deamon for dynamic i3 workspace names
        [exp_usr("~/.config/i3/battery-notify.py")],  # notifications on low battery
        [
            exp_usr("~/.config/i3/watch_keepassxc.py")
        ],  # watch keepassxc and stop evolution if needed
    ]

    # Start the subprocesses
    processes = []
    for cmd in cmds:
        process = subprocess.Popen(cmd)
        processes.append(process)

    conn = Connection()

    # Note: ipc_shutdown is also emitted on restart
    conn.on("ipc_shutdown", functools.partial(on_shutdown, processes=processes))

    try:
        # # Continuous check if 'i3' process is running
        # while True:
        #     if not is_process_running("i3"):
        #         print("i3 process not running. Terminating subprocesses.")
        #         for process in processes:
        #             process.terminate()
        #         break
        #     time.sleep(1)  # Check every second

        # Just wait for the i3 shutdown signal (also emitted on restart)
        conn.main()
    except KeyboardInterrupt:
        print("Received KeyboardInterrupt. Terminating subprocesses.")
        for process in processes:
            process.terminate()

        # Ensure all subprocesses have terminated
        for process in processes:
            process.wait()


if __name__ == "__main__":
    main()
