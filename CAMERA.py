import cv2
import mediapipe as mp
import numpy as np
from matplotlib import pyplot as plt
import time

# SETARI GENERALE
capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT,720)


#print(str(capture.get(cv2.CAP_PROP_FRAME_WIDTH)))
#print(str(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
# 640 W   X
# 480 H   Y


mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
fingerCoord = [ (8,6), (12,10), (16,14), (20,18) ]
thumbCoordinate= (4,2)



# FUNCTIE DE INVERSAT CAMERA
def mirror_this(image_file, gray_scale=False, with_plot=False) :
    image_rgb = image_file
    image_mirror = np.fliplr( image_rgb )
    if with_plot :
        fig = plt.figure( figsize=(10, 20) )
        ax1 = fig.add_subplot( 2, 2, 1 )
        ax1.axis( "off" )
        ax1.title.set_text( 'Original' )
        ax2 = fig.add_subplot( 2, 2, 2 )
        ax2.axis( "off" )
        ax2.title.set_text( "Mirrored" )
        if not gray_scale :
            ax1.imshow( image_rgb )
            ax2.imshow( image_mirror )
        else :
            ax1.imshow( image_rgb, cmap='gray' )
            ax2.imshow( image_mirror, cmap='gray' )
        return True
    return image_mirror

ACTION_STATUS = "IDLE"
ACTION_STATUS_PREV = "IDLE"

def camera_working():
    global ACTION_STATUS, ACTION_STATUS_PREV, hands, mpDraw, mpHands, thumbCoordinate, capture
    #while True:
    success, img = capture.read()
    results = hands.process(img)
    landmarks = results.multi_hand_landmarks

    if landmarks:
        # recunoastere degete si salvare coordonate
        for handLms in landmarks:

            #mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
            handPoints = []

                # MEMORARE COORDONATE
            for idx, lm in enumerate(handLms.landmark):
                h,w,c = img.shape
                cx, cy = int (lm.x * w), int (lm.y * h)
                handPoints.append((cx,cy))

                # EVIDENTIERE DEGETE
        for i in range(9):
            cv2.circle(img, handPoints[i], 10, (0,255,0), cv2.FILLED)

# fingerCoord = [ (), (12,10), (16,14), (20,18) ]

        # INTERPRETARE ACTIUNI
        #print( handPoints[4][0], handPoints[8][0], handPoints[4][1], handPoints[8][1] )

        thumbX = handPoints[4][0]
        thumbY = handPoints[4][1]
        indexX = handPoints[8][0]
        indexY = handPoints[8][1]

        # FINGERS POSSITIONS
        if 426 > indexX and indexX > 213 and indexY < 240:
            INDEX_CENTER = True
        else: INDEX_CENTER = False

        if 426 < indexX and indexY < 240 :
            INDEX_LEFT = True
        else :
            INDEX_LEFT = False

        if indexX < 213 and indexY < 240:
            INDEX_RIGHT = True
        else:
            INDEX_RIGHT = False

        if 426 > thumbX and thumbX > 213 and thumbY > 240 :
            THUMB_CENTER = True
        else :
            THUMB_CENTER = False

        if 426 < thumbX and thumbY > 240 :
            THUMB_LEFT = True
        else :
            THUMB_LEFT = False

        if thumbX < 213 and thumbY > 240 :
            THUMB_RIGHT = True
        else :
            THUMB_RIGHT = False

        # STATIC
        if THUMB_CENTER == True and INDEX_CENTER == True:
            ACTION_STATUS = "IDLE"
            ACTION_STATUS_PREV = "IDLE"

        # MOVE_LEFT
        elif THUMB_LEFT == True and INDEX_LEFT == True and ACTION_STATUS_PREV == "IDLE":
            ACTION_STATUS = "MOVE_LEFT"
            ACTION_STATUS_PREV = "MOVE_LEFT"

        # MOVE_RIGHT
        elif THUMB_RIGHT == True and INDEX_RIGHT == True and ACTION_STATUS_PREV == "IDLE":
            ACTION_STATUS = "MOVE_RIGHT"
            ACTION_STATUS_PREV = "MOVE_RIGHT"

        # ROTATE_LEFT
        elif THUMB_CENTER == True and INDEX_LEFT == True and ACTION_STATUS_PREV == "IDLE":
            ACTION_STATUS = "ROTATE_LEFT"
            ACTION_STATUS_PREV = "ROTATE_LEFT"

        #                   4X  8X  4Y  8Y
        #                  441 372 403 122
        #                  283 566 339 333      4X - 150    8X + 170   8Y + 200

        # ROTATE_RIGHT
        elif THUMB_CENTER == True and INDEX_RIGHT == True and ACTION_STATUS_PREV == "IDLE":
            ACTION_STATUS = "ROTATE_RIGHT"
            ACTION_STATUS_PREV = "ROTATE_RIGHT"

        #                   4X  8X  4Y  8Y
        #                  403 336 392 126
        #                  336 70  291 317                  8X - 270   8Y + 200


        if ACTION_STATUS == "IDLE":
            pass
        elif ACTION_STATUS == "MOVE_LEFT":
            print("MOVE_LEFT")
        elif ACTION_STATUS == "MOVE_RIGHT":
            print("MOVE_RIGHT")
        elif ACTION_STATUS == "ROTATE_LEFT":
            print("ROTATE_LEFT")
        elif ACTION_STATUS == "ROTATE_RIGHT":
            print("ROTATE_RIGHT")


        ACTION_STATUS = "-------"



    image = mirror_this(img, False, False)
    winname = "Finger track"
    cv2.namedWindow(winname)
    cv2.moveWindow(winname,40,30)
    cv2.imshow( winname, image )
    cv2.waitKey(5)


while True:
    camera_working()
