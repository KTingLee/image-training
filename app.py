#!/usr/bin/python3
# coding: utf-8
import lib.tool_images as imgService
import numpy as np
import tkinter
import tkinter.messagebox
import cv2
import os

trainingDataDir = './MLdata'


def mkdir(dirName):
    try:
        os.makedirs(f'{trainingDataDir}/{dirName}')
    except FileExistsError:
        pass


def getImgNames(path):
    fileNames = os.listdir(path)
    fileNames = [file for file in files if '.png' in file]
    return fileNames


def getMaxNum(filesNameArr):
    filesNameArr = [int(num.split('.png')[0]) for num in filesNameArr]
    if len(filesNameArr) == 0:
        return 0
    return max(filesNameArr)


def parseImg(imgName):
    path = f'./captcha_Images/{imgName}.png'
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    threshold, img = cv2.threshold(
        img, 200, 255, cv2.THRESH_BINARY)  # 大於 200 的值都變 255(白色)

    # 去除噪訊
    img = imgService.eraseImage(img)
    # 膨脹圖片
    img = imgService.dilateImage(img)
    # 銳化
    edge = imgService.edgedImage(img)
    charBox = imgService.getCharBox(edge)
    chars = imgService.resizeImage(img, charBox)

    # 儲存 charBox 內容
    return chars


class SaveWindow ():
    def saveImg(self):
        answer = self.inputTextBox.get().upper()
        mkdir(answer)
        imgNames = getImgNames(f'{trainingDataDir}/{answer}')
        fileName = getMaxNum(imgNames) + 1
        cv2.imwrite(f'{trainingDataDir}/{answer}/{fileName}.png', self.char)

    def skip(self):
        pass

    def readImg(self, path):
        self.chars = parseImg(path)
        pass

    def __init__(self):
        count = 0
        self.captchaDir = './captcha_Images'
        imgs = getImgNames(self.captchaDir)

        self.init()
        self.readImg(f'{self.captchaDir}/{imgs[count]}')
        self._window.mainloop()

    def init(self):
        self._window = tkinter.Tk()

        self._window.geometry(newGeometry='400x400+3000+250')
        self._window.title('儲存標記圖片')

        self.canvas = tkinter.Canvas(
            self._window, height=50, width=50, bg='white')
        self.canvas.pack()

        self.inputTextBox = tkinter.Entry(self._window, show=None, width=10)
        self.inputTextBox.pack()

        self.saveBtn = tkinter.Button(
            self._window, text='儲存', command=self.saveImg)
        self.saveBtn.pack()

        self.skipBtn = tkinter.Button(
            self._window, text='跳過', command=self.skip)
        self.skipBtn.pack()


if __name__ == '__main__':
    window = SaveWindow()
