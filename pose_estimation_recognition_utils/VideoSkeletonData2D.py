# Copyright 2026 Jonas David Stephan
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
VideoSkeletonData2D.py

This module defines a class for managing 2D skeleton data for videos, including data points and frame information.

Author: Jonas David Stephan
Date: 2026-04-12
License: Apache License 2.0 (https://www.apache.org/licenses/LICENSE-2.0)
"""

import json

from typing import List, Union

from .ImageSkeletonData2D import ImageSkeletonData2D
from .Save2DData import Save2DData
from .Save2DDataWithConfidence import Save2DDataWithConfidence
from .Save2DDataWithName import Save2DDataWithName
from .Save2DDataWithNameAndConfidence import Save2DDataWithNameAndConfidence
from .BoneVector import BoneVector


class VideoSkeletonData2D:
    """
    Represents 2D skeleton data for a specific frame, including multiple persons (each with their own data points).

    Attributes:
        data_points (list): Legacy attribute for single-person data points.
        persons (list): A list of ImageSkeletonData2D objects, one for each person in the frame.
        frame (int): The frame number corresponding to the skeleton data.
    """
    def __init__(self, frame: int):
        """
        Initialize the SkeletonData instance with a frame number.

        Args:
            frame (int): The frame number corresponding to the skeleton data.
        """
        self.data_points: List[Union[Save2DData, Save2DDataWithConfidence, Save2DDataWithName,
        Save2DDataWithNameAndConfidence]] = []
        self.persons: List[ImageSkeletonData2D] = []
        self.frame: int = frame
        self.bone_vectors: List[BoneVector] = []

    def add_bone_vector(self, bone_vector: BoneVector) -> None:
        """
        Add a bone vector to the skeleton.

        Args:
            bone_vector (BoneVector): A bone vector representation.
        """
        self.bone_vectors.append(bone_vector)

    def add_data_point(self, data_point: Union[Save2DData, Save2DDataWithConfidence, Save2DDataWithName,
        Save2DDataWithNameAndConfidence]) -> None:
        """
        Add a data point to the skeleton (legacy/single person).

        Args:
            data_point (Union[SkeletonDataPoint, SkeletonDataPointWithConfidence, SkeletonDataPointWithName,
                SkeletonDataPointWithNameAndConfidence]): A data point representing a part of the skeleton.
        """
        self.data_points.append(data_point)

    def add_person(self, person: ImageSkeletonData2D) -> None:
        """
        Add a person's skeleton data to the frame.

        Args:
            person (ImageSkeletonData2D): The skeleton data for one person.
        """
        self.persons.append(person)

    def get_data_points(self) -> List[Union[Save2DData, Save2DDataWithConfidence, Save2DDataWithName,
        Save2DDataWithNameAndConfidence]]:
        """
        Retrieve all data points in the skeleton (legacy/single person).

        Returns:
            list: A list of data points.
        """
        return self.data_points

    def get_frame(self) -> int:
        """
        Retrieve the frame number for the skeleton data.

        Returns:
            int: The frame number.
        """
        return self.frame

    def calculate_kinematics(self, prev_frame_data: 'VideoSkeletonData2D', time_dt: float) -> None:
        """
        Calculates and sets the velocity and acceleration for each data point based on the previous frame.

        Args:
            prev_frame_data (VideoSkeletonData2D): The skeleton data from the previous frame.
            time_dt (float): The time delta between the current frame and the previous frame.
        """
        if time_dt <= 0:
            return

        # Handle multiple persons
        if self.persons and prev_frame_data.persons:
            # Use person_id to match if available
            target_prev_persons = {p.person_id: p for p in prev_frame_data.persons if p.person_id is not None}
            has_person_ids = len(target_prev_persons) > 0
            
            for i, curr_person in enumerate(self.persons):
                prev_person = None
                if has_person_ids and curr_person.person_id is not None:
                    prev_person = target_prev_persons.get(curr_person.person_id)
                elif i < len(prev_frame_data.persons):
                    prev_person = prev_frame_data.persons[i]
                
                if prev_person:
                    self._calculate_kinematics_for_points(curr_person.data_points, prev_person.data_points, time_dt)
        else:
            # Handle legacy/single person
            self._calculate_kinematics_for_points(self.data_points, prev_frame_data.data_points, time_dt)

    def _calculate_kinematics_for_points(self, curr_points: List, prev_points: List, time_dt: float) -> None:
        """
        Helper to calculate kinematics between two lists of data points.
        
        Args:
            curr_points (list): Current frame's data points.
            prev_points (list): Previous frame's data points.
            time_dt (float): The time delta.
        """
        prev_points_dict = {p.data["id"]: p for p in prev_points if "id" in p.data}
        for curr_p in curr_points:
            p_id = curr_p.data.get("id")
            if p_id in prev_points_dict:
                prev_p = prev_points_dict[p_id]
                
                # Calculate vector components and Euclidean distance
                dx = curr_p.data.get("x", 0) - prev_p.data.get("x", 0)
                dy = curr_p.data.get("y", 0) - prev_p.data.get("y", 0)
                
                # Store individual velocity components
                vx = dx / time_dt
                vy = dy / time_dt
                curr_p.data["velocity_x"] = vx
                curr_p.data["velocity_y"] = vy
                
                # Store scalar velocity magnitude
                dist = (dx**2 + dy**2)**0.5
                curr_velocity = dist / time_dt
                curr_p.data["velocity"] = curr_velocity
                
                # Calculate acceleration taking vector into account
                prev_velocity = prev_p.data.get("velocity")
                if prev_velocity is not None:
                    curr_acceleration = (curr_velocity - prev_velocity) / time_dt
                    curr_p.data["acceleration"] = curr_acceleration
                    
                prev_vx = prev_p.data.get("velocity_x")
                prev_vy = prev_p.data.get("velocity_y")
                if prev_vx is not None and prev_vy is not None:
                    curr_p.data["acceleration_x"] = (vx - prev_vx) / time_dt
                    curr_p.data["acceleration_y"] = (vy - prev_vy) / time_dt

    @classmethod
    def from_dict(cls, data: dict) -> "VideoSkeletonData2D":
        """
        Create a VideoSkeletonData2D instance from a dictionary.
        """
        instance = cls(frame=data.get("frame", 0))
        if "persons" in data:
            for p_dict in data["persons"]:
                instance.add_person(ImageSkeletonData2D.from_dict(p_dict))
        elif "poseestimationpoints" in data:
            for p_dict in data["poseestimationpoints"]:
                instance.add_data_point(Save2DData.from_dict(p_dict))
        
        if "bone_vectors" in data:
            for bv_dict in data["bone_vectors"]:
                instance.add_bone_vector(BoneVector.from_dict(bv_dict))
        return instance

    def to_dict(self) -> dict:
        """
        Convert the skeleton data to a dictionary.

        Returns:
            dict: A dictionary representing the skeleton data.
        """
        res = {"frame": self.frame}
        if self.persons:
            res["persons"] = [p.to_dict() for p in self.persons]
        else:
            # Fallback for backward compatibility
            data_list = [data_point.to_dict() for data_point in self.data_points]
            res["poseestimationpoints"] = data_list
            
        if self.bone_vectors:
            res["bone_vectors"] = [bv.to_dict() for bv in self.bone_vectors]
            
        return res

    def to_json(self) -> str:
        """
        Convert the skeleton data to a JSON string.

        Returns:
            str: A JSON-formatted string representing the skeleton data.
        """
        return json.dumps(self.to_dict())
