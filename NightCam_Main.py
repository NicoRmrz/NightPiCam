import datetime
import os
import time
import sys
import PyQt5
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLineEdit, QLabel, QCheckBox, QTextEdit, QStatusBar,QProgressBar, QSizePolicy, QAbstractItemView, QWidget, QTabWidget, QHBoxLayout, QVBoxLayout, QSlider
from PyQt5.QtGui import QPixmap, QIcon, QFont, QTextCursor, QPalette, QImage, QBrush, QImage
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot, QObject, QSize

#Imports from made files
from Initialize_PiCam import Setup_PiCam
from RPICam_GUI_Buttons import Snapshot_Button, Record_Button, Stop_Button
from RPI_Capture_Thread import QRPICaptureThread
from RPI_Record_Thread import QRPIRecordVideoThread
from Handlers import Button_Reset_Handler, Error_Handler
from StreamWindow import Stream_Video
from RPI_StreamThread import QRPIVideoStreamThread
from Sleeper_Thread import QTimeThread
from web_stream import WebStream_Thread
from GUI_Stylesheets import GUI_Stylesheets

# Current version of application - Update for new builds
appVersion = "0.1"      # Update version


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

# Create folders for pictures/ videos
Image_Path = Main_path + "Snapshots/"
Video_Path = Main_path + "Videos/"

if not os.path.exists(Image_Path):
    os.makedirs(Image_Path)
    
if not os.path.exists(Video_Path):
    os.makedirs(Video_Path)
    
if not os.path.exists(TimeLapse_Path):
    os.makedirs(TimeLapse_Path)
        
# Instantiate style sheets for GUI Objects
GUI_Style = GUI_Stylesheets()

# --------------------------------------------------------------------------------------------------------------
# --------------------------------- Main Window Class ----------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------   
class Window(QMainWindow):
    
    # Initialization of the GUI
    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50,50,800,480)
        self.setWindowTitle("Night Cam v" + appVersion)
        self.setStyleSheet(GUI_Style.NM_mainWindow)
        self.setWindowIcon(QIcon(Icon_Path))
        
        # --------------------------------------------------------------
        # -------------------- Initialize  -----------------------------
        # --------------------------------------------------------------  
        # Initialize Pi Camera for all threads
        PiCam = Setup_PiCam()
        self.camera, self.rawCapture = PiCam.PiCam_Configuration() 
        
        # --------------------------------------------------------------
        # ---------------- Instantiate All Threads  --------------------
        # -------------------------------------------------------------- 
        self.RPICaptureThread = QRPICaptureThread(self.camera)
        self.RPIRecordThread = QRPIRecordVideoThread(self.camera)
        self.Video_Stream = QRPIVideoStreamThread(self.camera, self.rawCapture)
        self.Timer_Thread = QTimeThread()

        # --------------------------------------------------------------
        # ---------------- Start All Threads ---------------------------
        # -------------------------------------------------------------- 
        self.RPICaptureThread.start()
        self.RPIRecordThread.start()
        self.RPITimeLapseThread.start()
        self.Video_Stream.start()
        self.Timer_Thread.start()
    
        # --------------------------------------------------------------
        # ---------------- Create Main Widget --------------------------
        # -------------------------------------------------------------- 
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # --------------------------------------------------------------
        # -------------- Create Bottom Status Bar-----------------------
        # -------------------------------------------------------------- 
        self.StatusBar()
        self.setStatusBar(self.statusBar)
        
        # --------------------------------------------------------------
        # ------------- Create Main Window Layout ----------------------
        # --------------------------------------------------------------
        # Create Main window layout to hold tabs and GUI objects
        Main_Window_HLayout = QHBoxLayout()  
        
        # Instantiate Window objects
        self.VideoStream()
          
        Main_Window_HLayout.addWidget(self.Vid_Stream)       
        Main_Window_HLayout.setContentsMargins(20, 20, 20, 20)    
    
        # --------------------------------------------------------------
        # ------------ Add Final Layout to Main Window -----------------
        # -------------------------------------------------------------- 
        # Set Main window layout to GUI central Widget
        self.centralWidget().setLayout(Main_Window_HLayout)
        self.centralWidget().isWindow()
        
        # --------------------------------------------------------------
        # --------------- Initialize Start Up Services -----------------
        # -------------------------------------------------------------- 
        # Instantiate button reset handler and error handler
        self.allHandlers()
        
        # Display GUI Objects
        # self.show()
        #~ self.showFullScreen()
        self.showMaximized()
          
