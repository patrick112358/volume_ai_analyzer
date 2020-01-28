import cv2

cap = cv2.VideoCapture("rtsp://admin:Uniview@123@193.227.182.206/media/video1")
if (cap.isOpened() == False):
    print("Unable to read camera feed")

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

out = cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc('X','2','6','4'), 5, (frame_width,frame_height))


while(True):
    ret, frame = cap.read()
    if ret == True:
            cv2.imshow("feed",frame)
            out.write(frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    else:
        break


cap.release()
out.release()
cv2.destroyAllWindows()
print ("Done")