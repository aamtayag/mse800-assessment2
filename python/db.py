# coding=utf-8
import logging
import sqlite3


class DBBase(object):
    def __init__(self):
        self.db_conn = None
        pass

    def connect(self):
        logging.error('connect function need to be implemented by subclass')
        raise NotImplementedError
        pass

    def close(self):
        pass

    def get_connection(self):
        return self.db_conn


class DBSqlite(DBBase):
    def __init__(self):
        super().__init__()

        pass

    def connect(self):
        dbfilename = '../TourBooking.db'
        self.db_conn = sqlite3.connect(dbfilename)
        logging.debug(f"connect to sqlite db:{dbfilename}")
        pass

    def close(self):
        self.db_conn.close()
        pass


g_db = None


def get_db_instance() -> DBBase:
    global g_db
    if g_db is None:
        g_db = DBSqlite()
        g_db.connect()
        g_db.get_connection()
    return g_db