# coding=utf-8

import logging
import db
import system

class user_entity(object):
    def __init__(self):
        self.id = None
        self.username = None
        self.password = None
        self.email = None
        self.role = None

        pass

    def __str__(self):
        return f"{self.id},{self.username},{self.email},{self.role}"
        pass



'''

CREATE TABLE users (
	ID int primary key autoincrement,
    USERNAME char(50) not null,
    EMAIL char(50) not null,
    PASSWORD char(50) not null,
    ROLE char(10) not null
);

'''

class user_operation(object):
    def __init__(self):
        self.db_conn = db.get_db_instance().get_connection()
        pass



    #add a new user to the database
    def add_user(self, new_user_email, new_username, password, roles):
        # try:
        #     id = system.generate_random_id()
        #     cursor = self.db_conn.cursor()
        #     cursor.execute('INSERT INTO users (ID,FNAME, LNAME, USERID, PASSWORD, ROLE, ENTERED_BY, ENTRY_DATE) VALUES (?,?, ?, ?, ?, ?, ?, datetime("now"))', (id,fname, lname, userid, password, role, entered_by))
        #     self.db_conn.commit()
        #     logging.debug('add_user success')
        #     return True
        # except Exception as e:
        #     logging.error(f"add_user failed: {e}")
        #     return False

        try:
            id = system.generate_random_id()
            dbobj = db.DBSqlite()
            dbobj.connect()
            cursor = dbobj.get_connection().cursor()
            cursor.execute('INSERT INTO users (ID,USERNAME, EMAIL, PASSWORD, ROLE) VALUES (?,?,?,?,?)', (id,new_username, new_user_email, password, roles))
            dbobj.get_connection().commit()
            return True
        except Exception as e:
            logging.error(f"add_user failed: {e}")
            return False

        pass


    #modify user roles
    def modify_user_roles(self, EMAIL, role):
        try:
            dbobj = db.DBSqlite()
            dbobj.connect()
            cursor = dbobj.get_connection().cursor()
            cursor.execute('UPDATE users SET ROLE = ? WHERE EMAIL = ?', (role, EMAIL))
            dbobj.get_connection().commit()
            return True
        except Exception as e:
            logging.error(f"modify_user_roles failed: {e}")
            return False

        pass



    #query user list
    def query_user_list(self):
        try:
            #cursor = self.db_conn.cursor()
            dbobj = db.DBSqlite()
            dbobj.connect()
            cursor = dbobj.get_connection().cursor()
            cursor.execute('SELECT ID,USERNAME,EMAIL,ROLE FROM users')
            ret = cursor.fetchall()
            userlist = []
            for user in ret:
                user_obj = user_entity()
                user_obj.id = user[0]
                user_obj.username = user[1]
                user_obj.email = user[2]
                user_obj.role = user[3]
                userlist.append(user_obj)
            return userlist
        except Exception as e:
            logging.error(f"query_user_list failed: {e}")
            return []

        pass



