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
# --------------------------------- Exit QPushButton Class -------------------------------------------------
# --------------------------------------------------------------------------------------------------------------
class Exit_Button(QPushButton):        
    old_window = None
    new_window = None

    # Initializes the necessary objects into the button class for control
    def __init__(self, window, text):
        super(Exit_Button, self).__init__()
        self.setText(text)
        self.setParent(window)
   
