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
save2Ddata.py

This module defines a class for saving a combination of id, x coordinate and y coordinate.

Author: Chanyut Boonkhamsaen, Nathalie Dollmann, Jonas David Stephan
Date: 2025-07-17
License: Apache License 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
"""

class save2Ddata:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        