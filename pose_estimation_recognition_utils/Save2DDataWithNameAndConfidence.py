# Copyright 2025 Nathalie Dollmann, Jonas David Stephan
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
Save2DDataWithNameAndConfidence.py

This module defines a class for saving a combination of id, x coordinate and y coordinate with confidence.

Author: Nathalie Dollmann, Jonas David Stephan
Date: 2026-03-26
License: Apache License 2.0 (https://www.apache.org/licenses/LICENSE-2.0)
"""

import warnings
from .Save2DData import Save2DData

class Save2DDataWithNameAndConfidence(Save2DData):
    """
    Deprecated: Use Save2DData with name and confidence parameters instead.
    """

    def __init__(self, idx: int, name: str, x: float, y: float, confidence: float):
        """
        Initialize a new Save2DDataWithNameAndConfidence instance.
        """
        warnings.warn("Save2DDataWithNameAndConfidence is deprecated. Use Save2DData instead.", DeprecationWarning, stacklevel=2)
        super().__init__(idx=idx, x=x, y=y, name=name, confidence=confidence)