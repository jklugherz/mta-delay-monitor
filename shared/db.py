import os
from datetime import datetime

import pyodbc

db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')
db_server = os.environ.get('CLOUD_SQL_SERVER_NAME')


"""
DB TABLES: 

tbl_mta_subway_line
    - line_id (string, identity)
    - created_at (datetime)
    - is_delayed (boolean)

tbl_mta_subway_delay_alert
    - line_id (primary key)
    - alert id (primary key)
    - start (datetime)
    - end (datetime)
    - duration (int in seconds)
"""


def open_connection():
    connection = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + db_server + ';DATABASE=' + db_name + ';UID=' + db_user + ';PWD=' + db_password)
    return connection


def upsert_active_alert_duration(line_id: str, alert_id: str, start: datetime):
    # TODO: make this a merge into statement with open json - create the record if it doesn't exist yet
    connection = open_connection()
    cursor = connection.cursor()
    sql = """
    UPDATE tbl_mta_subway_delay_alert 
    SET duration = DATEDIFF(second, start, CURRENT_TIMESTAMP)
    WHERE line_id = ?
    AND alert_id = ?
    """
    result = cursor.execute(sql, (line_id, alert_id))
    connection.close()
    return result


def end_active_alert(line_id: str, alert_id: str, end: datetime):
    connection = open_connection()
    cursor = connection.cursor()
    sql = """
    UPDATE tbl_mta_subway_delay_alert 
    SET duration = DATEDIFF(second, start, ?)
        end = ?
    WHERE line_id = ?
    AND alert_id = ?
    """
    result = cursor.execute(sql, (end, end, line_id, alert_id))
    connection.close()
    return result


def set_is_delayed(line_id: str, is_delayed: bool):
    connection = open_connection()
    cursor = connection.cursor()
    sql = """
    UPDATE tbl_mta_subway_line 
    SET is_delayed = ?
    WHERE line_id = ?
    """
    result = cursor.execute(sql, (is_delayed, line_id))
    connection.close()
    return result


def get_is_delayed(line_id: str):
    connection = open_connection()
    cursor = connection.cursor()
    sql = """
    SELECT is_delayed FROM tbl_mta_subway_line
    WHERE line_id = ?
    """
    result = cursor.execute(sql, (line_id))
    connection.close()
    return result


def get_total_time_delayed(line_id: str):
    connection = open_connection()
    cursor = connection.cursor()
    sql = """
    SELECT SUM(duration) FROM tbl_mta_subway_delay_alert 
    where line_id = ?
    """
    result = cursor.execute(sql, (line_id))
    connection.close()
    return result


def get_total_time_line_exists(line_id: str):
    connection = open_connection()
    cursor = connection.cursor()
    sql = """
        SELECT DATEDIFF(s, created_at, CURRENT_TIMESTAMP) FROM tbl_mta_subway_line 
        where line_id = ?
        """
    result = cursor.execute(sql, (line_id))
    connection.close()
    return result

