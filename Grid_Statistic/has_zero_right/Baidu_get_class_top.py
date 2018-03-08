import shapefile
import sqlite3 as sql
from math import *
import os

top_num=10

city_name = "Beijing"
root_path = "/Users/mac/Desktop/CityVision/"

CLASS = ['road','sidewalk','building','wall','fence','pole','traffic_light','traffic_sign','vegetation','terrain','sky','person','rider','car','truck','bus','train','motorcycle','bicycle']

for class_i in CLASS:
	os.system("mkdir %sBaidu_Class_Top_Pictures/%s/%s"%(root_path,city_name,class_i))
	
def get_top(top_num):
	city_name = "Beijing"
	root_path = "/Users/mac/Desktop/CityVision/"
	CLASS = ['road','sidewalk','building','wall','fence','pole','traffic_light','traffic_sign','vegetation','terrain','sky','person','rider','car','truck','bus','train','motorcycle','bicycle']
	#遍历数据库，获取街景点信息
	for class_i in CLASS:
		conn = sql.connect("%sBaidu_Semantic_Database/%s_Baidu_Semantic.db"%(root_path,city_name))
		cursor = conn.cursor()
		data = cursor.execute("SELECT poiid,%s FROM %s ORDER BY %s DESC"%(class_i,city_name,class_i))
		class_set=[]
		for row in data:
			class_set.append(row)
		print("Now is the class:",class_i)
		for i in range(top_num):
			print(class_set[i])
			for j in range(4):
				now_pano = class_set[i][0]
				now_heading = j*90
				os.system("cp %sBaidu_Streetview_Pictures/%s/%s_%d.jpg %sBaidu_Class_Top_Pictures/%s/%s"%(
					root_path,city_name,now_pano,now_heading,
					root_path,city_name,class_i))
				os.system("cp %sBaidu_RGB_Pictures/%s/%s_%d_rgb.png %sBaidu_Class_Top_Pictures/%s/%s"%(
					root_path,city_name,now_pano,now_heading,
					root_path,city_name,class_i))




for class_i in CLASS:
	os.system("mkdir %sBaidu_Class_Top_Pictures/%s/%s"%(root_path,city_name,class_i))
	#遍历数据库，获取街景点信息
	conn = sql.connect("%sBaidu_Semantic_Database/%s_Baidu_Semantic.db"%(root_path,city_name))
	cursor = conn.cursor()
	data = cursor.execute("SELECT poiid,%s FROM %s ORDER BY %s DESC"%(class_i,city_name,class_i))
	class_set=[]
	for row in data:
		class_set.append(row)
	print("Now is the class:",class_i)
	for i in range(top_num):
		print(class_set[i])
		for j in range(4):
			now_pano = class_set[i][0]
			now_heading = j*90
			os.system("cp %sBaidu_Streetview_Pictures/%s/%s_%d.jpg %sBaidu_Class_Top_Pictures/%s/%s"%(
				root_path,city_name,now_pano,now_heading,
				root_path,city_name,class_i))
			os.system("cp %sBaidu_RGB_Pictures/%s/%s_%d_rgb.png %sBaidu_Class_Top_Pictures/%s/%s"%(
				root_path,city_name,now_pano,now_heading,
				root_path,city_name,class_i))




'''
#升序排列，占比最低

for class_i in CLASS:
	os.system("mkdir %sClass_Bottom_Pictures/%s/%s"%(root_path,city_name,class_i))
	#遍历数据库，获取街景点信息
	conn = sql.connect(root_path+'Semantic_Pixel_Database/%s_Semantic.db'%city_name)
	cursor = conn.cursor()
	data = cursor.execute("SELECT pano,heading,%s FROM %s ORDER BY %s"%(class_i,city_name,class_i))
	class_set=[]
	for row in data:
		class_set.append(row)
	print("Now is the class:",class_i)
	for i in range(top_num):
		print(class_set[i])
		for j in range(4):
			now_pano = class_set[i][0]
			now_heading = (class_set[i][1]+j*90)%360
			os.system("cp %sStreetview_Pictures/%s/%s_%d.jpg %sClass_Bottom_Pictures/%s/%s"%(
				root_path,city_name,now_pano,now_heading,
				root_path,city_name,class_i))

'''

