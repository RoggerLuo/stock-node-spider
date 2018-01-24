#-*- coding: utf-8 -*-
import numpy as np
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution1D, MaxPooling1D
# convolutional.Conv1D
from keras.optimizers import SGD
from keras.models import load_model
from keras import backend as K
from make_dataset import Dataset
from import_data import load_json
from sklearn import preprocessing

#CNN网络模型类            
class Model:
    def __init__(self):
        self.model = None 
        
    #建立模型
    def build_model(self, dataset, nb_classes = 2):
        #构建一个空的网络模型，它是一个线性堆叠模型，各神经网络层会被顺序添加，专业名称为序贯模型或线性堆叠模型
        self.model = Sequential() 
        
        #以下代码将顺序添加CNN网络需要的各层，一个add就是一个网络层
        self.model.add(Convolution1D(4, 3, padding='same', 
                                     input_shape = dataset.input_shape))    #1 2维卷积层
        self.model.add(Activation('relu'))                                  #2 激活函数层
        
        self.model.add(Convolution1D(4, 3))                             #3 2维卷积层                             
        self.model.add(Activation('relu'))                                  #4 激活函数层
        
        self.model.add(MaxPooling1D(pool_size=(2)))                      #5 池化层
        self.model.add(Dropout(0.25))                                       #6 Dropout层

        # self.model.add(Convolution1D(8, 3,  padding='same'))         #7  2维卷积层
        # self.model.add(Activation('relu'))                                  #8  激活函数层
        
        # self.model.add(Convolution1D(8, 3))                             #9  2维卷积层
        # self.model.add(Activation('relu'))                                  #10 激活函数层
        
        # self.model.add(MaxPooling1D(pool_size=(2)))                      #11 池化层
        # self.model.add(Dropout(0.25))                                       #12 Dropout层

        self.model.add(Flatten())                                           #13 Flatten层
        self.model.add(Dense(100)) #512                                        #14 Dense层,又被称作全连接层
        self.model.add(Activation('relu'))                                  #15 激活函数层   
        self.model.add(Dropout(0.25))                                        #16 Dropout层
        self.model.add(Dense(nb_classes))                                   #17 Dense层
        self.model.add(Activation('softmax'))                               #18 分类层，输出最终结果
        
        #输出模型概况
        self.model.summary()
    #训练模型
    def train(self, dataset, batch_size = 20, nb_epoch = 3, data_augmentation = False):        
        sgd = SGD(lr = 0.01, decay = 1e-6, 
                  momentum = 0.9, nesterov = True) #采用SGD+momentum的优化器进行训练，首先生成一个优化器对象  
        
        self.model.compile(loss='categorical_crossentropy',
                           optimizer=sgd,
                           metrics=['accuracy'])   #完成实际的模型配置工作
        
        self.model.fit(dataset.train_images,
                       dataset.train_labels,
                       batch_size = batch_size,
                       nb_epoch = nb_epoch,
                       validation_data = (dataset.valid_images, dataset.valid_labels),
                       shuffle = True)

    MODEL_PATH = './me.stock.model.h5'
    def save_model(self, file_path = MODEL_PATH):
        self.model.save(file_path)
 
    def load_model(self, file_path = MODEL_PATH):
            self.model = load_model(file_path)

    def evaluate(self, dataset):
        score = self.model.evaluate(dataset.test_images, dataset.test_labels, verbose = 1)
        print("%s: %.2f%%" % (self.model.metrics_names[1], score[1] * 100))

    #识别人脸
    def stock_predict(self, full_path):    
        print('full_path:')
        print(full_path)
        jsonData = load_json('/Users/RogersMac/Sites/stock/predictData.json')
        jsonData = np.array(jsonData)
        jsonData = preprocessing.scale(jsonData)
        image = jsonData.reshape((1,150,1))
        
        #浮点并归一化
        image = image.astype('float32')
        
        #给出输入属于各个类别的概率，我们是二值类别，则该函数会给出输入图像属于0和1的概率各为多少
        result = self.model.predict_proba(image)
        print('result:', result)
        
        #给出类别预测：0或者1
        result = self.model.predict_classes(image)        

        #返回类别预测结果
        return result[0]

if __name__ == '__main__':
    dataset = Dataset('./dataset')
    dataset.load()
    model = Model()
    model.build_model(dataset)
    #测试训练函数的代码
    model.train(dataset)
    model.save_model(file_path = './me.stock.model.h5')
    model.evaluate(dataset)
    model.stock_predict('/Users/RogersMac/Sites/stock/predictData.json')
    