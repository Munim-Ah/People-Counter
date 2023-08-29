import numpy as np
import cv2
import time
import imutils
import blinkt
#blinkt.set_clear_on_exit()

avg = None
video = cv2.VideoCapture(0)
xvalues = list()
motion = list()
count_entered = 0
count_left = 0
empty_places = 4
quantity = 4
rpixel=0
gpixel=0
j=0
initial_state = True
complete = False

def find_majority(k):
    myMap = {}
    maximum = ('', 0)  # (occurring element, occurrences)
    for n in k:
        if n in myMap:
            myMap[n] += 1
        else:
            myMap[n] = 1
        # Keep track of maximum on the go
        if myMap[n] > maximum[1]: maximum = (n, myMap[n])

    return maximum
    
while 1:
    if(initial_state):
        for i in range(blinkt.NUM_PIXELS):
          blinkt.set_pixel(i,0,255,0)
          blinkt.show()
        initial_state = False  

    if j == 30:
        peopleInside = count_entered - count_left
        j=0
        if(peopleInside > 0 and peopleInside <= quantity):
           for i in range(peopleInside*2):
               blinkt.set_pixel(i,255,0,0)
               blinkt.show()
           i = peopleInside*2
           while (i < blinkt.NUM_PIXELS):
               blinkt.set_pixel(i,0,255,0)
               blinkt.show()
               i+=1
        else: initial_state = True
    j+=1
    ret, frame = video.read()
    flag = True
    text = ""
    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    if avg is None:
        print ("[INFO] starting background model...")
        avg = gray.copy().astype("float")
        continue
    cv2.accumulateWeighted(gray, avg, 0.5)
    frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))
    thresh = cv2.threshold(frameDelta, 5, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    for c in cnts:
        if cv2.contourArea(c) < 5000:
            continue
        (x, y, w, h) = cv2.boundingRect(c)
        xvalues.append(x)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        flag = False

    no_x = len(xvalues)

    if (no_x > 2):
        difference = xvalues[no_x - 1] - xvalues[no_x - 2]
        if (difference > 0):
            motion.append(1)
        else:
            motion.append(0)

    if flag is True:
        if (no_x > 5):
            val, times = find_majority(motion)
            if val == 1 and times >= 15:
                if empty_places != 0: 
                   count_entered += 1
                   empty_places -= 1
                else:
                    for i in range(blinkt.NUM_PIXELS):
                      blinkt.set_pixel(i,255,0,0)
                      blinkt.show()
            else:
                if(count_entered > count_left):
                   count_left += 1
                   empty_places += 1
        xvalues = list()
        motion = list()  
          
    cv2.line(frame, (260, 0), (260, 480), (0, 255, 0), 2)
    cv2.line(frame, (420, 0), (420, 480), (255, 0,255), 2)
    cv2.putText(frame, "Number of people Entered: {}".format(count_entered), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, ( 255, 0, 0), 3)
    cv2.putText(frame, "Number of people Left: {}".format(count_left), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
    cv2.putText(frame, "Room status: {}".format(empty_places), (10, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    cv2.imshow("Frame", frame)
    #cv2.imshow("Gray", gray)
    #cv2.imshow("FrameDelta", frameDelta)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    
video.release()
cv2.destroyAllWindows()
