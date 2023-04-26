# Contains the function that locates the Surrounding Objects from the original feed.

import cv2
import numpy as np
from config import yolo_model, class_names
from modules.LensOpticCalculator import RatioProportionCalculator, LimitVal, SafetyLevel

    
def FindObjects(img,target_object_depth_val,monocular_depth_val):
    # Whenever the marker object is detected, other surrounding objects are also detected.
    if bool(target_object_depth_val):
        
        img_copy = img.copy()                                                                                                  # Creates an image copy to have clear feed free from drawn variables.
        
        # Rename Target Object Infomration variables for convienence. 
        reference_distance = target_object_depth_val[0]
        reference_point = target_object_depth_val[1]
    
        conf_threshold = 0.7                                                                                                   # Detection confidence treshold - 70% Treshold.
        nms_threshold = 0.4                                                                                                    # Detection boxing sensitivity - the Lower the value the more agressive and less boxes.   

        blob = cv2.dnn.blobFromImage(img_copy, 1/255, (320,320), [0,0,0],1,crop =False)
        yolo_model.setInput(blob)

        output_names = yolo_model.getUnconnectedOutLayersNames()  

        # Object Detection Using Yolo
        detection = yolo_model.forward(output_names)
        
        hT, wT, cT = img_copy.shape
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

            indices = cv2.dnn.NMSBoxes(bbox,confs,conf_threshold,nms_threshold)
            indices = np.array(indices).flatten() 
            
        for i in indices:
            box = bbox[i]
            x,y,w,h = box[0],box[1],box[2],box[3]

            xcoord = (x+(x+w))//2
            ycoord = (y+(y+h))//2

            # Inputs the detected centroid to the LimitVal Function to prevent indexing error.
            xcoord = LimitVal(xcoord, wT)
            ycoord = LimitVal(ycoord, hT)

            object_depthmap_val = monocular_depth_val[int(ycoord),int(xcoord)]                                                 # Retrieves the depth value of the detected Surrounding Object from the generated MDE feed.
            
            cv2.circle(monocular_depth_val,(int(xcoord),int(ycoord)), 3, (255,0,255), -1)                                      # Draws a circle on the center of the object on the MDE feed.
            cv2.putText(img,str(round(object_depthmap_val,5)), (x,y-20),cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,0), 2)
           
            output_face = RatioProportionCalculator(object_depthmap_val,reference_distance,reference_point)                    # Performs Ratio and Proprtion Calculation on the distance of the Target Object and detected Surrounding Object. 
            safety = SafetyLevel(output_face)
            #cv2.putText(img,"Distance Safety Level: " + f'{safety[0]}', (x,y-40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,255),2)
            
            #Displaying of necessary results on to the original feed.
            cv2.rectangle(img,(x,y),(x+w,y+h),(safety[1]),2)
            cv2.putText(img,f'{class_names[class_ids[i]].upper()}- '+ str(round(output_face,2)), (x,y-5),cv2.FONT_HERSHEY_SIMPLEX, 0.5,(safety[1]), 2)
            cv2.circle(img,(int(xcoord),int(ycoord)), 3, (safety[1]), -1)
   
    # When the Target Object is not present the following text is displayed. 
    else:
        cv2.putText(img,"Place Target Object within the ROI", (300,640), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,255),2)   