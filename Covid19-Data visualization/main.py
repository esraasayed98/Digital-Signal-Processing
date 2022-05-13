from PyQt5 import QtWidgets 
from ui import Ui_MainWindow
import sys
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer 
import os
import cv2


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        #Tab1
        pixmap=QPixmap('images/A/11.png')
        self.ui.view_1.setPixmap(pixmap)
        
        #connect buttons
        self.ui.startButton_1.clicked.connect(self.start1)
        self.ui.stopButton_1.clicked.connect(self.stop1)
        self.ui.ExportButton_1.clicked.connect(self.export1)
        self.files_it = iter([os.path.join('images/A', file) for file in os.listdir('images/A')])
       
        #Tab2
        pixmap2=QPixmap('images/C/confirmed_images/11.png')
        self.ui.view_2.setPixmap(pixmap2)
        
        #connect buttons
        self.ui.startButton_2.clicked.connect(self.start2)
        self.ui.stopButton_2.clicked.connect(self.stop2)
        self.ui.ExportButton_2.clicked.connect(self.export2)
        
        self.ui.sort_combo.activated.connect(self.sort)
        self.files_it1 = iter([os.path.join('images/C/confirmed_images', file) for file in os.listdir('images/C/confirmed_images')])

        #Tap3
        pixmap3=QPixmap('images/D/11.png')
        self.ui.view_4.setPixmap(pixmap3)
        
        #connect buttons
        self.ui.startButton_4.clicked.connect(self.start3)
        self.ui.stopButton_4.clicked.connect(self.stop3)
        
        self.ui.ExportButton_4.clicked.connect(self.export3)
        self.files_it2 = iter([os.path.join('images/D', file) for file in os.listdir('images/D')])
       
   
   
    
    def on_time1(self):
       
        try:
            file = next(self.files_it)
            pixmap = QPixmap(file)
            self.add_pixmap1(pixmap)
        except StopIteration:
            self.timer.stop()
            self.files_it = iter([os.path.join('images/A', file) for file in os.listdir('images/A')])
               

    def add_pixmap1(self, pixmap):
        if not pixmap.isNull():          
            self.ui.view_1.setPixmap(pixmap)
        
    def start1(self):
        self.timer = QTimer(self, interval=300)
        self.timer.timeout.connect(self.on_time1)
        self.timer.start()
        
    def stop1(self):
        self.timer.stop()
        
        
    def export1(self):
        image_folder = 'images/A'
        video_name = 'exported videos/covid-19 visualization_A.mp4'
        
        self.video(image_folder , video_name)
    
    def sort(self):
        index=self.ui.sort_combo.currentIndex()
        if index==2:
            self.files_it1 = iter([os.path.join('images/C/Death_images', file) for file in os.listdir('images/C/Death_images')])
        else:
            self.files_it1 = iter([os.path.join('images/C/confirmed_images', file) for file in os.listdir('images/C/confirmed_images')])

        
    def video(self,image_folder , video_name ):
        images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
        frame = cv2.imread(os.path.join(image_folder, images[0]))
        height, width, layers = frame.shape
        
        video = cv2.VideoWriter(video_name, 0, 5, (width,height))
        
        for image in images:
            video.write(cv2.imread(os.path.join(image_folder, image)))
        
        cv2.destroyAllWindows()
        video.release()
        
    
    def on_time2(self):
       
        try:
            file = next(self.files_it1)
            pixmap = QPixmap(file)
            self.add_pixmap2(pixmap)
        except StopIteration:
            self.timer.stop()
            self.sort()
           
    def add_pixmap2(self, pixmap):
        if not pixmap.isNull():
            
            self.ui.view_2.setPixmap(pixmap)
    
        
    def start2(self):
        self.timer = QTimer(self, interval=400)
        self.timer.timeout.connect(self.on_time2)
        self.timer.start()  
        
    def stop2(self):
        self.timer.stop()
            
    def export2(self):
        index=self.ui.sort_combo.currentIndex()
        if index==2:
            image_folder = 'images/C/Death_images'
            video_name = 'exported videos/Death Cases video_C.mp4'
            
        else:
            image_folder = 'images/C/confirmed_images'
            video_name = 'exported videos/Confirmed Cases video_C.mp4'      
        self.video(image_folder , video_name)
               
    def on_time3(self):
       
        try:
            file = next(self.files_it2 )
          
            pixmap = QPixmap(file)
            self.add_pixmap3(pixmap)
        except StopIteration:
            self.timer.stop()
            self.files_it2 = iter([os.path.join('images/D', file) for file in os.listdir('images/D')])
            
    def add_pixmap3(self, pixmap):
        if not pixmap.isNull():
            
            self.ui.view_4.setPixmap(pixmap) 
            
    def start3(self):
        self.timer = QTimer(self, interval=400)
        self.timer.timeout.connect(self.on_time3)
        self.timer.start()
        
    def stop3(self):
        self.timer.stop()
        
    def export3(self):
        image_folder = 'images/D'
        video_name = 'exported videos/covid-19 visualization_D.mp4'
        self.video(image_folder , video_name)






def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    application = ApplicationWindow()
    application.show()
    app.exec_()


if __name__ == "__main__":
    main()
