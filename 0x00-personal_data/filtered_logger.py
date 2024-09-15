#!/usr/bin/env python3
"""
Module for filtering log messages to obfuscate sensitive information.
"""

import re
from typing import List


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
