import os
import sqlite3

root_path = '/Users/mac/Desktop/CityVision/'
city_name = 'Guangzhou'




#####read input_files
conn = sqlite3.connect('%sBaidu_Streetview_Database/%s_Baidu.db'%(root_path, city_name) )
cursor = conn.cursor()

database = cursor.execute("SELECT poiid,address from %s_Baidu"%city_name)
poi_set = []
for row in database:
	print("poiid:%s address:%s"%(row[0],row[1]) )
	poi_set.append(row[0])

print("Database len:",len(poi_set))

conn.close()
#read cache 
seg_log = []
seg_log_file = open("%sSemantic_Segmentation/Baidu_cache/%s_segmentation_log.txt"%(root_path, city_name),"r")
seg_log = seg_log_file.read().strip().split("\n")
for i in seg_log:
	if(seg_log.count(i)!=4):
		print(i)
		seg_log.remove(i)
seg_log = set(seg_log)
seg_log_file.close()



print("Seg log len:",len(list(seg_log)))

conn = sqlite3.connect('%sBaidu_Streetview_Database/%s_Baidu.db'%(root_path, city_name) )
cursor = conn.cursor()

cnt = 0

for i in poi_set:
	if(i not in seg_log):
		cursor.execute("DELETE from %s_Baidu where poiid=%s"%(city_name,str(i)))
		print("Delete:",i)
		cnt+=1
		conn.commit()
print("Total delete:",cnt)
conn.close()


conn = sqlite3.connect('%sBaidu_Streetview_Database/%s_Baidu.db'%(root_path, city_name) )
cursor = conn.cursor()
cursor.execute('DELETE from %s_Baidu where rowid not in(select max(rowid) from %s_Baidu group by poiid)'%(city_name,city_name) )
conn.commit()
conn.close()


#####read input_files
conn = sqlite3.connect('%sBaidu_Streetview_Database/%s_Baidu.db'%(root_path, city_name) )
cursor = conn.cursor()

database = cursor.execute("SELECT poiid,address from %s_Baidu"%city_name)
poi_set = []
for row in database:
	poi_set.append(row[0])

print("Database len:",len(poi_set))

conn.close()

print("Now database len:",len(poi_set))


