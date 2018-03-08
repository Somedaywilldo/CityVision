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

'''
#less points
center_file = shapefile.Reader("%sCity_Shapefile/%s/%s_Inner_Center_001.shp"%(root_path,city_name,city_name))
grid_data = open("%sGrid_Statistic/%s_Grid_001_Data.txt"%(root_path,city_name),"w")
grid_length = 0.01
x_len,y_len = 32,40
'''


# more points
center_file = shapefile.Reader("%sCity_Shapefile/%s/%s_Baidu_0025_Point.shp"%(root_path,city_name,city_name))
grid_data = open("%sGrid_Statistic/%s_Grid_0025_Data.txt"%(root_path,city_name),"w")
grid_length = 0.0025
x_len, y_len = 132, 164


center_temp = center_file.shapes()
center_set = []
for i in center_temp:
	center_set.append(i.points[0])

center_set.sort()

#for i in center_set:
#	print(i)

img_size = 512*1024*4 #一个pano四张
sem_class = ['road','sidewalk','building','wall','fence','pole','traffic_light','traffic_sign','vegetation','terrain','sky','person','rider','car','truck','bus','train','motorcycle','bicycle']

#给定一个经纬度范围，返回该范围内的各类别平均值
def get_info_set(x):
	#遍历数据库，获取街景点经纬度信息
	conn = sqlite3.connect("%sBaidu_Semantic_Database/%s_Baidu_Semantic.db"%(root_path,city_name))
	cursor = conn.cursor()
	info = cursor.execute('''SELECT * FROM %s
							WHERE (lng >= %f AND lng <= %f) AND (lat >= %f AND lat<= %f) 
							'''%(city_name,x[0],x[1],x[2],x[3]))
	ret = np.zeros(19)
	set_len = 0
	for row in info:
		set_len += 1
		row_np = np.array(row[6:25])/img_size
		ret += row_np
	#	print(row_np)
	#print("set_len:",set_len)
	if(set_len !=0 ):
		ret = ret / set_len
	conn.close()
	return ret


def get_grid(x):
	global grid_length
	lng_min = x[0]-grid_length/2
	lng_max = x[0]+grid_length/2
	lat_min = x[1]-grid_length/2
	lat_max = x[1]+grid_length/2
	return [lng_min,lng_max,lat_min,lat_max]


cnt = 0

class_data = {}
for i in sem_class:
	class_data[i] = []

for i in range(len(center_set)):
	now_point = center_set[i]
	now_grid = get_grid(now_point)
	now_info = get_info_set(now_grid)
	#print(now_info)
	coord = [int(i%x_len),int(i//x_len)]
	for j in range(len(sem_class)):
		if(now_info[j]<0.01):
			continue
		class_data[sem_class[j]].append([coord[0],coord[1],round(now_info[j],2)])

for i in sem_class:
	now_class_data = []
	for j in range(len(class_data[i])):
		now_class_data.append(class_data[i][j][2])
	if(len(now_class_data) == 0):
		continue
	now_class_data = np.array(now_class_data) 
	min_max_scaler = preprocessing.MinMaxScaler()  
	now_class_data = min_max_scaler.fit_transform(now_class_data) 
	print(now_class_data)  
	print(len(now_class_data))
	for j in range(len(class_data[i])):
		class_data[i][j][2] = round(now_class_data[j],2)

grid_data.write(json.dumps(class_data))

