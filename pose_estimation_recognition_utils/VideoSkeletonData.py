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
VideoSkeletonData.py

This module defines a class for managing skeleton data, including data points and frame information.

Author: Jonas David Stephan
Date: 2026-03-12
License: Apache License 2.0 (https://www.apache.org/licenses/LICENSE-2.0)
"""

import json

from typing import List, Union

from .SkeletonDataPoint import SkeletonDataPoint
from .SkeletonDataPointWithConfidence import SkeletonDataPointWithConfidence
from .SkeletonDataPointWithName import SkeletonDataPointWithName
from .SkeletonDataPointWithNameAndConfidence import SkeletonDataPointWithNameAndConfidence


class VideoSkeletonData:
    """
    Represents skeleton data for a specific frame, including multiple persons (each with their own data points).

    Attributes:
        data_points (list): Legacy attribute for single-person data points.
        persons (list): A list of ImageSkeletonData objects, one for each person in the frame.
        frame (int): The frame number corresponding to the skeleton data.
    """
    def __init__(self, frame: int):
        """
        Initialize the SkeletonData instance with a frame number.

        Args:
            frame (int): The frame number corresponding to the skeleton data.
        """
        self.data_points: List[Union[SkeletonDataPoint, SkeletonDataPointWithConfidence, SkeletonDataPointWithName,
            SkeletonDataPointWithNameAndConfidence]] = []
        self.persons: List[ImageSkeletonData] = []
        self.frame: int = frame

    def add_data_point(self, data_point: Union[SkeletonDataPoint, SkeletonDataPointWithConfidence,
        SkeletonDataPointWithName, SkeletonDataPointWithNameAndConfidence]) -> None:
        """
        Add a data point to the skeleton (legacy/single person).

        Args:
            data_point (Union[SkeletonDataPoint, SkeletonDataPointWithConfidence, SkeletonDataPointWithName,
                SkeletonDataPointWithNameAndConfidence]): A data point representing a part of the skeleton.
        """
        self.data_points.append(data_point)

    def add_person(self, person: ImageSkeletonData) -> None:
        """
        Add a person's skeleton data to the frame.

        Args:
            person (ImageSkeletonData): The skeleton data for one person.
        """
        self.persons.append(person)

    def get_data_points(self) -> List[Union[SkeletonDataPoint, SkeletonDataPointWithConfidence,
        SkeletonDataPointWithName, SkeletonDataPointWithNameAndConfidence]]:
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
            res["skeletonpoints"] = data_list
        return res

    def to_json(self) -> str:
        """
        Convert the skeleton data to a JSON string.

        Returns:
            str: A JSON-formatted string representing the skeleton data.
        """
        return json.dumps(self.to_dict())
