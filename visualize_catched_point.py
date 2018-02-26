import shapefile
import sqlite3 as sql
from math import *

def dist(x,y): #两点欧氏距离
	x=list(x)
	y=list(y)
	return sqrt((x[0]-y[0])**2+(x[1]-y[1])**2)

def geo_dist(x,y):  #两点地理距离，单位km
	latitude1 = float(x[0])
	longitude1 = float(x[1])
	latitude2 = float(y[0]) 
	longitude2 = float(y[1])
	#地理距离，单位公里
	latitude1 = (pi/180.0)*latitude1  
	latitude2 = (pi/180.0)*latitude2  
	longitude1 = (pi/180.0)*longitude1  
	longitude2= (pi/180.0)*longitude2  
	#因此AB两点的球面距离为:{arccos[sina*sinx+cosb*cosx*cos(b-y)]}*R  (a,b,x,y)  
	#地球半径  
	R = 6378.1  
	temp=sin(latitude1)*sin(latitude2)+\
			cos(latitude1)*cos(latitude2)*cos(longitude2-longitude1)  
	if temp>1.0:  
		temp = 1.0  
	d = acos(temp)*R  
	return d

city_name = "Shanghai"
root_path = "/Users/mac/Desktop/CityVision/"


catch_point_file = []
catch_point_file = shapefile.Writer(shapefile.POINTM) #3是直线，1是点
catch_point_file.autoBalance = 1
catch_point_file.field('City')

#遍历数据库，获取街景点经纬度信息
conn = sql.connect(root_path+'Streetview_Database/%s.db'%city_name)
cursor = conn.cursor()
data = cursor.execute("SELECT pano,lng,lat,address from %s"%city_name)
for row in data:
	print("pano: %s | lng: %f| lat: %f | address: %s"%tuple(row))
	catch_point_file.record(city_name)
	catch_point_file.point(row[1],row[2])


catch_point_file.save(root_path+"City_Shapefile/%s/%s_Catched_Points"%(city_name,city_name))
