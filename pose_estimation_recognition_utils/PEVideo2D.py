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
PEVideo2D.py

This module defines a class for saving 2D pose estimation data of a video.

Author: Jonas David Stephan
Date: 2026-04-12
License: Apache License 2.0 (https://www.apache.org/licenses/LICENSE-2.0)
"""

import json
import gzip
from typing import List

from .VideoSkeletonData2D import VideoSkeletonData2D
from .SkeletonGraph import SkeletonGraph
from .BoneVector import BoneVector


class PEVideo2D:
    """
    Represents 2D skeleton data for a video.

    Attributes:
        origin (str): the name of the tool for pose estimation
        data (list): list of the VideoSkeletonData2D objects
        HumanDetectionModel (str): Optional metadata
        PoseEstimationModel (str): Optional metadata
    """
    def __init__(self, origin: str, data: List[VideoSkeletonData2D] = None,
                 HumanDetectionModel: str = None, PoseEstimationModel: str = None,
                 graph: SkeletonGraph = None):
        """
        Initialize a new PEVideo2D instance.

        Args:
            origin (str): the name of the tool for pose estimation
            data (List[VideoSkeletonData2D]): list of the VideoSkeletonData2D
        """
        if data is None:
            data = []
        self.origin = origin
        self.data = data
        self.HumanDetectionModel = HumanDetectionModel
        self.PoseEstimationModel = PoseEstimationModel
        self.graph = graph

    def set_data(self, data: List[VideoSkeletonData2D]) -> None:
        """
        Adds the VideoSkeletonData2D to the object.

        Args:
            data (list): list of the VideoSkeletonData2D
        """
        self.data = data

    def get_data(self) -> List[VideoSkeletonData2D]:
        """
        Retrieve the VideoSkeletonData2D to the object.

        Returns:
            List[VideoSkeletonData2D]: The VideoSkeletonData2D list of the video.
        """
        return self.data
    
    def add_frame(self, frame: VideoSkeletonData2D) -> None:
        """
        Adds the frame to the data list.

        Args:
            frame (VideoSkeletonData2D): video skeleton object of a frame
        """
        self.data.append(frame)

    def calculate_bone_vectors(self, min_confidence: float = 0.0, interpolate: bool = True) -> None:
        """
        Calculate bone vectors based on the SkeletonGraph topology for all frames.
        Vectors are marked as masked (with coordinates=None and confidence=0.0) if either
        involved joint is missing, below min_confidence, or invalid (x=0, y=0).
        If interpolate is True, masked vectors surrounded by valid frames will be linearly interpolated.

        Args:
            min_confidence (float): Minimum confidence threshold for a data point to be considered valid.
            interpolate (bool): If True, masked vectors will be linearly interpolated across time if possible.
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

        def process_container(container) -> None:
            pts_dict = {
                p.data["id"]: p.data 
                for p in container.get_data_points()
                if "id" in p.data
            }
            container.bone_vectors = []
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
                container.add_bone_vector(bv)

        # First Pass: Compute raw vectors
        for frame_obj in self.data:
            if frame_obj.persons:
                for person in frame_obj.persons:
                    process_container(person)
            else:
                process_container(frame_obj)

        if not interpolate:
            return

        # Second Pass: Temporal Interpolation
        tracks = {}
        for frame_idx, frame_obj in enumerate(self.data):
            if frame_obj.persons:
                for p_idx, person in enumerate(frame_obj.persons):
                    track_id = person.person_id if person.person_id is not None else f"idx_{p_idx}"
                    if track_id not in tracks:
                        tracks[track_id] = []
                    tracks[track_id].append((frame_idx, person))
            else:
                track_id = "legacy"
                if track_id not in tracks:
                    tracks[track_id] = []
                tracks[track_id].append((frame_idx, frame_obj))

        for track_id, elements in tracks.items():
            for start_id, end_id in edges:
                edge_sequence = []
                for _, container in elements:
                    for bv in container.bone_vectors:
                        if bv.start == start_id and bv.end == end_id:
                            edge_sequence.append(bv)
                            break

                last_valid_idx = -1
                for curr_idx, bv in enumerate(edge_sequence):
                    if bv.x is not None:
                        # Found a valid point
                        if last_valid_idx != -1 and curr_idx > last_valid_idx + 1:
                            # Apply interpolation for the gap
                            prev_bv = edge_sequence[last_valid_idx]
                            steps = curr_idx - last_valid_idx
                            for i in range(last_valid_idx + 1, curr_idx):
                                fraction = (i - last_valid_idx) / steps
                                interp_bv = edge_sequence[i]
                                interp_bv.x = prev_bv.x + fraction * (bv.x - prev_bv.x)
                                interp_bv.y = prev_bv.y + fraction * (bv.y - prev_bv.y)
                                if prev_bv.confidence is not None and bv.confidence is not None:
                                    interp_bv.confidence = prev_bv.confidence + fraction * (bv.confidence - prev_bv.confidence)
                        last_valid_idx = curr_idx

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

        res["frames"] = [frame.to_dict() for frame in self.data]
        return json.dumps(res, indent=2)

    def save_in_file(self, filename: str) -> None:
        """
        Writes the object in JSON format into file.
        Recommended extension: .pev2

        Args:
            filename (str): The filename (with path) to the file to save
        """
        with open(filename, "w") as f:
            f.write(self.to_json())

    def save_in_compressed_file(self, filename: str) -> None:
        """
        Writes the object in JSON format into a compressed file.
        Recommended extension: .pev2z

        Args:
            filename (str): The filename (with path) to the file to save
        """
        with gzip.open(filename, "wt", encoding="utf-8") as f:
            f.write(self.to_json())
