from ultralytics import YOLO
import easyocr
import cv2
import os
from os import listdir
from pathlib import Path
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QWidget
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys

model = YOLO('LicensePlateDetector.pt')

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 200, 1150, 800)
        self.setFixedSize(1150, 800)
        self.setStyleSheet("QMainWindow {background-color: #639163; border-radius: 5000px;}")
        #CSS
        logofont = QtGui.QFont()
        logofont.setPointSize(25)
        logofont.setFamilies(["Arial"])

        titlefont = QtGui.QFont()
        titlefont.setPointSize(40)
        titlefont.setFamilies(["Arial"])

        trafficbg = "traffic background.jpg"
        pixmap = QPixmap(trafficbg)
        scaled_pixmap = pixmap.scaledToWidth(790, Qt.SmoothTransformation)

        ## Main Code

        trafficset= QLabel(self)
        trafficset.setPixmap(scaled_pixmap)
        trafficset.setGeometry(QtCore.QRect(0, 0, 900, 900))

        logo = QtWidgets.QLabel(self)
        logo.setText("S&V")
        logo.move(800, 20)
        logo.setFont(logofont)
        logo.setStyleSheet("QLabel {color: #FFFFFF}")

        title = QtWidgets.QLabel(self)
        title.setText("License Plate Detector")
        title.setGeometry(QtCore.QRect(800, 110, 341, 201))
        title.setWordWrap(True)
        title.setFont(titlefont)
        title.setStyleSheet("QLabel {color: #FFFFFF}")

        proceed = QtWidgets.QPushButton(self)
        proceed.setEnabled(True)
        proceed.setGeometry(QtCore.QRect(860, 410, 211, 31))
        proceed.setText("Proceed")
        proceed.setStyleSheet("""QPushButton {background-color: #FFFFFF; border: 2px solid rgba(0, 0, 0, 0.3);  color: #030101; border-radius: 5px;} 
                              QPushButton:hover {background-color: #E0E0E0; border: 1px solid rgba(0, 0, 0, 0.5)}""")
        proceed.clicked.connect(self.on_proceed_button_clicked)

        exit = QtWidgets.QPushButton(self)
        exit.setEnabled(True)
        exit.setGeometry(QtCore.QRect(860, 450, 211, 31))
        exit.setText("Exit")
        exit.setStyleSheet("""QPushButton {background-color: #FFFFFF; border: 2px solid rgba(0, 0, 0, 0.3);  color: #030101; border-radius: 5px;} 
                              QPushButton:hover {background-color: #E0E0E0; border: 1px solid rgba(0, 0, 0, 0.5)}""")
        exit.clicked.connect(self.on_close_click)

    def on_proceed_button_clicked(self):
        self.close()
        self.second_wind = secondwind()
        self.second_wind.show()
    def on_close_click(self):
        self.close()

class secondwind(QWidget):
    def __init__(self):
        super(secondwind, self).__init__()
        self.setGeometry(300, 200, 780, 600)
        self.setFixedSize(780, 600)
        self.setStyleSheet("QWidget {background-color: #639163}")

        self.VBL = QVBoxLayout()
        self.VBL.setContentsMargins(10, 1, 20, 30)
        self.FeedLabel = QLabel()
        self.VBL.addWidget(self.FeedLabel)

        self.CancelBTN = QPushButton("Return")
        self.CancelBTN.setMinimumSize(100, 31)
        self.CancelBTN.clicked.connect(self.CancelFeed)
        self.CancelBTN.setStyleSheet("""QPushButton {background-color: #FFFFFF; border: 2px solid rgba(0, 0, 0, 0.3);  color: #030101; border-radius: 5px;} 
                              QPushButton:hover {background-color: #E0E0E0; border: 1px solid rgba(0, 0, 0, 0.5)}""")
        self.VBL.addWidget(self.CancelBTN, alignment=Qt.AlignRight)

        self.exitBTN = QPushButton("Exit")
        self.exitBTN.setMinimumSize(100, 31)
        self.exitBTN.clicked.connect(self.ExitFeed)
        self.exitBTN.setStyleSheet("""QPushButton {background-color: #FFFFFF; border: 2px solid rgba(0, 0, 0, 0.3);  color: #030101; border-radius: 5px;} 
                              QPushButton:hover {background-color: #E0E0E0; border: 1px solid rgba(0, 0, 0, 0.5)}""")
        self.VBL.addWidget(self.exitBTN, alignment=Qt.AlignRight)

        self.camera = camera()

        self.camera.start()
        self.camera.ImageUpdate.connect(self.ImageUpdateSlot)
        self.setLayout(self.VBL)

    def ImageUpdateSlot(self, Image):
        self.FeedLabel.setPixmap(QPixmap.fromImage(Image))

    def CancelFeed(self):
        self.camera.stop()
        self.Main = MainWindow()
        self.Main.show()
        self.close()

    def ExitFeed(self):
        self.camera.stop()
        self.close()

class camera(QThread):
    ImageUpdate = pyqtSignal(QImage)
    def run(self):
        self.model = YOLO('LicensePlateDetector.pt')
        self.ThreadActive = True
        Capture = cv2.VideoCapture(0)
        while self.ThreadActive:
            ret, frame = Capture.read()
            if ret:
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.model(image)
                boxresults = results[0].plot()
                ConvertToQtFormat = QImage(boxresults.data, boxresults.shape[1], boxresults.shape[0], QImage.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)
    def stop(self):
        self.ThreadActive = False
        self.quit()  
        self.wait()   
        del self.model  

def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()















