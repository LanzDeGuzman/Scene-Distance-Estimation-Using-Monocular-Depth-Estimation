# Realtime Scene Distance Estimation Using Monocular Depth Estimation 
Significant advancements in the field of robotics engineering and autonomous systems development led to the necessity of precise depth measurement solutions as challenges in obstacle detection, obstacle avoidance, and autonomous navigation are becoming increasingly relevant. Conventionally, in measuring depth, distance sensors, 3D scanners, LIDARs, and stereo cameras are used; however, consequent to their popularity is their respective expense. With the popularity of mobile robotic applications, preference for low-form factor and low-cost solutions led to the interest in developing monocular solutions for depth estimation. The conventional depth estimation solution for real-time applications involves a Deep Learning-based approach to measuring distance by using trained models to generate disparity maps from a single camera feed. 

**The challenge in monocular depth solutions is their reliability in various precision-based applications.** Results of MDE models are often represented as normalized values rather than actualized measurement values, which limit interpretations and applications without an accompaniment of intricate control systems such as a fuzzy control system or PID controller.

**This repository contains the source code of the method of actualizing generated depth map values for static and dynamic scenario applications.** On top of using an MDE model, the proposed method involves relating physical optic concepts and YOLO object detection in calculating actual distance information. Accordingly, the established method was applied to road obstacle detection.

# Monocular Depth Estimation Model 

<img align="left" width = 820 src ="https://github.com/LanzDeGuzman/Scene-Distance-Estimation-Using-Monocular-Depth-Estimation/assets/97860488/8fd5e9a3-7107-4cde-a71b-4bd25ba752db">
                                       
Throughout this repository **MiDaS - MDE models trained by Ranftl et al. were used.** Compared to various MDE models available, MiDaS' approach in training a model by mixing datasets to cover diverse environments provided an effective and robust MDE model for multiple applications.

Read More @ https://github.com/isl-org/MiDaS.

# Actualizing Method and Physical Concepts Used
### Thin Lens Diagram
<p align="center">
  <img width="700" src="https://github.com/LanzDeGuzman/Scene-Distance-Estimation-Using-Monocular-Depth-Estimation/assets/97860488/c07d8cad-94fc-4b89-aae6-06a4cc3cf54a">
</p>
In order to actualize depth map values into measurement quantities such as the SI units, physical relationships were inferred using the thin lens diagram together with ground
truths from the camera's information and a known object's pixel height. Given this formulaic constraint, the actualizing approach is limited to scenarios where a target object with known physical height measurement is present within a video feed.

### Inferred Equations

<p align="center">
  <img width= '700' src="https://github.com/LanzDeGuzman/Scene-Distance-Estimation-Using-Monocular-Depth-Estimation/assets/97860488/35f44bbb-4724-441a-a71a-17998a7a85d6">
</p>

From the thin lens model, the following equations are drawn. The proportion between the sensor height (measured in millimeters) and the object's pixel height, as observed in the image feed, is utilized to calculate the object's height on the sensor in millimeters. By dividing this proportion by the overall image resolution height (measured in pixels), the object's height in millimeters on the physical camera sensor is essentially inferred.

In summary, this equation allows us to linearize the observable data to estimate the physical size of an object on the camera sensor and correspondingly use it to accommodate the thin lens diagram. These variables that comprise the thin lens diagram are algebraically re-arranged to compute an object's distance to the camera.  

### Limitations
Given the formulaic constraint the actualizing method is limited to the following- Accuracy of the camera's information, Scenarios where a, **Target Object**, an Object with known physical height measurement is present within the camera's feed, and that the Target Object is always perpendicular to the camera.

### YOLO Object Detection 
<p align="center">
 <img width= '700' src= "https://github.com/LanzDeGuzman/Scene-Distance-Estimation-Using-Monocular-Depth-Estimation/assets/97860488/e9c235c4-d922-4f6a-bffa-866e2a7ad791">
</p>

To continuously compute the object's actualized distance, **YOLO Object detection** was used. YOLO's bounding box outputs were extensively used to determine the Target Object's pixel height (h) and accompany the actualization of values through the lens optic equation.

