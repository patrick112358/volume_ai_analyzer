import numpy as np
import copy
import cv2
from lookups import VehicleType, ClassType, CLASS_A_RANGE, CLASS_B_RANGE, CLASS_C_RANGE, CLASS_D_RANGE
from skimage.measure import compare_ssim
import imutils


def getClassName(volume, vehicleType):
    # if vehicleType:
    #     if vehicleType == VehicleType.MOTORCYCLE.value or vehicleType == VehicleType.BICYCLE.value:
    #         return ClassType.CLASS_A.value
    #     if vehicleType == VehicleType.TRUCK.value:
    #         return ClassType.CLASS_D.value
    
    volume = round(volume)
    if volume in range(int(CLASS_A_RANGE.FROM.value), int(CLASS_A_RANGE.TO.value)):
        return ClassType.CLASS_A.value
    elif volume in range(int(CLASS_B_RANGE.FROM.value), int(CLASS_B_RANGE.TO.value)):
        return ClassType.CLASS_B.value
    elif volume in range(int(CLASS_C_RANGE.FROM.value), int(CLASS_C_RANGE.TO.value)):
        return ClassType.CLASS_C.value
    elif volume in range(int(CLASS_D_RANGE.FROM.value), int(CLASS_D_RANGE.TO.value)):
        return ClassType.CLASS_D.value
    

def cleanImage(image_array, image_reference, detection, filter =4):
    r = detection
    crop_img = image_array[int(r[1]) : int(r[3]), int(r[0]):int(r[2])]
    ref_crop = image_reference[int(r[1]) : int(r[3]), int(r[0]): int(r[2])]
    # grayA = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    # grayB = cv2.cvtColor(ref_crop, cv2.COLOR_BGR2GRAY)    
    # (score, diff) = compare_ssim(grayA, grayB, full=True)
    # diff = (diff * 255).astype("uint8")
    # print("SSIM: {}".format(score))
    # thresh = cv2.threshold(diff, 0, 255,
	# cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    # cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
    #     cv2.CHAIN_APPROX_SIMPLE)
    # cnts = imutils.grab_contours(cnts)
    # cv2.imshow("Thresh", thresh)
    diff=copy.deepcopy(crop_img)
    for c in range(0,3):
        for y in range(0,len(crop_img),filter):
            for x in range(0,len(crop_img[0]),filter):
                if np.sum(crop_img[y:y+filter,x:x+filter,c])>0.9*np.sum(ref_crop[y:y+filter,x:x+filter,c]) and np.sum(crop_img[y:y+filter,x:x+filter,c])<1.1*np.sum(ref_crop[y:y+filter,x:x+filter,c]):
                    diff[y:y+filter,x:x+filter,c]=0

                else:
                    diff[y:y+filter,x:x+filter,c]=254
    end_dif = np.bitwise_or(diff[:,:,0],np.bitwise_or(diff[:,:,1],diff[:,:,2]))

    outputImage = cv2.copyMakeBorder(end_dif,3,3,3,3,cv2.BORDER_CONSTANT,value=0)
    # erode and dilate

    kernel = np.ones((5,5), np.uint8)
    outputImage=cv2.erode(outputImage,kernel,iterations=5)
    outputImage=cv2.dilate(outputImage,kernel,iterations=5)
    # outputImage1=cv2.erode(thresh,kernel,iterations=5)
    # outputImage1=cv2.dilate(thresh,kernel,iterations=5)
    # cv2.imshow("threshold_",outputImage)
    # # cv2.imshow("output1",thresh)
    contours, _  = cv2.findContours(outputImage.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cont_sorted = sorted(contours, key = lambda x: cv2.contourArea(x), reverse= True)
    if cont_sorted:
        area=cv2.contourArea(cont_sorted[0])
        rect = cv2.boundingRect(cont_sorted[0])
        return rect, cont_sorted,outputImage

def getRealVolume(image_array, rect,outputImage, debug = False, cont_sorted = None):
    width=min(rect[3],rect[2])
    height=max(rect[3],rect[2])
    realwidth=(10500*width*8.46667/(5*len(image_array[0])))/1000.0
    realwidth = realwidth * 0.8
    print("read width = " + str(realwidth))
    realheight=(10500*height*6.35/(5*len(image_array)))/1000.0
    realheight = realheight * 0.7063
    print("real height = " + str(realheight))
    realdepth = (2 + realheight/23.0) * 1.42
    print("real depth = " + str(realdepth))
    return (realwidth*realheight*realdepth),realwidth,realheight,realdepth
    