from ultralytics import YOLO
import easyocr
import cv2
import os
from os import listdir
from pathlib import Path
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QWidget, QSpacerItem
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import numpy as np
import time

model = YOLO('LicensePlateDetector.pt')
reader = easyocr.Reader(['en'], gpu=True)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 200, 1150, 800)
        self.setFixedSize(1150, 800)
        self.setStyleSheet("QMainWindow {background-color: #0b061b; border-radius: 5000px;}")
        #CSS
        logofont = QtGui.QFont()
        logofont.setPointSize(30)
        logofont.setFamilies(["Arial"])

        buttonfont = QtGui.QFont()
        buttonfont.setPointSize(20)
        buttonfont.setFamilies(["Arial"])

        titlefont = QtGui.QFont()
        titlefont.setPointSize(50)
        titlefont.setFamilies(["Arial"])

        trafficbg = "traffic background (1).jpg"
        pixmap = QPixmap(trafficbg)
        scaled_pixmap = pixmap.scaledToWidth(1150, Qt.SmoothTransformation)

        ## Main Code

        trafficset= QLabel(self)
        trafficset.setPixmap(scaled_pixmap)
        trafficset.setGeometry(QtCore.QRect(0, 0, 1150, 800))

        logo = QtWidgets.QLabel(self)
        logo.setText("S&V")
        logo.move(525, 80)
        logo.setFont(logofont)
        logo.setStyleSheet("QLabel {color: #FFFFFF}")

        title = QtWidgets.QLabel(self)
        title.setText("License Plate Detector")
        title.setGeometry(QtCore.QRect(230, 80, 700, 201))
        title.setWordWrap(False)
        title.setFont(titlefont)
        title.setStyleSheet("QLabel {color: #FFFFFF}")

        proceed = QtWidgets.QPushButton(self)
        proceed.setEnabled(True)
        proceed.setGeometry(QtCore.QRect(450, 410, 250, 90))
        proceed.setFont(buttonfont)
        proceed.setText("Proceed")
        proceed.setStyleSheet("""QPushButton {background-color: rgba(255, 255, 255, 0.2);  color: #000000; border-radius: 5px;} 
                              QPushButton:hover {background-color: rgba(255, 255, 255, 0.5); box-shadow: 0 0 5px rgba(0, 0, 0, 0.2)}""")
        proceed.clicked.connect(self.on_proceed_button_clicked)

        exit = QtWidgets.QPushButton(self)
        exit.setEnabled(True)
        exit.setGeometry(QtCore.QRect(450, 530, 250, 90))
        exit.setFont(buttonfont)
        exit.setText("Exit")
        exit.setStyleSheet("""QPushButton {background-color: rgba(255, 255, 255, 0.2);  color: #000000; border-radius: 5px;} 
                              QPushButton:hover {background-color: rgba(255, 255, 255, 0.5); box-shadow: 0 0 5px rgba(0, 0, 0, 0.2)}""")
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
        self.setGeometry(300, 200, 780, 630)
        self.setFixedSize(780, 630)
        self.setStyleSheet("QWidget {background-color: #010b3d}")

        buttonfont = QtGui.QFont()
        buttonfont.setPointSize(30)
        buttonfont.setFamilies(["Arial"])

        self.VBL = QVBoxLayout()
        self.HBL = QHBoxLayout()

        self.FeedLabel = QLabel()
        self.FeedLabel.setStyleSheet("border: 2px solid rgba(0, 0, 0, 1); color: #FFFFFF")
        self.FeedLabel.setText("Initializing Camera Here")
        self.FeedLabel.setMinimumSize(640,480)
        self.FeedLabel.setFont(buttonfont)
        self.FeedLabel.setAlignment(Qt.AlignCenter)
        self.VBL.addWidget(self.FeedLabel, alignment=Qt.AlignCenter)
        
        self.Vbuttons = QVBoxLayout()
        spacer = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Maximum)

        ## Buttons 
        self.CancelBTN = QPushButton("Return")
        self.CancelBTN.setMinimumSize(100, 31)
        self.CancelBTN.clicked.connect(self.CancelFeed)
        self.CancelBTN.setStyleSheet("""QPushButton {background-color: #FFFFFF; border: 2px solid rgba(0, 0, 0, 0.3);  color: #030101; border-radius: 5px;} 
                              QPushButton:hover {background-color: #E0E0E0; border: 1px solid rgba(0, 0, 0, 0.5)}""")
        self.Vbuttons.addWidget(self.CancelBTN, alignment=Qt.AlignRight)

        self.exitBTN = QPushButton("Exit")
        self.exitBTN.setMinimumSize(100, 31)
        self.exitBTN.clicked.connect(self.ExitFeed)
        self.exitBTN.setStyleSheet("""QPushButton {background-color: #FFFFFF; border: 2px solid rgba(0, 0, 0, 0.3);  color: #030101; border-radius: 5px;} 
                              QPushButton:hover {background-color: #E0E0E0; border: 1px solid rgba(0, 0, 0, 0.5)}""")
        self.Vbuttons.addWidget(self.exitBTN, alignment=Qt.AlignRight)

        self.RestartBTN = QPushButton("Record Restart")
        self.RestartBTN.setMinimumSize(100, 31)
        self.RestartBTN.clicked.connect(self.restart)
        self.RestartBTN.setStyleSheet("""QPushButton {background-color: #FFFFFF; border: 2px solid rgba(0, 0, 0, 0.3);  color: #030101; border-radius: 5px;} 
                              QPushButton:hover {background-color: #E0E0E0; border: 1px solid rgba(0, 0, 0, 0.5)}""")
        self.Vbuttons.addWidget(self.RestartBTN, alignment=Qt.AlignRight)

        ## Lables
        self.recordlab = QLabel()
        self.recordlab.setMinimumSize(190,95)
        self.recordlab.setMaximumSize(190,95)
        self.recordlab.setStyleSheet("background-color: rgba(255, 255, 255, 0.1)")

        self.recordlab1 = QLabel()
        self.recordlab1.setMinimumSize(190,95)
        self.recordlab1.setMaximumSize(190,95)
        self.recordlab1.setStyleSheet("background-color: rgba(255, 255, 255, 0.1)")

        self.recordlab2 = QLabel()
        self.recordlab2.setMinimumSize(190,95)
        self.recordlab2.setMaximumSize(190,95)
        self.recordlab2.setStyleSheet("background-color: rgba(255, 255, 255, 0.1)")

        ## Layouting
        self.HBL.addItem(spacer)
        self.HBL.addWidget(self.recordlab)
        self.HBL.addItem(spacer)
        self.HBL.addWidget(self.recordlab1)
        self.HBL.addItem(spacer)
        self.HBL.addWidget(self.recordlab2)
        self.HBL.addLayout(self.Vbuttons)
        self.VBL.addLayout(self.HBL)
    
        ##Functionallity of Threads
        self.camera = camera()
        self.camera.start()
        self.camera.ImageUpdate.connect(self.ImageUpdateSlot)
        self.setLayout(self.VBL)

        self.record = record()
        QTimer.singleShot(5000, self.record.start)
        self.record.processingFinished.connect(self.imagerecord)

        self.current_lab_index = 0

    ## Functions 
    def ImageUpdateSlot(self, Image):
        self.FeedLabel.setPixmap(QPixmap.fromImage(Image))
    def imagerecord(self,qImg):
        if self.current_lab_index == 0:
            self.recordlab.setPixmap(QPixmap.fromImage(qImg))
            self.current_lab_index += 1
        elif self.current_lab_index == 1:
            self.recordlab1.setPixmap(self.recordlab.pixmap())
            self.recordlab.setPixmap(QPixmap.fromImage(qImg))
            self.current_lab_index += 1
        elif self.current_lab_index == 2:
            self.recordlab2.setPixmap(self.recordlab1.pixmap())
            self.recordlab1.setPixmap(self.recordlab.pixmap())
            self.recordlab.setPixmap(QPixmap.fromImage(qImg))
            self.current_lab_index = 2
        
    def CancelFeed(self):
        self.camera.stop()
        QTimer.singleShot(2000, self.record.stop2)
        self.Main = MainWindow()
        self.Main.show()
        self.close()
    def restart(self):
        self.current_lab_index = 0
        self.record.stop2
        QTimer.singleShot(8000, self.record.start)

        if self.recordlab.pixmap() is not None:
            self.recordlab.clear()
        if self.recordlab1.pixmap() is not None:
            self.recordlab1.clear()
        if self.recordlab2.pixmap() is not None:
            self.recordlab2.clear()

    def ExitFeed(self):
        QTimer.singleShot(2000, self.record.stop2)
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
                results = self.model(image, save_crop=True, conf= 0.7)
                boxresults = results[0].plot()
                ConvertToQtFormat = QImage(boxresults.data, boxresults.shape[1], boxresults.shape[0], QImage.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)
    def stop(self):
        self.ThreadActive = False
        self.quit()  
        self.wait()   
        del self.model 

