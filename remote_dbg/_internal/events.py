import json

import fasteners

from .constants import (
    REMOTE_DBG_EVENT_TYPE_STARTING_DEBUG_SESSION,
    REMOTE_DBG_EVENTS_FILE,
    REMOTE_DBG_EVENTS_FILE_LOCKFILE,
)

REMOTE_DBG_EVENTS_FILE_RW_LOCK = fasteners.InterProcessReaderWriterLock(REMOTE_DBG_EVENTS_FILE_LOCKFILE)


def log_event_starting_debug_session(debugger_type, host, port):
    _log_event(REMOTE_DBG_EVENT_TYPE_STARTING_DEBUG_SESSION, {"debugger_type": debugger_type, "host": host, "port": port})


def read_all_events():
    with REMOTE_DBG_EVENTS_FILE_RW_LOCK.read_lock():
        with open(REMOTE_DBG_EVENTS_FILE, "r") as fh:
            lines = fh.readlines()

    return [json.loads(line.strip()) for line in lines]


def _log_event(event_type, data):
    log_line = json.dumps({"event_type": event_type, "event_data": data}, sort_keys=True)
    with REMOTE_DBG_EVENTS_FILE_RW_LOCK.write_lock():
        # -- Artificially increase time spent for demonstration purposes
        # -- See: https://stackoverflow.com/questions/55361769/docker-and-file-locking
        # import time
        # time.sleep(5)  # seconds

        with open(REMOTE_DBG_EVENTS_FILE, "a") as fh:
            fh.write("{}\n".format(log_line))
