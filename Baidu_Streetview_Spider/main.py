import urllib.request
import urllib.parse
from datetime import *
import shapefile
from math import *
import pygeohash as pgh
import json
import time
from random import randint
from multiprocessing import Pool
import os, time, random

#引入自己写的模块
from convert_txt_to_DB import *


root_path = "/Users/mac/Desktop/CityVision/"
city_name = "Beijing"


#根据url获取数据 格式：bytes（通用）
def get_data_from_url(url):
    response = urllib.request.urlopen(url);
    temp = response.read()
    return temp;

#保存街景图像，成功返回True，失败返回False
def save_picture(arg,path):
	global keys
	remove_flag = 0
	try:
		s = "http://api.map.baidu.com/panorama/v2?fov=90&pitch=20&coordtype=wgs84ll&width=%d&height=%d&location=%f,%f&ak=%s&heading=%d"
		s = s % (arg["width"],arg["height"],arg["location"][0],arg["location"][1],arg["ak"],arg["heading"]) 
		data = get_data_from_url(s)
		#print(data)
		test_data = {}
		try:
			test_data = json.loads(data)
			if(test_data["message"]=="request over" or test_data["status"]=="302"):
				remove_flag = 1
				print("Key burnt:",arg["ak"])
				#print(len(keys))
				keys.remove(arg["ak"])
				#print(keys)
				#print("Key left number:",len(keys))
		except:
			test_data = {} #fail to load json,说明这真的是图片不是错误信息
		if(remove_flag == 1):
			keys.remove(arg["ak"])
		if (test_data != {}):
			return False
		else:
			f = open(path, "wb")
			f.write(data)
			f.close()
			return True
	except:
		return False

def get_rev_info(arg):
	global keys
	s = 'http://api.map.baidu.com/geocoder/v2/?coordtype=wgs84ll&pois=1&output=json&location=%f,%f&radius=%d&ak=%s'
	s = s % (arg["location"][1],arg["location"][0],arg["radius"],arg["ak"])
	data = get_data_from_url(s).decode()
	#print(data)
	remove_flag = 0
	try:
		test_data = json.loads(data)
		if(test_data["message"]=="天配额超限，限制访问" or test_data["status"]==302):
			remove_flag = 1
			print("Key burnt:",arg["ak"])
			keys.remove(arg["ak"])
			#print("Key left number:",len(keys))
	except:
		test_data = {} #fail to load json,说明这真的是图片不是错误信息
	if(remove_flag == 1):
		keys.remove(arg["ak"])
	return data



point_file = shapefile.Reader("%sCity_Shapefile/%s/%s_Random_Inner_Point_2.shp"%(root_path,city_name,city_name))
point_temp = point_file.shapes()

point_set = []
for i in point_temp:
	point_set.append(i.points[0])

arg_rev_info = {
'location':[116.347945,40.000404],
'ak':'aMhjKoFAHR8W1cuQR5fcOKCIOsRQovgU',
'radius':1000
}

arg_picture={
'width':1024,
'height':512,
'location':[116.347945,40.000404],
'ak':'aMhjKoFAHR8W1cuQR5fcOKCIOsRQovgU',
'heading':0
}


def str_filter(x):
	return list(filter(lambda x:x!="",x))

#read cache 
catch_log = []
try:
	catch_log_file = open("%sBaidu_Streetview_Spider/Cache/%s_catchlog_file.txt"%(root_path,city_name),"r")
	catch_log_file.close()
except:
	catch_log_file = open("%sBaidu_Streetview_Spider/Cache/%s_catchlog_file.txt"%(root_path,city_name),"w")
	catch_log_file.write(r'{"time": 0, "try": 0, "catch": 0}')
	catch_log_file.write("\n")
	catch_log_file.close()
#{'time': 1, 'try': 3 ,'catch': 1}

catch_log_file = open("%sBaidu_Streetview_Spider/Cache/%s_catchlog_file.txt"%(root_path,city_name),"r")
catch_log = catch_log_file.read().split("\n")
catch_log = str_filter(catch_log)
catch_log_file.close()

last_time = 0 
last_try = 0
last_catch = 0
last_log = {}
if(len(catch_log)!=0):
	last_log = json.loads(catch_log[-1])
	last_time = last_log['time']
	last_try = last_log['try']
	last_catch = last_log['catch']

print("last_log:",last_log)

#read keys
keys_file = open("%sBaidu_Streetview_Spider/keys.txt"%(root_path),"r")
keys = []
keys = keys_file.read().split("\n")
keys = str_filter(keys)

#begin to spider
cnt_try = last_try
cnt_catch = last_catch
cnt_time = last_time+1


