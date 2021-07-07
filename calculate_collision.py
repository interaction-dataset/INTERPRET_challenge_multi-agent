import numpy as np

"""
 This funcition returns the list of origins of circles for the given vehicle at all predictied timestames and modalities.
 x, y, and yaw has the same shape (T, Modality).
 l, w are scalars represents the length and width of the vehicle.
 The output has the shape (T, Modality, c, 2) where c is the number of circles tand c is determined by the length of the given vehicle.
"""
def return_circle_list(x, y, l, w, yaw):
    r = w/np.sqrt(2)
    cos_yaw = np.cos(yaw)
    sin_yaw = np.sin(yaw)
    if l < 4.0:
        c1 = [x-(l-w)/2*cos_yaw, y-(l-w)/2*sin_yaw]
        c2 = [x+(l-w)/2*cos_yaw, y+(l-w)/2*sin_yaw]
        c = [c1, c2]
    elif l >= 4.0 and l < 8.0:
        c0 = [x, y]
        c1 = [x-(l-w)/2*cos_yaw, y-(l-w)/2*sin_yaw]
        c2 = [x+(l-w)/2*cos_yaw, y+(l-w)/2*sin_yaw]
        c = [c0, c1, c2]
    else:
        c0 = [x, y]
        c1 = [x-(l-w)/2*cos_yaw, y-(l-w)/2*sin_yaw]
        c2 = [x+(l-w)/2*cos_yaw, y+(l-w)/2*sin_yaw]
        c3 = [x-(l-w)/2*cos_yaw/2, y-(l-w)/2*sin_yaw/2]
        c4 = [x+(l-w)/2*cos_yaw/2, y+(l-w)/2*sin_yaw/2]
        c = [c0, c1, c2, c3, c4]
    for i in range(len(c)):
        c[i] = np.stack(c[i], axis=-1)
    c = np.stack(c, axis=-2)
    return c

"""
 This funcition returns the threshold for collision. If any of two circles' origins' distance between two vehicles is lower than the threshold, it is considered as they have a collision at that timestamp.

 w1, w2 is scalar value which represents the width of vehicle 1 and vehicle 2.
"""
def return_collision_threshold(w1, w2):
    return (w1 + w2) / np.sqrt(3.8)