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
PEImage.py

This module defines a class for saving pose estimation data of an image.

Author: Jonas David Stephan
Date: 2026-04-04
License: Apache License 2.0 (https://www.apache.org/licenses/LICENSE-2.0)
"""

import json
import gzip
from typing import List

from .ImageSkeletonData import ImageSkeletonData
from .SkeletonGraph import SkeletonGraph


class PEImage:
    """
    Represents skeleton data for an image.

    Attributes:
        origin (str): the name of the tool for pose estimation
        data (ImageSkeletonData): The ImageSkeletonData Object of the image (single person/legacy)
        persons (list): List of ImageSkeletonData objects (multi-person)
        HumanDetectionModel (str): Optional metadata
        PoseEstimationModel (str): Optional metadata
        Pose3DGenerationMethod (str): Optional metadata
        lifting_model_3d (str): Optional metadata (3DLiftingModel)
        graph (SkeletonGraph): The static topology graph (optional).
    """
    def __init__(self, origin: str, data: ImageSkeletonData = None,
                 HumanDetectionModel: str = None, PoseEstimationModel: str = None,
                 Pose3DGenerationMethod: str = None, lifting_model_3d: str = None,
                 graph: SkeletonGraph = None):
        """
        Initialize a new PEImage instance.

        Args:
            origin (str): the name of the tool for pose estimation
            data (ImageSkeletonData): The ImageSkeletonData Object of the image
        """
        self.origin = origin
        self.data = data
        self.persons: List[ImageSkeletonData] = []
        self.HumanDetectionModel = HumanDetectionModel
        self.PoseEstimationModel = PoseEstimationModel
        self.Pose3DGenerationMethod = Pose3DGenerationMethod
        self.lifting_model_3d = lifting_model_3d
        self.graph = graph

    def set_data(self, data: ImageSkeletonData) -> None:
        """
        Adds the ImageSkeletonData to the object.

        Args:
            data (ImageSkeletonData): The ImageSkeletonData Object of the image
        """
        self.data = data

    def add_person(self, person: ImageSkeletonData) -> None:
        """
        Adds a person's skeleton data.

        Args:
            person (ImageSkeletonData): Skeleton data for one person.
        """
        self.persons.append(person)

    def get_data(self) -> ImageSkeletonData:
        """
        Retrieve the ImageSkeletonData to the object.

        Returns:
            ImageSkeletonData: The ImageSkeletonData Object of the image.
        """
        return self.data

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

        if self.persons:
            res["persons"] = [p.to_dict() for p in self.persons]
        elif self.data:
            res["skeletonpoints"] = self.data.to_dict()["skeletonpoints"]
            if self.data.person_id is not None:
                res["person_id"] = self.data.person_id
            if self.data.BoundingBox is not None:
                res["BoundingBox"] = self.data.BoundingBox

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
        Writes the object in JSON format into a compressed file (.peiz)

        Args:
            filename (str): The filename (with path) to the file to save
        """
        with gzip.open(filename, "wt", encoding="utf-8") as f:
            f.write(self.to_json())