#!/usr/bin/env python3
"""
Module for filtering log messages and redacting sensitive information.
"""

import re
import logging
from typing import List


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str) -> str:
    """
    Replaces values of specific fields in a log message with a redacted value.

    Args:
        fields: List of field names to obfuscate.
        redaction: String to replace the obfuscated field values.
        message: The original log message.
        separator: The character that separates fields in the log message.

    Returns:
        The obfuscated log message as a string.
    """
    return re.sub(rf"({'|'.join(fields)})=[^{separator}]*",
                  lambda m: f"{m.group(1)}={redaction}",
                  message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class for filtering PII fields. """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize the formatter with a list of fields to redact.

        Args:
            fields: List of field names to obfuscate in log messages.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record by filtering out sensitive fields.

        Args:
            record: The log record to be formatted and obfuscated.

        Returns:
            The formatted string with sensitive data obfuscated.
        """
        original_message = super(RedactingFormatter, self).format(record)
        return filter_datum(
            self.fields,
            self.REDACTION,
            original_message,
            self.SEPARATOR)


def get_logger() -> logging.Logger:
    """
    Returns a logger with a StreamHandler and a RedactingFormatter.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)

    return logger
