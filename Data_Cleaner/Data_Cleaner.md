# Data_Cleaner 数据清洗模块

### 模块功能列表

| 模块                    | 功能               |
| --------------------- | ---------------- |
| DataCleaner.py        | 数据清洗类            |
| perform_data_clean.py | 按流程、利用数据清洗类进行清洗  |
| data_trans.py         | 数据格式转换，用于统一信息格式  |
| filename_changer.py   | 批量修改文件名，用于统一文件格式 |

数据清洗模块负责整理街景爬虫模块所保存的数据。整个清洗流程是一个用文件和信息双向匹配和筛选的过程，清洗之后保证每个街景点有4张街景、四面之间转角为90度，且与信息完全匹配。

### 初始化

```python
self.city_name=city_name_in #设置城市名
self.city_wander_dir=city_wander_dir_in #CityWander目录
self.data_clean_cache_dir=self.city_wander_dir+"Data_Cleaner/data_clean_cache/" #清洗缓存目录
```

###DataCleaner类的方法

| 方法                     | 功能                             |
| ---------------------- | ------------------------------ |
| get_file_name()        | 获取街景文件目录下的所有文件名                |
| error_point_name()     | 使用文件名筛选出来的错误街景点                |
| deleter_name()         | 删除error_point_name筛选出的文件       |
| get_info()             | 筛选现在剩余街景文件的信息                  |
| error_point_info()     | 根据get_info方法筛选出的信息，找出信息有错误的街景点 |
| deleter_info()         | 删除error_point_info方法找出的错误街景点   |
| error_info_to_name()   | 找出文件名和信息不匹配的点                  |
| deleter_info_to_name() | 删除文件名和信息不匹配的点                  |

###清洗流程

整个清洗流程是一个用文件和信息双向匹配和筛选的过程，清洗之后保证每个街景点有4张街景、四面之间转角为90度，且与信息完全匹配。

perform_data_clean.py中的操作即为完整的清洗流程。

具体代码及功能：

```python
from DataCleaner import *
#dir format:/Users/mac/Desktop/CityWander/
cleaner=DataCleaner("Shanghai","/Users/mac/Desktop/CityWander/")

cleaner.get_file_name()			#获取街景文件目录下的所有文件名
cleaner.error_point_name()		#使用文件名筛选出来的错误街景点
cleaner.deleter_name()			#删除error_point_name筛选出的文件
cleaner.get_info()				#筛选现在剩余街景文件的信息
cleaner.error_point_info()		#根据get_info方法筛选出的信息，找出信息有错误的街景点
cleaner.deleter_info()			#删除error_point_info方法找出的错误街景点
cleaner.error_info_to_name()	#找出文件名和信息不匹配的点
cleaner.deleter_info_to_name() 	#删除文件名和信息不匹配的点

```