class record(QThread):
    processingFinished = pyqtSignal(QImage)
    def run(self):
        base_folder = "runs/detect"
        reader = easyocr.Reader(['en'], gpu=True)
        self.ThreadActive = True
        while self.ThreadActive:
            newest_folder_path = self.find_newest_folder(base_folder)
            if newest_folder_path:
              self.process_images(newest_folder_path)

    def perform_ocr_on_image(self, img):
        try:
            gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            results = reader.readtext(gray_img)
            text = ""
            if len(results) == 1:
                text = results[0][1]
            elif results:
                for res in results:
                    if res[2] > 0.2:
                        text = res[1]
                        break
            cv2.putText(img, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            return img, text
        except Exception as e:
            print(f"Error performing OCR: {e}")
            return ""
    def find_newest_folder(self, base_folder):
        folders = [f for f in os.listdir(base_folder) if os.path.isdir(os.path.join(base_folder, f))]
        folders.sort(key=lambda f: os.path.getmtime(os.path.join(base_folder, f)), reverse=True)
        if folders:
            return os.path.join(base_folder, folders[0])
        else:
            return None
        
    def process_images(self, folder_path):
        for subfolder in os.listdir(folder_path):
            subfolder_path = os.path.join(folder_path, subfolder)
            if os.path.isdir(subfolder_path):
                self.process_images(subfolder_path)
            else:
                if subfolder.lower().endswith((".jpg", ".jpeg", ".png")):
                    image_path = os.path.join(folder_path, subfolder)
                    img = cv2.imread(image_path)
                    if img is None:
                        print(f"Error reading image: {image_path}")
                        continue
                    try:
                        text = ""
                        process, newtext = self.perform_ocr_on_image(img)
                        if newtext != text:
                            ConvertQtFormat = QImage(process.data, process.shape[1], process.shape[0], QImage.Format_RGB888)
                            Pic = ConvertQtFormat.scaled(190, 95, Qt.KeepAspectRatio)
                            self.processingFinished.emit(Pic)  
                            text = newtext      
                    except Exception as e:
                        print(f"Error processing image: {image_path}\n{e}")
                    time.sleep(3)
    def stop2(self):
        self.threadActive = False
        self.quit()  
        self.wait()   


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()















