# Realtime Scene Distance Estimation Using Monocular Depth Estimation 
Significant advancements in the field of robotics engineering and autonomous systems development led to the necessity of precise depth measurement solutions as challenges in obstacle detection, obstacle avoidance, and autonomous navigation are becoming increasingly relevant. Conventionally, in measuring depth, distance sensors, 3D scanners, LIDARs, and stereo cameras are used; however, consequent to their popularity is their respective expense. With the popularity of mobile robotic applications, the preference for low-form factor and low-cost solutions led to the interest in developing monocular solutions for depth estimation. The conventional depth estimation solution for real-time applications involves a Deep Learning-based approach to measuring distance by using trained models to generate disparity maps from a single camera feed. 

**The challenge in monocular depth solutions is their reliability in various precision-based applications.** Results of MDE models are often represented as normalized values rather than actualized measurement values, which limit interpretations and applications without an accompaniment of intricate control systems such as a fuzzy control system or PID controller.

**This repository contains the source code of the method of actualizing generated depth map values for static and dynamic scenario applications.** On top of using an MDE model, the proposed method involves relating physical optic concepts and YOLO object detection in calculating actual distance information. Accordingly, the established method was applied to road obstacle detection.

# Monocular Depth Estimation Model 
<img align="left" width = 820 src ="https://github.com/LanzDeGuzman/Scene-Distance-Estimation-Using-Monocular-Depth-Estimation/assets/97860488/af288b93-84ca-445a-be73-d5bd5e1725c5">
                                       
Throughout this repository **MiDaS - MDE models trained by Ranftl et al. were used.** Compared to various MDE models available, MiDaS' approach in training a model by mixing datasets to cover diverse environments provided an effective and robust MDE model for multiple applications.

Read More @ https://github.com/isl-org/MiDaS.

# Actualizing Method and Physical Concepts Used
### Thin Lens Diagram
<p align="center">
  <img width="700" src="https://github.com/LanzDeGuzman/Scene-Distance-Estimation-Using-Monocular-Depth-Estimation/assets/97860488/dee5a119-14d4-49c6-a831-8455648921c6">
</p>
In order to actualize depth map values into measurement quantities such as the SI units, physical relationships were inferred using the thin lens diagram together with ground
truths from the camera's information and a known object's pixel height. Given this formulaic constraint, the actualizing approach is limited to scenarios where a target object with known physical height measurement is present within a video feed.

### Inferred Equations

<p align="center">
  <img width= '700' src="https://github.com/LanzDeGuzman/Scene-Distance-Estimation-Using-Monocular-Depth-Estimation/assets/97860488/7bf8bf9a-d150-4455-8fc6-1d42bc46bfe3">
</p>

From the thin lens model, the following equations are drawn. The proportion between the sensor height (measured in millimeters) and the object's pixel height, as observed in the image feed, is utilized to calculate the object's height on the sensor in millimeters. By dividing this proportion by the overall image resolution height (measured in pixels), the object's height in millimeters on the physical camera sensor is essentially inferred.

In summary, this equation allows us to linearize the observable data to estimate the physical size of an object on the camera sensor and correspondingly use it to accommodate the thin lens diagram. These variables that comprise the thin lens diagram are algebraically re-arranged to compute an object's distance to the camera.  

### Limitations
Given the formulaic constraint, the actualizing method is limited to the following- Accuracy of the camera's information, Scenarios where a **Target Object**, an Object with known physical height measurement, is present within the camera's feed, and that the Target Object is always perpendicular to the camera.

### YOLO Object Detection 
<p align="center">
 <img width= '700' src= "https://github.com/LanzDeGuzman/Scene-Distance-Estimation-Using-Monocular-Depth-Estimation/assets/97860488/59e98a7f-88b6-4612-be2d-c53b34eeecfb">
</p>

To continuously compute the object's actualized distance, **YOLO Object detection** was used. YOLO's bounding box outputs were extensively used to determine the Target Object's pixel height (h) and accompany the actualization of values through the lens optic equation.

Moreover, YOLO allowed the classification of the Target Object and other Surrounding Objects, and from its bounding box centroids, the Target and Surrounding Object's distances based on the MDE-generated depth map are adequately referenced.
<p align="center">
  <img width= '700' src= https://github.com/LanzDeGuzman/Scene-Distance-Estimation-Using-Monocular-Depth-Estimation/assets/97860488/9c769079-901e-4be7-bd59-4f6cd1807707 >
  <img width= '700' src= https://github.com/LanzDeGuzman/Scene-Distance-Estimation-Using-Monocular-Depth-Estimation/assets/97860488/6943aef8-922f-4f3f-bfa4-1899d574f7fe >
