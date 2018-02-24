import sqlite3
from DBMobject import DBMobject
import logging
import re
class Table(DBMobject):
    __sql_create_table_header__= '''CREATE TABLE %s ('''
    __sql_drop_table__         = "DROP TABLE IF EXISTS %s"
    __sql_savein_model__       = "insert INTO %s values ("
    __sql_selectByRange__      = "SELECT * FROM %s WHERE lat>=%f and lat<=%f and lng>=%f and lng<=%f"
    __whitelist_name__         = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890_"
    __whitelist_args__         = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890(,)"

    def __check__name__(self,name):
        if(len(name)==0):
            return False
        for i in name:
            if i not in self.__whitelist_name__:
                return False
        return True
    def __check__args__(self,name):
        if (len(name) == 0):
            return False
        for i in name:
            if i not in self.__whitelist_args__:
                return False
        return True

    def __init__(self, conn=None, tablename=None, args=None, key=None):
        self.flag = False
        if(conn==None or tablename==None or args==None or key==None):
            return
        self.__conn         = conn
        self.TableName      = tablename.lower()
        self.Table_log_name = tablename.lower() + "_TABLE"
        self.args           = args
        self.key            = key
        self.argslen        = len(args)
        if (self.__check__name__(self.TableName) == False):
            self.logger.warning("TableName is forbidden.")
            return
        super(Table, self).__init__(logname=self.Table_log_name)
        self.__build_up__()

    def __build_up__(self):
        #__sql_savein__
        self.__sql_savein__ = self.__sql_savein_model__
        for i in range (0,len(self.args)-1):
            self.__sql_savein__ = self.__sql_savein__ + "?, "
        self.__sql_savein__  = self.__sql_savein__ + "?)"
        self.__sql_savein__ = self.__sql_savein__%self.TableName
        print(self.__sql_savein__)
    def createTableinDB(self):
        command = self.__sql_create_table_header__
        if(self.__check__name__(self.TableName)==False):
            self.logger.warning("TableName is forbidden.")
            return False

        for i in range(0,len(self.args)):
            if(self.__check__name__(self.args[i][0])==True and self.__check__args__(self.args[i][1])==True):
                command = command + "\n`" + self.args[i][0] + "` " + self.args[i][1] + " NOT NULL,"
            else:
                self.logger.warning("args are forbidden.")
                return False
        command =command + "\nPRIMARY KEY (`" + self.key + "`) )"
        print(command)
        command = command%self.TableName
        cu = self.__get_cu__(self.__conn)
        try:
            cu.execute(command)
            self.__conn.commit()
            self.logger.info(command)
            cu.close()
        except Exception as err:
            self.logger.warning(str(err))
        self.flag = True
    #def __dropTable__(self, ):

    def dropTable(self):
        command = self.__sql_drop_table__%self.TableName
        cu = self.__get_cu__(self.__conn)
        try:
            cu.execute(command)
            self.__conn.commit()
            logging.info(command)
            cu.close()
        except Exception as err:
            self.logger.error(str(err))
            return False
        return True
    def savelist(self, alist = None):
        if(isinstance(alist, list)):
            command = self.__sql_savein__
            cu = self.__get_cu__(self.__conn)
            for i in alist:
                if(isinstance(i, tuple)==False or len(i)!=self.argslen):
                    self.logger.warning("format wrong.[(,),]"+str(isinstance(i, tuple))+" "+str(i))
                    return
                else:
                    try:
                        cu.execute(command, i)
                        self.__conn.commit()
                        self.logger.info("insert:" + str(i))
                    except Exception as err:
                        self.logger.warning(str(err) + str(i))
        else:
            self.logger.warning("format wrong.[(,),]")

    def fetchall(self):
        if (self.__check__name__(self.TableName) == False):
            self.logger.error("Type of tablename is not list(or None).")
            return False
        sql = '''SELECT * FROM %s''' % self.TableName
        cu = self.__get_cu__(self.__conn)
        r = None
        try:
            cu.execute(sql)
            r = cu.fetchall()
            self.__conn.commit()
            cu.close()
            #print(sql)
        except Exception as err:
            self.logger.warning(str(err))
            return False
        return r
    def selectByRange(self,tablename = None, latran = (0,0), lngran = (0,0)):
        if(self.__check__name__(tablename)==False):
            self.logger.error("Type of tablename is not list(or None).")
            print("Type of tablename is not list(or None).")
            return False
        if(self.__check__name__(latran)==False or self.__check__name__(lngran)==False):
            self.logger.error("Latran or lngran is not allowed.")
            print("Latran or lngran is not allowed.")
            return False
        sql = self.__sql_selectByRange__ %(tablename, latran[0], latran[1], lngran[0], lngran[1])
        cu = self.__get_cu__(self.__conn)
        r = None
        try:
            cu.execute(sql)
            r = cu.fetchall()
            print("selectByCircle:" + tablename)
            self.logger.info("selectByCircle:" + tablename +str(latran)+":"+str(lngran))
        except Exception as err:
            self.logger.warning(str(err))
            print(str(err))
        return r
    # 按照要求获取信息，返回值为list
    #latran，lngran皆为元组: latran[0]<=result<=latran[1]（lngran同理）
    def showTables(self):
        cu = self.__get_cu__(self.__conn)
        try:
            cu.execute("SELECT name FROM sqlite_master WHERE type='table'")
            r = cu.fetchall()
            print(r)
            self.logger.info(r)
            cu.close()
        except Exception as err:
            self.logger.warning(str(err))
            print(str(err))
            return False
        return r
    def get_density(self,class_id,point1=(0,0),point2=(0,0)):
        num = class_id + 6
        list = self.selectByRange(self.TableName,(point1[0],point2[0]),(point1[0],point2[0]))
		div = len(list)*512*1024
        result = 0
        for i in list:
            result += i[num]
		result = result / div
        return result
