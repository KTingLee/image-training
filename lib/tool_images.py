import matplotlib.pyplot as plt
import numpy as np
import math
import cv2

kernel = np.ones((3, 3), np.int8)

# 去除雜訊
def eraseImage (image):
  return cv2.erode(image, kernel, iterations = 1)

# 模糊圖片
def blurImage (image):
  return cv2.GaussianBlur(image, (5, 5), 0)

# 銳利化圖片
# threshold1,2，較小的值為作為偵測邊界的最小值
def edgedImage (image, threshold1 = 30, threshold2 = 150):
  return cv2.Canny(image, threshold1, threshold2)

# 圖片膨脹
def dilateImage (image, level = (3, 3)):
  level = np.ones(level, np.int8)
  return cv2.dilate(image, level, iterations = 1)

# 獲得字元外盒
def getCharBox (image, minW = 15, minH = 15):

  def setBoundingBox (contours):
    box = []
    for cnt in contours:
      (x, y, w, h) = cv2.boundingRect(cnt)
      # NOTE: 字元有一定大小，所以其盒子寬高也有基本門檻值
      if w > minW and h > minH:
        box.append((x, y, w, h))
    #     cv2.rectangle(image, (x, y), (x + w, y + h), (127, 255, 0), 2)  # 依照contour畫邊界
    # cv2.imshow('test', image)
    return box

  def removeInnerBox (boxes):
    # 對各個字元的外盒，依照 x 大小排列
    boxes.sort(key = lambda e: e[0])
    results = [boxes[0]]
    for i in range(len(boxes) - 1):
      x1, y1, w1, h1 = boxes[i]
      x2, y2, w2, h2 = boxes[i+1]
      if (x2 > x1 and x2 + w2 > x1 + w1):
        results.append(boxes[i+1])
    return results

  contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  boundingBox = setBoundingBox(contours)
  boundingBox = removeInnerBox(boundingBox)
  return boundingBox

def showCharBox (image, boxes):
  for x, y, w, h in boxes:
    cv2.rectangle(image, (x, y), (x + w, y + h), (127, 255, 0), 2)  # 依照contour畫邊界
    cv2.imshow('charBox', image)
    cv2.waitKey(0)

def showCountour (contours):
  row = 2
  col = math.ceil(len(contours)/row)
  for i, cnt in enumerate(contours, start = 1):
    x = []
    y = []
    # plt.subplot(row, col, i)
    for point in cnt:
      x.append(point[0][0])
      y.append(point[0][1])
    plt.plot(x, y)
  plt.show()

def resizeImage (image, charBox, size = (50, 50)):
  results = []
  for (x, y, w, h) in charBox:
    char = image[y:y+h, x:x+w]
    char = cv2.resize(char, size)
    results.append(char)
  return results

def diffPictures (picA, picB):
  err = np.sum( (picA.astype('float') - picB.astype('float')) ** 2 )
  err /= float(picA.shape[0] * picA.shape[1])
  return err

if __name__ == '__main__':
  pic = cv2.imread('../captcha_Images/0.png')
  print(pic)
  cv2.imshow('pic', pic)
  cv2.waitKey(0)

  erosion = eraseImage(pic)
  blured = blurImage(erosion)
  edged = edgedImage(blured)
  dilated = dilateImage(edged)
  charBox = getCharBox(dilated)
  showCharBox(dilated, charBox)
  dilated = dilateImage(edged, (4, 4))
  chars = resizeImage(dilated, charBox)
  # input("Press Enter to continue.")
  # c = result[0][0][0][0]
  # print(c)
  # plt.plot(c)
  cv2.waitKey(0)
  cv2.destroyAllWindows()


  
  