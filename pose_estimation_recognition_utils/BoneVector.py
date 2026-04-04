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
BoneVector.py

This module defines a class for storing BoneVectors.

Author: Jonas David Stephan
"""

from typing import Optional

class BoneVector:
    """
    Represents a bone vector with start, end, x, y, and optional z coordinates.
    """
    def __init__(self, start: int, end: int, x: Optional[float], y: Optional[float], z: Optional[float] = None, confidence: Optional[float] = None):
        self.start = start
        self.end = end
        self.x = x
        self.y = y
        self.z = z
        self.confidence = confidence

    def to_dict(self) -> dict:
        """
        Convert the bone vector to a dictionary representation.
        """
        res = {
            "start": self.start,
            "end": self.end
        }
        if self.x is not None:
            res["x"] = self.x
        if self.y is not None:
            res["y"] = self.y
        if self.z is not None:
            res["z"] = self.z
        if self.confidence is not None:
            res["confidence"] = self.confidence
        return res
