from __future__ import print_function

import time
import signal

from remote_dbg._internal.events import read_all_events
from remote_dbg._internal import constants


_continue_running = True


def main():
    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)

    info("Starting to monitor remote debugger events")
    time.sleep(2)

    global _continue_running
    last_event_seen_idx = -1

    while _continue_running:
        events = read_all_events()

        for idx in range(last_event_seen_idx + 1, len(events)):
            event = events[idx]
            event_type = event["event_type"]
            event_data = event["event_data"]

            if event_type == constants.REMOTE_DBG_EVENT_TYPE_STARTING_DEBUG_SESSION:
                debugger_type = event_data["debugger_type"]
                port = event_data["port"]
                info("New {} debugger session available on port {}".format(debugger_type.lower(), port))
            else:
                warning("Ignoring unrecognized event type: {}".format(event_type))

        last_event_seen_idx = len(events) - 1
        time.sleep(2)

    info("Shutting down. Bye!")


def info(msg):
    print("[MONITOR_DEBUG_EVENTS] {}".format(msg))


def warning(msg):
    info("WARNING: {}".format(msg))


def handle_exit(*args):
    global _continue_running
    _continue_running = False


if __name__ == "__main__":
    main()
