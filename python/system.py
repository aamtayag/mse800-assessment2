# coding=utf-8

import random
import logging

import db


g_init_log = None

def init_log():
    global g_init_log
    if g_init_log is not None:
        return
    LOG_FORMAT = "[LOG]%(filename)s:%(lineno)d:%(funcName)s()  %(message)s"
    DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
    #logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, datefmt=DATE_FORMAT)
    logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)
    logging.debug("logging init finish")
    g_init_log = True

def init_db():
    db.get_db_instance()

def init_system():
    random.seed()

def generate_random_id():
    return random.randint(1, 9000000000)
