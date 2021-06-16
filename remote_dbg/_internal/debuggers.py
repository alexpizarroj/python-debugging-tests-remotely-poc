import logging

import remote_pdb
import web_pdb

from .constants import (
    REMOTE_DBG_DEBUGGER_TYPE_REMOTE,
    REMOTE_DBG_DEBUGGER_TYPE_WEB,
    REMOTE_DBG_HOST,
    REMOTE_DBG_PORT,
)
from .events import log_event_starting_debug_session

logger = logging.getLogger(__name__)


class RemotePdb(remote_pdb.RemotePdb, object):
    """
    Project home:
        https://github.com/ionelmc/python-remote-pdb

    To connect to a debug session:
        which socat || brew install socat  # installs `socat` if you don't have it
        socat readline tcp:127.0.0.1:7200
    """

    def __init__(self):
        log_event_starting_debug_session(
            debugger_type=REMOTE_DBG_DEBUGGER_TYPE_REMOTE,
            host=REMOTE_DBG_HOST,
            port=REMOTE_DBG_PORT,
        )
        super(RemotePdb, self).__init__(host=REMOTE_DBG_HOST, port=REMOTE_DBG_PORT)


class WebPdb(web_pdb.WebPdb, object):
    """
    Project home:
        https://github.com/romanvm/python-web-pdb

    To connect to a debug session:
        open https://127.0.0.1:7200
    """

    def __init__(self):
        log_event_starting_debug_session(
            debugger_type=REMOTE_DBG_DEBUGGER_TYPE_WEB,
            host=REMOTE_DBG_HOST,
            port=REMOTE_DBG_PORT,
        )
        super(WebPdb, self).__init__(host=REMOTE_DBG_HOST, port=REMOTE_DBG_PORT)


def set_remote_trace():
    RemotePdb().set_trace()


def set_web_trace():
    WebPdb().set_trace()
