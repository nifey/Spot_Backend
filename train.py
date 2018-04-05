from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import Adam
from keras.models import load_model
from sklearn.model_selection import train_test_split
from keras.preprocessing.image import img_to_array
from keras.utils import to_categorical
from CNN import CNN
from imutils import paths
import numpy as np
import argparse
import random
import cv2
import os

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True,
        help="path to input dataset")
ap.add_argument("-m", "--model", required=True,
        help="path to output model folder")
args = vars(ap.parse_args())

EPOCHS = 25
INIT_LR = 1e-3
BS = 32

def train(dataset):
    print("[INFO] loading images in "+dataset+"...")
    data = []
    labels = []
    labellist=[]
    for item in os.scandir(dataset):
        if item.is_dir():
            labellist.append(item.name)
    labellist.sort()
    imagePaths=[]
    #imagePaths = sorted(list(paths.list_images(dataset)))
    for direc in os.listdir(dataset):
        i=0
        for item in os.scandir(dataset+os.path.sep+direc):
            if item.is_file():
                i=i+1
                imagePaths.append(item.path)
        print(direc)
        print(i)
    random.seed(42)
    random.shuffle(imagePaths)
    for imagePath in imagePaths:
        label = imagePath.split(dataset)[1].split(os.path.sep)
        if (len(label)>2):
            image = cv2.imread(imagePath)
            image = cv2.resize(image, (64, 64))
            image = img_to_array(image)
            data.append(image)
            #print(imagePath)
            #print(label)
            #print(labellist)
            for (i, labelname) in enumerate(labellist):
                    if label[1] == labelname:
                            labelnum = i
                            break
            labels.append(labelnum)
        
    data = np.array(data, dtype="float") / 255.0
    labels = np.array(labels)

    (trainX, testX, trainY, testY) = train_test_split(data,
        labels, test_size=0.25, random_state=42)

    trainY = to_categorical(trainY, num_classes=len(labellist))
    testY = to_categorical(testY, num_classes=len(labellist))

    aug = ImageDataGenerator(rotation_range=30, width_shift_range=0.1,
        height_shift_range=0.1, shear_range=0.2, zoom_range=0.2,
        horizontal_flip=True, fill_mode="nearest")

    print("[INFO] compiling model...")
    model = CNN.build(width=64, height=64, depth=3, classes=len(labellist))
    opt = Adam(lr=INIT_LR, decay=INIT_LR / EPOCHS)
    model.compile(loss="categorical_crossentropy", optimizer=opt,
        metrics=["accuracy"])

    print("[INFO] training network...")
    H = model.fit_generator(aug.flow(trainX, trainY, batch_size=BS),
        validation_data=(testX, testY), steps_per_epoch=len(trainX) // BS,
        epochs=EPOCHS, verbose=1)

    print("[INFO] serializing network...")
    if len(dataset.split(os.path.sep)) > 1 :
        filename = args["model"]+os.path.sep+dataset.split(os.path.sep)[-1]
    else:
        filename = args["model"]+os.path.sep+dataset
    model.save(filename)

    print("[INFO] saving network...")

train(args['dataset'])
for plant in os.listdir(args['dataset']):
    train(args['dataset']+os.path.sep+plant)
