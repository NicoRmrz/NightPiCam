from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot, QObject
from PyQt5.QtGui import QPixmap, QIcon, QFont, QTextCursor, QPalette, QImage, QBrush, QImage

from time import sleep
import os
from GUI_Stylesheets import GUI_Stylesheets

# Instantiate style sheets for GUI Objects
GUI_Style = GUI_Stylesheets()

# Icon Image locations
Main_path = os.getcwd() + "/"     
Icon_Path = Main_path + 'Icon_Image/pup.jpg'
Logo_Path = Main_path + 'Icon_Image/logo_icon_white.png'
Camera_Idle_Path = Main_path + 'Icon_Image/cam_idle.png'
Camera_Capture_Path = Main_path + 'Icon_Image/cam_capture.png'
Video_Idle_Path = Main_path + 'Icon_Image/video_idle.png'
Video_Recording_Path = Main_path + 'Icon_Image/video_recording.png'
Stop_Idle_Path = Main_path + 'Icon_Image/stop_idle.png'
Stop_Greyed_Path = Main_path + 'Icon_Image/stop_grey.png'
TimeLapse_Idle_Path = Main_path + 'Icon_Image/timelapse_idle1.png'
TimeLapse_InUse_Path = Main_path + 'Icon_Image/timelapse_inuse.png'
Main_Tab_Path = Main_path + 'Icon_Image/mainTab.png'
Settings_Tab_Path = Main_path + 'Icon_Image/settingsTab.png'
ServoController_Tab_Path = Main_path + 'Icon_Image/controllerTab.png'
Left_Button_Path = Main_path + 'Icon_Image/leftButton.png'
Right_Button_Path = Main_path + 'Icon_Image/rightButton.png'
Up_Button_Path = Main_path + 'Icon_Image/upButton.png'
Down_Button_Path = Main_path + 'Icon_Image/downButton.png'
Left_Button_Pressed_Path = Main_path + 'Icon_Image/leftButton_Pressed.png'
Right_Button_Pressed_Path = Main_path + 'Icon_Image/rightButton_Pressed.png'
Up_Button_Pressed_Path = Main_path + 'Icon_Image/upButton_Pressed.png'
Down_Button_Pressed_Path = Main_path + 'Icon_Image/downButton_Pressed.png'
Freelook_Path = Main_path + 'Icon_Image/freelook1.png'

# --------------------------------------------------------------------------------------------------------------
# ------------------------------------ Button Reset Handler Class ----------------------------------------------
# --------------------------------------------------------------------------------------------------------------
class Button_Reset_Handler(QObject):
        def __init__(self, captureThre, recordThre capture, record, vidSteam, statusBar):
                super(Button_Reset_Handler, self).__init__()
                self.captureThread = captureThre
                self.recordThread = recordThre
                self.captureBtn = capture
                self.recordBtn = record
                self.Video_Stream = vidSteam
                self.statusBar = statusBar
                
                # Connect signals to handler function
                self.recordThread.Btn_Handler.connect(self.Button_Handler)
                self.captureThread.Btn_Handler.connect(self.Button_Handler)
                
        # Resets button if button is pressed while recording video
        def Button_Handler(self, string):
                self.RstBtn = string
                
                if self.RstBtn == "Capture":
                        self.captureBtn.setIcon(QIcon(Camera_Idle_Path))
                        
                elif self.RstBtn == "Record":     
                        self.recordBtn.setIcon(QIcon(Video_Idle_Path))        

                elif self.RstBtn == "Stream":
                        self.Video_Stream.Set_Video_Stream_Ready(True)          

# --------------------------------------------------------------------------------------------------------------
# ------------------------------------ Error Handler Class -----------------------------------------------------
# --------------------------------------------------------------------------------------------------------------
class Error_Handler(QObject):
        def __init__(self, captureThre, recordThre, videoStreamThre, statusBar):
                super(Error_Handler, self).__init__()
                self.captureThread = captureThre
                self.recordThread = recordThre
                self.videoStream = videoStreamThre
                self.statusBar = statusBar
                
                # Connect signals to error function
                self.recordThread.Error_Signal.connect(self.Show_Error)
                self.captureThread.Error_Signal.connect(self.Show_Error)
                self.videoStream.Error_Signal.connect(self.Show_Error)
                
        # Function to write error message to console log
        def Show_Error(self, string):
                self.errorMessage = string
                self.statusBar.setStyleSheet(GUI_Style.statusBarRed)
                self.statusBar.showMessage(self.errorMessage, 5000) 
                
        # Function to continue streams after any errors
        def resetAllStreams(self, string):
                self.videoStream.Set_Video_Stream_Ready(True)
 
