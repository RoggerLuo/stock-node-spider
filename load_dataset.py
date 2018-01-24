# -*- coding: utf-8 -*-
import os
import sys
import numpy as np
import json

def load_json(full_path):
    with open(full_path) as json_file:
        data = json.load(json_file)
        return data
#读取训练数据
images = []
labels = []
def read_path(path_name):    
    for dir_item in os.listdir(path_name):
        #从初始路径开始叠加，合并成可识别的操作路径
        full_path = os.path.abspath(os.path.join(path_name, dir_item))
        
        if os.path.isdir(full_path):    #如果是文件夹，继续递归调用
            read_path(full_path)
        else:   #文件
            if dir_item.endswith('.json'):
                image = load_json(full_path)
                image = np.array(image)
                image = image.reshape((150,1))
                # print(image.shape)                    
                images.append(image)                
                labels.append(path_name)                                
                    
    return images,labels
    

#从指定路径读取训练数据
def load_dataset(path_name):
    images,labels = read_path(path_name)    
    
    #将输入的所有图片转成四维数组，尺寸为(图片数量*IMAGE_SIZE*IMAGE_SIZE*3)
    #我和闺女两个人共1200张图片，IMAGE_SIZE为64，故对我来说尺寸为1200 * 64 * 64 * 3
    #图片为64 * 64像素,一个像素3个颜色值(RGB)
    images = np.array(images)
    print(images.shape)    
    #标注数据，'me'文件夹下都是我的脸部图像，全部指定为0，另外一个文件夹下是闺女的，全部指定为1
    labels = np.array([0 if label.endswith('fail') else 1 for label in labels])    
    print(labels)
    
    return images, labels

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage:%s path_name\r\n" % (sys.argv[0]))    
    else:
        images, labels = load_dataset(sys.argv[1])

