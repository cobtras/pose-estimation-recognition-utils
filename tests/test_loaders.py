import sys
import os
import json
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pose_estimation_recognition_utils.ImageSkeletonLoader import load_image_skeleton_from_string, load_image_bone_vectors_from_string
from pose_estimation_recognition_utils.VideoSkeletonLoader import load_multi_person_video_skeleton_from_string, load_video_bone_vectors_from_string

v_data = {
    "origin": "test",
    "frames": [
        {
            "frame": 0,
            "persons": [
                {
                    "person_id": 0,
                    "skeletonpoints": [{"id": 0, "x": 1, "y": 1, "z": 1}],
                    "bone_vectors": [{"start": 0, "end": 1, "x": 0.5, "y": 0.5, "z": 0.5, "confidence": 0.9}]
                },
                {
                    "person_id": 1,
                    "skeletonpoints": [{"id": 0, "x": 2, "y": 2, "z": 2}]
                }
            ]
        },
        {
            "frame": 1,
            "persons": [
                {
                    "person_id": 0,
                    "skeletonpoints": [{"id": 0, "x": 3, "y": 3, "z": 3, "velocity_x": 0.5, "velocity_y": 0.5, "velocity_z": 0.5, "acceleration_x": -0.1, "acceleration_y": -0.1, "acceleration_z": -0.1}],
                    "bone_vectors": [{"start": 0, "end": 1, "x": None, "y": None, "z": None, "confidence": 0.0}]
                }
            ]
        }
    ]
}

v_str = json.dumps(v_data)

# Test 1: Single image extraction with velocity/accel
p0 = load_image_skeleton_from_string(json.dumps(v_data["frames"][1]), "0", person_id=0, include_velocity=True, include_acceleration=True)
print("Image p0:", p0)
# Expect shape (1, 9)

# Test 2: Multi-person loader
arr = load_multi_person_video_skeleton_from_string(v_str, "0", include_velocity=True)
print("Multi-person shape:", arr.shape)
# expects shape (2, 2, 1, 6) -> (num_persons, num_frames, num_points, features)
# wait, wait! The shape should be (2, 2, 1, 6)
# Person 0 frame 0: [1, 1, 1, 0, 0, 0]
# Person 0 frame 1: [3, 3, 3, 0.5, 0.5, 0.5]
# Person 1 frame 0: [2, 2, 2, 0, 0, 0]
# Person 1 frame 1: [0, 0, 0, 0, 0, 0]

# Test 3: Bone vectors
b_arr = load_video_bone_vectors_from_string(v_str, person_id=0)
print("Video bones shape:", b_arr.shape)
# expect (2, 1, 6)
