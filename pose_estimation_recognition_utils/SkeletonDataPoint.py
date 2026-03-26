# Copyright 2025 Jonas David Stephan
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
SkeletonDataPoint.py

This module defines a class to represent a single data point in a 3D skeleton model.

Author: Jonas David Stephan
Date: 2025-01-28
License: Apache License 2.0 (https://www.apache.org/licenses/LICENSE-2.0)
"""

import json
import warnings
from typing import Dict, Optional


class SkeletonDataPoint:
    """
    Represents a single data point in a 3D skeleton model.

    Attributes:
        data (dict): A dictionary containing the point's ID, 3D coordinates (x, y, z), and optional name/confidence.
    """

    def __init__(self, idx: int, x: float, y: float, z: float, name: Optional[str] = None, confidence: Optional[float] = None):
        """
        Initialize a new SkeletonDataPoint instance.

        Args:
            idx (int): The ID of the data point.
            x (float): The x-coordinate of the data point.
            y (float): The y-coordinate of the data point.
            z (float): The z-coordinate of the data point.
            name (str, optional): The name associated with the data point.
            confidence (float, optional): The confidence value of the data point.

        Raises:
            ValueError: If coordinates or confidence are not numeric, or name is not a string.
        """
        if not all(isinstance(coord, (int, float)) for coord in [x, y, z]):
            raise ValueError("Coordinates x, y, and z must be numeric.")
        
        self.data: Dict[str, object] = {"id": idx, "x": x, "y": y, "z": z}
        
        if name is not None:
            if not isinstance(name, str):
                raise ValueError("The name must be a string.")
            self.data["name"] = name
            
        if confidence is not None:
            if not isinstance(confidence, (int, float)):
                raise ValueError("Confidence must be numeric.")
            self.data["confidence"] = float(confidence)

    def get_data(self) -> Dict[str, object]:
        """
        Retrieve the data point as a dictionary.
        
        Deprecated: Use to_dict() instead.

        Returns:
            dict: The dictionary representation of the data point.
        """
        warnings.warn("SkeletonDataPoint.get_data() is deprecated. Use to_dict() instead.", DeprecationWarning, stacklevel=2)
        return self.to_dict()

    def to_dict(self) -> Dict[str, object]:
        """
        Convert the data point to a dictionary. Returns fields only if they have values.

        Returns:
            dict: The dictionary representation of the data point.
        """
        return {k: v for k, v in self.data.items() if v is not None}

    def to_json(self) -> str:
        """
        Convert the data point to a JSON string.

        Returns:
            str: The JSON-formatted string representation of the data point.
        """
        return json.dumps(self.to_dict(), indent=4)
