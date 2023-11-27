import numpy as np
import pyrealsense2 as rs
import cv2
import json
import os 
from gpiozero import LED
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
import keyboard

import pickle
# factory = PiGPIOFactory(host='10.10.4.161')

# move_cloth = LED(4, pin_factory=factory)

class Camera:
    def __init__(self):
        self.pipeline   = rs.pipeline()
        self.rs_config  = rs.config()
        self.rs_config.enable_stream(rs.stream.depth, 848, 480, rs.format.z16, 90)
        self.rs_config.enable_stream(rs.stream.color, 848, 480, rs.format.bgr8, 90)
        self.profile = self.pipeline.start(self.rs_config)
        depth_sensor = self.profile.get_device().first_depth_sensor()
        self.depth_scale = depth_sensor.get_depth_scale()
        self.clipping_distance = 0.5 / self.depth_scale
        align_to = rs.stream.color
        self.align = rs.align(align_to)
        cv2.namedWindow('Video', cv2.WINDOW_AUTOSIZE)
        cv2.resizeWindow('Video', 848,480)

    def get_lowest_middle_point_at_catch(self):
        aligned_depth_frame, color_frame = False, False
        while not aligned_depth_frame or not color_frame:
            frames = self.pipeline.wait_for_frames()
            aligned_frames = self.align.process(frames)
            aligned_depth_frame = aligned_frames.get_depth_frame()
            color_frame = aligned_frames.get_color_frame()
        depth_image = np.asanyarray(aligned_depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        mask = (depth_image <= self.clipping_distance) & (depth_image > 0)
        depth_image_3d = np.dstack((depth_image,depth_image,depth_image)) 
        bg_removed = np.where((depth_image_3d > self.clipping_distance) | (depth_image_3d <= 0), 0, color_image)
        
        y, x = np.where(mask)
        median_x, max_y, depth = 0, 0, 10
        if y.size > 0 and x.size > 0:
            max_y = np.max(y)-15
            x_at_max_y = x[y == max_y]
            median_x = np.median(x_at_max_y).astype(int)
            if median_x>0 and max_y>0:
                top_left        = (median_x-5, max_y-5)
                bottom_right    = (median_x, max_y)
                bg_removed      = cv2.rectangle(bg_removed, top_left, bottom_right, (0, 255, 255), 10)
                depth_value     = depth_image[max_y, median_x]
                depth           = depth_value * self.depth_scale

        cv2.imshow('Video', bg_removed)
        cv2.waitKey(1)
        
        return median_x, max_y
    
# cam = Camera()
# for _ in range(200):
    

#     move_cloth.on()
#     sleep(2)
#     move_cloth.off()
#     x,y=[],[]
#     for i in range(200):
#         x_, y_ = cam.get_lowest_middle_point_at_catch()
#         x.append(x_)
#         y.append(y_) 


#     # X positions

#     x_filename = 'positions_x.txt'
#     counter_x = 1
#     while os.path.exists(x_filename):
#             x_filename = f'positions_x_{counter_x}.txt'
#             counter_x += 1

#     with open(x_filename, 'wb') as f:
#         pickle.dump(x,f)
#     print(f'Saved data to {x_filename}')

#     # Y positions 
#     y_filename = 'positions_y.txt'
#     counter_y = 1
#     while os.path.exists(y_filename):
#             y_filename = f'positions_y_{counter_y}.txt'
#             counter_y += 1

#     with open(y_filename, 'wb') as f:
#         pickle.dump(y,f)

#     print(f'Saved data to {y_filename}')


with open('positions_x/positions_x.txt', 'rb') as f:
    x= pickle.load(f)

with open('positions_y/positions_y.txt', 'rb') as f:
    y= pickle.load(f)

for i in range(200):
    print(f"({x[i]},{y[i]})")