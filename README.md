# Realtime Scene Distance Estimation Using Monocular Depth Estimation 
Significant advancements in the field of robotics engineering and autonomous systems development led to the necessity of precise depth measurement solutions as challenges in obstacle detection, obstacle avoidance, and autonomous navigation are becoming increasingly relevant. Conventionally, in measuring depth, distance sensors, 3D scanners, LIDARs, and stereo cameras are used; however, consequent to their popularity is their respective expense. With the popularity of mobile robotic applications, preference for low-form factor and low-cost solutions led to the interest in developing monocular solutions for depth estimation. The conventional depth estimation solution for real-time applications involves a Deep Learning-based approach to measuring distance by using trained models to generate disparity maps from a single camera feed. 

**The challenge in monocular depth solutions is their reliability in various precision-based applications.** Results of MDE models are often represented as normalized values rather than actualized measurement values, which limit interpretations and applications without an accompaniment of intricate control systems such as a fuzzy control system or PID controller.

**This repository contains the source code of the method of actualizing generated depth map values for static and dynamic scenario applications.** On top of using an MDE model, the proposed method involves relating physical optic concepts and YOLO object detection in calculating actual distance information. Accordingly, the established method was applied to road obstacle detection.

# Monocular Depth Estimation Model 

<img align="left" width = 820 src ="https://github.com/LanzDeGuzman/Scene-Distance-Estimation-Using-Monocular-Depth-Estimation/assets/97860488/8fd5e9a3-7107-4cde-a71b-4bd25ba752db">
                                       
Throughout this repository **MiDaS - MDE models trained by Ranftl et al. were used.** Compared to various MDE models available, MiDaS' approach in training a model by mixing datasets to cover diverse environments provided an effective and robust MDE model for multiple applications.




# Actualizing Method

**The novelty of this approach is** the ingenuous use of the bounding box output of the YOLO object detection, precisely the bounding box height, the computable detection centroid, and the lens optic formula, for continuous computation of the target object's distance. Since the generated depth map of MiDaS is presented in normalized values, the output of this equation, via lens optic equation, and its location via centroid computation, is then used as a ground reference value for the remainder of the depth map that is adequately related through inverse proportion.

<p align="center">
  <img width="700" src="https://github.com/LanzDeGuzman/Scene-Distance-Estimation-Using-Monocular-Depth-Estimation/assets/97860488/c7c3ce1b-29a2-46dd-ac71-5c17b9092d6b"]>
</p>

### Physical Concepts Used 

<p align="center">
  <img width="700" src="https://github.com/LanzDeGuzman/Scene-Distance-Estimation-Using-Monocular-Depth-Estimation/assets/97860488/c07d8cad-94fc-4b89-aae6-06a4cc3cf54a"]>
</p>
In order to actualize depth map values into measurement quantities such as the SI units, physical relationships were inferred using the thin lens diagram together with ground
truths from the camera's information and a known object's pixel height. Given this formulaic constraint, the actualizing approach is limited to scenarios where a target object with known physical height measurement is present within a video feed.

### Inferred Equations

<p align="center">
  <img width= '700' src="https://github.com/LanzDeGuzman/Scene-Distance-Estimation-Using-Monocular-Depth-Estimation/assets/97860488/35f44bbb-4724-441a-a71a-17998a7a85d6"]>
</p>

From the thin lens model, the following equations are drawn. 

To relate everything 

