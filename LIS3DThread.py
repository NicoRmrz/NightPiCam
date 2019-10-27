import LIS3DH
import time, spidev, sys, smbus
from time import sleep
from PyQt5.QtGui import QImage
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot

             
# --------------------------------------------------------------------------------------------------------------
# ----------------------------- LIS3D Accelerometer Thread Class -----------------------------------------------
# --------------------------------------------------------------------------------------------------------------                   
class AcellerometerThread(QThread):
	axisSignals = pyqtSignal(int, int, int) 
    
	def __init__(self):
		QThread.__init__(self)
		self.exitProgram = False
		
		self.accel = LIS3DH.Accelerometer('i2c',i2cAddress = 0x19)
		#accel = LIS3DH.Accelerometer('spi', i2cAddress = 0x0, spiPort = 0, spiCS = 0)  # spi connection alternative
		self.accel.set_ODR(odr=50, powerMode='normal')
		self.accel.axis_enable(x='on',y='on',z='on')
		self.accel.interrupt_high_low('high')
		self.accel.latch_interrupt('on')
		self.accel.set_BDU('on')
		self.accel.set_scale()
        
    #Sets up the program to initiate video stream
	# ~ def startReading(self, Rdy):
		# ~ self.readReady = Rdy
        
    #Sets up the program to exit when the main window is shutting down
	def Set_Exit_Program(self, exiter):
		self.exitProgram = exiter,
        
	def run(self):

		while (1):
			
			# ~ if (self.readReady != False):
			x = self.accel.x_axis_reading()   
			y = self.accel.y_axis_reading()
			z = self.accel.z_axis_reading()    
			self.axisSignals.emit(x,y,z)
				# ~ self.readReady = False
			
			if(self.exitProgram == True):
				self.exitProgram = False
				break
            
			time.sleep(0.1)
          
				
            

