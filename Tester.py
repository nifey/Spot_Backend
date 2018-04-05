from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import imutils
import os
import cv2
class Tester:
    @staticmethod
    def test(imagepath,modelname,dataset):
        image = cv2.imread(imagepath)
        image = cv2.resize(image, (64, 64))
        image = image.astype("float") / 255.0
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0)
    
        print("[INFO] loading network...")
        model = load_model("models"+os.path.sep+modelname)

        predictions = model.predict(image)[0]
        labellist=[]
        for item in os.scandir(dataset):
            if item.is_dir():
                labellist.append(item.name)
        labellist.sort()
        sortList = list(predictions)
        sortList.sort()
        resultlist=[]
        for i in range(len(labellist)):
            label={}
            label['class']=labellist[list(predictions).index(sortList[-(i+1)])]
            label['probability']=str(sortList[-(i+1)])
            resultlist.append(label)
        return resultlist

    #@staticmethod
    #def train(imagepath,plant,disease):
    #    data=[]
    #    labels=[]
    #    labellist=[]
    #    for item in os.scandir(
    #    image = cv2.imread(imagepath)
    #    image = cv2.resize(image, (64, 64))
    #    image = img_to_array(image)
    #    data.append(image)
    #    for (i,labelname in enumerate(labellist):
        


print(Tester.test('data'+os.path.sep+'tomato'+os.path.sep+'Leaf_Spot'+os.path.sep+'Leaf_Spot00000003.jpg','tomato','data/tomato'))
