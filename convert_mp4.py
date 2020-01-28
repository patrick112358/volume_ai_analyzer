import cv2

src_dir = "2.mp4"
dst_dir = "worked.avi"

video_cap = cv2.VideoCapture(src_dir)
#fps = video_cap.get(cv2.cv.CV_CAP_PROP_FPS)
#cv2.cv會出現錯誤：AttributeError: 'module' object has no attribute 'cv'
#在Opencv3.2中cv2.CV_CAP_PROP_FPS需要改為cv2.CAP_PROP_FPS
#也就是都要去掉CV_字眼
fps = video_cap.get(cv2.CAP_PROP_FPS)
size = (int(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH)),   
        int(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))  
#video_writer = cv2.VideoWriter_fourcc(dst_dir, cv2.FOURCC('M', 'J', 'P', 'G'), fps, size) 
video_writer = cv2.VideoWriter(dst_dir, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), fps, size) 

success, frame = video_cap.read()
while success:
    video_writer.write(frame)
    success, frame = video_cap.read()