class TableList(DBMobject):
    __sql_gettables__ = "SELECT name FROM sqlite_master WHERE type='table'"
    __sql_getlines__  = "select sql from sqlite_master WHERE name='%s'"

    def __init__(self, conn=None, dbname=None):
        if(conn==None or dbname==None):
            return
        self.__conn = conn
        self.__TableList__ = {}
        self.__TableListLen__ = 0

        self.TABLE_log_name = dbname+"_TABLELIST"
        super(TableList, self).__init__(logname=self.TABLE_log_name)
        self.__load_tablelist__()

    def __get_tablelist__(self):
        cu = self.__get_cu__(self.__conn)
        templist = []
        try:
            cu.execute(self.__sql_gettables__)
            self.__conn.commit()
            self.logger.info(self.__sql_gettables__)
            templist = cu.fetchall()
            cu.close()
        except Exception as err:
            self.logger.warning(str(err))
        return templist
    def __get_linelist__(self,tablename=None):
        cu = self.__get_cu__(self.__conn)
        templist = []
        temptypelist = []
        tempnamelist = []
        try:
            cu.execute(self.__sql_getlines__%tablename)
            self.__conn.commit()
            self.logger.info(self.__sql_getlines__)
            templist = cu.fetchall()
            templist = templist[0][0]
            temptypelist = re.findall("` (.+?) NOT NULL,",templist)
            tempnamelist = re.findall("`(.+?)`",templist)
            cu.close()
        except Exception as err:
            self.logger.warning(str(err))
        if(len(tempnamelist)!=len(temptypelist)+1):
            self.logger.warning("Unsupported DB type.")
        templist = []
        for i in range(0, len(temptypelist)):
            templist.append((tempnamelist[i], temptypelist[i]))

        return (templist, tempnamelist[len(tempnamelist)-1])
    def __load_tablelist__(self):
        templist = self.__get_tablelist__()
        #print(templist)
        if(len(templist)>0):
            for i in templist:
                tempname = i[0]
                (args, key) = self.__get_linelist__(tempname)
                NewTable = Table(conn= self.__conn, tablename=tempname, args=args, key=key)
                self.__TableList__[tempname] = NewTable
                self.__TableListLen__+=1
        print(self.__TableList__)
    def getTable(self, tablename=None):
        if(tablename in self.__TableList__):
            return self.__TableList__[tablename]
        else:
            self.logger.warning("No found.")
            return None

    def addTable(self, tablename=None, args=None, key=None):
        tablename = tablename.lower()
        #check
        for i in self.__TableList__:
            if(str(i).lower()==tablename):
                self.logger.warning("the table has existed.")
                return False
        #
        NewTable = Table(conn=self.__conn, tablename=tablename, args=args, key=key)
        if(NewTable.createTableinDB()==False):
            self.logger.warning("failed..")
            return False
        #
        self.__TableList__[tablename] = NewTable
        self.__TableListLen__+=1
        return True

    def update(self):
        self.__TableList__ = {}
        self.__TableListLen__ = 0
        self.__load_tablelist__()

    def dropTable(self,tablename=None):
        tablename = tablename.lower()
        for i in self.__TableList__:
            if(str(i).lower()==tablename):
                flag = self.__TableList__[tablename].dropTable()
                if(flag==True):
                    del self.__TableList__[tablename]
                    self.__TableListLen__-=1
                else:
                    self.logger.error("failed to drop Table. try update TableList")
