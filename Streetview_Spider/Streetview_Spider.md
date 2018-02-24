# Streetview_Spider 街景爬虫模块

### 模块功能列表

| 模块                  | 功能                         |
| ------------------- | -------------------------- |
| GPSTrans.py         | 定义point对象，解析地理信息           |
| KeyModule.py        | 操作使用key，包含所有key的腾讯API      |
| keys.txt            | 可用key列表                    |
| main.py             | 爬虫主文件，爬取数据位于Catched_data目录 |
| NetWork.py          | 封装、解析url                   |
| shapefile_reader.py | 读取城市shp文件                  |
| shapefile_writer.py | 将爬取的点写入shp文件               |

街景爬虫模块使用腾讯地图开放平台的API，配合规划院提供的中国城市shapefile文件，使用QGIS生成的随机点阵确定街景点，进而爬取街景数据，包含每个点四面街景图、经纬度信息、地址信息、地址描述信息。街景爬虫模块中带有cache，具有中断后继续爬取的功能。

### Streetview_Spider用法：

####一、打开shapefile_reader.py

1、“#基本路径设置”中修改city_name、city_wander_dir，完成初始化。

2、可以先运行shapefile_reader.py，设置stop_cnt变量为Total Points数量，北京应为60000。

3、修改后再运行一次shapefile_reader.py

#### 二、打开key.txt

1、每天开始爬取时，需要重新设置该文件。将所有key的time设为10000。

2、当time值小于key_module.py中的alert值时，爬虫将停止。

#### 三、打开main.py

1、“#基本路径设置”中修改city_name

2、直接运行main.py即可。



### 意外情况：

1、main.py执行过程中出现中断，此时请正常结束main.py的运行，如在shell中使用“ctrl+C”，此时main.py会更改key.txt。之后可以重新运行main.py，数据不会丢失，会接着上一次的进度爬取。

2、若想完全重新爬取，需要删除目录“Streetview_Spider/Cache/”下的所有文件，同时删除目录“Streetview_Spider/Catched_data/”中对应城市文件夹中的所有文件。

3、连续出现大量“No pano！”，很可能是因为当天腾讯街景key的额度已经达到上限，此时应该停止爬取，并在第二天进行下一次爬取。下一次爬取前，将key.txt中值设为10000。此时，应查看Cache文件中的Cityname_catchlog_file.txt，并找到最后一条有街景点的记录，将其后的记录内容删除，即可继续上一次的爬取。

