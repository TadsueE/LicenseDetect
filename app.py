import sys
# sys.stdout = open(os.devnull, "w")
# sys.stderr = open(os.path.join(os.getenv("TEMP"), "stderr-"+os.path.basename(sys.argv[0])), "w")

from ultralytics import YOLO
import easyocr
import cv2
import os
from os import listdir
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QWidget, QSpacerItem, QTextEdit
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QEvent
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import multiprocessing
import time

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
                              QPushButton:hover {background-color: rgba(255, 255, 255, 0.5)}""")
        proceed.clicked.connect(self.on_proceed_button_clicked)

        exit = QtWidgets.QPushButton(self)
        exit.setEnabled(True)
        exit.setGeometry(QtCore.QRect(450, 530, 250, 90))
        exit.setFont(buttonfont)
        exit.setText("Exit")
        exit.setStyleSheet("""QPushButton {background-color: rgba(255, 255, 255, 0.2);  color: #000000; border-radius: 5px;} 
                              QPushButton:hover {background-color: rgba(255, 255, 255, 0.5)}""")
        exit.clicked.connect(self.on_close_click)

    def on_proceed_button_clicked(self):
        self.hide()
        self.second_wind = secondwind()
        self.second_wind.show()
    def on_close_click(self):
        self.close()

class secondwind(QMainWindow):
    def __init__(self):
        super(secondwind, self).__init__()
        self.setGeometry(300, 200, 790, 630)
        self.setFixedSize(790, 630)
        self.setStyleSheet("QMainWindow {background-color: #131e57}")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        initfont = QtGui.QFont()
        initfont.setPointSize(30)
        initfont.setFamilies(["Arial"])

        self.VBL = QVBoxLayout()
        self.HBL = QHBoxLayout()
        self.FeedHbl = QHBoxLayout()
        spacer = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Maximum)

        ## Camera Label
        self.FeedLabel = QLabel()
        self.FeedLabel.setStyleSheet("color: #FFFFFF")
        self.FeedLabel.setText("Initializing Camera Here")
        self.FeedLabel.setMinimumSize(640,480)
        self.FeedLabel.setFont(initfont)
        self.FeedLabel.setAlignment(Qt.AlignCenter)
        self.FeedHbl.addWidget(self.FeedLabel, alignment=Qt.AlignLeft)
        self.FeedHbl.addItem(spacer)
        self.VBL.addLayout(self.FeedHbl)

        ## Text Label
        self.TextList = QVBoxLayout()
        self.TextList.setSpacing(0)
        self.HeaderText = QLabel()
        self.HeaderText.setMinimumSize(120,50)
        self.HeaderText.setMaximumSize(120,50)
        self.HeaderText.setStyleSheet("color: #FFFFFF; font-size: 25px; font-family: Helvetica; ")
        self.HeaderText.setWordWrap(True)
        self.HeaderText.setText("Plate Numbers :")
        self.TextList.addWidget(self.HeaderText, alignment=Qt.AlignCenter)

        self.TextPlace = QLabel()
        self.TextPlace.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.TextPlace.setMinimumSize(120,400)
        self.TextPlace.setMaximumSize(120,400)
        self.TextPlace.setStyleSheet("color: #FFFFFF; font-size: 20px; font-family: Helvetica") 
        self.TextList.addWidget(self.TextPlace, alignment=Qt.AlignCenter)
        self.counter = 1

        self.FeedHbl.addLayout(self.TextList)

        ## Buttons 
        self.Vbuttons = QVBoxLayout()
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

        ## Image Lables
        self.recordlab = QLabel()
        self.recordlab.setMinimumSize(190,95)
        self.recordlab.setMaximumSize(190,95)
        self.recordlab.setStyleSheet("background-color: rgba(255, 255, 255, 0.1); border-radius: 5px")

        self.recordlab1 = QLabel()
        self.recordlab1.setMinimumSize(190,95)
        self.recordlab1.setMaximumSize(190,95)
        self.recordlab1.setStyleSheet("background-color: rgba(255, 255, 255, 0.1); border-radius: 5px")

        self.recordlab2 = QLabel()
        self.recordlab2.setMinimumSize(190,95)
        self.recordlab2.setMaximumSize(190,95)
        self.recordlab2.setStyleSheet("background-color: rgba(255, 255, 255, 0.1); border-radius: 5px")

        ## Layouting
        self.HBL.addItem(spacer)
        self.HBL.addWidget(self.recordlab)
        self.HBL.addItem(spacer)
        self.HBL.addWidget(self.recordlab1)
        self.HBL.addItem(spacer)
        self.HBL.addWidget(self.recordlab2)
        self.HBL.addLayout(self.Vbuttons)
        self.VBL.addLayout(self.HBL)
        central_widget.setLayout(self.VBL)
    
        ##Functionallity of Thread
       
        self.camera = camera()
        self.camera.start()
        self.camera.ImageUpdate.connect(self.ImageUpdateSlot)

        self.record = record()
        QTimer.singleShot(2000, self.record.start)
        self.record.processingFinished.connect(self.imagerecord)
        self.record.processtext.connect(self.TextSlot)

        self.current_lab_index = 0

    ## Qthread Signals
    def ImageUpdateSlot(self, Image):
        self.FeedLabel.setPixmap(QPixmap.fromImage(Image))

    def imagerecord(self,qImg):
        if self.current_lab_index == 0:
            self.recordlab.setPixmap(QPixmap.fromImage(qImg))
            self.current_lab_index += 1
        elif self.recordlab.pixmap() is None or self.recordlab.pixmap().isNull():
            self.recordlab.setPixmap(QPixmap.fromImage(qImg))
        elif self.current_lab_index == 1:
            self.recordlab1.setPixmap(self.recordlab.pixmap())
            self.recordlab.setPixmap(QPixmap.fromImage(qImg))
            self.current_lab_index += 1
        elif self.current_lab_index == 2:
            self.recordlab2.setPixmap(self.recordlab1.pixmap())
            self.recordlab1.setPixmap(self.recordlab.pixmap())
            self.recordlab.setPixmap(QPixmap.fromImage(qImg))
            self.current_lab_index = 2

    def TextSlot(self, Text):
        current_text = self.TextPlace.text()
        new_text = current_text + "\n" + str(self.counter) + ". " + Text
        self.TextPlace.setText(new_text)
        self.counter += 1

    ## Button Functions
    def CancelFeed(self):
        self.camera.stop()
        QTimer.singleShot(2000, self.record.stop2)
        self.counter = 1
        self.Main = MainWindow()
        self.Main.show()
        self.close()
    def restart(self):
        self.current_lab_index = 0
        if self.recordlab.pixmap() is not None:
            self.recordlab.clear()
        if self.recordlab1.pixmap() is not None:
            self.recordlab1.clear()
        if self.recordlab2.pixmap() is not None:
            self.recordlab2.clear()
        if self.TextPlace.text() != "":
            self.TextPlace.clear()
            self.counter = 1
        self.record.stop2()
        QTimer.singleShot(2000, self.record.start)

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
    processtext = pyqtSignal(str)
    def run(self):
        self.text = []
        base_folder = "runs/detect"
        self.ThreadActive = True
        while self.ThreadActive:
            newest_folder_path = self.find_newest_folder(base_folder)
            if newest_folder_path:
              self.process_images(newest_folder_path)

    def perform_ocr_on_image(self, img):
        reader = easyocr.Reader(['en'], gpu=True)
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
            cv2.putText(img, text, (1, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1)
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
                        time.sleep(3)
                        process, newtext = self.perform_ocr_on_image(img)
                        if newtext not in self.text:
                            ConvertQtFormat = QImage(process.data, process.shape[1], process.shape[0], QImage.Format_RGB888)
                            scaled = ConvertQtFormat.scaled(190, 95, Qt.KeepAspectRatio)
                            self.processingFinished.emit(scaled)
                            self.processtext.emit(newtext)
                            self.text.append(newtext)   
                    except Exception as e:
                        print(f"Error processing image: {image_path}\n{e}")
    def stop2(self):
        self.ThreadActive = False
        self.terminate()


def main():
    multiprocessing.freeze_support()
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

