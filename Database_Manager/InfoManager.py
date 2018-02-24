import sqlite3
import os
import logging

class InfoManager(object):
	'''常量声明'''

	#防注入字符白名单
	__box_name ="ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_abcdefghijklmnopqrstuvwxyz."
	__box_argsi = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

	#sql操作模板语句
	__create_table_sql = '''CREATE TABLE %s (
								`pano` ntext NOT NULL,
								`heading` int NOT NULL,
								`lat` decimal(13,9) NOT NULL,
								`lng` decimal(13,9) NOT NULL,
								`address` ntext NOT NULL,
								`description` ntext NOT NULL,
								PRIMARY KEY (`pano`)
								)'''#ntext为UTF-8编码#decimal(总位数, 小数点后位数)#设置pano为key
	__savein_sql = '''insert INTO %s values (?, ?, ?, ?, ?, ?)'''
	__update_sql = '''UPDATE %s SET heading = ?, lat = ?, lng = ?, address = ?, description = ? WHERE pano = ?'''
	__selectByRange_sql = ''' SELECT * FROM %s WHERE lat>=%f and lat<=%f and lng>=%f and lng<=%f'''
	__select_sql = ''' SELECT * FROM %s WHERE 1'''

	#列名分类列表
	__key_box_ntext = ["pano", "address", "description"]
	__key_box_int = ["heading"]
	__key_box_float = ["lat", "lng"]

	def __init__(self, add = None, log_le = None):
		#初始化logging日志模块
		logging.basicConfig(level= logging.INFO,
							filename="DB_InfoManager.log",
							filemode='a',
							format='%(asctime)s line:%(lineno)d,%(funcName)s %(levelname)s %(message)s',
                			datefmt='%d %b %H:%M:%S')#filemode设置为附加模式#format设置日志记录的格式
		#logging模块是多线程安全的

		#链接数据库
		self.__conn=None
		add_temp=add
		address = ""
		if(add_temp is not None and os.path.exists(add_temp)):
			if(os.path.isfile(add_temp)):#如果是文件则尝试打开
				try:
					self.__conn= sqlite3.connect(add_temp)
				except Exception as err:
					logging.warning(str(err))
					print(str(err))
			else:#如果是目录则尝试在该目录下建立新的数据库
				address = add_temp
				print("The DB will be create under " + address)
				while (self.__checktablename(add_temp) == False):  # 输入数据库文件名
					logging.warning("DB's name is not allowed.")
					# print("The address or is empty.If the file is not exist, one will be created.")
					add_temp = input("Enter a name:")
				self.__add = address + add_temp
				# 尝试连接
				try:
					self.__conn = sqlite3.connect(self.__add)
				except Exception as err:
					logging.warning(str(err))
					print(str(err))
		else:
			#如果add为None则在当前文件夹下建立数据库
			while(self.__checktablename(add_temp) == False):#输入数据库文件名
				logging.warning("DB's name is not allowed.")
				#print("The address or is empty.If the file is not exist, one will be created.")
				add_temp = input ("Enter a name:")
			self.__add = address + add_temp
			#尝试连接
			try:
				self.__conn= sqlite3.connect(self.__add)
			except Exception as err:
				logging.warning(str(err))
				print(str(err))
	'''内部函数'''
	def __get_cu(self ):
		if self.__conn is not None:
			return self.__conn.cursor()
		else:
			return None
	# 获取数据库指针
	def __checktablename(self, tablename):
		if (tablename is None or type(tablename) is not str or tablename == ''):
			#logging.error("Type of tablename is not list(or None).")
			return False
		for i in tablename:
			if( i not in self.__box_name):
				return False
		return True
	#检查表名
	def __checkargsi(self,name):
		if (name is None or type(name) is not str or name == ''):
			#logging.error("Type of tablename is not list(or None).")
			return False
		for i in name:
			if( i not in self.__box_argsi):
				return False
		return True
	#检查参数名
	def __checkdata(self, data, typename):
		if (data is None or type(data) is not typename):
			#logging.error("Type of data is not list(or None).")
			return False
		return True
	#检查数据格式
	def __checknum(self, temp):
		if(temp is None):
			return False
		if(type(temp) is int or type(temp) is float):
			return True
		if(type(temp) is tuple or type(temp) is list):
			for i in temp:
				if(type(i) is not int and type(i) is not float):
					return False
			return True
		return False
	#检查数格式（支持元组）

	'''新建表'''
	def creNewTable(self, tablename = None):
		if (self.__checktablename(tablename)==False):
			logging.error("Type of tablename is not list(or None).")
			print("Type of tablename is not list(or None).")
			return False
		#check tablename
		if (self.__checktablename(tablename) == False):
			logging.error("Type of tablename is not list(or None).")
			return False
		cu = self.__get_cu()
		sql = self.__create_table_sql %tablename
		try:
			cu.execute(sql)
			self.__conn.commit()
			logging.info(sql)
			cu.close()
		except Exception as err:
			logging.warning(str(err))
			print(str(err))

	'''Dengrous!!!'''
	def dropTable(self,tablename = None):
		if (self.__checktablename(tablename)==False):
			logging.error("Type of tablename is not list(or None).")
			print("Tablename is empty.")
			return False

		sql = "DROP TABLE IF EXISTS " + tablename
		cu = self.__get_cu()
		try:
			cu.execute(sql)
			self.__conn.commit()
			logging.info(sql)
			cu.close()
		except Exception as err:
			logging.warning(str(err))
			print(str(err))


	'''savein:按补充数据库中的条目。若pano已存在，则保留先前条目，不进行更新'''
	def savein_list(self, tablename = None, data = None):
		if (self.__checkdata(data=data,typename=list)==False):
			logging.error("Type of data is not list(or None).")
			return False
		if(self.__checktablename(tablename)==False):
			logging.error("Type of tablename is not list(or None).")
			return False
		cu = self.__get_cu()
		if (cu is not None):
			for d in data:
				self.__savein(tablename=tablename,
							  cu=cu,
							  data=d)
			logging.info("")
			print("savein_list")
			try:
				self.__conn.commit()
				cu.close()
				return True
			except Exception as err:
				logging.warning(str(err))
				print(str(err))
				return False
		else:
			return False

	def __savein(self,tablename = None,data = None, cu = None):
		if (self.__checkdata(data=data, typename=tuple) == False):
			logging.error("Type of data is not list(or None).")
			return False
		if(cu == None):
			logging.error("Type of cu is not list(or None).")
			return False
		sql = self.__savein_sql % tablename
		try:
			cu.execute(sql, data)
		except Exception as err:
			logging.warning(str(err))
		return

	def savein_tuple(self, tablename = None, data = None):
		if (self.__checkdata(data=data, typename=tuple) == False):
			logging.error("Type of data is not list(or None).")
			return False

		if (self.__checktablename(tablename) == False):
			logging.error("Type of tablename is not list(or None).")
			return False

		cu = self.__get_cu()
		if (cu is not None):
			self.__savein(tablename=tablename,
						  cu=cu,
						  data=data)
			try:
				self.__conn.commit()
				logging.info(str(data))
				print("savein_tuple" + str(data))
				cu.close()
				return True
			except Exception as err:
				logging.warning(str(err))
				print(str(err))
				return False
		else:
			return False


	'''update:按补充数据库中的条目。若pano已存在，则更新先前条目'''
	def update_list(self, tablename = None, data = None):
		if (self.__checkdata(data=data,typename=list)==False):
			logging.error("Type of data is not list(or None).")
			return False
		if(self.__checktablename(tablename)==False):
			logging.error("Type of tablename is not list(or None).")
			return False
		cu = self.__get_cu()
		if(cu is not None):
			for d in data:
				self.__update(tablename=tablename,
							  cu=cu,
							  data=d)
			logging.info("")
			print("update_list")
			try:
				self.__conn.commit()
				cu.close()
				return True
			except Exception as err:
				logging.warning(str(err))
				print(str(err))
				return False
		else:
			return False

	def __update(self, tablename = None, data = None, cu = None):
		if (self.__checkdata(data=data, typename=tuple) == False):
			logging.error("Type of data is not list(or None).")
			return False
		if (cu == None):
			logging.error("Type of cu is not list(or None).")
			return False
		sql = self.__update_sql % tablename
		d = []
		for i in range(1,len(data)):
			d.append(data[i])
		d.append(data[0])
		d = tuple(d)
		try:
			cu.execute(sql, d)
		except Exception as err:
			logging.warning(str(err))
		return

	def update_tuple(self, tablename = None, data = None):
		if (self.__checkdata(data=data, typename=tuple) == False):
			logging.error("Type of data is not list(or None).")
			return False

		if (self.__checktablename(tablename) == False):
			logging.error("Type of tablename is not list(or None).")
			return False

		cu = self.__get_cu()
		if(cu is not None):
			self.__update(tablename=tablename,
						  cu=cu,
						  data=data)
			try:
				self.__conn.commit()
				logging.info(str(data))
				print("update_tuple" + str(data))
				cu.close()
				return True
			except Exception as err:
				logging.warning(str(err))
				print(str(err))
				return False
		else:
			return False


	'''GetInfo:获取数据库中的相关信息'''
	def fetchall(self, tablename = None):
		if (self.__checktablename(tablename) == False):
			logging.error("Type of tablename is not list(or None).")
			return False
		sql = '''SELECT * FROM %s'''%tablename
		cu = self.__get_cu()
		r = None
		try:
			cu.execute(sql)
			r = cu.fetchall()
			logging.info(sql)
			self.__conn.commit()
			cu.close()
			print(sql)
		except Exception as err:
			logging.warning(str(err))
			print(str(err))
			return False
		return r
	#获取全部信息，返回值为list
	def select(self, args = None, tablename =None):
		r = None
		if (self.__checktablename(tablename) == False):
			logging.error("Type of tablename is not list(or None).")
			return False
		if(type(args) is not list):
			logging.warning("args is not list")
			return False
		sql = self.__select_sql
		t =[]
		flag = 0
		for i in args:
			if(type(i) is not tuple):
				continue
			else:
				if(self.__checkargsi(i[0])==False):
					logging.warning("i[0] is not allowed.")
				else:
					if(i[0] in self.__key_box_ntext):
						flag = 1
						sql = sql +" and " + i[0] + " LIKE ?"
						t.append(i[1])
					else:
						if(i[0] in self.__key_box_int or i[0] in self.__key_box_float):
							flag = 1
							sql = sql + " and " + i[0] + "= ?"
							t.append(i[1])

		if(flag == 0):
			return False
		t = tuple(t)
		sql = sql % tablename
		print(sql)
		try:
			cu = self.__get_cu()
			cu.execute(sql,t)
			r =cu.fetchall()
			cu.close()
			logging.info(sql+str(t))
		except Exception as err:
			logging.warning(str(err))
			print(str(err))
		return r
	#按照要求获取信息，返回值为list
	#args需为list，元素为元组。
	# 每个元组包含两个元素，前一个必须为str，代表选取的列。
	#如果列为ntext，则匹配模式为like，支持模糊匹配查找
	#如果列为num，则匹配模式为数值等于，若想使用数值模糊匹配，可以使用selectByRange
	#元组中后一个可以为数值或文本，代表查找内容。此处不限制参数类型，由上游模块过滤筛选。

	def selectByRange(self,tablename = None, latran = (0,0), lngran = (0,0)):
		if(self.__checktablename(tablename)==False):
			logging.error("Type of tablename is not list(or None).")
			print("Type of tablename is not list(or None).")
			return False
		if(self.__checknum(latran)==False or self.__checknum(lngran)==False):
			logging.error("Latran or lngran is not allowed.")
			print("Latran or lngran is not allowed.")
			return False
		sql = self.__selectByRange_sql %(tablename, latran[0], latran[1], lngran[0], lngran[1])
		print(sql)
		cu = self.__get_cu()
		r = None
		try:
			cu.execute(sql)
			r = cu.fetchall()
			print("selectByCircle:" + tablename)
			logging.info("selectByCircle:" + tablename +str(latran)+":"+str(lngran))
		except Exception as err:
			logging.warning(str(err))
			print(str(err))
		return r
	# 按照要求获取信息，返回值为list
	#latran，lngran皆为元组: latran[0]<=result<=latran[1]（lngran同理）
	def showTables(self):
		cu = self.__get_cu()
		try:
			cu.execute("SELECT name FROM sqlite_master WHERE type='table'")
			r = cu.fetchall()
			print(r)
			logging.info(r)
			cu.close()
		except Exception as err:
			logging.warning(str(err))
			print(str(err))
			return False
		return r
	#获取数据库中全部的表，返回值为list
	def __del__(self):
		self.__conn.close()
		print("close")



		