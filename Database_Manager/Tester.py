from GeoInfoManager import GeoInfoManager
from cv2 import cv2
import numpy as np
import pickle
NewDB = GeoInfoManager(add=None, dbname="Beijing")
args=[["pano"         ,"ntext"        ],
      ["heading"      ,"int"          ],
      ["lat"          ,"decimal(13,9)"],
      ["lng"          ,"decimal(13,9)"],
      ["address"      ,"ntext"        ],
      ["description"  ,"ntext"        ],
      ["null"         ,"int"          ],
      ["road"         ,"int"          ],
      ["sidewalk"     ,"int"          ],
      ["building"     ,"int"          ],
      ["wall"         ,"int"          ],
      ["fence"        ,"int"          ],
      ["pole"         ,"int"          ],
      ["traffic_light","int"          ],
      ["traffic_sign" ,"int"          ],
      ["vegetation"   ,"int"          ],
      ["terrain"      ,"int"          ],
      ["sky"          ,"int"          ],
      ["person"       ,"int"          ],
      ["car"          ,"int"          ],
      ["truck"        ,"int"          ],
      ["bus"          ,"int"          ],
      ["train"        ,"int"          ],
      ["motorcycle"   ,"int"          ],
      ["bicycle"      ,"int"          ]
      ]

TableList = NewDB.aTableList
TableList.addTable(tablename="beijing",args=args,key="pano")
beijing = TableList.getTable("beijing")
print(beijing.orderby("car"))

#beijing.get_density(class_id=,point1=.point2=)
#aList = NewDB.infofromfile(filepath="/media/neolin/488959EB10ECB6FC/CityHorizon/Streetview_Spider/Catched_data/Beijing/Beijing_img_info_file_filtered.txt")
'''GroupLenth = 10
aListLenth = len(aList)
keyfile = open('keyfile.pkl', 'wb')
passlistfile = open('passlistfile.pkl', 'wb')
#key = pickle.load(keyfile)
#passlist = pickle.load(passlistfile)
key = 0
passlist = []

while(key<aListLenth):
    tail = min(key+GroupLenth, aListLenth)
    print(tail)
    alist=aList[key:tail]
    purelist = []
    #for i in alist:
    #    if(i[0] not in passlist):
    #        passlist.append(i[0])
    #        purelist.append(i)
    #alist = purelist
    NewPicInfo = NewDB.infofrompic(alist=alist,picadd="/media/neolin/488959EB10ECB6FC/CityHorizon/Label_Pictures/Beijing")
    beijing.savelist(NewPicInfo)
    key+=GroupLenth
    pickle.dump(key, keyfile, True)
    pickle.dump(passlist, passlistfile, True)

#print(TableList.__TableList__["Test"])
#picpath = "/media/neolin/488959EB10ECB6FC/CityHorizon/Label_Pictures/Beijing/10011001140611130704600_180_label.png"'''
