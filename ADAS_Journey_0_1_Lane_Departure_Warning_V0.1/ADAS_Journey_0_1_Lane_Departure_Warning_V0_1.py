import cv2
import numpy as np
import mss
import pygame

LDW_WARNING = f"D:\skill\ML\Git_Repo\ADAS-Level0-Lane-Departure-Warning\ADAS_Journey_0_1_Lane_Departure_Warning_V0.1\Audio\LDW_Warning.mp3"
# LDW_WARNING = f"Git_Repo\ADAS-Level0-Lane-Departure-Warning\ADAS_Journey_0_1_Lane_Departure_Warning_V0.1\Audio\LDW_Warning.mp3"
GAME_WINDOW = (0, 40, 800, 600)

pygame.mixer.init()
def play_sound(path=None):
    try:
        if path:
            sound = pygame.mixer.Sound(path)
            sound.play()
        else:
            pygame.mixer.stop() 
    except Exception as e:
        print("Error in LDW sound", e) 


def grab_screen(region=None):
    with mss.mss() as sct:
        screen = np.array(sct.grab(sct.monitors[1] if not region else region))
        return cv2.cvtColor(screen, cv2.COLOR_BGRA2BGR)

def fit_roi_perspective(frame):
    top_left, bottom_left = [(300,320), (150,450)]
    top_right, bottom_right = [(500,320), (700,450)]
    cv2.circle(frame, top_left, 5, (0,0,255), -1)
    cv2.circle(frame, bottom_left, 5, (0,255,255), -1)
    cv2.circle(frame, top_right, 5, (0,255,255), -1)
    cv2.circle(frame, bottom_right, 5, (0,255,255), -1)

    pts1 = np.float32([top_left, bottom_left, top_right, bottom_right])
    pts2 = np.float32([[0,0], [0,480], [640, 0], [640, 480]])

    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    transformed_frame = cv2.warpPerspective(frame, matrix, (640, 480))

    return transformed_frame

def image_thresholding(frame):
    hsv_transformed_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    l_h = cv2.getTrackbarPos("L - H", "Trackbars")
    l_s = cv2.getTrackbarPos("L - S", "Trackbars")
    l_v = cv2.getTrackbarPos("L - V", "Trackbars")
    u_h = cv2.getTrackbarPos("U - H", "Trackbars")
    u_s = cv2.getTrackbarPos("U - S", "Trackbars")
    u_v = cv2.getTrackbarPos("U - V", "Trackbars")

    # l_h = 0
    # l_s = 34
    # l_v = 149
    # u_h = 255
    # u_s = 141
    # u_v = 255

    lower = np.array([l_h, l_s, l_v])
    upper = np.array([u_h, u_s, u_v])
    cv2.imshow('tmp', hsv_transformed_frame)
    mask = cv2.inRange(hsv_transformed_frame, lower, upper)
    return mask

def histogram_func(mask):
    histogram = np.sum(mask[mask.shape[0]//2:, :], axis = 0)
    midpoint = np.int(histogram.shape[0]/2)
    left_base = np.argmax(histogram[:midpoint])
    right_base = np.argmax(histogram[midpoint:])

    return left_base, right_base+midpoint

def sliding_window_func(mask, histo_output):
    y = 472
    lx = []
    rx = []

    left_base = histo_output[0]
    right_base = histo_output[1]
    msk  = mask.copy()
    msk = cv2.cvtColor(msk, cv2.COLOR_GRAY2BGR)
    cv2.circle(msk, (left_base, 450), 5, (0,0,255), -1)
    cv2.circle(msk, (right_base, 450), 5, (0,255,255), -1)
    while y>0:
        # left threshold
        img = mask[y-40:y, left_base-50:left_base+50]
        contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cx = int(M["m10"]/M["m00"])
                cy = int(M["m01"]/M["m00"])
                lx.append(left_base-50 + cx)
                left_base = left_base-50 + cx
        
        # Right threshold
        img = mask[y-40:y, right_base-50:right_base+50]
        contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cx = int(M["m10"]/M["m00"])
                cy = int(M["m01"]/M["m00"])
                rx.append(right_base-50 + cx)
                right_base = right_base-50 + cx
    
        cv2.rectangle(msk, (left_base-50, y), (left_base+50, y-40), (0,255,255), 2)
        cv2.rectangle(msk, (right_base-50, y), (right_base+50, y-40), (255,255,255), 2)
        y-=40
    return msk


from pynput.keyboard import Key, Controller
import time

keyboard = Controller()

def press_key(key):
    keyboard.press(key)
    time.sleep(0.05)
    keyboard.release(key)


set = False

def nothing(x):
    pass
cv2.namedWindow("Trackbars")

cv2.createTrackbar("L - H", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("L - S", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("L - V", "Trackbars", 200, 255, nothing)
cv2.createTrackbar("U - H", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U - S", "Trackbars", 50, 255, nothing)
cv2.createTrackbar("U - V", "Trackbars", 255, 255, nothing)


def LDW_func(histogram_output, transformed_frame):
    
    lane_center = (histogram_output[0] + histogram_output[1]) // 2
    frame_center = thresholded_frame.shape[1] // 2
    offset = lane_center - frame_center

    if histogram_output[0] > 200 or histogram_output[1] < 400:
        play_sound(LDW_WARNING)
        cv2.putText(transformed_frame, f"LDW Warning !", (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), 3)
    else:
        play_sound(None)
    
    return 

while True:
    frame = grab_screen(region=GAME_WINDOW)
    transformed_frame = fit_roi_perspective(frame)
    thresholded_frame = image_thresholding(transformed_frame)
    histogram_output = histogram_func(thresholded_frame)


    
    sliding_window_output = sliding_window_func(thresholded_frame.copy(), histogram_output)
    LDW_func(histogram_output, transformed_frame)
    cv2.imshow('screen', transformed_frame)
    cv2.imshow('thresholded_screen', thresholded_frame)
    cv2.imshow('sliding_window', sliding_window_output)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cv2.destroyAllWindows()