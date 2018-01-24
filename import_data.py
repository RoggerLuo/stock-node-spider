# -*- coding: utf-8 -*-
import os
import sys
import numpy as np
import json
from sklearn import preprocessing

def load_json(full_path):
    with open(full_path) as json_file:
        data = json.load(json_file)
        return data

#读取训练数据
jsons = []
labels = []

def read_path(path_name):    

    for dir_item in os.listdir(path_name):
        #从初始路径开始叠加，合并成可识别的操作路径
        full_path = os.path.abspath(os.path.join(path_name, dir_item))
        
        if os.path.isdir(full_path):    #如果是文件夹，继续递归调用
            read_path(full_path)
        else:   #文件
            if dir_item.endswith('.json'):
                jsonData = load_json(full_path)
                jsonData = np.array(jsonData)
                jsonData = jsonData.reshape((150,1))
                # jsonData = preprocessing.scale(jsonData)
                jsons.append(jsonData)        
                labels.append(path_name)                                
    # jsons = np.array(jsons)
    # labels = np.array([0 if label.endswith('fail') else 1 for label in labels])    
    return jsons,labels
    
if __name__ == '__main__':
    jsons, labels = read_path('./dataset')
    print(jsons[2])
    print(len(jsons))
    print(labels)

    # if len(sys.argv) != 2:
    #     print("Usage:%s path_name\r\n" % (sys.argv[0]))    
    # else:
    #     jsons, labels = read_path(sys.argv[1])

