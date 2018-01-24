# -*- coding: utf-8 -*-
import numpy as np
from import_data import read_path
from keras.utils import np_utils
from sklearn.cross_validation import train_test_split
class Dataset:
    def __init__(self, path_name):
        #训练集
        self.train_images = None
        self.train_labels = None
        
        #验证集
        self.valid_images = None
        self.valid_labels = None
        
        #测试集
        self.test_images  = None            
        self.test_labels  = None
        
        #数据集加载路径
        self.path_name = path_name
        
        #当前库采用的维度顺序
        self.input_shape = None
        
    #加载数据集并按照交叉验证的原则划分数据集并进行相关预处理工作
    def load(self, nb_classes = 2):
        #加载数据集到内存
        images, labels = read_path(self.path_name)        
        images = np.array(images)
        labels = np.array([0 if label.endswith('fail') else 100 for label in labels])    


        train_images, valid_images, train_labels, valid_labels = train_test_split(images, labels, test_size = 0.3, random_state = np.random.randint(0, 100))        
        _, test_images, _, test_labels = train_test_split(images, labels, test_size = 0.5, random_state = np.random.randint(0, 100))                
        
        self.input_shape = (150,1)            
            
        #输出训练集、验证集、测试集的数量
        print(train_images.shape, 'train samples') #[0]
        print(valid_images.shape, 'valid samples') #[0]
        print(test_images.shape, 'test samples') #[0]

    
        #我们的模型使用categorical_crossentropy作为损失函数，因此需要根据类别数量nb_classes将
        #类别标签进行one-hot编码使其向量化，在这里我们的类别只有两种，经过转化后标签数据变为二维
        # train_labels = np_utils.to_categorical(train_labels, nb_classes)                        
        # valid_labels = np_utils.to_categorical(valid_labels, nb_classes)            
        # test_labels = np_utils.to_categorical(test_labels, nb_classes)                        
    
        #像素数据浮点化以便归一化
        train_images = train_images.astype('float32')            
        valid_images = valid_images.astype('float32')
        test_images = test_images.astype('float32')
            
        self.train_images = train_images
        self.valid_images = valid_images
        self.test_images  = test_images
        self.train_labels = train_labels
        self.valid_labels = valid_labels
        self.test_labels  = test_labels
        print(test_labels)
        print(len(test_labels))
        print(test_labels.shape)

            
if __name__ == '__main__':
    dataset = Dataset('./dataset')    
    dataset.load()

