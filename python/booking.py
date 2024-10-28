# coding=utf-8

import logging
import db
import system


class booking_operation:
    def __init__(self):
        # self.db_conn = db.get_db_instance().get_connection()
        pass

    def update_booking_status(self, email, id, name, status):
        try:
            dbobj = db.DBSqlite()
            dbobj.connect()
            cursor = dbobj.get_connection().cursor()
            cursor.execute(
                "UPDATE bookings SET STATUS = ? WHERE EMAIL = ? AND ID = ?",
                (status, email, id),
            )
            dbobj.get_connection().commit()

            # Check to see if any lines are affected
            return cursor.rowcount > 0
        except Exception as e:
            logging.error(f"update_booking_status failed: {e}")
            return False

        pass
