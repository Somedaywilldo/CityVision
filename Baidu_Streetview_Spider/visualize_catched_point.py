import shapefile
import sqlite3 as sql
from math import *

city_name = "Beijing"
root_path = "/Users/mac/Desktop/CityVision/"


catch_point_file = []
catch_point_file = shapefile.Writer(shapefile.POINTM) #3是直线，1是点
catch_point_file.autoBalance = 1
catch_point_file.field('City_Baidu')

#遍历数据库，获取街景点经纬度信息
conn = sql.connect('%sBaidu_Streetview_Database/%s_Baidu.db'%(root_path,city_name))
cursor = conn.cursor()
data = cursor.execute("SELECT poiid,lng,lat,address,description from %s_Baidu"%city_name)
for row in data:
	print("pano: %s | lng: %f| lat: %f |address: %s| description: %s"%tuple(row))
	catch_point_file.record(city_name)
	catch_point_file.point(row[1],row[2])

catch_point_file.save('%sCity_Shapefile/%s/%s_Baidu_Catched_Points.shp'%(root_path,city_name,city_name))
