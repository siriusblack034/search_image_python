from cProfile import label
import sys
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from matplotlib import ticker
from search import Search
import cv2
import numpy as np
import tkinter


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "Tìm kiểm áo sơ mi theo hình ảnh"
        self.top = 100
        self.left = 800
        self.width = 500
        self.height = 500
        self.imageQuery = ""
        self.imagesSearch = []
        self.InitWindow()

    def InitWindow(self):
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        vbox = QGridLayout()
        self.btn1 = QPushButton("Open Image to Search")
        self.btn1.clicked.connect(self.getImage)
        # self.btn1.setFixedWidth(400)
        self.btn1.setFixedHeight(50)
        # self.btn1.setStyleSheet("margin-left:100px")
        vbox.addWidget(self.btn1)
        self.label = QLabel("Ảnh tìm kiếm:")
        self.label = QLabel()
        vbox.addWidget(self.label)
        self.vbox = vbox
        # self.label1 = QLabel("Kết quả: ")
        self.label1 = QLabel()
        vbox.addWidget(self.label1, 2, 0)
        self.setLayout(vbox)
        self.show()

    def getImage(self):
        fname = QFileDialog.getOpenFileName(
            self, 'Open file', 'd:\'', "Image filesz (*.jpg *.gif *.png)")
        imagePathSearch = fname[0]
        print(imagePathSearch)
        if(imagePathSearch):
            pixmap = QPixmap(imagePathSearch)
            search = Search(imagePathSearch)
            results = search.searching()
            self.label.setPixmap(
                QPixmap(pixmap.scaledToWidth(200).scaledToHeight(200))
            )

            # self.label.setAlignment(Qt.AlignCenter)
            self.label1.setText("Kết quả: ")
            self.label1.setFont(QFont('Times', 20))
            color_effect = QGraphicsColorizeEffect()
            color_effect.setColor(Qt.darkGreen)
            self.label1.setGraphicsEffect(color_effect)
            self.label1.setAlignment(Qt.AlignCenter)
            i = 5
            j = 0
            for result in results:
                pathResult = "D:/PTIT/BTL/dataset/" + result[1]
                pixmapResult = QPixmap(pathResult)
                if not pixmapResult.isNull():
                    label = QLabel("Hello")
                    label.setPixmap(
                        QPixmap(pixmapResult.scaledToWidth(
                            200).scaledToHeight(200))
                    )
                    self.vbox.addWidget(label, i, j, 1, 1)
                    j = j+1
                    if j == 5:
                        i = i+1
                        j = 0
            self.vbox.columnStretch(200)


App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