</p>
### MiDaS - YOLO
Since the target object's actualized distance, position in feed, and corresponding depth map value from the MiDaS model are calculated. These values are then related to the rest of the depth map via inverse proportion to calculate the surrounding objects' actualized distances. 

Upon testing, the relationship of the generated depth map was observed to be inversely proportional. Whereby within the normalized scale of 0 - 1, closer values to 0 represent that an object is far and vice versa and whose relationship is represented by the equation: 

<p align="center">
 <img width= '700' src= https://github.com/LanzDeGuzman/Scene-Distance-Estimation-Using-Monocular-Depth-Estimation/assets/97860488/c1ab69ba-3f40-49f7-829d-2fdeaab5c959 >
</p>

The Reference Distance is the Target Object's calculated distance using the equation drawn from the thin lens model, Reference MiDaS Value is the Target Object centroid's MiDaS value, and the Surrounding Object MiDaS Value is/are the Surrounding Object/s centroid's MiDaS value.

### Process Flow
**The novelty of this approach is** the ingenuous use of the bounding box output of the YOLO object detection, precisely the bounding box height, the computable detection centroid, and the lens optic formula, for continuous computation of the target object's distance. Since the generated depth map of MiDaS is presented in normalized values, the output of this equation, via lens optic equation, and its location via centroid computation, is then used as a ground reference value for the remainder of the depth map that is adequately related through inverse proportion.

<p align="center">
  <img width="700" src="https://github.com/LanzDeGuzman/Scene-Distance-Estimation-Using-Monocular-Depth-Estimation/assets/97860488/9a00bd93-4143-4dcc-baf2-dabcd755da5c">
</p>

# Camera Set Up, Data Sets, & Models Used

### Camera Set Up and Information Used

<p align="center">
  <img width="700" src= https://github.com/LanzDeGuzman/Scene-Distance-Estimation-Using-Monocular-Depth-Estimation/assets/97860488/e2f29dbc-77c2-44ba-9fdb-7156b4cd9e62>
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
## Accuracy Testing 

Household items such as cups and bottles were used throughout the accuracy testing period. From the test samples below, a cup was the target object, and the bottles were the surrounding objects. Results from the test showed an average of **98% accuracy** in detecting the target object and **87% accuracy** in detecting the target objects.  

