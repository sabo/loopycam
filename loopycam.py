import numpy as np
import cv2

from itertools import cycle


# Change these settings. You'll probably need to tweak them for your particular camera.
OUTNAME = 'loop.avi'
BRIGHTNESS = 0.25
CONTRAST = 1
SATURATION = 1
THRESHOLD = 220
ENDTRIGGER = 3
STARTTRIGGER = 5
HSIZE = WSIZE = 2000 # max it out

# '0' here represents the first camera OpenCV detects.
cap = cv2.VideoCapture(0)
cap.set(cv2.cv.CV_CAP_PROP_BRIGHTNESS, BRIGHTNESS)
cap.set(cv2.cv.CV_CAP_PROP_CONTRAST, CONTRAST)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, HSIZE)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, WSIZE)
cap.set(cv2.cv.CV_CAP_PROP_SATURATION, SATURATION)
fourcc = cv2.cv.FOURCC(*"XVID")
out = cv2.VideoWriter(OUTNAME, fourcc, 20.0,
        (int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)),int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))))

# Outframes stores the frames we captures earlier. Cheaper and easier than looping the
# actual recorded movie.
outframes = []

# Started gets set to True when we start recording.
started = False

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    # We convert to grayscale, then apply a threshold function.
    grayframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret, frame2 = cv2.threshold(grayframe,THRESHOLD,255,cv2.THRESH_BINARY)

    # Take the average value of the frame
    average = np.average(frame2)

    # If we've started recording, and the average value is less than the end trigger
    # value, stop recording.
    if started and average < ENDTRIGGER:
        break
    # If we *haven't* started recording and the frame average is greater than our start
    # trigger value, start recording and showing frames.
    if not started and average > STARTTRIGGER:
        cv2.namedWindow('LoopyCam', flags=cv2.WINDOW_NORMAL)
        started = True
    # If the average value is greater than the end trigger, then show the frame, write it
    # to the video, and add it to the looping list.
    if average > ENDTRIGGER:
        cv2.imshow('LoopyCam', frame)
        out.write(frame)
        outframes.append(frame)
    # Wait a millisecond for the user to press 'q', for quit.
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and the video file
out.release()
cap.release()

# Use cycle to make the list into a generator that goes on forever
loopyness = cycle(outframes)
for frame in loopyness:
    # Show the frame
    cv2.imshow('LoopyCam',frame)
    # Wait 50ms (because our movie was recorded at 20fps) between frames.
    if cv2.waitKey(50) & 0xFF == ord('q'):
        break

# Clean up.
cv2.destroyAllWindows()
