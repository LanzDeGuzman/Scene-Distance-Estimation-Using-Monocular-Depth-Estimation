# Contains functions regarding Lens Optic Calculation, Ratio and Proportion Calutation, and other auxilairy functions invovlving an object's distance safety level and value limiter.

from config import sensor_height_mm, sensor_height_px, focal_length, real_object_height

# Formulation of the lens Optic Calculation based on the Thin Lens Model.
def LensOpticCalculator (px_height):
    computed_object_distance = (real_object_height*focal_length*sensor_height_px)/(px_height*sensor_height_mm)                                
    return computed_object_distance

# Performs surrounding object distance estimation calculation using inverse proportion and referencing target object values
def RatioProportionCalculator (object_depthmap_Val,reference_distance,reference_point):
    computed_distance = ((reference_distance*reference_point)/object_depthmap_Val)                               
    return (computed_distance)

# Determines distance safety of an object and changes detections boundibg box to green when safe and red when a potential danger
def SafetyLevel(distance):
    if distance > 3000: 
        dist = ("Safe")                                                                                                        # Object beyond 3000 mm or 3m is considered to be safe
        bbox_color = (0,153,76)
    else:
        dist = ("Potential Danger")
        bbox_color = (153,0,0)
    return dist,bbox_color

## Detection Coordinate Value Limiter -This prevents errors when indexing values outside of feed when detection centroid is not within the bounds of the video feed. 
def LimitVal (coord,val):
    if coord < val:
        coord = coord
    else:
        coord = val - 1 
    return coord
