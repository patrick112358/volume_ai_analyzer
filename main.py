#IMPORTS
from Classifier import load_detector,detect
from Processing import cleanImage,getRealVolume, getClassName
from lookups import ClassType, DetectionSpeed, VehicleType, ModelType
import cv2

model_type = ModelType.YOLO
#GLOBALS
threshold=50
#MAIN
resnet_model = "./models/resnet50_coco_best_v2.0.1.h5"
yolo_tiny_model = "./models/yolo-tiny.h5"
yolo_model = "./models/yolo.h5"

if model_type == ModelType.RES_NET:
    model_to_use = resnet_model
elif model_type == ModelType.YOLO:
    model_to_use = yolo_model
elif model_type == ModelType.YOLO_TINY:
    model_to_use = yolo_tiny_model

detector=load_detector(model_type,model_to_use , DetectionSpeed.NORMAL.value)
vidcap = cv2.VideoCapture('3.avi')
success,image = vidcap.read()
r =(542, 112, 825, 889)
# print (r)
# exit()
reference = image[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
height, width, channels = reference.shape
count = 0
volume = None
while success:
    try:
        image = image[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
        # exit()
        if count%24==0:
            height_to_use = int(height/4.5)
            detection=detect(image,detector,threshold)
            point_1 = (0,height_to_use)
            point_2 = (width, height_to_use)
            cv2.line(image, point_1, point_2, (0,0,255), 4)
            vehicle_type = None 
            print(detection)
            if detection:
                vehicle_type = detection.get("name")
                bounding_boxes = detection.get("box_points")
                # cv2.line(image, (bounding_boxes[0] - 10, bounding_boxes[1] -10 ), (bounding_boxes[0] -5 ,bounding_boxes[3] -5 ), (0,255,0), 4)
                midpoint = (bounding_boxes[0], (bounding_boxes[1] + bounding_boxes[3]) /2)
                # print(midpoint)
                print(abs(midpoint[1] - height_to_use))
                if  abs(midpoint[1] - height_to_use) < 80:
                    print("NOW")
                    cv2.rectangle(image, (bounding_boxes[0], bounding_boxes[1]), (bounding_boxes[2], bounding_boxes[3]), (255,0,0), 2)
                    rect, cont_sorted,outputImage=cleanImage(image, reference, bounding_boxes, filter = 24)
                    volume,realwidth,realheight,realdepth=getRealVolume(image, rect,outputImage, debug = True, cont_sorted = cont_sorted)
                    print("volume = " + str(volume))
                    class_name = (getClassName(volume, vehicle_type))
                    bounding=detection['box_points']
                    vehicle_type = None
                    cv2.putText(image, str(round(volume,2))+ str("m3"), (bounding[0], bounding[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,0,0), 2)
                else:
                    print("NOT NOW")
                # cv2.rectangle(image, (bounding_boxes[0], bounding_boxes[1]), (bounding_boxes[2], bounding_boxes[3]), (255,0,0), 2)
                # rect, cont_sorted,outputImage=cleanImage(image, reference, bounding_boxes, filter = 24)
                # volume,realwidth,realheight,realdepth=getRealVolume(image, rect,outputImage, debug = True, cont_sorted = cont_sorted)
                # class_name = (getClassName(volume, vehicle_type))
                # bounding=detection['box_points']
                # vehicle_type = None
                # cv2.putText(image, str(round(volume,2)), (bounding[0], bounding[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,0,0), 2)

            cv2.imshow("output",image)

            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        vehicle_type = None
        success,image = vidcap.read()
        #image[:,1000:]=0
        count += 1
    except Exception as e:
        print(str(e))
        pass




