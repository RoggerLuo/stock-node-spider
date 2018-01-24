#-*- coding: utf-8 -*-

# from cv2 import cvLoadImage
# import cv2
import sys
from train import Model
import numpy as np
import json

def load(full_path):
    with open(full_path) as json_file:
        data = json.load(json_file)
        return data


if __name__ == '__main__':
    # if len(sys.argv) == 2:


        # frame = cv2.imread(sys.argv[1], cv2.IMREAD_COLOR) #cv2.IMREAD_GRAYSCALE
        # cv2.imshow('image',frame)
        # cv2.waitKey(0) 
        # cv2.destroyAllWindows()

    model = Model()
    model.load_model(file_path = './me.stock.model.h5')


    image = load('/Users/RogersMac/Sites/stock/predictData.json')
    # image = resize_image(image, IMAGE_SIZE, IMAGE_SIZE)
    image = np.array(image)
    image = image.reshape((1,150,1))
    image = image.astype('float32')            
    print(image)
    faceID = model.predict_stock(image)  
    print(faceID)

