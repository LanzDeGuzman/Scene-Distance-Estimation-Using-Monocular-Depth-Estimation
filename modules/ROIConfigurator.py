# Containts the function responsible for creating configurable sliders for the cropped ROI region.

import cv2

def ROIConfigurator(cam):
    
    def on_trackbar(val):
        pass  

    cv2.namedWindow("ROI Size")
    width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

    initial_widthcrop = int(width*.4)                                                                                          # Declares a width value - 40% of the initial feed width.
    initial_heightcrop = int(height*.8)                                                                                        # Declares a height value - 80% of the initial height feed.

    # Create trackbars for setting the top-bottom and left-right size of the ROI
    cv2.createTrackbar("Left-Right Crop", "ROI Size", initial_widthcrop, width, on_trackbar)                                   # Max slider values do not exceed the feed's dimensions. 
    cv2.createTrackbar("Top-Bottom Crop", "ROI Size", initial_heightcrop, height, on_trackbar)