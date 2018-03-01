import sqlite3

root_path = "/Users/mac/Desktop/CityVision/"
city_name = "Shanghai"


#create database

def create_DB():
	conn = sqlite3.connect("%sBaidu_Streetview_Database/%s_Baidu.db"%(root_path,city_name))
	cursor = conn.cursor()
	cursor.execute(''' CREATE TABLE 
			%s_Baidu
	      (
	       poiid 		TEXT 	NOT NULL,
	       lng  		REAL	NOT NULL,
	       lat       	REAL    NOT NULL,
	       address      TEXT	NOT NULL,
	       description  TEXT	NOT NULL,
	       place 		TEXT	NOT NULL
	       );'''%city_name)
	print("Table created successfully")
	conn.commit()
	conn.close()

#insert
def insert_DB(data):
	if(find_DB(data)==True):
		return False
	conn = sqlite3.connect("%sBaidu_Streetview_Database/%s_Baidu.db"%(root_path,city_name))
	cursor = conn.cursor()
	temp_list = []
	for i in data:
		temp_list.append(data[i])
	cursor.execute("""INSERT INTO %s_Baidu (poiid,lng,lat,address,description,place)
	    VALUES 	('%s',   %f,  %f,'%s',  '%s', '%s')"""%tuple([city_name]+temp_list) )
	conn.commit()
	conn.close()
	return True

def find_DB(data):
	conn = sqlite3.connect("%sBaidu_Streetview_Database/%s_Baidu.db"%(root_path,city_name))
	cursor = conn.cursor()
	table = cursor.execute("SELECT poiid from %s_Baidu WHERE poiid == '%s'"%(city_name,data["poiid"]))
	cnt=0
	for row in table:
		cnt+=1
	conn.close()
	return (cnt!=0)

arg_data = {"poiid":"a",
	       "lng":0.1, 
	       "lat":0.1,
	       "address":"a",
	       "description":"a",
	       "place":"a"}	

def data_format(x):
	ret = arg_data
	temp_list = x.split("_")
	ret["poiid"]=temp_list[0]
	ret["lng"]=float(temp_list[1])
	ret["lat"]=float(temp_list[2])
	ret["address"]=temp_list[3]
	ret["description"]=temp_list[4]
	ret["place"]=temp_list[5]
	return ret




