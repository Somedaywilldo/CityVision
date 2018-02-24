# Semantic_Segmentation 语义分割模块

### 模块功能列表

| 模块                      | 功能                                 |
| ----------------------- | ---------------------------------- |
| test_segmentation.py    | 分割模块，保存label图片，具有cache，可以中断后继续分割   |
| perform_segmentation.py | 多线程调用test_segmentation.py，一个城市一个线程 |
### 初始化

以下是test_segmentation.py的初始化步骤。

```python
caffe_root = '/home/yyh/ENet/caffe-enet/'  # ENet-Caffe根目录
ENet_dir='/home/yyh/ENet/' #ENet根目录
city_wander_dir='/data/yyh/CityWander/' 
catched_data_dir=city_wander_dir+'Streetview_Spider/Catched_data/'
```


### 分割流程

直接运行perform_segmentation.py即可，分割文件将存储于CityWander/Label_Pictures目录下。

### 注意

分割带有cache，位置位于Semantic_Segmentation/segmentation_cache中，删除cache文件即可重新开始分割。




