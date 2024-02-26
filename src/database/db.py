import os
import sys
import sqlite3


DATABASE = "egtea_gaze_plus_cache.db"


def connect_to_database():
    try:
        return sqlite3.connect(DATABASE)
    except (sqlite3.Error, sqlite3.Warning) as e:
        raise Exception(e)


def create_cache_table():
    try:
        conn = connect_to_database()
        conn.execute(
            """CREATE TABLE IF NOT EXISTS http_cache
                     (ID            INTEGER PRIMARY KEY AUTOINCREMENT,
                     URL           TEXT NOT NULL,
                     TIMESTAMP     DATETIME NOT NULL,
                     HITS          INT NOT NULL DEFAULT   1
                     );"""
        )
        conn.close()
    except (sqlite3.Error, sqlite3.Warning) as e:
        raise Exception(e)


def insert_cache(url: str, timestamp: str) -> None:
    try:
        conn = connect_to_database()
        conn.execute(
            "INSERT INTO http_cache (URL, TIMESTAMP) VALUES (?, ?);",
            (url, timestamp),
        )
        conn.commit()
        conn.close()
    except (sqlite3.Error, sqlite3.Warning) as e:
        raise Exception(e)


def get_cached_response(url: str) -> tuple:
    try:
        conn = connect_to_database()
        cursor = conn.execute(
            "SELECT ID, TIMESTAMP FROM http_cache WHERE URL = ?;",
            (url,)
        )
        response = cursor.fetchone()
        conn.close()
    except (sqlite3.Error, sqlite3.Warning) as e:
        raise Exception(e)
    return response if response else (None, None, None, None)


def clean_cache() -> None:
    try:
        conn = connect_to_database()
        cursor = conn.execute("DELETE FROM http_cache;")
        conn.commit()
        conn.close()
        print("Cache cleaned")
    except (sqlite3.Error, sqlite3.Warning) as e:
        raise Exception(e)


def init_db() -> None:
    if not os.path.isfile(DATABASE):
        try:
            with open(DATABASE, "w") as f:
                pass
        except Exception as e:
            raise Exception(e)
        create_cache_table()