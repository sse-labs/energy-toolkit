"""
Logger class that implements a singleton logger
"""

import logging


class Logger:
    """Singleton Logger class"""

    # Singleton instance
    _instance = None
    _logger = None
    _handler = None
    _formatter = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialize_logger()
        return cls._instance

    def _initialize_logger(self):
        """Creates a new logger object"""
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(logging.DEBUG)

        self._handler = logging.StreamHandler()
        self._handler.setLevel(logging.DEBUG)

        self._formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        self._handler.setFormatter(self._formatter)

        # Verhindern, dass Handler mehrfach hinzugefügt werden
        if not self._logger.handlers:
            self._logger.addHandler(self._handler)

    def get_logger(self):
        """Returns the singleton logger instance"""
        return self._logger