Moreover, YOLO allowed the classification of the Target Object and other Surrounding Objects, and from its bounding box centroids, the Target and Surrounding Object's distances based on the MDE-generated depth map are adequately referenced.

![image](https://github.com/LanzDeGuzman/Scene-Distance-Estimation-Using-Monocular-Depth-Estimation/assets/97860488/be4148dd-5e4e-40c6-b169-30edeccd7c0b)
![image](https://github.com/LanzDeGuzman/Scene-Distance-Estimation-Using-Monocular-Depth-Estimation/assets/97860488/b60d6460-a5c5-4f01-8a6d-2b2f41967c57)

### MiDaS - YOLO
Since the target object's actualized distance, position in feed, and corresponding depth map value from the MiDaS model are calculated. These values are then related to the rest of the depth map via inverse proportion to calculate the surrounding objects' actualized distances. 

Upon testing, the relationship of the generated depth map was observed to be inversely proportional. Whereby within the normalized scale of 0 - 1, closer values to 1 represent that an object is far and vice versa and whose relationship is represented by the equation: 

<p align="center">
 <img width= '700' src= https://github.com/LanzDeGuzman/Scene-Distance-Estimation-Using-Monocular-Depth-Estimation/assets/97860488/c6c906c0-dab3-46f3-b805-827e3ac6c855 >
</p>

The Reference Distance is the Target Object's calculated distance using the equation drawn from the thin lens model, Reference MiDaS Value is the Target Object centroid's MiDaS value, and the Surrounding Object MiDaS Value is/are the Surrounding Object/s centroid's MiDaS value.

### Process Flow
**The novelty of this approach is** the ingenuous use of the bounding box output of the YOLO object detection, precisely the bounding box height, the computable detection centroid, and the lens optic formula, for continuous computation of the target object's distance. Since the generated depth map of MiDaS is presented in normalized values, the output of this equation, via lens optic equation, and its location via centroid computation, is then used as a ground reference value for the remainder of the depth map that is adequately related through inverse proportion.

<p align="center">
  <img width="700" src="https://github.com/LanzDeGuzman/Scene-Distance-Estimation-Using-Monocular-Depth-Estimation/assets/97860488/c7c3ce1b-29a2-46dd-ac71-5c17b9092d6b">
</p>

# Camera Set Up, Data Sets, & Models Used

### Camera Set Up and Information Used

<p align="center">
  <img width="700" src=https://github.com/LanzDeGuzman/Scene-Distance-Estimation-Using-Monocular-Depth-Estimation/assets/97860488/49f492cd-8db7-4bf2-bf43-3823d1d87870 >
</p>

Throughout the experimentation and testing period, **Logitech's C310**, a single USB camera, was used. Note that the sensor height is multiplied by two due to the pixel resolution being upscaled by the software from 640 (w) x 480 (h) to 1280 (w) x 960 (h). An Apple M1 MacBook Air was used as the primary computing device throughout the testing period.

### Data Set and Models Used
The MDE model that was specifically used was the MiDaS v2.1 Small. The small model variant was favored based on its low computational requirement, which is deemed suitable for real-time applications whilst being able to output an adequate depth map. Correspondingly, throughout the study, various YOLO versions, data sets, and models were used to detect surroundings and **Target Objects: Cups and License Plates**, such as the YOLOv3 MS COCO data set, YOLOv4 Road Obstacle, and YOLOv4 License Plate Detection Data Set.

|     MODEL     |    Repository  Link     |
| ------------- | ------------- |
| MiDaS Models   |  https://github.com/isl-org/MiDaS |
| YOLOv3 MS COCO  Model | https://pjreddie.com/darknet/yolo/ |
| YOLOv4 Road Obstacle | https://github.com/dec880126/Self-driving-with-YOLO |
| YOLOv4 License Plate Detection | https://github.com/GautamKataria/Yolov4-Pytesseract-License-plate-detection-and-reading |

# Testing and Results 
**Accuracy testing** was performed under controlled static environments, and **performance testing** was conducted under uncontrolled environments.   



