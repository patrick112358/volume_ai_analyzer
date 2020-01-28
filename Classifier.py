from imageai.Detection import ObjectDetection
from lookups import ModelType


def load_detector(model_type , model_path,detection_speed="normal"):
    detector = ObjectDetection()
    if model_type == ModelType.YOLO:
        detector.setModelTypeAsYOLOv3()
    elif model_type == ModelType.YOLO_TINY:
        detector.setModelTypeAsTinyYOLOv3()
    elif model_type == ModelType.RES_NET:
        detector.setModelTypeAsRetinaNet()

    detector.setModelPath(model_path)
    detector.loadModel(detection_speed=detection_speed)
    return detector

def detect(image_array,detector,threshold):
    detection = None
    custom_objects = detector.CustomObjects(car=True, motorcycle=True, bicycle = True, bus = True, truck = True)
    _, detections = detector.detectCustomObjectsFromImage(custom_objects=custom_objects, input_type = "array", input_image=image_array, output_type = "array")
    acceptable_detections=[]
    for d in detections:
        if d.get("percentage_probability") > threshold:
            acceptable_detections.append(d)
    area_list = list()

    if len(acceptable_detections) > 0:
        for detection in acceptable_detections:
            boundingbox = (detection.get("box_points"))
            area = int(boundingbox[3]) * int(boundingbox[2])
            area_list.append(area)
        detection = detections[area_list.index(max(area_list))]

    else:
        detection=None
    return detection
