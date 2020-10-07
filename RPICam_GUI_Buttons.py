import datetime
import os
import time
import sys
import PyQt5
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLineEdit, QLabel, QCheckBox, QTextEdit, QProgressBar, QSizePolicy, QWidget, QTabWidget, QHBoxLayout, QVBoxLayout, QSlider
from PyQt5.QtGui import QPixmap, QIcon, QFont, QTextCursor, QPalette, QImage, QBrush
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot, QObject, QSize
from GUI_Stylesheets import GUI_Stylesheets

# Instantiate style sheets for GUI Objects
GUI_Style = GUI_Stylesheets()

RECORD_TIME = 100        # 100 seconds

# Icon Image locations
Main_path = os.getcwd() + "/"     
# ~ Icon_Path = Main_path + 'Icon_Image/pup.jpg'
Camera_Idle_Path = Main_path + 'Icon_Image/cam_idle.png'
Camera_Capture_Path = Main_path + 'Icon_Image/cam_capture.png'
Video_Idle_Path = Main_path + 'Icon_Image/video_idle.png'
Video_Recording_Path = Main_path + 'Icon_Image/video_recording.png'
Stop_Idle_Path = Main_path + 'Icon_Image/stop_idle.png'
Stop_Greyed_Path = Main_path + 'Icon_Image/stop_grey.png'


#GUI Classes
# --------------------------------------------------------------------------------------------------------------
# --------------------------------- Snapshot QPushButton Class -------------------------------------------------
# --------------------------------------------------------------------------------------------------------------
class Snapshot_Button(QPushButton):        
    old_window = None
    new_window = None

    # Initializes the necessary objects into the button class for control
    def __init__(self, window, text, capture_thread, Vid_Stream, TimeThread, record_thread):
        super(Snapshot_Button, self).__init__()
        self.setText(text)
        self.setParent(window)
        self.captureThread = capture_thread
        self.Video_Stream = Vid_Stream
        self.TimerThread = TimeThread
        self.recordThread = record_thread
        
        #Connecting completions signals to functions
        self.captureThread.Snap_Captured_signal.connect(self.Snapshot_Captured)    
        self.TimerThread.time_signal.connect(self.Timer_Finished)   
        self.captureThread.Status_Signal.connect(self.Camera_Status)    
        self.captureThread.Capture_Terminated_signal.connect(self.Camera_Stopped)

    # Function call for the click event
    def On_Click(self):
        
        # Button turns red for activated
        self.setIcon(QIcon(Camera_Capture_Path))

    # Function call for the Un_click event
    def Un_Click(self):
        #Stop video stream to capture image
        self.Video_Stream.Set_Video_Stream_Ready(False)
       
        #Take a picture
        self.captureThread.Set_Snapshot_Ready(True)
        self.captureThread.Set_Stop(False)      # set stop button to false
        self.recordThread.Set_Snapshot_Ready(True)  #let other  thread know capture button was pressed
        self.captureThread.start()
        
    #Function for picture capture completion
    def Snapshot_Captured(self, Snap_done):
        self.Snap_captured = Snap_done
        
        #Display picture taken for 3 seCamera_Statusconds
        self.TimerThread.set_Timer(1.5, True)
    
    #Function for completion of timer    
    def Timer_Finished(self, timeout):
        self.Timeout = timeout
        
        #set to find out if camera is ready
        self.captureThread.Get_Rec_Status()
        
    #Function to reset GUI object pending on recording status
    def Camera_Status(self, rec_status):
        self.status = rec_status

        if (self.status > 0):
            self.setIcon(QIcon(Camera_Idle_Path)) 
            self.Reset_GUI() 
        else:
            self.Reset_GUI() 
        
    #Function when stopped button is pressed
    def Camera_Stopped(self, text):
        self.stopText = text 
        self.Reset_GUI() 
        
    #Resets the necessary objects when the test is reran
    def Reset_GUI(self):
        self.Video_Stream.Set_Video_Stream_Ready(True) #Continue video stream 
        self.setIcon(QIcon(Camera_Idle_Path))

# --------------------------------------------------------------------------------------------------------------
# --------------------------------- Record QPushButton Class ---------------------------------------------------
# --------------------------------------------------------------------------------------------------------------
class Record_Button(QPushButton):      
    old_window = None
    new_window = None

    # Initializes the necessary objects into the button class for control
    def __init__(self, window, text, record_thread, Vid_Stream, capture_thread, TimeThread):
        super(Record_Button, self).__init__()
        self.setText(text)
        self.setParent(window)
        self.recordThread = record_thread
        self.captureThread = capture_thread
        self.Video_Stream = Vid_Stream
        self.TimerThread = TimeThread
        
        #Connecting thread (emits) to functions
        self.recordThread.Recording_Completed_signal.connect(self.Video_Finished)
        self.recordThread.Recording_Terminated_signal.connect(self.Video_Stopped)
        self.TimerThread.sleep_signal.connect(self.PostPauseStream)

    # Function call for the click event
    def On_Click(self):        
        #Rests progress bar
        pass

    # Function call for the Un_click event
    def Un_Click(self):
        
        #Stop video stream to record a video
        self.Video_Stream.Set_Video_Stream_Ready(False)
        
        #Wait for stream to pause
        self.TimerThread.set_recTimer(0.5, True)
                  
    def PostPauseStream(self, timeout):
        self.Timeout = timeout
        
         # Button turns red for activated
        self.setIcon(QIcon(Video_Recording_Path))
        
        #Set thread to record video
        self.recordThread.Set_Record_Ready(True, RECORD_TIME)
        self.recordThread.Set_Stop(False)                 # set stop button to false
        self.recordThread.Set_Snapshot_Ready(False)
        self.captureThread.Set_Record_Ready(True)          #let other  thread know record button was pressed        
        
    # Function of video completion
    def Video_Finished(self, Video_name):
        self.Reset_GUI()
        
    # Function of stop button pressed
    def Video_Stopped(self, str_):
        self.Reset_GUI()
                
    # Resets the necessary objects when the procedure is finished
    def Reset_GUI(self):
        self.Video_Stream.Set_Video_Stream_Ready(True) #Continue video stream 
        self.setIcon(QIcon(Video_Idle_Path))

# --------------------------------------------------------------------------------------------------------------
# --------------------------------- STOP QPushButton Class -----------------------------------------------------
# --------------------------------------------------------------------------------------------------------------
class Stop_Button(QPushButton):        
	old_window = None
	new_window = None

    #Initializes the necessary objects into the button class for control
	def __init__(self, window, text, Record_Thread, Record_Button, Vid_Stream, Capture_Thread):
		super(Stop_Button, self).__init__()
		self.setText(text)
		self.setParent(window)
		self.recordVideoThread = Record_Thread
		self.RecordBtn = Record_Button
		self.Video_Stream = Vid_Stream
		self.captureThread = Capture_Thread

	#Function call for the click event
	def On_Click(self):
		# Button turns grey
		self.setIcon(QIcon(Stop_Greyed_Path))
		
	#Function call for the Un_click event
	def Un_Click(self):

		#Stop all running procedure
		self.recordVideoThread.Set_Stop(True)
		self.captureThread.Set_Stop(True)
		self.Reset_GUI()

	#Resets the necessary objects when the test is reran
	def Reset_GUI(self):
		#Turn button color back to normal
		self.setIcon(QIcon(Stop_Idle_Path))
		self.RecordBtn.setIcon(QIcon(Video_Idle_Path))
