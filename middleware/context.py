
import os

# This is a bad place for this import
import pymysql


def get_context():
    _default_context = {
        "auth_id": "6a771c1e-b994-4853-806d-10a6a166b76e",
        "auth_token": "C708kJT1NXFgVtA7O3cQ"
    }
    return _default_context

def get_db_info():
    """
    This is crappy code.

    :return: A dictionary with connect info for MySQL
    """
    db_host = os.environ.get("DBHOST", None)
    db_user = os.environ.get("DBUSER", None)
    db_password = os.environ.get("DBPASSWORD", None)

    if db_host is not None:
        db_info = {
            "host": db_host,
            "user": db_user,
            "password": db_password,
            "port": 3306,
            "cursorclass": pymysql.cursors.DictCursor
        }
    else:
        db_info = {
            "host": "localhost",
            "user": "root",
            "password": "09094130z",
            "cursorclass": pymysql.cursors.DictCursor
        }

    return db_info
