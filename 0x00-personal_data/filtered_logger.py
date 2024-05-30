#!/usr/bin/env python3
"""
filtered_logger module
"""
from typing import List
import re
import logging
import os
import mysql.connector


# tuple containing the fields from user_data.csv
PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
     returns the log message obfuscated:
    """
    for f in fields:
        message = re.sub(f'{f}=.*?{separator}',
                         f'{f}={redaction}{separator}', message)
    return message


def get_logger() -> logging.Logger:
    """
    logget configuation and return the logger name
    """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Create a handler (a StreamHandler)
    stream_handler = logging.StreamHandler()

    # create a formatter
    formatter = RedactingFormatter(fields=PII_FIELDS)

    # set formatter for handler
    stream_handler.setFormatter(formatter)

    # add handler to logger
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    connect to database using credentials in environnement
    """
    username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')

    db_connection = mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=db_name
    )

    return db_connection


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
