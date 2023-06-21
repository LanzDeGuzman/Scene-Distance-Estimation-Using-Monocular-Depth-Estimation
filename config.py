# Contains the initialization of necessary variables, models, and etc comming from the config.yml file

import yaml
import cv2

# Load the YAML config file
with open("config.yml", "r") as f:
    config = yaml.safe_load(f)

coco_names = config["model_path"]["coco_names"]
vehicle_names = config["model_path"]["vehicle_names"]
licenseplate_names = config["model_path"]["licenseplate_names"]
coco_yolo_cfg = config["model_path"]["coco_yolo_cfg"]
coco_yolo_weights = config["model_path"]["coco_yolo_weights"]
vehicle_yolo_cfg = config["model_path"]["vehicle_yolo_cfg"]
vehicle_yolo_weights = config["model_path"]["vehicle_yolo_weights"]
licenseplate_yolo_cfg = config["model_path"]["licenseplate_yolo_cfg"]
licenseplate_yolo_weights = config["model_path"]["licenseplate_yolo_weights"]
MDE_model_path = config["model_path"]["MDE_model_path"]

sensor_height_mm = config["camera_information"]["sensor_height_mm"] 
sensor_height_px = config["camera_information"]["sensor_height_px"] 
focal_length = config["camera_information"]["focal_length"]

real_object_height = config["target_object"]["real_object_height"]
target = config["target_object"]["target"]

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

# Initializes the MDE Model to be used throughout the script.
mde_model = cv2.dnn.readNet(MDE_model_path)
mde_model.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
mde_model.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

# Checkpoint of sucessfully initializing the necessary models.
print('Yolo Initialization Successful')
print('Depth Estimation Model Initialization Successful')

