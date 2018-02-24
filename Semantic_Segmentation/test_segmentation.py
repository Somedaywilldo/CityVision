#/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This script visualize the semantic segmentation of ENet.
"""
import os
import numpy as np
from argparse import ArgumentParser
from os.path import join
import argparse
import sys

#设置目录

caffe_root = '/home/yyh/ENet/caffe-enet/'  # Change this to the absolute directory to ENet Caffe
ENet_dir='/home/yyh/ENet/' #ENet根目录
city_wander_dir='/data/yyh/CityWander/' 
catched_data_dir=city_wander_dir+'Streetview_Spider/Catched_data/'

sys.path.insert(0, caffe_root + 'python')
import caffe
sys.path.append('/usr/local/lib/python2.7/site-packages')
import cv2


__author__ = 'Timo Sämann'
__university__ = 'Aschaffenburg University of Applied Sciences'
__email__ = 'Timo.Saemann@gmx.de'
__data__ = '24th May, 2017'

def fil(x): #过滤空字符串
    return list(filter(lambda x:x!="",x))

#真正需要传递的参数是Cityname，没有默认Beijing

def make_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('--model', type=str, default=ENet_dir+'prototxts/enet_deploy_final.prototxt', help='.prototxt file for inference')
    parser.add_argument('--weights', type=str, default=ENet_dir+'enet_weights_zoo/cityscapes_weights.caffemodel', help='.caffemodel file')
    parser.add_argument('--colours', type=str, default=ENet_dir+'scripts/cityscapes19.png', help='label colours')
    parser.add_argument('--out_dir', type=str, default=None, help='output directory in which the segmented images '                                                             'should be stored')
    parser.add_argument('--gpu', type=str, default='0', help='0: gpu mode active, else gpu mode inactive')
    parser.add_argument('--city_name', type=str, required=Ture , help='argument city_name is necessary')

    #parser.add_argument('--model', type=str, required=True, help='.prototxt file for inference')
    #parser.add_argument('--weights', type=str, required=True, help='.caffemodel file')
    #parser.add_argument('--colours', type=str, required=True, help='label colours')
    #parser.add_argument('--input_image', type=str, required=True, help='input image path')
    #parser.add_argument('--out_dir', type=str, default=None, help='output directory in which the segmented images '                                                             'should be stored')
    

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

    input_files=open(catched_data_dir+args.city_name+"/"+args.city_name+"_img_name_file_filtered.txt","r")
    input_files=input_files.read().split("\n")
    input_files=fil(input_files)

    log_set_dir = city_wander_dir+"Semantic_Segmentation/segmentation_cache/"+args.city_name+"_segmentation_log.txt"
    log_set_file = open(log_set_dir,"a+") #读取log文件
    log_set = log_set_file.read()
    log_set = fil(log_set.split("\n"))
    log_set = set(log_set) #生成log set
    log_set_file.close() 

    for i in input_files:

        if(i in log_set):
            continue

        args.input_image=city_wander_dir+"Streetview_Pictures/"+args.city_name+"/"+i

        input_image = cv2.imread(args.input_image, 1).astype(np.float32)
        input_image = input_image[0:600, 0:960] #去掉水印保留从左上角开始600*960的图片，去除水印

        input_image = cv2.resize(input_image, (input_shape[3], input_shape[2]))
        input_image = input_image.transpose((2, 0, 1))
        input_image = np.asarray([input_image])

        out = net.forward_all(**{net.inputs[0]: input_image})

        prediction = net.blobs['deconv6_0_0'].data[0].argmax(axis=0)

        prediction = np.squeeze(prediction) #分割
        prediction = np.resize(prediction, (3, input_shape[2], input_shape[3]))
        prediction = prediction.transpose(1, 2, 0).astype(np.uint8)

       # prediction_rgb = np.zeros(prediction.shape, dtype=np.uint8)
       # label_colours_bgr = label_colours[..., ::-1]
       # cv2.LUT(prediction, label_colours_bgr, prediction_rgb)

        #cv2.imshow("ENet", prediction_rgb)
        key = cv2.waitKey(0)

        args.out_dir = city_wander_dir+"Label_Pictures/"+args.city_name+"/"

        input_path_ext = args.input_image.split(".")[-1]
        input_image_name = args.input_image.split("/")[-1:][0].replace('.' + input_path_ext, '')

       # args.out_dir = city_wander_dir + args.city_name
        out_path_label = args.out_dir + input_image_name + '_label' + '.png'
        
        cv2.imwrite(out_path_label, prediction)  #只保留label图片，为单通道灰度图

        log_change_dir = city_wander_dir+"Semantic_Segmentation/segmentation_cache/"+args.city_name+"_segmentation_log.txt"
        log_change_file = open(log_set_dir,"a+")
        log_set.add(i)
        log_change_file.write(i+"\n")
        log_change_file.close()
        #  label images, where each pixel has an ID that represents the class
	#print "City:",args.city_name,"|| Total:",len(input_files),"|| Now:",len(log_set),"|| Now_pic:",i
	print "City: %10s || Total: %5d || Now: %5d || Percent: %.3f || Now_pic: %35s"%(args.city_name,len(input_files),len(log_set),1.0*len(log_set)/len(input_files),i)
        





