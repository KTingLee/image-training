import os
import cv2
import numpy as np
from PIL import Image

from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
import joblib

imgExt = '.jpg'
sourceDir = './MLdata'
def listImgs(path):
  files = os.listdir(path)
  files = [file for file in files if imgExt in file]
  return files

def listDir(path):
  dirs = os.listdir(path)
  dirs = [dir for dir in dirs if len(dir) == 1]
  return dirs

def getTrainingData():
  digits = []
  labels = []

  dirs = listDir(sourceDir)
  for dir in dirs:
    imgDir = f'{sourceDir}/{dir}'
    imgs = listImgs(imgDir)
    for img in imgs:
      pilImg = Image.open(f'{imgDir}/{img}').convert('1')
      pixel = [pixel for pixel in iter(pilImg.getdata())]
      digits.append(pixel)
      labels.append(dir)
  digits = np.array(digits)
  return digits, labels

def standardData(trainingData):
  scaler = StandardScaler()
  scaler.fit(trainingData)
  xScaled = scaler.transform(trainingData)
  return xScaled

def saveModel(model):
  joblib.dump(model, './captchaModel.pkl')

def importModel():
  return joblib.load('./captchaModel.pkl')

def testModel(model):
  pridictionDir = './prediction'
  imgs = os.listdir(pridictionDir)
  imgs = [img for img in imgs if '.jpg' in img]
  testData = []
  for img in imgs:
    pilImg = Image.open(f'{pridictionDir}/{img}').convert('1')
    pilImg.show()
    pixel = [pixel for pixel in iter(pilImg.getdata())]
    testData.append(pixel)
  testData = np.array(testData)
  xScaled = standardData(testData)
  predicted = model.predict(xScaled)
  print(predicted)


if __name__ == '__main__':
  digits, labels = getTrainingData()
  xScaled = standardData(digits)

  mlp = MLPClassifier(hidden_layer_sizes=(30, 30, 30), activation='logistic', max_iter=2000)
  mlp.fit(xScaled, labels)

  predicted = mlp.predict(xScaled)
  target = np.array(labels)
  print(predicted == target)

  # saveModel(mlp)

  # model = importModel()
  testModel(mlp)