### Position 1
![1](https://github.com/LanzDeGuzman/Scene-Distance-Estimation-Using-Monocular-Depth-Estimation/assets/97860488/96a99c8e-c9dc-49a0-9ba0-8874c6cc6b4b)

### Position 2
![2](https://github.com/LanzDeGuzman/Scene-Distance-Estimation-Using-Monocular-Depth-Estimation/assets/97860488/0c3f5106-8ace-409f-8deb-a0f9e4e41943)

### Position 3
![3](https://github.com/LanzDeGuzman/Scene-Distance-Estimation-Using-Monocular-Depth-Estimation/assets/97860488/01122895-4c95-43da-a9e9-eed96ef4a3f5)

### Position 4 (Three Items)
![4](https://github.com/LanzDeGuzman/Scene-Distance-Estimation-Using-Monocular-Depth-Estimation/assets/97860488/9bf702c9-6569-4dcf-bcc9-337f0f32ddf0)

## Performance Testing 

Throughout the performance testing, the surrounding objects are the road elements, while the target object is the license plate. Within this test, bounding boxes are updated based on their level of potential danger. Whenever a detected object is less than 3000 mm or 3 m, around the length of 2 cars, they are regarded as a potential danger and are represented by changing their bounding boxes to red. Whenever an object is considered safe, its bounding box colors change to green. This scenario showcases the program's performance in city driving conditions.

**Real-Time Road Performance Testing#1 x5 Speed**

https://github.com/LanzDeGuzman/Scene-Distance-Estimation-Using-Monocular-Depth-Estimation/assets/97860488/c90d0ab7-3f7d-4446-b7a7-73dd3cb390b0

**Real-Time Road Performance Testing#2 x5 Speed**

https://github.com/LanzDeGuzman/Scene-Distance-Estimation-Using-Monocular-Depth-Estimation/assets/97860488/6c4d9a49-0c31-459c-b795-567034a29755

**Road Performance Testing Using Pre-Recorded Videos**

https://github.com/LanzDeGuzman/Scene-Distance-Estimation-Using-Monocular-Depth-Estimation/assets/97860488/405baa79-969c-437f-a829-c9b2d74e7543

Actual Processing Speed - https://youtu.be/bOl1fs1QDyg

Because of the dynamic nature of these scenarios, variability is observed when measuring distances. The use of detecting license plates as target objects had pros and cons. These are only applicable when a car is in front; thus, detection and depth retrieval is rarely observed when turning left or right. Accordingly, the test was highly limited by the machine's processing capability. Frame processing is far from usable and must be improved for further studies and real-time applications. Unable to measure the computed and predicted distance estimation accuracy, the test shows promise and proof of the concept of using MDE in obstacle detection and is a potential tool for autonomous navigation.

# Future Work
1. Perform further experiments to validate the proposed method in dynamic scenarios.
2. Run the program alongside a different distance-measuring device, such as a LIDAR or stereo camera, and compare results accordingly.
3. Integrate 3D object detection with 3D bounding boxes to address inaccuracy in non-perpendicular detection of the target object. 
4. Train models using customized datasets to adequately detect country-specific vehicles.
5. Use newer MDE models and Detection architecture. 

# Using The Source Code

The Following dependencies must be installed:
  1. Python
  2. OpenCV (Building OpenCV into the computer's CUDA cores is suggested for better performance)
  3. Numpy
  4. yaml

To run the program locally, follow the following steps:
  1. Clone this Repository to your computer either by using Git clone or the repository's download tab.
  2. Open the Repository into an IDE of your choice.
  3. Open the config.yml file and update the models' file paths accordingly.
  4. From the config.yml file, update the camera's information - physical and pixel sensor height and focal length. Cameras have different specifications depending on the model, and inputting the wrong information will yield inaccuracy in using the program. Most cameras' information and specifications are available online. 
  5. For the Road Obstacle Application, update the **real_object_height** to the standard license plate height in mm in your area/country. For most applications or applications that use the MS COCO detection model, choose a target object present within the names file and correspondingly update its physical height in mm beside **real_object_height**.

      For Road Obstacle Application License Plates as Target Object
      ```Python
      target_object:
        target: Vehicle registration plate
        real_object_height: 160  #object height in mm
      ```
      For Other Applications using MS COCO and Cup as Target Object
       ```Python
      target_object:
        target: cup
        real_object_height: 95  #object height in mm
      ```
  7. Open the config.py and make sure that the target and surrounding object's YOLO files - name, cfg, and weight files are consistently initialized.

     For Road Application config.py must look like this 
      ```Python
      class_names = []
      with open(vehicle_names, 'rt') as f:
          class_names = f.read().rstrip('\n').split('\n')
      
      target_names = []
      with open(licenseplate_names, 'rt') as f:
          target_names = f.read().rstrip('\n').split('\n') 
      
      # Initalizes the Surrounding Objects' YOLO CFG and Weights File to be used throughout the script. 
      yolo_model_cfg = vehicle_yolo_cfg                                                                 
      yolo_model_weight = vehicle_yolo_weights
      yolo_model = cv2.dnn.readNetFromDarknet(yolo_model_cfg,yolo_model_weight)
      yolo_model.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
      yolo_model.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
      
      # Initializes the Target Object's YOLO CFG and Weights File to be used throughout the script. 
      yolo_target_model_cfg = licenseplate_yolo_cfg
      yolo_target_model_weight = licenseplate_yolo_weights
      yolo_target_model = cv2.dnn.readNetFromDarknet(yolo_target_model_cfg,yolo_target_model_weight)
      yolo_target_model.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
      yolo_target_model.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
      ```
  8. Run the code by executing the Main.py file.

## Running the program with different YOLO models
To run the code using different YOLO models, update the config.yml file by adding variables with corresponding file paths. 

Sample:
``` Python
model_path:
  model_names: filepath\model.names
  model_yolo_cfg: filepath\model.cfg
  model_yolo_weights: filepath\model.weights
```
From the config.py create additional lines for file initialization consistent with the config.yml file

Sample:
```Python 
model_names = config["model_path"]["model_names"]
model_yolo_cfg = config["model_path"]["model_yolo_cfg"]
model_yolo_weights = config["model_path"]["model_yolo_weights"]
```
Correspondingly update class names and initialization lines consistent with the specified model.



