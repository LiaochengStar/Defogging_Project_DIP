#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QSlider, QPushButton, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
import PyQt5.QtGui as QtGui

import cv2


class MainWin(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()  # 界面绘制交给InitUi方法
        # self.timer_camera = QtCore.QTimer()
        # self.timer_camera.timeout.connect(self.TimerOutFun)
        # self.timer_camera.start()
        # self.timer_camera.setInterval(1)
        # self.camera = cv2.VideoCapture(0)

    def ShowImage(self):
        img = cv2.imread("img.png")
        if self.image.ndim == 3:
            gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        else:
            gray = self.image  # if语句：如果img维度为3，说明不是灰度图，先转化为灰度图gray，如果不为3，也就是2，原图就是灰度图

        qimg = QtGui.QImage(img.data, img.shape[1], img.shape[0], QtGui.QImage.Format_RGB888)
        dynamicImg = QtGui.QImage(img.data, img.shape[1], img.shape[0], QtGui.QImage.Format_RGB888)
        self.DispLb.setPixmap(QtGui.QPixmap.fromImage(qimg).scaled(self.DispLb.width(), self.DispLb.height()))
        self.DispLb1.setPixmap(QtGui.QPixmap.fromImage(dynamicImg).scaled(self.DispLb1.width(), self.DispLb1.height()))
        self.DispLb.show()
        self.DispLb1.show()

    def ChangeMinArgValue(self, value):
        print(value)
    def openimage(self):
        imgName, imgType = QFileDialog.getOpenFileName(self, "打开图片", "", "*.jpg;;*.png;;All Files(*)")
        jpg = QtGui.QPixmap(imgName).scaled(self.DispLb.width(), self.DispLb.height())
        self.DispLb.setPixmap(jpg)
    def ChangeMaxArgValue(self, value):
        print(value)
    def printf(self):
        print("on click")
    def initUI(self):
        # 设置窗口的位置和大小
        self.setGeometry(300, 300, 900, 600)
        # 设置窗口的标题
        self.setWindowTitle('Dehaze software')
        # 设置窗口的图标，引用当前目录下的web.png图片
        # self.setWindowIcon(QIcon('web.png'))
        # 摄像头窗口
        self.DispLb = QLabel('Zetcode', self)
        self.DispLb1 = QLabel('Zetcode1', self)
        self.DispLb.move(0, 0)
        self.DispLb1.move(500, 0)
        self.DispLb1.setFixedSize(400, 350)
        self.DispLb.setFixedSize(500, 350)

        # button
        self.btnSave = QPushButton('Upload File', self)
        self.btnSave.clicked.connect(self.openimage)
        self.btnSave.setCheckable(True)
        self.btnSave.move(100, 480)

        self.btnSave2 = QPushButton('Dd DeHaze', self)
        self.btnSave2.setCheckable(True)
        self.btnSave2.move(300, 480)

        # 显示窗口
        self.show()


if __name__ == '__main__':
    # 创建应用程序和对象
    app = QApplication(sys.argv)
    ex = MainWin()
    sys.exit(app.exec_())
