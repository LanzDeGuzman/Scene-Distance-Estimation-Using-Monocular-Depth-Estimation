# Initialization of Libraries and Dependencies

import cv2
import os
import numpy as np

from config import target
from modules.SceneLocator import FindObjects
from modules.ROIConfigurator import ROIConfigurator
from modules.MonocularEstimator import MonocularEstimator
from modules.TargetObjectLocator import FindTargetObject

# Initialization of camera 
cam = cv2.VideoCapture(0)                                                                                                      # To test webacm use "cv2.VideoCapture(0)" 0 is the default value, change whenever necessary.
#cam = cv2.VideoCapture('/Users/espiedeguzman/Desktop/Untitled.mp4')                                                           # To test on pre recorded videos replace "0" with the file path and file.
#cam = cv2.imread('/path')                                                                                                     # To test on imagge use the following line and inpute the file path and file.

ROIConfigurator(cam)

while True:
  success, img = cam.read()                                                                                               # Use for video/camera feed.
  #img = cam                                                                                                              # Use for image.
  #img = cv2.resize(img, None, fx=0.6, fy=0.6)                                                                            # Use to reszie images **Note however that this may cause inacuracy in distance estimation calulations.
  
  img_height, img_width, channels = img.shape
  img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)                                                                              # Converts color feed from BGR to RGB.

  monocular_depth_val = MonocularEstimator(img)                                                                           # Executes the MDE Model.                                                                                  
  target_object_depth_val = FindTargetObject(img,target,monocular_depth_val)                                              # YOLO Object Detection execution for Target Object.
  FindObjects(img,target_object_depth_val,monocular_depth_val)                                                            # YOLO OBject Detection execution for Surrounding Object and Lens Optic Calculation.

  img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)                                                                              # Converts color feed back to inital format.
  
  cv2.imshow('Depth Map', monocular_depth_val)                                                                            # Shows MDE Generated Depth Map.
  cv2.imshow('Monocular Depth Estimation',img)                                                                            # Video Feed with Results.
  key = cv2.waitKey(1)
  # Exit the loop if the 'q' key is pressed
  if key == ord("q"):
    break

cam.release()
cv2.destroyAllWindows()