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
ImageSkeletonData2D.py

This module defines a class for managing 2D skeleton data, including data points.

Author: Jonas David Stephan
Date: 2026-04-12
License: Apache License 2.0 (https://www.apache.org/licenses/LICENSE-2.0)
"""

import json

from typing import List, Union, Optional

from .Save2DData import Save2DData
from .Save2DDataWithConfidence import Save2DDataWithConfidence
from .Save2DDataWithName import Save2DDataWithName
from .Save2DDataWithNameAndConfidence import Save2DDataWithNameAndConfidence
from .SkeletonGraph import SkeletonGraph
from .BoneVector import BoneVector


class ImageSkeletonData2D:
    """
    Represents 2D skeleton data for a specific person in a frame, including multiple data points and metadata.

    Attributes:
        data_points (list): A list of data points associated with the skeleton.
        person_id (int): The ID of the person (optional).
        BoundingBox (list): The bounding box [x, y, w, h] of the person (optional).
    """
    def __init__(
        self,
        person_id: Optional[int] = None,
        BoundingBox: Optional[List[float]] = None,
        graph: Optional[SkeletonGraph] = None
    ):
        """
        Initialize the SkeletonData instance.

        Args:
            person_id (int): The ID of the person (optional).
            BoundingBox (list): The bounding box [x, y, w, h] of the person (optional).
            graph (SkeletonGraph): The static topology graph (optional).
        """
        self.data_points: List[Union[Save2DData, Save2DDataWithConfidence, Save2DDataWithName,
        Save2DDataWithNameAndConfidence]] = []
        self.person_id = person_id
        self.BoundingBox = BoundingBox
        self.graph = graph
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
        Add a data point to the skeleton.

        Args:
            data_point (Union[Save2DData, Save2DDataWithConfidence, Save2DDataWithName,
        Save2DDataWithNameAndConfidence]): A data point representing a part of the skeleton.
        """
        self.data_points.append(data_point)

    def get_data_points(self) -> List[Union[Save2DData, Save2DDataWithConfidence, Save2DDataWithName,
        Save2DDataWithNameAndConfidence]]:
        """
        Retrieve all data points in the skeleton.

        Returns:
            list: A list of data points.
        """
        return self.data_points

    def to_dict(self) -> dict:
        """
        Convert the skeleton data to a dictionary.

        Returns:
            dict: A dictionary representing the skeleton data.
        """
        data_list = [data_point.to_dict() for data_point in self.data_points]
        res = {"poseestimationpoints": data_list}
        if self.person_id is not None:
            res["person_id"] = self.person_id
        if self.BoundingBox is not None:
            res["BoundingBox"] = self.BoundingBox
        if self.graph is not None:
            res["graph"] = self.graph.to_dict()
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
