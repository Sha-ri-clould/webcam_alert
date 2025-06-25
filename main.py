import cv2
import time
import glob
import os
from emailing import send_email
from threading import Thread

video = cv2.VideoCapture(0)
time.sleep(0.05)
first_frame = None
status_list =[]
count = 1

def clean_folder():
    images= glob.glob("images/*.png")
    for img in images:
        os.remove(img)
    pass


while True:
    status = 0
    check, frame = video.read()

    if check:
        # Image pre-processing
        grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur_frame = cv2.GaussianBlur(grey_frame, (3, 3), 0)

        #set reference frame
        if first_frame is None:
            first_frame = blur_frame

        # frame difference to detect motion
        delta_frame = cv2.absdiff(first_frame, blur_frame)
        thresh_frame = cv2.threshold(delta_frame, 60,255, cv2.THRESH_BINARY)[1]
        dilate_frame = cv2.dilate(thresh_frame, None, iterations=2)

        contours, check = cv2.findContours(dilate_frame, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            if cv2.contourArea(contour) < 5000:
                continue
            x,y,w,h = cv2.boundingRect(contour)
            rectangle = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
            if rectangle.any() :
                status= 1 # object entered
                cv2.imwrite(f"images/frame{count}.png", frame)
                count += 1
                all_img = glob.glob("images/frame*.png")
                index = int(len(all_img)/2)
                main_image = all_img[index]

        cv2.imshow('Live frame', frame)
        status_list.append(status)
        status_list= status_list[-2:]
        print(status_list)
        if status_list[0]==1 and status_list[1]==0:
            email1_thread = Thread(target=send_email, args=(main_image,))
            email1_thread.deamon = True
            clean_thread = Thread(target=clean_folder)
            clean_thread.daemon = True

            email1_thread.start()


        key = cv2.waitKey(10)
        if key == ord('q'):
            break
    else:
        print("Camera not available")
        break

video.release()
clean_thread.start()
cv2.destroyAllWindows()


