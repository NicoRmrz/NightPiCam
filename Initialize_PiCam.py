from picamera import PiCamera, Color
from picamera.array import PiRGBArray
from time import sleep

# --------------------------------------------------------------------------------------------------------------
# ------------------------------- Raspberry Pi Camera Setup Class ----------------------------------------------
# -------------------------------------------------------------------------------------------------------------- 
class Setup_PiCam(object):
        def __init__(self):
                self.camera = None
                  
        # Instantiate PiCamera module
        def PiCam_Configuration(self):
                self.camera = PiCamera()  
                self.camera.rotation = 90
                self.camera.annotate_text_size = 25
               # self.camera.resolution = (800, 480)
                self.camera.resolution = (1280, 720)
                # ~ self.camera.resolution = (640, 480)
                # ~ self.camera.resolution = (1920, 1088)
                self.rawCapture = PiRGBArray(self.camera)
                self.camera.framerate = 90
                 
                # allow the camera to warmup
                sleep(0.1)
                
                #~ return self.camera
                return self.camera, self.rawCapture
                