for i in range(last_try,len(point_set)):
	if(len(keys)==0):
		print("Run out of keys!")
		break
	#read to write new logs
	now_catch_log_file = open("%sBaidu_Streetview_Spider/Cache/%s_catchlog_file.txt"%(root_path,city_name),"a")
	now_img_info_file = open("%sBaidu_Streetview_Spider/Catched_data/%s/%s_img_info_file.txt"%(root_path,city_name,city_name),"a")
	#print(point_set[i])
	cnt_try += 1
	temp_arg_rev = arg_rev_info
	temp_arg_rev['location'][0] = round(point_set[i][0],6)
	temp_arg_rev['location'][1] = round(point_set[i][1],6)
	temp_arg_rev['radius']=10
	temp_arg_rev['ak'] = keys[i%len(keys)]

	#keys.remove(temp_arg_rev['ak'])
	#print("LEN: *****************,",len(keys))

	ret = get_rev_info(temp_arg_rev)
	ret = json.loads(ret)
	#print(ret)
	if(ret['status']==0):
		#print("success")
		address = ret['result']["formatted_address"]
		pois = ret['result']["pois"]
		if(len(pois)==0):
			continue
		for poi_index in range(len(pois)):
			one_poi = pois[poi_index]
			poi_description = one_poi['addr']
			poi_place = one_poi['name']
			poi_id = one_poi['uid']
			poi_coord = [one_poi["point"]["x"],one_poi["point"]["y"]]
			temp_arg = arg_picture
			temp_arg['location'] = poi_coord
			temp_arg['ak'] = keys[i%len(keys)]
			cnt_heading = 0
			now_img_info = "%s_%f_%f_%s_%s_%s"%(poi_id,poi_coord[0],poi_coord[1],
													address,poi_description,poi_place)
			now_img_info = now_img_info.replace("'","")
			if(find_DB(data_format(now_img_info))):
				print("Already exist!")
				continue
			#multiprocess
			#print('Parent process %s.' % os.getpid())
			
			print("Multiprocessing...")
			process = Pool(4)
			save_result=[]
			for j in range(4):
				temp_arg['heading'] = j*90
				img_path = '%sBaidu_Streetview_Pictures/%s/%s_%d.jpg'%(root_path,city_name,poi_id,j*90)
				save_result.append( process.apply_async(save_picture, args=(temp_arg,img_path,)) )
			#print('Waiting for all subprocesses done...')
			process.close()
			process.join()
			#print('All subprocesses done.')
			for res in save_result:
				cnt_heading += res.get()
			
			'''
			for j in range(4):
				temp_arg['heading'] = j*90
				img_path = '%sBaidu_Streetview_Pictures/%s/%s_%d.jpg'%(root_path,city_name,poi_id,j*90)
				cnt_heading += save_picture(temp_arg,img_path)
			'''
			if (cnt_heading == 4):
				cnt_catch += 1
				print("Total: %d Try: %d"%(len(point_set),cnt_try))
				print("Streetview Number:",cnt_catch)
				#
				temp_catch_log = {"time": cnt_time, "try": cnt_try, "catch": cnt_catch}
				now_catch_log = json.dumps(temp_catch_log)
				print(now_img_info)
				print(now_catch_log)
				now_catch_log_file.write(now_catch_log+"\n") 
				now_img_info_file.write(now_img_info+"\n")
				insert_DB(data_format(now_img_info))
		print("*******************************")
	print("-"*66)
	now_catch_log_file.close()
	now_img_info_file.close()





'''
temp_img_info = {
			"poi_id":"a",
			"poi_coord":[1,1],
			"address":"a",
			"poi_description":"a",
			"poi_place":"a"
			}
			temp_img_info["poi_id"]=poi_id
			temp_img_info["poi_coord"]=poi_coord
			temp_img_info["address"]=address
			temp_img_info["poi_description"]=poi_description
			temp_img_info["poi_place"]=poi_place
			#

'''


'''
http://api.map.baidu.com/panorama/v2?width=1024&height=512&fov=90&pitch=20&coordtype=wgs84ll
&location=116.347945,40.000404
&ak=aMhjKoFAHR8W1cuQR5fcOKCIOsRQovgU
&heading=0
'''

#逆向地址解析API
'''

http://api.map.baidu.com/geocoder/v2/
?location=39.811579,116.20381
&output=json
&pois=1
&radius=10
&ak=aMhjKoFAHR8W1cuQR5fcOKCIOsRQovgU
&coordtype=wgs84ll


'''


'''

http://api.map.baidu.com/geocoder/v2/?callback=renderReverse
&location=40.056628722822296,116.44511299336622
&output=json
&pois=1
&radius=10
&ak=aMhjKoFAHR8W1cuQR5fcOKCIOsRQovgU
&coordtype=wgs84ll


'''


