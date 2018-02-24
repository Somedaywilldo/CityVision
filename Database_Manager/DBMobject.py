import logging
import os

class DBMobject(object):
    def __get_cu__(self,conn):
        if conn is not None:
            return conn.cursor()
        else:
            return None

    def __init__(self, logname="DBMobject"):
        self.__conn = None
        self.logger = logging.getLogger(logname)
        self.logpath = logname + ".log"
        formatter = logging.Formatter('%(asctime)s line:%(lineno)d,%(funcName)s %(levelname)-8s: %(message)s')
        file_handler = logging.FileHandler(logname+".log")
        file_handler.setFormatter(formatter)
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        self.logger.addHandler(console)
        self.logger.addHandler(file_handler)
        self.logger.setLevel(logging.INFO)
        if(logname=="DBMobject"):
            self.logger.error("logname may be wrong.")


