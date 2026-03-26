# Copyright 2025 Chanyut Boonkhamsaen, Nathalie Dollmann, Jonas David Stephan
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
Save2DDataWithName.py

This module defines a class for saving a combination of id, name, x coordinate and y coordinate.

Author: Chanyut Boonkhamsaen, Nathalie Dollmann, Jonas David Stephan
Date: 2026-03-26
License: Apache License 2.0 (https://www.apache.org/licenses/LICENSE-2.0)
"""

import warnings
from .Save2DData import Save2DData

class Save2DDataWithName(Save2DData):
    """
    Deprecated: Use Save2DData with name parameter instead.
    """

    def __init__(self, idx: int, name: str, x: float, y: float):
        """
        Initialize a new Save2DDataWithName instance.
        """
        warnings.warn("Save2DDataWithName is deprecated. Use Save2DData instead.", DeprecationWarning, stacklevel=2)
        super().__init__(idx=idx, x=x, y=y, name=name)