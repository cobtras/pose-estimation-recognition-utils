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
PEVideo.py

This module defines a class for saving pose estimation data of a video.

Author: Jonas David Stephan, Nathalie Dollmann
Date: 2026-04-03
License: Apache License 2.0 (https://www.apache.org/licenses/LICENSE-2.0)
"""

import json
import gzip
from typing import List

from .VideoSkeletonData import VideoSkeletonData
from .SkeletonGraph import SkeletonGraph


class PEVideo:
    """
    Represents skeleton data for a video.

    Attributes:
        origin (str): the name of the tool for pose estimation
        data (list): list of the VideoSkeletonData
        HumanDetectionModel (str): Optional metadata
        PoseEstimationModel (str): Optional metadata
        Pose3DGenerationMethod (str): Optional metadata
        lifting_model_3d (str): Optional metadata (3DLiftingModel)
        graph (SkeletonGraph): The static topology graph (optional).
    """
    def __init__(self, origin: str, data: List[VideoSkeletonData] = None,
                 HumanDetectionModel: str = None, PoseEstimationModel: str = None,
                 Pose3DGenerationMethod: str = None, lifting_model_3d: str = None,
                 graph: SkeletonGraph = None):
        """
        Initialize a new PEVideo instance.

        Args:
            origin (str): the name of the tool for pose estimation
            data (List[VideoSkeletonData]): list of the VideoSkeletonData
        """
        if data is None:
            data = []
        self.origin = origin
        self.data = data
        self.HumanDetectionModel = HumanDetectionModel
        self.PoseEstimationModel = PoseEstimationModel
        self.Pose3DGenerationMethod = Pose3DGenerationMethod
        self.lifting_model_3d = lifting_model_3d
        self.graph = graph

    def set_data(self, data: List[VideoSkeletonData]) -> None:
        """
        Adds the VideoSkeletonData to the object.

        Args:
            data (list): list of the VideoSkeletonData
        """
        self.data = data

    def get_data(self) -> List[VideoSkeletonData]:
        """
        Retrieve the VideoSkeletonData to the object.

        Returns:
            VideoSkeletonData: The VideoSkeletonData Object of the video.
        """
        return self.data
    
    def add_frame(self, frame: VideoSkeletonData) -> None:
        """
        Adds the frame to the data list.

        Args:
            frame (VideoSkeletonData): video skeleton object of a frame
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
        if self.Pose3DGenerationMethod:
            res["Pose3DGenerationMethod"] = self.Pose3DGenerationMethod
        if self.lifting_model_3d:
            res["3DLiftingModel"] = self.lifting_model_3d
            
        if self.graph is not None:
            res["graph"] = self.graph.to_dict()

        res["frames"] = [frame.to_dict() for frame in self.data]
        return json.dumps(res, indent=2)

    def save_in_file(self, filename: str) -> None:
        """
        Writes the object in JSON format into file

        Args:
            filename (str): The filename (with path) to the file to save
        """
        with open(filename, "w") as f:
            f.write(self.to_json())

    def save_in_compressed_file(self, filename: str) -> None:
        """
        Writes the object in JSON format into a compressed file (.pevz)

        Args:
            filename (str): The filename (with path) to the file to save
        """
        with gzip.open(filename, "wt", encoding="utf-8") as f:
            f.write(self.to_json())