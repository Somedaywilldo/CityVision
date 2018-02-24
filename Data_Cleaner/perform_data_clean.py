from DataCleaner import *
#dir format:/Users/mac/Desktop/CityWander/
cleaner=DataCleaner("Guangzhou","/data/yyh/CityWander/")

print("City:",cleaner.city_name)

cleaner.get_file_name()			#获取街景文件目录下的所有文件名
cleaner.error_point_name()		#使用文件名筛选出来的错误街景点
cleaner.deleter_name()			#删除error_point_name筛选出的文件
cleaner.get_info()				#筛选现在剩余街景文件的信息
cleaner.error_point_info()		#根据get_info方法筛选出的信息，找出信息有错误的街景点
cleaner.deleter_info()			#删除error_point_info方法找出的错误街景点
cleaner.error_info_to_name()	#找出文件名和信息不匹配的点
cleaner.deleter_info_to_name() 	#删除文件名和信息不匹配的点