# --------------------------------------------------------------------------------------------------------------
# -------------------------------- GUI Object Functions --------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------     
    # Create Window to stream live feed
    def VideoStream(self):
        self.Vid_Stream = Stream_Video(self, self.Video_Stream, self.RPIRecordThread, self.RPICaptureThread)
        self.Vid_Stream.setMinimumSize(800, 480)
        self.Vid_Stream.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.Vid_Stream.setBackgroundRole(QPalette.Base)
        self.Vid_Stream.setScaledContents(True)
        self.Vid_Stream.setStyleSheet(GUI_Style.videoStream)

    # ------------------------------------------------------------------
    # ---------------- Create Status Bar Function ----------------------
    # ------------------------------------------------------------------
    def StatusBar(self):
        self.statusBar = QStatusBar()
        self.statusBar.setStyleSheet(GUI_Style.statusBarWhite)
        
        # self.xHorizontal = QLabel()
        # self.xHorizontal.setMinimumSize(50, 12)
        # self.xHorizontal.setStyleSheet(GUI_Style.statusBar_XY)
        # self.xHorizontal.setText("| X: 90")
        # self.xHorizontal.setAlignment(Qt.AlignCenter)
        
        # self.yVertical = QLabel()
        # self.yVertical.setMinimumSize(50, 12)
        # self.yVertical.setStyleSheet(GUI_Style.statusBar_XY)
        # self.yVertical.setText("| Y: 90")
        # self.yVertical.setAlignment(Qt.AlignCenter)
        
        # self.res = QLabel()
        # self.res.setMinimumSize(50, 15)
        # self.res.setStyleSheet(GUI_Style.statusBar_widgets)
        # self.res.setText("| res 1280x720")
        # self.res.setAlignment(Qt.AlignCenter)
        
        # self.statusBar.addPermanentWidget(self.xHorizontal, 0)
        # self.statusBar.addPermanentWidget(self.yVertical, 0)
        # self.statusBar.addPermanentWidget(self.res, 0)
        
        self.statusBar.showMessage("Starting Up... ", 4000)
        
    # ------------------------------------------------------------------
    # ------------ Home Tab GUI Objects Functions ----------------------
    # ------------------------------------------------------------------
    # Creating button for snapshots
    def Snapshot_Btn_GUI(self):
        self.snpsht_btn = Snapshot_Button(self, "" self.RPICaptureThread, self.Video_Stream, self.Timer_Thread, self.RPIRecordThread)
        self.snpsht_btn.setStyleSheet(GUI_Style.startButton)
        self.snpsht_btn.pressed.connect(self.snpsht_btn.On_Click)
        self.snpsht_btn.released.connect(self.snpsht_btn.Un_Click)
        self.snpsht_btn.setIcon(QIcon(Camera_Idle_Path))
        self.snpsht_btn.setIconSize(QSize(65, 70))

    # Creating button for recording video
    def Record_Btn_GUI(self):
        self.rec_btn = Record_Button(self, "", self.RPIRecordThread,  self.Video_Stream,  self.RPICaptureThread, self.Timer_Thread)
        self.rec_btn.setStyleSheet(GUI_Style.recordButton)
        self.rec_btn.pressed.connect(self.rec_btn.On_Click)
        self.rec_btn.released.connect(self.rec_btn.Un_Click)
        self.rec_btn.setIcon(QIcon(Video_Idle_Path))
        self.rec_btn.setIconSize(QSize(80, 80))

    # Creating button for recording video
    def Stop_Btn_GUI(self):
        self.stp_rec_btn = Stop_Button(self, "", self.RPIRecordThread, self.rec_btn, self.Video_Stream, self.RPICaptureThread)
        self.stp_rec_btn.setStyleSheet(GUI_Style.stopButton)
        self.stp_rec_btn.pressed.connect(self.stp_rec_btn.On_Click)
        self.stp_rec_btn.released.connect(self.stp_rec_btn.Un_Click) 
        self.stp_rec_btn.setIcon(QIcon(Stop_Idle_Path))
        self.stp_rec_btn.setIconSize(QSize(60, 60))

    # ------------------------------------------------------------------
    # ------------ Handler Insantiation Function -----------------------
    # ------------------------------------------------------------------
    # Instantiate button handler object class
    def allHandlers(self):
        self.buttonHandler = Button_Reset_Handler(self.RPICaptureThread, self.RPIRecordThread, self.snpsht_btn, self.rec_btn, self.Video_Stream, 
                                                         self.statusBar)
        self.errorHandler = Error_Handler(self.RPICaptureThread, self.RPIRecordThread, self.Video_Stream, self.statusBar)
   

    # ------------------------------------------------------------------
    # ----------- Close All Threads at app closure ---------------------
    # ------------------------------------------------------------------             
    # Stop all threads when GUI is closed
    def closeEvent(self, *args, **kwargs):
        self.RPICaptureThread.Set_Exit_Program(True)
        self.RPICaptureThread.wait(100)
        self.RPIRecordThread.Set_Exit_Program(True)
        self.RPIRecordThread.wait(100)
        self.Video_Stream.Set_Exit_Program(True)
        self.Video_Stream.wait(100)
        self.Timer_Thread.Set_Exit_Program(True)
        self.Timer_Thread.wait(100)

# ----------------------------------------------------------------------
# -------------------- MAIN LOOP ---------------------------------------
# ----------------------------------------------------------------------
def run():
    #Run the application
    app = QApplication(sys.argv)
    #Create GUI
    GUI = Window()
    #Exit
    sys.exit(app.exec())

#Main code
if __name__ == "__main__":
    run()
    
    
# Changelog:
# 0.1 - Strip RPICAM code for only needed parts