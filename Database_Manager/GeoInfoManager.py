from DBMobject import *
import sys
import sqlite3
from TableManager import Table
from TableManager import TableList
from cv2 import cv2
import numpy as np

class GeoInfoManager(DBMobject):
    __sql_create_table_header = '''CREATE TABLE %s ('''
    __savein_sql = '''insert INTO %s values ('''
    __update_sql = '''UPDATE %s SET heading = ?, lat = ?, lng = ?, address = ?, description = ? WHERE pano = ?'''
    __selectByRange_sql = ''' SELECT * FROM %s WHERE lat>=%f and lat<=%f and lng>=%f and lng<=%f'''
    __select_sql = ''' SELECT * FROM %s WHERE 1'''
    __classnum__ = 19
    def __init__(self, add=None, dbname=None):
        #init workspace add
        if(add==None):
            self.workspace_add = sys.path[0]
        else:
            self.workspace_add = add
        if(dbname!=None):
            self.DBname = dbname
            self.DB_log_name = dbname + "_DB"
            self.DBpath = self.workspace_add + "/" + self.DBname + ".db"
            super(GeoInfoManager, self).__init__(logname=self.DB_log_name)
        else:
            self.logger.error("dbname is none.")
            return
        try:
            self.__conn = sqlite3.connect(self.DBpath)
            self.logger.info("try to connect to the DB:"+self.DBpath)
            self.aTableList = TableList(conn=self.__conn, dbname=self.DBname)
        except Exception as err:
            self.logger.error(str(err))
            print(str(err))
            return

    def infofromfile(self, filepath=None):
        alist = []
        with open(filepath, 'r', encoding='UTF-8') as info:
            for i in info:
                temp = i.replace('\n', '')
                temp = temp.replace('\t', '')
                temp = temp.split('_')
                heading = int(temp[1])
                heading = heading % 90
                temp[1] = heading
                temp = tuple(temp)
                alist.append(temp)
        return alist
    def infofrompic(self, alist=None, picadd=None):
        aList = []
        print(len(alist))
        for ele in alist:
            heading_ori  = ele[1]
            NewClassList = [ 0 for k in range(0, self.__classnum__)]
            NewIList     = list(ele)
            #size         = 0
            for k in range(0,4):
                heading = (heading_ori + 90*k)%360
                picpath = picadd + "/" + str(NewIList[0]) + "_" + str(heading) + "_label.png"
                print(picpath)
                input_pic = cv2.imread(picpath, 1).astype(np.uint8)
                (input_pic_height, input_pic_width, pixnum) = input_pic.shape
                for i in range(0,input_pic_height):
                    for j in range(0,input_pic_width):
                        flag = input_pic[i][j][0]
                        NewClassList[flag] += 1
                #size+=input_pic.size
            NewIList = NewIList + NewClassList
            #NewIList.append(size)
            aList.append(tuple(NewIList))
        return aList

    def savelist(self,tablename=None, alist=None):
        aTable = self.aTableList.getTable(tablename=tablename)
        if(aTable is not None):
            aTable.savelist(alist)
        else:
            self.logger.warning("can not find the table.")



