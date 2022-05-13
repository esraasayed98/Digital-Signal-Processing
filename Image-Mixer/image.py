import numpy as np
import logging

#Create logger
logging.basicConfig(filename="LoggingFile.log", 
                    format='%(asctime)s %(message)s', 
                    filemode='w')
logger=logging.getLogger() 
logger.setLevel(logging.DEBUG) 

class ImageModel():

    def __init__(self , image ,view , combo ,component,output_display_in ):
        
        
        self.images=image
        self.views=view
        self.Box=combo
        self.components=component
        self.show_in=output_display_in
        
        
        
    def  fourier(self,image):
        
        self.f=np.fft.fft2(image)
        self.fshift=np.fft.fftshift(self.f)
        self.magnitude= 20*np.log(np.abs(self.fshift))
        self.magnitude=np.asarray(self.magnitude , dtype=np.uint8)
        self.phase =np.angle(self.f)
        self.real=np.real(self.f)
        self.imag=np.imag(self.f)
        self.Mag=np.abs(self.f)
        self.fft=[self.magnitude ,self.phase , self.real , self.imag]
     
    def view(self , view_image ,image):
        view_image.show()
        view_image.setImage(image)
        view_image.setImage(image.T)
         
     
    def Combo_index(self): 
        #to get the index in the fourier combo_boxes
        if type(self.images[0]) == np.ndarray and type(self.images[1]) == np.ndarray :
           
                  
            for i in range (0,2):
                
                index=self.Box[i].currentIndex()
                
                self.fourier(self.images[i])
                for j in range (0,4):
                   
                    if index==j:
                        text=self.Box[i].currentText()  
                        self.view(self.views[i+2] ,self.fft[j]) 
                        logger.debug("User shows " + str( text) + " part oF image " +str(i+1) )
                        
                        
        elif  type(self.images[0]) != np.ndarray and type(self.images[1]) == np.ndarray :
            #only have image2
            index=self.Box[1].currentIndex()
           
            self.fourier(self.images[1])
            for j in range (0,4):
                
                if index==j:
                    text=self.Box[1].currentText()  
                    self.view(self.views[3] ,self.fft[j])
                    logger.debug("User shows  " + str( text) + " part oF image2 " )
                        
        else:
            #only have image1
            index=self.Box[0].currentIndex()
           
            self.fourier(self.images[0])
            for j in range (0,4):
                
                if index==j:
                    text=self.Box[0].currentText()
                    self.view(self.views[2] ,self.fft[j])
                    logger.debug("User shows  " + str( text) + " part oF image1 "  )
                     
        
                  

    def Mix(self , mode , w1 , w2 ) :
        
        
        self.item1=self.Box[2].currentText()
        self.item2=self.Box[3].currentText()
        
        self.fourier(self.components[0])
        self.component1 =[self.Mag ,self.phase , self.real , self.imag]
    
        self.fourier(self.components[1])
        self.component2  =[self.Mag ,self.phase , self.real , self.imag]
    
        if  mode == "magnitudeAndPhase" :
            
            if (self.item1 =="Uniform Magnitude" and self.item2=="Uniform Phase" ) or (self.item1 =="Uniform Phase" and self.item2=="Uniform Magnitude" ) :
               
                self.component1[1]=np.zeros(self.components[0].shape)
                self.component2[1]=np.zeros(self.components[0].shape)
                self.component1[0]=np.ones(self.components[0].shape)
                self.component2[0]=np.ones(self.components[0].shape)
                
            elif self.item1=="Uniform Phase" or self.item2=="Uniform Phase":
            
               
                self.component1[1]=np.zeros(self.components[0].shape)
                self.component2[1]=np.zeros(self.components[0].shape)
                
            elif self.item1=="Uniform Magnitude" or self.item2=="Uniform Magnitude":
              
                self.component1[0]=np.ones(self.components[0].shape)
                self.component2[0]=np.ones(self.components[0].shape)
       
            
            mix= (w1* self.component1[0] + (1-w1) *self.component2[0] )* np.exp(np.vectorize(complex)(0,(1-w2)*self.component1[1]+(w2 )*self.component2[1] ))
            self.inverse=np.real(np.fft.ifft2( mix))
            self.view(self.show_in , self.inverse)
            
            
        else:
            mix=np.vectorize(complex)((w1 *  self.component1[2] +(1-w1 ) *  self.component2[2]), ((1-w2) *self.component1[3] + (w2)*self.component2[3] )) 
            self.inverse=np.real(np.fft.ifft2( mix))
            self.view(self.show_in , self.inverse)
        logger.debug("user mixes component 1 and component2 with mode  " + str(mode) +"  with weghits  " +str(w1) + "  and  "+str(w2) )
        
    
   
        
    
  