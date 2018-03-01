#/usr/bin/env python
#-*- coding: utf-8 -*-
"""
This script visualize the semantic segmentation of ENet.
"""
import os
import numpy as np
from argparse import ArgumentParser
from os.path import join
import argparse
import sys
import sqlite3

#设置目录
#

ENet_path = '/home/yyh/ENet/' #ENet根目录
caffe_root = '%scaffe-enet/'%ENet_path  # Change this to the absolute directory to ENet Caffe
root_path = '/data/yyh/CityVision/' 
#data_path = city_wander_dir+'Streetview_Spider/Catched_data/'

sys.path.insert(0, caffe_root + 'python')
import caffe
sys.path.append('/usr/local/lib/python2.7/site-packages')
import cv2

def fil(x): #过滤空字符串
    return list(filter(lambda x:x!="",x))

#真正需要传递的参数是Cityname，没有默认Beijing
def make_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str, default=ENet_path+'prototxts/enet_deploy_final.prototxt', help='.prototxt file for inference')
    parser.add_argument('--weights', type=str, default=ENet_path+'enet_weights_zoo/cityscapes_weights.caffemodel', help='.caffemodel file')
    parser.add_argument('--colours', type=str, default=ENet_path+'scripts/cityscapes19.png', help='label colours')
    parser.add_argument('--out_dir', type=str, default=None, help='output directory in which the segmented images '                                                             'should be stored')
    parser.add_argument('--gpu', type=str, default='0', help='0: gpu mode active, else gpu mode inactive')
    parser.add_argument('--city_name', type=str, required=True , help='argument city_name is necessary')
    return parser

if __name__ == '__main__':
    parser1 = make_parser()
    args = parser1.parse_args()
    if args.gpu == '0': #GPU模式默认开启
        caffe.set_mode_gpu()
    else:
        caffe.set_mode_cpu()

    net = caffe.Net(args.model, args.weights, caffe.TEST)

    input_shape = net.blobs['data'].data.shape
    output_shape = net.blobs['deconv6_0_0'].data.shape

    label_colours = cv2.imread(args.colours, 1).astype(np.uint8)

    #####read input_files
    conn = sqlite3.connect('%sBaidu_Streetview_Database/%s_Baidu.db'%(root_path, args.city_name) )
    cursor = conn.cursor()

    database = cursor.execute("SELECT poiid,address from %s_Baidu"%args.city_name)
    poi_set = []
    for row in database:
        print "poiid:%s address:%s"%(row[0],row[1])
        poi_set.append(row[0])

    conn.close()


    #read cache 
    seg_log = []
    seg_log_file = open("%sSemantic_Segmentation/Baidu_cache/%s_segmentation_log.txt"%(root_path,args.city_name),"a+")
    seg_log = seg_log_file.read().strip().split("\n")
    seg_log = set(seg_log)
    seg_log_file.close()

    for i in poi_set:
        if(i in seg_log):
            continue
        for j in range(4):
            args.input_image="%sBaidu_Streetview_Pictures/%s/%s_%d.jpg"%(root_path,args.city_name,i,j*90)

            input_image = cv2.imread(args.input_image, 1).astype(np.float32)
            input_image = input_image[0:450, 0:1024] #去掉水印保留从左上角开始600*960的图片，去除水印

            input_image = cv2.resize(input_image, (input_shape[3], input_shape[2]))
            input_image = input_image.transpose((2, 0, 1))
            input_image = np.asarray([input_image])

            out = net.forward_all(**{net.inputs[0]: input_image})

            prediction = net.blobs['deconv6_0_0'].data[0].argmax(axis=0)

            prediction = np.squeeze(prediction) #分割
            prediction = np.resize(prediction, (3, input_shape[2], input_shape[3]))
            prediction = prediction.transpose(1, 2, 0).astype(np.uint8)
            
            prediction_rgb = np.zeros(prediction.shape, dtype=np.uint8)
            label_colours_bgr = label_colours[..., ::-1]
            cv2.LUT(prediction, label_colours_bgr, prediction_rgb)
            #cv2.imshow("ENet", prediction_rgb)

            key = cv2.waitKey(0)

            #save Label picture
            args.out_dir = '%sBaidu_Label_Pictures/'%root_path
            input_path_ext = args.input_image.split(".")[-1]
            input_image_name = args.input_image.split("/")[-1:][0].replace('.' + input_path_ext, '')
            output_label = args.out_dir + input_image_name + '_label' + '.png'
            
            cv2.imwrite(output_label, prediction)  #只保留label图片，为单通道灰度图

            #save RGB picture
            args.out_dir = '%sBaidu_RGB_Pictures/'%root_path
            input_path_ext = args.input_image.split(".")[-1]
            input_image_name = args.input_image.split("/")[-1:][0].replace('.' + input_path_ext, '')
            output_label = args.out_dir + input_image_name + '_rgb' + '.png'
            
            cv2.imwrite(output_label, prediction_rgb)  #只保留label图片，为单通道灰度图

            #change segmentation log
            log_change_file = open("%sSemantic_Segmentation/Baidu_cache/%s_segmentation_log.txt"%(root_path,args.city_name),"a+")
            log_change_file.write(i+"\n")
            log_change_file.close()
            seg_log.add(i)
            #  label images, where each pixel has an ID that represents the class
            print("City: %10s || Total: %5d || Now: %5d || Percent: %.3f || Now_Pic: %s_%d.jpg"%(args.city_name,len(poi_set),len(seg_log),1.0*len(seg_log)/len(poi_set),i,j) )
            



