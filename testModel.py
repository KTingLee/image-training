import os
import cv2
import joblib
from app import parseImg
from makeModel import standardData
import numpy as np
from PIL import Image

pridictionDir = './prediction'
def importModel():
  return joblib.load('./captchaModel.pkl')

def saveChars(chars):
  for i, char in enumerate(chars):
    cv2.imwrite(f'{pridictionDir}/{i}.jpg', char)

def showAndSaveImg(imgName):
  img = cv2.imread(f'./captcha_Images/{imgName}')
  cv2.imshow('img', img)
  cv2.waitKey(0)
  chars = parseImg(imgName)
  saveChars(chars)
  return chars

def testModel(model):
  imgs = os.listdir(pridictionDir)
  imgs = [img for img in imgs if '.jpg' in img]
  testData = []
  for img in imgs:
    pilImg = Image.open(f'{pridictionDir}/{img}')
    pixel = [pixel for pixel in iter(pilImg.getdata())]
    testData.append(pixel)
  testData = np.array(testData)
  xScaled = standardData(testData)
  print(model.predict(xScaled))

def main():
  model = importModel()
  imgs = os.listdir('./captcha_Images')
  imgs = [img for img in imgs if '.png' in img]
  for img in imgs:
    print(img)
    chars = showAndSaveImg(img)
    if len(chars) != 5:
      continue
    testModel(model)

if __name__ == '__main__':
  # main()
  model = importModel()
  testModel(model)
