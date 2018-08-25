import sqlite3

from utils import unify_datetime

conn = sqlite3.connect('ts.db')
cursor = conn.cursor()


def create_table():
    cursor.execute('CREATE TABLE ts (cve text, ts text)')


def get_ts(cve_file_id):
    try:
        cursor.execute("SELECT ts FROM ts WHERE cve = '%s'" % cve_file_id)
    except sqlite3.OperationalError:
        create_table()
        cursor.execute("SELECT ts FROM ts WHERE cve = '%s'" % cve_file_id)

    rows = cursor.fetchall()

    for row in rows:
        if row:
            return unify_datetime(row[0])
        else:
            return None
    else:
        return None


def insert_ts(cve_file_id, ts_value):
    cursor.execute("INSERT INTO ts VALUES ('%s', '%s')" % (cve_file_id, ts_value))
    conn.commit()


def update_ts(cve_file_id, ts_value):
    cursor.execute("UPDATE ts SET ts = '%s' WHERE cve = '%s'" % (ts_value, cve_file_id))
    conn.commit()


def remove_record(cve_file_id):
    cursor.execute("DELETE from ts WHERE cve = '%s'" % cve_file_id)
    conn.commit()
