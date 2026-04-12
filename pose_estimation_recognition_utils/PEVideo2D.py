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
PEVideo2D.py

This module defines a class for saving 2D pose estimation data of a video.

Author: Jonas David Stephan
Date: 2026-04-12
License: Apache License 2.0 (https://www.apache.org/licenses/LICENSE-2.0)
"""

import json
import gzip
from typing import List

from .VideoSkeletonData2D import VideoSkeletonData2D


class PEVideo2D:
    """
    Represents 2D skeleton data for a video.

    Attributes:
        origin (str): the name of the tool for pose estimation
        data (list): list of the VideoSkeletonData2D objects
        HumanDetectionModel (str): Optional metadata
        PoseEstimationModel (str): Optional metadata
    """
    def __init__(self, origin: str, data: List[VideoSkeletonData2D] = None,
                 HumanDetectionModel: str = None, PoseEstimationModel: str = None):
        """
        Initialize a new PEVideo2D instance.

        Args:
            origin (str): the name of the tool for pose estimation
            data (List[VideoSkeletonData2D]): list of the VideoSkeletonData2D
        """
        if data is None:
            data = []
        self.origin = origin
        self.data = data
        self.HumanDetectionModel = HumanDetectionModel
        self.PoseEstimationModel = PoseEstimationModel

    def set_data(self, data: List[VideoSkeletonData2D]) -> None:
        """
        Adds the VideoSkeletonData2D to the object.

        Args:
            data (list): list of the VideoSkeletonData2D
        """
        self.data = data

    def get_data(self) -> List[VideoSkeletonData2D]:
        """
        Retrieve the VideoSkeletonData2D to the object.

        Returns:
            List[VideoSkeletonData2D]: The VideoSkeletonData2D list of the video.
        """
        return self.data
    
    def add_frame(self, frame: VideoSkeletonData2D) -> None:
        """
        Adds the frame to the data list.

        Args:
            frame (VideoSkeletonData2D): video skeleton object of a frame
        """
        self.data.append(frame)

    def to_json(self) -> str:
        """
        Retrieve the object as JSON string.

        Returns:
             str: The object as JSON string.
        """
        res = {"origin": self.origin}

        # Add metadata if present
        if self.HumanDetectionModel:
            res["HumanDetectionModel"] = self.HumanDetectionModel
        if self.PoseEstimationModel:
            res["PoseEstimationModel"] = self.PoseEstimationModel

        res["frames"] = [frame.to_dict() for frame in self.data]
        return json.dumps(res, indent=2)

    def save_in_file(self, filename: str) -> None:
        """
        Writes the object in JSON format into file.
        Recommended extension: .pev2

        Args:
            filename (str): The filename (with path) to the file to save
        """
        with open(filename, "w") as f:
            f.write(self.to_json())

    def save_in_compressed_file(self, filename: str) -> None:
        """
        Writes the object in JSON format into a compressed file.
        Recommended extension: .pev2z

        Args:
            filename (str): The filename (with path) to the file to save
        """
        with gzip.open(filename, "wt", encoding="utf-8") as f:
            f.write(self.to_json())
