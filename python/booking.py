# coding=utf-8

import logging
import db
import system



class booking_operation:
    def __init__(self):
        self.db_conn = db.get_db_instance().get_connection()
        pass

    def update_booking_status(self, email, tour, status):
        try:
            cursor = self.db_conn.cursor()
            cursor.execute('UPDATE booking SET status = ? WHERE email = ? AND tour = ?', (status, email, tour))
            self.db_conn.commit()
            return True
        except Exception as e:
            logging.error(f"update_booking_status failed: {e}")
            return False

        pass


