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
PEImage2D.py

This module defines a class for saving 2D pose estimation data of an image.

Author: Jonas David Stephan
Date: 2026-04-12
License: Apache License 2.0 (https://www.apache.org/licenses/LICENSE-2.0)
"""

import json
import gzip
from typing import List

from .ImageSkeletonData2D import ImageSkeletonData2D
from .SkeletonGraph import SkeletonGraph
from .BoneVector import BoneVector


class PEImage2D:
    """
    Represents 2D skeleton data for an image.

    Attributes:
        origin (str): the name of the tool for pose estimation
        data (ImageSkeletonData2D): The ImageSkeletonData2D Object of the image (single person/legacy)
        persons (list): List of ImageSkeletonData2D objects (multi-person)
        HumanDetectionModel (str): Optional metadata
        PoseEstimationModel (str): Optional metadata
    """
    def __init__(self, origin: str, data: ImageSkeletonData2D = None,
                 HumanDetectionModel: str = None, PoseEstimationModel: str = None,
                 graph: SkeletonGraph = None):
        """
        Initialize a new PEImage2D instance.

        Args:
            origin (str): the name of the tool for pose estimation
            data (ImageSkeletonData2D): The ImageSkeletonData2D Object of the image
        """
        self.origin = origin
        self.data = data
        self.persons: List[ImageSkeletonData2D] = []
        self.HumanDetectionModel = HumanDetectionModel
        self.PoseEstimationModel = PoseEstimationModel
        self.graph = graph

    def set_data(self, data: ImageSkeletonData2D) -> None:
        """
        Adds the ImageSkeletonData2D to the object.

        Args:
            data (ImageSkeletonData2D): The ImageSkeletonData2D Object of the image
        """
        self.data = data

    def add_person(self, person: ImageSkeletonData2D) -> None:
        """
        Adds a person's skeleton data.

        Args:
            person (ImageSkeletonData2D): Skeleton data for one person.
        """
        self.persons.append(person)

    def get_data(self) -> ImageSkeletonData2D:
        """
        Retrieve the ImageSkeletonData2D to the object.

        Returns:
            ImageSkeletonData2D: The ImageSkeletonData2D Object of the image.
        """
        return self.data

    def calculate_bone_vectors(self, min_confidence: float = 0.0) -> None:
        """
        Calculate bone vectors based on the SkeletonGraph topology.
        Vectors are marked as masked (coordinates=None, confidence=0.0) if either
        involved joint is missing, below min_confidence, or invalid (x=0, y=0).

        Args:
            min_confidence (float): Minimum confidence threshold for a data point to be considered valid.
        """
        if self.graph is None:
            return

        edges = self.graph.edges

        def _is_valid_point(p_data: dict) -> bool:
            x = p_data.get("x")
            y = p_data.get("y")
            if x is None or y is None:
                return False
            if x == 0.0 and y == 0.0:
                return False
            conf = p_data.get("confidence")
            if conf is not None and conf < min_confidence:
                return False
            return True

        persons_to_process = self.persons if self.persons else ([self.data] if self.data else [])

        for person in persons_to_process:
            pts_dict = {
                p.data["id"]: p.data 
                for p in person.get_data_points()
                if "id" in p.data
            }

            person.bone_vectors = []
            for start_id, end_id in edges:
                pt_start = pts_dict.get(start_id)
                pt_end = pts_dict.get(end_id)

                if pt_start and pt_end and _is_valid_point(pt_start) and _is_valid_point(pt_end):
                    dx = pt_end["x"] - pt_start["x"]
                    dy = pt_end["y"] - pt_start["y"]
                    dz = None
                    
                    conf_start = pt_start.get("confidence")
                    conf_end = pt_end.get("confidence")
                    
                    if conf_start is not None and conf_end is not None:
                        bone_conf = min(conf_start, conf_end)
                    elif conf_start is not None:
                        bone_conf = conf_start
                    elif conf_end is not None:
                        bone_conf = conf_end
                    else:
                        bone_conf = None
                        
                    bv = BoneVector(start=start_id, end=end_id, x=dx, y=dy, z=dz, confidence=bone_conf)
                else:
                    bv = BoneVector(start=start_id, end=end_id, x=None, y=None, z=None, confidence=0.0)

                person.add_bone_vector(bv)

    @classmethod
    def from_json(cls, json_str: str) -> "PEImage2D":
        """
        Create a PEImage2D instance from a JSON string.

        Args:
            json_str (str): The JSON string representation of the object.

        Returns:
            PEImage2D: A new PEImage2D instance.
        """
        data = json.loads(json_str)
        graph_dict = data.get("graph")
        graph = SkeletonGraph.from_dict(graph_dict) if graph_dict else None
        
        instance = cls(
            origin=data.get("origin"),
            HumanDetectionModel=data.get("HumanDetectionModel"),
            PoseEstimationModel=data.get("PoseEstimationModel"),
            graph=graph
        )
        
        if "persons" in data:
            for p_dict in data["persons"]:
                if graph and "graph" not in p_dict:
                    p_dict["graph"] = graph_dict
                instance.add_person(ImageSkeletonData2D.from_dict(p_dict))
        elif "poseestimationpoints" in data:
            sd_dict = {
                "poseestimationpoints": data["poseestimationpoints"],
                "person_id": data.get("person_id"),
                "BoundingBox": data.get("BoundingBox"),
                "graph": graph_dict
            }
            instance.set_data(ImageSkeletonData2D.from_dict(sd_dict))
            
        return instance

    @classmethod
    def load_from_file(cls, filename: str) -> "PEImage2D":
        """
        Loads the object from a JSON file.

        Args:
            filename (str): The filename (with path) to the file to load.

        Returns:
            PEImage2D: The loaded PEImage2D object.
        """
        with open(filename, "r") as f:
            return cls.from_json(f.read())

    @classmethod
    def load_from_compressed_file(cls, filename: str) -> "PEImage2D":
        """
        Loads the object from a compressed (.pei2z) file.

        Args:
            filename (str): The filename (with path) to the file to load.

        Returns:
            PEImage2D: The loaded PEImage2D object.
        """
        with gzip.open(filename, "rt", encoding="utf-8") as f:
            return cls.from_json(f.read())

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

        if self.graph is not None:
            res["graph"] = self.graph.to_dict()

        if self.persons:
            res["persons"] = [p.to_dict() for p in self.persons]
        elif self.data:
            res["poseestimationpoints"] = self.data.to_dict()["poseestimationpoints"]
            if self.data.person_id is not None:
                res["person_id"] = self.data.person_id
            if self.data.BoundingBox is not None:
                res["BoundingBox"] = self.data.BoundingBox

        return json.dumps(res, indent=2)

    def save_in_file(self, filename: str) -> None:
        """
        Writes the object in JSON format into file.
        Recommended extension: .pei2

        Args:
            filename (str): The filename (with path) to the file to save
        """
        with open(filename, "w") as f:
            f.write(self.to_json())

    def save_in_compressed_file(self, filename: str) -> None:
        """
        Writes the object in JSON format into a compressed file.
        Recommended extension: .pei2z

        Args:
            filename (str): The filename (with path) to the file to save
        """
        with gzip.open(filename, "wt", encoding="utf-8") as f:
            f.write(self.to_json())
