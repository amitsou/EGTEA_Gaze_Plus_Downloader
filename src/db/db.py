from utils.config import DATABASE
import os
import sqlite3
import logging


def get_db():
    try:
        return sqlite3.connect(DATABASE)
    except sqlite3.Error as e:
        logging.error(f"Error occurred while connecting to the database: {e}")
        raise Exception(e)

def create_downloads_table():
    try:
        conn = get_db()
        conn.execute(
            """CREATE TABLE DOWNLOADS
                     (ID            INTEGER PRIMARY KEY AUTOINCREMENT,
                     FNAME          TEXT NOT NULL,
                     URL            TEXT NOT NULL,
                     TIMESTAMP      DATETIME NOT NULL
                     );"""
        )
        conn.close()
    except sqlite3.Error as e:
        logging.error(f"Error occurred while creating the table: {e}")
        raise Exception(e)

def insert_to_db(filename: str, url: str, timestamp: str) -> None:
    try:
        conn = get_db()
        conn.execute(
            "INSERT INTO DOWNLOADS (FNAME, URL, TIMESTAMP) VALUES (?, ?, ?);",
            (filename, url, timestamp),
        )
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        logging.error(f"Error occurred while inserting into the database: {e}")
        raise Exception(e)

def delete_from_db(url: str) -> None:
    try:
        conn = get_db()
        conn.execute(f"DELETE FROM DOWNLOADS WHERE URL = '{url}';")
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        logging.error(f"Error occurred while deleting from the database: {e}")
        raise Exception(e)

def search_url(url_param: str) -> tuple:
    try:
        conn = get_db()
        cursor = conn.execute(
            f"""SELECT ID, FNAME, URL, TIMESTAMP FROM DOWNLOADS WHERE URL LIKE '%{url_param}%';"""
        )
        result = cursor.fetchone()
        conn.close()
    except sqlite3.Error as e:
        logging.error(f"Error occurred while searching the database: {e}")
        raise Exception(e)
    return result if result else None

def init_db() -> None:
    if not os.path.isfile(DATABASE):
        try:
            with open(DATABASE, "w"):
                pass
        except Exception as e:
            logging.error(f"Error occurred while creating the database: {e}")
            raise Exception(e)
        create_downloads_table()