# coding=utf-8

import logging
import db
import system

class user_entity(object):
    def __init__(self):
        self.id = None
        self.fname = None
        self.lname = None
        self.userid = None
        self.password = None
        self.role = None
        self.entered_by = None
        self.entry_date = None
        pass

    def __str__(self):
        return f"id:{self.id}, fname:{self.fname}, lname:{self.lname}, userid:{self.userid}, password:{self.password}, role:{self.role}, entered_by:{self.entered_by}, entry_date:{self.entry_date}"
    pass


'''

CREATE TABLE users ( 
        ID int primary key not null, 
        FNAME char(50) not null, 
        LNAME char(50) not null, 
USERID char(50) not null, 
PASSWORD char(50) not null, 
ROLE char(10) not null, 
ENTERED_BY char(50) not null, 
ENTRY_DATE text not null 
);

'''

class user_operation(object):
    def __init__(self):
        self.db_conn = db.get_db_instance().get_connection()
        pass



    #add a new user to the database
    def add_user(self, fname, lname, userid, password, role, entered_by):
        try:
            id = system.generate_random_id()
            cursor = self.db_conn.cursor()
            cursor.execute('INSERT INTO users (ID,FNAME, LNAME, USERID, PASSWORD, ROLE, ENTERED_BY, ENTRY_DATE) VALUES (?,?, ?, ?, ?, ?, ?, datetime("now"))', (id,fname, lname, userid, password, role, entered_by))
            self.db_conn.commit()
            logging.debug('add_user success')
            return True
        except Exception as e:
            logging.error(f"add_user failed: {e}")
            return False

        pass


    #modify user roles
    def modify_user_roles(self, USERID, role):
        try:
            cursor = self.db_conn.cursor()
            cursor.execute('UPDATE users SET ROLE = ? WHERE USERID = ?', (role, USERID))
            self.db_conn.commit()
            return True
        except Exception as e:
            logging.error(f"modify_user_roles failed: {e}")
            return False

        pass



    #query user list
    def query_user_list(self):
        try:
            cursor = self.db_conn.cursor()
            cursor.execute('SELECT ID,FNAME,LNAME,USERID,ROLE FROM users')
            ret = cursor.fetchall()
            userlist = []
            for user in ret:
                user_obj = user_entity()
                user_obj.id = user[0]
                user_obj.fname = user[1]
                user_obj.lname = user[2]
                user_obj.userid = user[3]
                user_obj.role = user[4]
                userlist.append(user_obj)
            return userlist
        except Exception as e:
            logging.error(f"query_user_list failed: {e}")
            return []

        pass



