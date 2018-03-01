from datetime import *
import shapefile
from math import *
import pygeohash as pgh
import json
import sqlite3
import numpy as np
from sklearn import preprocessing

root_path = "/Users/mac/Desktop/CityVision/"
city_name = "Beijing"

center_file = shapefile.Reader("%sCity_Shapefile/%s/%s_Inner_Center_001.shp"%(root_path,city_name,city_name))
center_temp = center_file.shapes()

center_set = []
for i in center_temp:
	center_set.append(i.points[0])

img_size = 512*1024*4 #一个pano四张
sem_class = ['road','sidewalk','building','wall','fence','pole','traffic_light','traffic_sign','vegetation','terrain','sky','person','rider','car','truck','bus','train','motorcycle','bicycle']

grid_lenth = 0.01

def get_info_set(now_class,x):
	#遍历数据库，获取街景点经纬度信息
	conn = sqlite3.connect("%sSemantic_Pixel_Database/%s_Semantic.db"%(root_path,city_name))
	cursor = conn.cursor()
	info = cursor.execute('''SELECT pano,lng,lat,%s FROM %s
							WHERE (lng >= %f AND lng <= %f) AND (lat >= %f AND lat<= %f) 
							'''%(now_class,city_name,x[0],x[1],x[2],x[3]))
	ret = []
	for row in info:
		#print("pano: %s | lng: %f| lat: %f | address: %s |class: %d"%tuple(row))
		ret.append(row[-1]/img_size)
	if(len(ret)==0):
		#print("No info!")
		return []
	conn.close()
	return ret

cnt = 0
x_len = 32
y_len = 40

grid_data = open("%sGrid_Statistic/%s_Grid_Data.txt"%(root_path,city_name),"w")

#class_data = np.zeros([len(sem_class),x_len,y_len])

data_multi = []

for class_i in range(len(sem_class)):
	class_data_list = []
	class_data = np.zeros([len(center_set),3])
	grid_data.write("\"%s\"=\n"%sem_class[class_i])
	print("\"%s\"="%sem_class[class_i])
	for i in range(len(center_set)):
		now_point = center_set[i]
		lng_min = now_point[0]-grid_lenth/2
		lng_max = now_point[0]+grid_lenth/2
		lat_min = now_point[1]-grid_lenth/2
		lat_max = now_point[1]+grid_lenth/2
		extent = [lng_min,lng_max,lat_min,lat_max]
		#print("*"*40)
		#print("Now Point",now_point)
		#print("Now Grid:",i)
		#print("Now extent:",extent)
		#print("Now class:",sem_class[j])
		now_info_set = []
		now_info_set = get_info_set(sem_class[class_i],extent)
		#print(i//y_len,i%y_len)
		if(len(now_info_set)==0):
			class_data[i]=[int(i//y_len)+1,int(i%y_len)+1,0]
		else:
			class_data[i]=[int(i//y_len)+1,int(i%y_len)+1,sum(now_info_set)/len(now_info_set)]
	#feature scaling
	#class_data/=class_data.max()
	min_max_scaler = preprocessing.MinMaxScaler()   
	class_data = min_max_scaler.fit_transform(class_data)   
	#class_data = preprocessing.MinMaxScaler(class_data)
	grid_data.write("[\n")
	print("[")
	for i in range(len(class_data)):
		#print(i)
		if(i != len(class_data)-1):
			class_data_list.append([int(i//y_len),int(i%y_len),class_data[i][2])])
			grid_data.write("[%d,%d,%f],"%(int(i//y_len),int(i%y_len),class_data[i][2]))
			print("[%d,%d,%f],"%(int(i//y_len),int(i%y_len),class_data[i][2]),end="")
		else:
			grid_data.write("[%d,%d,%f]"%(int(i//y_len),int(i%y_len),class_data[i][2]))
			print("[%d,%d,%f]"%(int(i//y_len),int(i%y_len),class_data[i][2]),end="")
	grid_data.write("]\n")
	print("]")
	grid_data.write(",\n")
	print(",")
		

'''
for class_i in range(len(sem_class)):
	class_data = np.zeros([len(center_set),3])
	grid_data.write("\"%s\"=\n"%sem_class[class_i])
	print("\"%s\"="%sem_class[class_i])
	for i in range(len(center_set)):
		now_point = center_set[i]
		lng_min = now_point[0]-grid_lenth/2
		lng_max = now_point[0]+grid_lenth/2
		lat_min = now_point[1]-grid_lenth/2
		lat_max = now_point[1]+grid_lenth/2
		extent = [lng_min,lng_max,lat_min,lat_max]
		#print("*"*40)
		#print("Now Point",now_point)
		#print("Now Grid:",i)
		#print("Now extent:",extent)
		#print("Now class:",sem_class[j])
		now_info_set = []
		now_info_set = get_info_set(sem_class[class_i],extent)
		#print(i//y_len,i%y_len)
		if(len(now_info_set)==0):
			class_data[i]=[int(i//y_len)+1,int(i%y_len)+1,0]
		else:
			class_data[i]=[int(i//y_len)+1,int(i%y_len)+1,sum(now_info_set)/len(now_info_set)]
	#feature scaling
	#class_data/=class_data.max()
	min_max_scaler = preprocessing.MinMaxScaler()   
	class_data = min_max_scaler.fit_transform(class_data)   
	#class_data = preprocessing.MinMaxScaler(class_data)
	grid_data.write("[\n")
	print("[")
	for i in range(len(class_data)):
		#print(i)
		if(i != len(class_data)-1):
			grid_data.write("[%d,%d,%f],"%(class_data[i][0],class_data[i][1],class_data[i][2]))
			print("[%d,%d,%f],"%(class_data[i][0],class_data[i][1],class_data[i][2]),end="")
		else:
			grid_data.write("[%d,%d,%f]"%(class_data[i][0],class_data[i][1],class_data[i][2]))
			print("[%d,%d,%f]"%(class_data[i][0],class_data[i][1],class_data[i][2]),end="")
	grid_data.write("]\n")
	print("]")
	grid_data.write(",\n")
	print(",")

'''

'''
		if(len(now_info_set)==0):
			#print(0)
			class_data[i//y_len][i%y_len] = 0
		else:
			#print(sum(now_info_set)/len(now_info_set))
			class_data[i//y_len][i%y_len] = sum(now_info_set)/len(now_info_set)
		'''
