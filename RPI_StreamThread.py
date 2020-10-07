from picamera import PiCamera, Color
from picamera.array import PiRGBArray
from picamera.exc import PiCameraValueError, PiCameraRuntimeError
import time
import numpy as np
from time import sleep
import datetime
import os
from PyQt5.QtGui import QImage
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot

# File Structure
Main_path = os.getcwd() + "/"
Image_Path = Main_path + "Snapshots/"
             
# --------------------------------------------------------------------------------------------------------------
# ----------------------------------- VIdeo Stream Thread Class ------------------------------------------------
# --------------------------------------------------------------------------------------------------------------                   
class QRPIVideoStreamThread(QThread):
	Video_Stream_signal = pyqtSignal(np.ndarray)
	Error_Signal = pyqtSignal(str) 
    
	def __init__(self, RPICamera, rawcap):
		QThread.__init__(self)
		self.camera = RPICamera
		self.raw = rawcap
		self.VideoStream_Ready = False
        
    #Sets up the program to initiate video stream
	def Set_Video_Stream_Ready(self, stream_Rdy):
		self.VideoStream_Ready = stream_Rdy
       
	def run(self):
		self.setPriority(QThread.HighestPriority)

		while (1):
			
            #Set Video Stream to GUI Qlabel
			if (self.VideoStream_Ready != False):
				try:
					# PiCam Stream configuration
					#emit frame captured
					self.StreamArray()
				
				except PiCameraValueError:
					self.SendError("Stream Error.. Try Again!")	
							
				except PiCameraRuntimeError:
					self.SendError("Stream Error.. Try Again!")	
					self.VideoStream_Ready = True
		
			#time.sleep(0.01)
          

# ------------------------------------------------------------------			
# --------------- Stream Array Function ----------------------------
# ------------------------------------------------------------------			
	def StreamArray(self):

		for frame in (self.camera.capture_continuous(self.raw, format = 'bgr', splitter_port= 2)): 

			# PiCam Stream configuration
			self.camera.annotate_foreground = Color('white')
			ts = datetime.datetime.now().strftime("%d %B %Y %I:%M:%S%p")
			self.camera.annotate_text = (ts)
		#	self.camera.annotate_background = Color.from_rgb_bytes(152, 251, 152) 
		
			# grab the raw NumPy array representing the image
			image = frame.array
			
			# clear the stream in preparation for the next frame
			self.raw.truncate(0)
						
			#emit frame data captured
			self.Video_Streaming(image)
			
			if (self.VideoStream_Ready != True):
				break
							
# ------------------------------------------------------------------		
# ------------Emit Signals Functions -------------------------------
# ------------------------------------------------------------------  
    #Emits the estring to console log GUI
	def Video_Streaming(self,stream_str):
		self.Video_Stream_signal.emit(stream_str) 
   
	# Emits error message to console log
	def SendError(self, string):
		self.Error_Signal.emit(string)              

