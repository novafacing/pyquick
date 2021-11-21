"""Set up logging when pyquick is imported"""

import logging
from typing import Any, Dict, List

from coloredlogs import ColoredFormatter, install

DEFAULT_LEVEL = "INFO"
MAX_NAME_LEN = 24
SNAME_INTERSP = "..."
LOG_FMT = (
    f"{{levelname:<8s}} | {{name:>{MAX_NAME_LEN + len(SNAME_INTERSP)}s}} | {{message}}"
)
FACTORY = logging.getLogRecordFactory()


def record_factory(*args: List[Any], **kwargs: Dict[str, Any]) -> logging.LogRecord:
    """
    Override the default logging record factory to truncate the logger name.

    :param args: The arguments to the record.
    :param kwargs: The keyword arguments to the record.
    """
    record = FACTORY(*args, **kwargs)
    if len(record.name) > MAX_NAME_LEN:
        record.name = (
            record.name[: MAX_NAME_LEN // 2]
            + SNAME_INTERSP
            + record.name[-(MAX_NAME_LEN // 2) :]
        )
    else:
        record.name = record.name.rjust(MAX_NAME_LEN + len(SNAME_INTERSP), " ")
    return record


try:
    logging.setLogRecordFactory(record_factory)
    root_logger = logging.getLogger()
    root_logger.setLevel(DEFAULT_LEVEL)
    root_handler = root_logger.handlers[0]
    root_handler.setFormatter(ColoredFormatter(fmt=LOG_FMT, style="{"))
except IndexError:
    install(level=DEFAULT_LEVEL, fmt=LOG_FMT, style="{", reconfigure=False)
