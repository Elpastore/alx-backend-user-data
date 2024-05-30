#!/usr/bin/env python3
"""
filtered_logger module
"""
from typing import List
import re
import logging


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
     returns the log message obfuscated:
    """
    for f in fields:
        message = re.sub(f'{f}=.*?{separator}',
                         f'{f}={redaction}{separator}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        format method
        """
        original_msg = record.getMessage()
        formated_msg = filter_datum(self.fields, self.REDACTION,
                                    original_msg, self.SEPARATOR)
        record.msg = formated_msg

        return super(RedactingFormatter, self).format(record)
