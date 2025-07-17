# Copyright 2025 Chanyut Boonkhamsaen, Nathalie Dollmann, Jonas David Stephan
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
MediaPipePoseEstimationfrom3DFrame.py

This module defines a class for extracting Pose Estimation from 3D frames with MediaPipe.

Author: Chanyut Boonkhamsaen, Nathalie Dollmann, Jonas David Stephan
Date: 2025-07-17
License: Apache License 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
"""

import mediapipe as mp
from save2Ddata import save2Ddata

class MediaPipePoseEstimationfrom3DFrame:
    def __init__(self, min_detection_confidence, min_tracking_confidence):
        # Initialize pose estimation class
        self.mp_pose = mp.solutions.pose.Pose(min_detection_confidence=min_detection_confidence, min_tracking_confidence=min_tracking_confidence)

    def extract_frame(self, frame):
        frame_left, frame_right = self.divide_3Dframe(frame)

        #detecting the object using mediapipe
        results_left = self.mp_pose.process(frame_left)
        results_right = self.mp_pose.process(frame_right)
        
        pixel_list_right = []
        pixel_list_left = []
        
        for idx, landmark in enumerate(results_left.pose_landmarks.landmark):  
            pixel_x_left = landmark.x * frame_left.shape[1]
            pixel_y_left = landmark.y * frame_left.shape[0]
            object = save2Ddata(idx, pixel_x_left, pixel_y_left)
            pixel_list_left.append(object)
        
        for idx, landmark in enumerate(results_right.pose_landmarks.landmark): 
            pixel_x_right = landmark.x * frame_right.shape[1]
            pixel_y_right = landmark.y * frame_right.shape[0]
            object = save2Ddata(idx, pixel_x_right, pixel_y_right)
            pixel_list_right.append(object)
        
        # TODO

    def divide_3Dframe(self, frame):
        frame_width = frame.shape[1]
        dividing_point = frame_width//2
        frame_left = frame[:, :dividing_point]
        frame_right = frame[:, dividing_point:]
        return (frame_left, frame_right)