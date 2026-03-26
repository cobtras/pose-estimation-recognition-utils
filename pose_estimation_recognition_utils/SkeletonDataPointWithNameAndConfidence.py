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
SkeletonDataPointWithNameAndConfidence.py

This module defines a class to represent a single data point in a 3D skeleton model with confidence.

Author: Jonas David Stephan
Date: 2026-03-26
License: Apache License 2.0 (https://www.apache.org/licenses/LICENSE-2.0)
"""
import warnings
from .SkeletonDataPoint import SkeletonDataPoint

class SkeletonDataPointWithNameAndConfidence(SkeletonDataPoint):
    """
    Deprecated: Use SkeletonDataPoint with name and confidence parameters instead.
    """

    def __init__(self, idx: int, name: str, x: float, y: float, z: float, confidence: float):
        """
        Initialize a new SkeletonDataPointWithNameAndConfidence instance.
        """
        warnings.warn("SkeletonDataPointWithNameAndConfidence is deprecated. Use SkeletonDataPoint instead.", DeprecationWarning, stacklevel=2)
        super().__init__(idx=idx, x=x, y=y, z=z, name=name, confidence=confidence)