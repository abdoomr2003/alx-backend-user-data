#!/usr/bin/env python3
"""
This script provides a function to redact sensitive information from log
messages.

The `filter_datum` function replaces specified fields in a log message with
a redaction string.

Usage example:
    filtered_message = filter_datum(fields=["password", "email"],
    redaction="***", message="user=password=12345;email=user@example.com;",
    separator=";")
"""

import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    Redacts sensitive information from a log message.

    Args:
        fields (List[str]): A list of strings representing the field names to
        be redacted.
        redaction (str): The string to replace the field values with.
        message (str): The log message containing the sensitive information.
        separator (str): The character used to separate the fields in the log
        message.

    Returns:
        str: The log message with the specified fields redacted.

    Example:
        >>> filter_datum(fields=["password", "email"], redaction="***",
        message="user=password=12345;email=user@example.com;", separator=";")
        'user=password=***;email=***;'
    """
    for field in fields:
        pattern = rf"{field}=.*?{separator}"
        message = re.sub(pattern, rf"{field}={redaction}{separator}", message)
    return message
