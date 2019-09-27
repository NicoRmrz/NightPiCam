from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot, QObject, QSize

# --------------------------------------------------------------------------------------------------------------
# --------------------------------- GUI setStylesheet Class ----------------------------------------------------
# -------------------------------------------------------------------------------------------------------------- 
class GUI_Stylesheets(QObject):
	
	 # Initializes the necessary objects into the slider class for control
	def __init__(self):
		super(GUI_Stylesheets, self).__init__()
		
		self.mainWindow = 	("background-color: #95c8d8") 
		
		self.NM_mainWindow = ("background-color: rgba(49, 51, 53, 240);")
	
		
		self.statusBarWhite = ("QStatusBar { background: #95c8d8; "
										"color:white;} "

							"QStatusBar::item {border: 1px solid #95c8d8; "
								"border-radius: 3px; }"
								
							)
		
		self.NM_statusBarWhite = ("QStatusBar { background: #313335;"
										"color:white;} "

							"QStatusBar::item {border: 1px solid #313335; "
								"border-radius: 3px; }"
								
							)
		
		self.statusBarRed = ("QStatusBar {color:red;} ")
							
		self.statusBar_XY	= (	"QLabel {border: none; "
								"background-color: qlineargradient(spread:pad x1:0.45, y1:0.3695, x2:0.427, y2:0, "
								"stop:0 rgba(242, 242, 242, 0), "
								"stop:1 rgba(242,242,242, 0)); "						
								"font: 20 px; "
								"font-weight: bold; "
								"color: black; }"			
							)			
							
		self.NM_statusBar_XY	= (	"QLabel {border: none; "
								"background-color: qlineargradient(spread:pad x1:0.45, y1:0.3695, x2:0.427, y2:0, "
								"stop:0 rgba(242, 242, 242, 0), "
								"stop:1 rgba(242,242,242, 0)); "						
								"font: 20 px; "
								"font-weight: bold; "
								"color: white; }"			
							)			
							
		self.statusBar_widgets	= (	"QLabel {border: none; "
								"background-color: qlineargradient(spread:pad x1:0.45, y1:0.3695, x2:0.427, y2:0, "
								"stop:0 rgba(242, 242, 242, 0), "
								"stop:1 rgba(242,242,242, 0)); "						
								"font: 20 px; "
								"font-weight: lighter; "
								"color: black; }"			
							)			
							
		self.NM_statusBar_widgets	= (	"QLabel {border: none; "
								"background-color: qlineargradient(spread:pad x1:0.45, y1:0.3695, x2:0.427, y2:0, "
								"stop:0 rgba(242, 242, 242, 0), "
								"stop:1 rgba(242,242,242, 0)); "						
								"font: 20 px; "
								"font-weight: lighter; "
								"color: white; }"			
							)			
		
		self.videoStream = 	("background-color: qlineargradient(spread:pad x1:0.45, y1:0.3695, x2:0.427, y2:0, "
								"stop:0 rgba(0, 0, 0, 100), "
								"stop:1 rgba(242,242,242,100))"
							)
		
		self.consoleLog	=	("font: 12px Verdana; "
							"background-color: qlineargradient(spread:pad x1:0.45, y1:0.3695, x2:0.427, y2:0, "
								"stop:0 rgba(242, 242, 242, 240), "
								"stop:1 rgba(255,255,255,255)); "
								"color: black; "
							)
		
		self.NM_consoleLog	=	("font: 12px Verdana; "
							"background-color: qlineargradient(spread:pad x1:0.45, y1:0.3695, x2:0.427, y2:0, "
								"stop:0 rgba(242,242,242, 0), "
								"stop:1 rgba(242,242,242, 0));"
								"color: white; "
								"border: none;"
							)
		
		self.progressBar = 	("QProgressBar::chunk {background-color: #CD96CD;} "
							"background-color: qlineargradient(spread:pad x1:0.45, y1:0.3695, x2:0.427, y2:0, "
								"stop:0 rgba(242, 242, 242, 240), "
								"stop:1 rgba(255,255,255,255))"
							)
							
		self.startButton = 	("font: bold 12px Verdana; "
							"background-color: qlineargradient(spread:pad x1:0.45, y1:0.3695, x2:0.427, y2:0, "
								"stop:0 rgba(242, 242, 242, 0), "
								"stop:1 rgba(255,255,255,0)); "
								"border-style: outset; "
								"border-radius: 4px"
							)
							
		self.recordButton = ("font: bold 12px Verdana; "
							"background-color: qlineargradient(spread:pad x1:0.45, y1:0.3695, x2:0.427, y2:0, "
								"stop:0 rgba(250, 218, 94, 0), "
								"stop:1 rgba(255,255,255,0)); "
								"border-style: outset; "
								"border-radius: 4px; "
							)

		self.stopButton	=	("font: bold 12px Verdana; "
							"color: white; "
							"background-color: qlineargradient(spread:pad x1:0.45, y1:0.3695, x2:0.427, y2:0, "
								"stop:0 rgba(250, 41, 57, 0), "
								"stop:1 rgba(255,255,255,0)); "
								"border-style: outset; "
								"border-radius: 4px"
							)