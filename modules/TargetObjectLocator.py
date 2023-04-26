# Contains the function that locates the Target Object within the ROI.

import cv2
import numpy as np
from config import yolo_target_model, target_names
from modules.LensOpticCalculator import LensOpticCalculator, LimitVal

def FindTargetObject(img,target,mde_Model):
    img_copy = img.copy()                                                                                                      # Creates an image copy to have clear feed free from drawn variables.
    img_height, img_width, channels = img_copy.shape
 
    top_bottom_crop = cv2.getTrackbarPos("Top-Bottom Crop", "ROI Size")                                                        # Retrieves the current ROI slider top-bottom crop values.
    left_right_crop = cv2.getTrackbarPos("Left-Right Crop", "ROI Size")                                                        # Retrieves the current ROI slider left-right crop values.

    # Calculates the coordinates of the ROI based on the current trackbar positions.
    x1 = int(img_width / 2 - left_right_crop / 2)
    x2 = int(img_width / 2 + left_right_crop / 2)
    y1 = int(img_height / 2 - top_bottom_crop / 2)
    y2 = int(img_height / 2 + top_bottom_crop / 2)

    # Declares the ROI and draws a reference box on the non-cropped video feed.
    img_roi = img_copy[y1:y2, x1:x2]
    cv2.rectangle(img,(x1,y1),(x2,y2),(0,0,0),2)

    # Converts YOLO's names file indexing to numerical values for convenient referencing.
    yolo_labels_indexing = {label:index for index,label in enumerate(target_names)}

    # Declares offset variables based on the ROI, used in referencing detected targets object within the ROI from the original feed.
    xoff = x1
    yoff = y1
    
    conf_threshold = 0.7                                                                                                       # Detection confidence treshold - 70% Treshold.
    nms_treshold = 0.4                                                                                                         # Detection boxing sensitivity - the Lower the value the more agressive and less boxes.    
    
    blob = cv2.dnn.blobFromImage(img_roi, 1/255, (320,320), [0,0,0],1,crop =False)
    yolo_target_model.setInput(blob)

    output_names = yolo_target_model.getUnconnectedOutLayersNames()  

    # Object Detection Using Yolo
    detection = yolo_target_model.forward(output_names)
    
    hT, wT, cT = img_roi.shape
    bbox = []
    class_ids = []
    confs = []

    for output in detection:
          for det in output:
              scores = det[5:]
              class_id = np.argmax(scores)
              confidence = scores[class_id]
              if confidence > conf_threshold:
                  w,h = int(det[2]*wT) , int(det[3]*hT)
                  x,y = int((det[0]*wT)-w/2), int((det[1]*hT)-h/2)
                  bbox.append([x,y,w,h])
                  class_ids.append(class_id)
                  confs.append(float(confidence))
              

    indices = cv2.dnn.NMSBoxes(bbox,confs,conf_threshold,nms_treshold)
    indices = np.array(indices).flatten() 

    # Whenever the target object is located from the ROI, its distance is computed using the lens optic calulation, along with this its centroid and midas depth value is stored. 
    target_index = yolo_labels_indexing[target]
    if target_index in class_ids:
        indexes = np.where(np.array(class_ids) == target_index)[0]
        box1 = bbox[indexes[0]]
        x,y,w,h = box1[0],box1[1],box1[2],box1[3]

        xcoord = (x+(x+w))/2
        ycoord = (y+(y+h))/2

        xoffset_coord = xcoord+xoff
        yoffset_coord = ycoord+yoff 

        # Inputs the detected centroid to the LimitVal Function to prevent indexing error.
        xoffset_coord = LimitVal(xoffset_coord, img_width)     
        yoffset_coord = LimitVal(yoffset_coord, img_height)

        img_roi = cv2.cvtColor(img_roi, cv2.COLOR_RGB2BGR)
        
        # Draws a bounding box and a circle on the target object and its centroid.
        cv2.rectangle(img_roi,(x,y),(x+w,y+h),(0,153,76),2)
        cv2.circle(img,(int(xoffset_coord),int(yoffset_coord)), 3, (0,0,0),2)

        target_midas_val = mde_Model[int(yoffset_coord),int(xoffset_coord)]                                                    # Retrieves the depth value of the Target Object from the generated MDE feed.
        target_computed_depthmap_val = LensOpticCalculator(h)                                                                  # Computes the Target Object's actualized distance using the Lens Optic Equation, and detected Target Object's pixel height.

        cv2.imshow('ROI',img_roi)
        return (target_computed_depthmap_val,target_midas_val)                                                                 # Returns the Target Object's computed actualized distance and midas value.