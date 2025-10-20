"""
Logger class that implements a singleton logger
"""

import logging
import sys
from datetime import datetime
import click


class ClickFormatter(logging.Formatter):
    """Custom formatter that styles output similar to click.echo logs"""

    def format(self, record):
        current_time = datetime.now().strftime("%H:%M:%S")

        # Choose color based on level
        if record.levelno >= logging.ERROR:
            colored_time = click.style(f"[{current_time}]", fg="red")
        elif record.levelno >= logging.WARNING:
            colored_time = click.style(f"[{current_time}]", fg="yellow")
        elif record.levelno >= logging.INFO:
            colored_time = click.style(f"[{current_time}]", fg="blue")
        else:  # DEBUG
            colored_time = click.style(f"[{current_time}]", fg="green")

        # Format base message
        message = super().format(record)
        return f"{colored_time} {message}"


class SingleLineStreamHandler(logging.StreamHandler):
    """
    Custom handler that supports overwriting the same line when a record
    has an attribute 'same_line=True'. Automatically adds a newline
    before the next normal message.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._last_was_same_line = False

    def emit(self, record):
        try:
            msg = self.format(record)

            if getattr(record, "same_line", False):
                # Overwrite same line
                sys.stdout.write("\r" + msg)
                sys.stdout.flush()
                self._last_was_same_line = True
            else:
                # If previous log was same-line, ensure newline first
                if self._last_was_same_line:
                    sys.stdout.write("\n")
                    self._last_was_same_line = False
                sys.stdout.write(msg + "\n")
                sys.stdout.flush()

        except Exception: # pylint: disable=broad-exception-caught
            self.handleError(record)



class Logger:
    """Singleton Logger class with click-style color and same-line updates."""

    _instance = None
    _logger = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialize_logger()
        return cls._instance

    def _initialize_logger(self):
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(logging.DEBUG)

        handler = SingleLineStreamHandler()
        handler.setLevel(logging.DEBUG)

        formatter = ClickFormatter("%(message)s")
        handler.setFormatter(formatter)

        if not self._logger.handlers:
            self._logger.addHandler(handler)

    def get_logger(self):
        """Return logger instance"""
        return self._logger
