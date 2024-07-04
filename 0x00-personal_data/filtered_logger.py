#!/usr/bin/env python3
"""
"""

import logging
import re
import os
import mysql.connector
from typing import List

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str):
    """
    Returns log Message
    """
    for f in fields:
        message = re.sub(
            rf"{f}=(.*?)\{separator}", f"{f}={redaction}{separator}", message
        )
    return message


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        return filter_datum(
            self.fields, self.REDACTION, super().format(record), self.SEPARATOR
        )


def get_logger() -> logging.Logger:
    """creating a logger"""
    log = logging.getLogger("user_data")
    log.setLevel(logging.INFO)
    log.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    log.addHandler(handler)
    return log


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Get a secure db connection
    """

    host = os.environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    user = os.environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    pwd = os.environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    db = os.environ.get("PERSONAL_DATA_DB_NAME")
    conn = mysql.connector.connect(
        host=host,
        database=db,
        user=user,
        password=pwd
        )
    return conn


def main():
    """
    Obtain Connection and retrieve rows in the users tables
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    for row in cursor:
        message = (
            f"name={row[0]}; email={row[1]}; phone={row[2]}; "
            + f"ssn={row[3]}; password={row[4]};ip={row[5]}; "
            + f"last_login={row[6]}; user_agent={row[7]};"
        )
        print(message)
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
