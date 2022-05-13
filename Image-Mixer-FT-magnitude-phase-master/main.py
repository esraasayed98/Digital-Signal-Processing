from PyQt5 import QtWidgets 
from GUI import Ui_MainWindow
import sys
import cv2
from image import ImageModel
import logging

#Create logger
logging.basicConfig(filename="LoggingFile.log", 
                    format='%(asctime)s %(message)s', 
                    filemode='w')
logger=logging.getLogger() 
logger.setLevel(logging.DEBUG) 


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.Box=[self.ui.fourier1_combo , self.ui.fourier2_combo,self.ui.select_modes1 ,self.ui.select_modes2 ,self.ui.componentBox_1 , self.ui.componentBox_2  ,self.ui.outputBox ]
         
        #connect Buttons
        self.Buttons=[self.ui.Add_image1,self.ui.Add_image2 ]
        self.fun=[self.Add_image ,self.Add_image ]
        for i in range(0, len(self.Buttons)):
            
            self.Buttons[i].setCheckable(True)
            self.Buttons[i].clicked.connect(self.fun[i])
          
        #disable some ui 
        self.disable_Uis()
        
        self.image_labels=[self.ui.image1 ,self.ui.image2]
        self.sliders=[self.ui.slider1 ,self.ui.slider2]
        self.sliders_label=[self.ui.slider1_label ,self.ui.slider2_label]
        self.modes_combo=[self.ui.select_modes1 ,self.ui.select_modes2] 
       
        #connect sliders
        self.slider_style()
        
        
        
        #to clear widgets
        self.views=[self.ui.view_image1 ,self.ui.view_image2 ,self.ui.view_fourier1,self.ui.view_fourier2 ,self.ui.view_output1,self.ui.view_output2]
        for item in self. views:
            item.ui.histogram.hide()
            item.ui.roiBtn.hide()
            item.ui.menuBtn.hide()
            item.ui.roiPlot.hide()
     
        #initialize variables
        self.size=[0,0]  
        self.images=[0,0]
        self.components=[0 ,0]
        self.show_in=self.views[4]
        self.weights=[0,0]
        self.mode=["magnitudeAndPhase" , "realAndImaginary" ]
        self.indecies=[0,0]
        
        #connect to image class 
        self.model=ImageModel(self.images , self.views , self.Box ,  self.components ,self.show_in  )
        
        #connect functions
        self.functions=[self.model.Combo_index,self.model.Combo_index,self.Modes ,self.Modes,self.select_component,self.select_component ,self.Show_Output  ]
        for i in range(0,len(self.Box)):
            self.Box[i].activated.connect(self.functions[i])
            #logger.debug("The user added image"  + str(i+1)  )
            
        
        
       
    def Add_image(self):
        #load image
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file','c:\\', "Image files (*.jpg *.png)" )
        imagePath = fname[0]
        if imagePath :            
            for i in range(0,2):                
                if self.Buttons[i].isChecked()==True: 
                    logger.debug("User added image"  + str(i+1)  )
                    self.image_labels[i].setStyleSheet('color: black')
                    self.image_labels[i].setText("Image"+str(i+1)  )                    
                    self.img = cv2.imread(imagePath,cv2.IMREAD_GRAYSCALE)                    
                    self.size[i]=self.img.shape

                    if i==0:                        
                        self.images[0]=self.img 
                        self.components=[self.images[0] , self.images[0] ]
                    else:                        
                        self.images[i]=self.img
                        self.components=[self.images[1] , self.images[1] ]
                        
                    logger.debug("The path of image" +str(i+1)+"   " + str(  imagePath)  )
                  
                    #check size
                    if self.size[0]==0 or self.size[1]==0  :                        
                        self.model.view(self.views[i] ,self.img)
                        self.Buttons[i].setChecked(False)                       
                        self.Box[i].setEnabled(True)
                        self.model.fourier(self.images[i])
                        self.model.view(self.views[i+2] ,self.model.fft[0])
                         
                    elif  self.size[0] == self.size[1] :                       
                        self.model.view(self.views[i] ,self.img)
                        self.Buttons[i].setChecked(False)                       
                        
                        self.Box[i].setEnabled(True)
                        self.model.fourier(self.images[i])
                        self.model.view(self.views[i+2] ,self.model.fft[0])
                        self.components=[self.images[0] , self.images[0] ]
                        
                        
                    else:
                        self.views[i].clear()
                        self.views[i+2].clear()
                        self.image_labels[i].setStyleSheet('color: red')
                        self.image_labels[i].setText("You must \nchoose image \nof size " + str(self.size[i-1]))
                        self.images[i]=0
                        self.size[i]=0
                        self.Buttons[i].setChecked(False)
                        self.Box[i].setEnabled(False)
                        logger.debug(" User tried to add image"  + str(i+1)+" " + "with different size." )
                   
            self.ui.outputBox.setEnabled(True)
           
        else: 
            self.Buttons[0].setChecked(False)
            self.Buttons[1].setChecked(False)
  
    
    def select_component(self ):
        for i in range(0,2):
            self.indecies[i]=self.Box[i+4].currentIndex()
            self.components[i]=self.images[self.indecies[i]]
            logger.debug("Component" +str(i+1)+ "  selected by the user is image"  + str(self.indecies[i] +1  )  )
        self.Box[2].setEnabled(True)
        self.Box[3].setEnabled(True)
    
    
    def slider_style(self):
        for i in range(0,2):
            self.sliders[i].setTickPosition(QtWidgets.QSlider.TicksBelow)
            self.sliders[i].setTickInterval(1)
            self.sliders[i].setMinimum(0)
            self.sliders[i].setMaximum(100)
            self.sliders[i].valueChanged.connect(self.get_slider_value)
            
    
    def get_slider_value(self):
        for i in range (0,2):
            
            self.weights[i] = self.sliders[i].value()/100
            
            self.sliders_label[i].setText(str( int(100 * self.weights[i])) + "%")
            logger.debug("slider"+str(i+1)+"  has been set to   "+str( int(100 * self.weights[i])) + "%"   )
        
                  
            
        self.Modes()
   
    def enabel_items(self):
        for i in range(0,6):
             self.Box[3].view().setRowHidden(i,False)
    
    def disable_items(self): 
        for i in range(0,6):         
            self.Box[3].view().setRowHidden(i,True)
        
    def items(self , item1 ,item2):
        self.enabel_items()
        self.disable_items()
        self.Box[3].view().setRowHidden( item1,False)
        self.Box[3].view().setRowHidden(item2,False)
        
    def Modes(self):
        self.Box[3].setEnabled(True)
        self.item1=self.Box[2].currentText()
        self.item2=self.Box[3].currentText()
             
        if self.item1=="Magnitude" or self.item1=="Uniform Magnitude" :
            
            self.items(2,3)
            
            if self.item1=="Magnitude" and self.item2=="Phase":
                 self.model.Mix(self.mode[0],self.weights[0] , self.weights[1])
            
            elif self.item1=="Magnitude"  and self.item2=="Uniform Phase" :
            
                self.model.Mix(self.mode[0],self.weights[0] ,self.weights[1])
                
            elif  self.item1=="Uniform Magnitude" and self.item2=="Phase"  :
              
                self.model.Mix(self.mode[0],self.weights[0] ,self.weights[1])
            
            elif self.item1 =="Uniform Magnitude" and self.item2=="Uniform Phase":
            
                self.model.Mix(self.mode[0],self.weights[0] ,self.weights[1])
           
        elif self.item1=="Phase" or self.item1=="Uniform Phase":
            self.items(0 , 1)
            
            if self.item1=="Phase" and self.item2=="Magnitude":
               
                self.model.Mix(self.mode[0],1-self.weights[1] ,1-self.weights[0])
            
            elif self.item1=="Phase" and self.item2=="Uniform Magitude":
                self.model.Mix(self.mode[0], 1-self.weights[1] ,1-self.weights[0])
            
            elif self.item1=="Uniform Phase" and self.item2=="Uniform Magitude":
                
                self.model.Mix(self.mode[0] ,self.weights[0] ,self.weights[1] )
            elif  self.item1=="Uniform Phase" and self.item2=="Magitude":
               
                self.model.Mix(self.mode[0] ,1-self.weights[1] ,self.weights[0] )
        elif self.item1=="Real":
            self.items(5,6)  
            self.model.Mix(self.mode[1] , self.weights[0] , self.weights[1])
        
        elif self.item1=="Imaginary":
             self.items(4,6)
             self.model.Mix(self.mode[1] , 1-self.weights[1] , 1-self.weights[0])
        logger.debug("User selects the mode to consist of :" + self.item1 + "  and  "+self.item2 )
        
    def disable_Uis(self):
        
        for box in self.Box:
            box.setEnabled(False)
        
    
    def Show_Output(self):
        
        index=self.Box[6].currentIndex()
        if index==0:
           
            self.show_in=self.views[4]
            logger.debug("user displayed the output of the mixer on output1" )
            
        else:
            self.show_in=self.views[5]
            logger.debug("user displayed the output of the mixer on output2" )
            
         
        self.Box[4].setEnabled(True)
        self.Box[5].setEnabled(True) 
        self.model=ImageModel(self.images , self.views , self.Box ,  self.components,self.show_in  )
        self.model.Mix(self.mode[0] ,self.weights[0] ,self.weights[1]  )
        

def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    application = ApplicationWindow()
    application.show()
    app.exec_()


if __name__ == "__main__":
    main()

