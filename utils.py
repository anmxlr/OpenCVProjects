import numpy as np

def get_angle(a,b,c):
    rad = np.arctan2(c[1]-b[1], c[0]-b[0])-np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.rad2deg(rad)
    return angle

def get_distance(landmark_list,lm_1,lm_2):
    (x1,y1),(x2,y2) = landmark_list[lm_1],landmark_list[lm_2]
    dist = np.hypot(x2-x1,y2-y1)
    return dist


def get_finger_lms_indexes(finger_no):
    if finger_no==1:
        return [0,3,4]
    elif finger_no==2:
        return [5,6,8]
    elif finger_no==3:
        return [9,10,12]
    elif finger_no==4:
        return [13,14,16]
    elif finger_no==5:
        return [17,18,20]

def is_down(landmark_list,finger_no):
    finger_lms_list=[landmark_list[get_finger_lms_indexes(finger_no)[0]],landmark_list[get_finger_lms_indexes(finger_no)[1]],landmark_list[get_finger_lms_indexes(finger_no)[2]]]
    if abs(get_angle(finger_lms_list[0],finger_lms_list[1],finger_lms_list[2])) <120:
        return True
    else:
        return False

def get_gesture(landmarkList):
    ##VICTORY
    if not is_down(landmarkList, 2) and not is_down(landmarkList, 3) and is_down(landmarkList, 4) and is_down(landmarkList, 5) and is_down(landmarkList, 1):
        return "Victory"

    ##FUCK_OFF
    if is_down(landmarkList, 2) and not is_down(landmarkList, 3) and is_down(landmarkList, 4) and is_down(landmarkList, 5) and is_down(landmarkList, 1):
        return "Fuck Off"

    ##THUMBS_UP
    if is_down(landmarkList, 2) and is_down(landmarkList, 3) and is_down(landmarkList, 4) and is_down(landmarkList, 5) and not is_down(landmarkList, 1):
        return "THUMBS UP"

    ##ROCK
    if not is_down(landmarkList, 2) and is_down(landmarkList, 3) and is_down(landmarkList, 4) and not is_down(landmarkList, 5) and is_down(landmarkList, 1):
        return "ROCK"

    ##good
    if not is_down(landmarkList,3) and not is_down(landmarkList,4) and not is_down(landmarkList,5) and get_distance(landmarkList,4,8) < 25:
        return "GOOD"

    return None






