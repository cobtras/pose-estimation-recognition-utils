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
SkeletonLoader.py

This module provides functions to load and filter skeleton data from a JSON file, string, or object for image data.

Author: Jonas David Stephan
Date: 2026-04-04
License: Apache License 2.0 (https://www.apache.org/licenses/LICENSE-2.0)
"""
import gzip
import numpy as np
import json

from typing import List, Set, Tuple

from pose_estimation_recognition_utils import ImageSkeletonData


def load_image_skeleton(file_path: str, points_to_include: str, person_id: int = 0, include_velocity: bool = False, include_acceleration: bool = False) -> np.ndarray:
    """
    Loads skeleton data from a JSON file and filters the points based on specified ranges and individual points.
    
    Args:
        file_path (str): Path to the JSON file containing the skeleton data.
        points_to_include (str): A string specifying ranges and individual point IDs to include (e.g., "1-22,100").
        person_id (int): ID of the person to extract. Default is 0.
        include_velocity (bool): If True, appends velocity vectors (v_x, v_y, v_z) to the point arrays.
        include_acceleration (bool): If True, appends acceleration vectors (a_x, a_y, a_z) to the point arrays.
        
    Returns:
        np.ndarray: A numpy array containing the filtered skeleton data.
    """
    with open(file_path, "r") as file:
        file_content = file.read()
        return load_image_skeleton_from_string(file_content, points_to_include, person_id, include_velocity, include_acceleration)
    

def load_image_skeleton_all_points(file_path: str, points_to_include: str, person_id: int = 0, include_velocity: bool = False, include_acceleration: bool = False) -> np.ndarray:
    """
    Loads skeleton data from a JSON file and filters the points. Fills unwanted points with zeros.
    
    Args:
        file_path (str): Path to the JSON file containing the skeleton data.
        points_to_include (str): A string specifying ranges and individual point IDs to include.
        person_id (int): ID of the person to extract. Default is 0.
        include_velocity (bool): If True, appends velocity vectors (v_x, v_y, v_z) to the point arrays.
        include_acceleration (bool): If True, appends acceleration vectors (a_x, a_y, a_z) to the point arrays.
        
    Returns:
        np.ndarray: A numpy array containing the filtered skeleton data padded with zeros for unwanted points.
    """
    with open(file_path, "r") as file:
        file_content = file.read()
        return load_image_skeleton_from_string_all_points(file_content, points_to_include, person_id, include_velocity, include_acceleration)


def load_image_skeleton_from_string(string: str, points_to_include: str, person_id: int = 0, include_velocity: bool = False, include_acceleration: bool = False) -> np.ndarray:
    """
    Loads skeleton data from a JSON string and filters the points based on specified ranges and individual points.
    
    Args:
        string (str): JSON string containing the skeleton data.
        points_to_include (str): A string specifying ranges and individual point IDs to include.
        person_id (int): ID of the person to extract. Default is 0.
        include_velocity (bool): If True, appends velocity vectors.
        include_acceleration (bool): If True, appends acceleration vectors.
        
    Returns:
        np.ndarray: A numpy array containing the filtered skeleton data.
    """
    content = json.loads(string)

    skeleton_points = []
    if 'persons' in content and len(content['persons']) > 0:
        for p in content['persons']:
            if p.get('person_id', 0) == person_id:
                skeleton_points = p.get('skeletonpoints', [])
                break
    elif 'skeletonpoints' in content:
        if person_id == 0:
            skeleton_points = content['skeletonpoints']

    points: Set[int] = set()
    ranges: List[Tuple[int, int]] = []

    for part in points_to_include.split(','):
        if '-' in part:
            start, end = part.split('-')
            ranges.append((int(start), int(end)))
        else:
            points.add(int(part))

    def should_include_point(point_id):
        if point_id in points:
            return True
        for start_id, end_id in ranges:
            if start_id <= point_id <= end_id:
                return True
        return False

    point_array = []
    for point in skeleton_points:
        if should_include_point(point['id']):
            skeleton_array = [point.get('x', 0), point.get('y', 0), point.get('z', 0)]
            if include_velocity:
                skeleton_array.extend([point.get('velocity_x', 0), point.get('velocity_y', 0), point.get('velocity_z', 0)])
            if include_acceleration:
                skeleton_array.extend([point.get('acceleration_x', 0), point.get('acceleration_y', 0), point.get('acceleration_z', 0)])
            point_array.append(np.array(skeleton_array))

    return np.array(point_array)


def load_image_skeleton_from_string_all_points(string: str, points_to_include: str, person_id: int = 0, include_velocity: bool = False, include_acceleration: bool = False) -> np.ndarray:
    """
    Loads skeleton data from a JSON string and filters the points. Fills unwanted points with zeros.
    
    Args:
        string (str): JSON string containing the skeleton data.
        points_to_include (str): A string specifying ranges and individual point IDs to include.
        person_id (int): ID of the person to extract. Default is 0.
        include_velocity (bool): If True, appends velocity vectors.
        include_acceleration (bool): If True, appends acceleration vectors.
        
    Returns:
        np.ndarray: A numpy array containing the filtered skeleton data. Unwanted points are filled with zeros.
    """
    content = json.loads(string)

    skeleton_points = []
    if 'persons' in content and len(content['persons']) > 0:
        for p in content['persons']:
            if p.get('person_id', 0) == person_id:
                skeleton_points = p.get('skeletonpoints', [])
                break
    elif 'skeletonpoints' in content:
        if person_id == 0:
            skeleton_points = content['skeletonpoints']

    points: Set[int] = set()
    ranges: List[Tuple[int, int]] = []

    for part in points_to_include.split(','):
        if '-' in part:
            start, end = part.split('-')
            ranges.append((int(start), int(end)))
        else:
            points.add(int(part))

    def should_include_point(point_id):
        if point_id in points:
            return True
        for start_id, end_id in ranges:
            if start_id <= point_id <= end_id:
                return True
        return False

    zero_vec_len = 3
    if include_velocity: zero_vec_len += 3
    if include_acceleration: zero_vec_len += 3
    zero_vec = [0] * zero_vec_len

    point_array = []
    for point in skeleton_points:
        if should_include_point(point['id']):
            skeleton_array = [point.get('x', 0), point.get('y', 0), point.get('z', 0)]
            if include_velocity:
                skeleton_array.extend([point.get('velocity_x', 0), point.get('velocity_y', 0), point.get('velocity_z', 0)])
            if include_acceleration:
                skeleton_array.extend([point.get('acceleration_x', 0), point.get('acceleration_y', 0), point.get('acceleration_z', 0)])
            point_array.append(np.array(skeleton_array))
        else:
            point_array.append(np.array(zero_vec))

    return np.array(point_array)


def load_image_skeleton_object(skeleton_object: ImageSkeletonData, points_to_include: str, include_velocity: bool = False, include_acceleration: bool = False) -> np.ndarray:
    """
    Loads skeleton data directly from an ImageSkeletonData object and filters the points.
    
    Args:
        skeleton_object (ImageSkeletonData): The given skeleton data object.
        points_to_include (str): A string specifying ranges and individual point IDs to include.
        include_velocity (bool): If True, appends velocity vectors.
        include_acceleration (bool): If True, appends acceleration vectors.
        
    Returns:
        np.ndarray: A numpy array containing the filtered skeleton data.
    """
    points: Set[int] = set()
    ranges: List[Tuple[int, int]] = []
    for part in points_to_include.split(','):
        if '-' in part:
            start, end = part.split('-')
            ranges.append((int(start), int(end)))
        else:
            points.add(int(part))

    def should_include_point(point_id):
        if point_id in points:
            return True
        for start_id, end_id in ranges:
            if start_id <= point_id <= end_id:
                return True
        return False

    point_array = []
    for point in skeleton_object.get_data_points():
        p_dict = point.to_dict()
        if should_include_point(p_dict['id']):
            skeleton_array = [p_dict.get('x', 0), p_dict.get('y', 0), p_dict.get('z', 0)]
            if include_velocity:
                skeleton_array.extend([p_dict.get('velocity_x', 0), p_dict.get('velocity_y', 0), p_dict.get('velocity_z', 0)])
            if include_acceleration:
                skeleton_array.extend([p_dict.get('acceleration_x', 0), p_dict.get('acceleration_y', 0), p_dict.get('acceleration_z', 0)])
            point_array.append(np.array(skeleton_array))

    return np.array(point_array)


def load_image_skeleton_object_all_points(skeleton_object: ImageSkeletonData, points_to_include: str, include_velocity: bool = False, include_acceleration: bool = False) -> np.ndarray:
    """
    Loads skeleton data directly from an ImageSkeletonData object and filters the points. Fills unwanted points with zeros.
    
    Args:
        skeleton_object (ImageSkeletonData): The given skeleton data object.
        points_to_include (str): A string specifying ranges and individual point IDs to include.
        include_velocity (bool): If True, appends velocity vectors.
        include_acceleration (bool): If True, appends acceleration vectors.
        
    Returns:
        np.ndarray: A numpy array containing the filtered skeleton data.
    """
    points: Set[int] = set()
    ranges: List[Tuple[int, int]] = []
    for part in points_to_include.split(','):
        if '-' in part:
            start, end = part.split('-')
            ranges.append((int(start), int(end)))
        else:
            points.add(int(part))

    def should_include_point(point_id):
        if point_id in points:
            return True
        for start_id, end_id in ranges:
            if start_id <= point_id <= end_id:
                return True
        return False

    zero_vec_len = 3
    if include_velocity: zero_vec_len += 3
    if include_acceleration: zero_vec_len += 3
    zero_vec = [0] * zero_vec_len

    point_array = []
    for point in skeleton_object.get_data_points():
        p_dict = point.to_dict()
        if should_include_point(p_dict['id']):
            skeleton_array = [p_dict.get('x', 0), p_dict.get('y', 0), p_dict.get('z', 0)]
            if include_velocity:
                skeleton_array.extend([p_dict.get('velocity_x', 0), p_dict.get('velocity_y', 0), p_dict.get('velocity_z', 0)])
            if include_acceleration:
                skeleton_array.extend([p_dict.get('acceleration_x', 0), p_dict.get('acceleration_y', 0), p_dict.get('acceleration_z', 0)])
            point_array.append(np.array(skeleton_array))
        else:
            point_array.append(np.array(zero_vec))

    return np.array(point_array)


def load_image_skeleton_from_compressed_file(file_path: str, points_to_include: str, person_id: int = 0, include_velocity: bool = False, include_acceleration: bool = False) -> np.ndarray:
    """
    Loads skeleton data from a compressed JSON file (.peiz) and filters the points.
    
    Args:
        file_path (str): Path to the compressed JSON file.
        points_to_include (str): A string specifying ranges and individual point IDs to include.
        person_id (int): ID of the person to extract. Default is 0.
        include_velocity (bool): If True, appends velocity vectors.
        include_acceleration (bool): If True, appends acceleration vectors.
        
    Returns:
        np.ndarray: A numpy array containing the filtered skeleton data.
    """
    with gzip.open(file_path, "rt", encoding="utf-8") as file:
        file_content = file.read()
        return load_image_skeleton_from_string(file_content, points_to_include, person_id, include_velocity, include_acceleration)


def load_image_skeleton_all_points_from_compressed_file(file_path: str, points_to_include: str, person_id: int = 0, include_velocity: bool = False, include_acceleration: bool = False) -> np.ndarray:
    """
    Loads skeleton data from a compressed JSON file (.peiz) and filters the points. Fills unwanted points with zeros.
    
    Args:
        file_path (str): Path to the compressed JSON file.
        points_to_include (str): A string specifying ranges and individual point IDs to include.
        person_id (int): ID of the person to extract. Default is 0.
        include_velocity (bool): If True, appends velocity vectors.
        include_acceleration (bool): If True, appends acceleration vectors.
        
    Returns:
        np.ndarray: A numpy array containing the filtered skeleton data.
    """
    with gzip.open(file_path, "rt", encoding="utf-8") as file:
        file_content = file.read()
        return load_image_skeleton_from_string_all_points(file_content, points_to_include, person_id, include_velocity, include_acceleration)

# ----------------- Bone Vector functions -----------------

def load_image_bone_vectors_from_string(string: str, person_id: int = 0) -> np.ndarray:
    """
    Loads bone vectors from a string for a specific person.
    
    Args:
        string (str): JSON string containing the sequence.
        person_id (int): ID of the person to extract. Default is 0.
        
    Returns: 
        np.ndarray: shape (num_bones, 6) where columns are [start, end, x, y, z, confidence].
                    Masked coordinates are loaded as 0.0 with 0.0 confidence.
    """
    content = json.loads(string)
    bone_vectors = []
    
    if 'persons' in content and len(content['persons']) > 0:
        for p in content['persons']:
            if p.get('person_id', 0) == person_id:
                bone_vectors = p.get('bone_vectors', [])
                break
    elif 'bone_vectors' in content:
        if person_id == 0:
            bone_vectors = content['bone_vectors']

    bv_array = []
    for bv in bone_vectors:
        x = bv.get('x')
        x = x if x is not None else 0.0
        y = bv.get('y')
        y = y if y is not None else 0.0
        z = bv.get('z')
        z = z if z is not None else 0.0
        c = bv.get('confidence')
        c = c if c is not None else 0.0
        bv_array.append(np.array([bv.get('start', -1), bv.get('end', -1), x, y, z, c]))

    return np.array(bv_array)

def load_image_bone_vectors(file_path: str, person_id: int = 0) -> np.ndarray:
    """
    Loads bone vectors from a JSON file for a specific person.
    
    Args:
        file_path (str): Path to the JSON file.
        person_id (int): ID of the person to extract. Default is 0.
        
    Returns:
        np.ndarray: A numpy array containing the bone vectors.
    """
    with open(file_path, "r") as file:
        return load_image_bone_vectors_from_string(file.read(), person_id)

def load_image_bone_vectors_from_compressed_file(file_path: str, person_id: int = 0) -> np.ndarray:
    """
    Loads bone vectors from a compressed JSON file (.peiz) for a specific person.
    
    Args:
        file_path (str): Path to the compressed JSON file.
        person_id (int): ID of the person to extract. Default is 0.
        
    Returns:
        np.ndarray: A numpy array containing the bone vectors.
    """
    with gzip.open(file_path, "rt", encoding="utf-8") as file:
        return load_image_bone_vectors_from_string(file.read(), person_id)

def load_image_bone_vectors_object(skeleton_object: ImageSkeletonData) -> np.ndarray:
    """
    Loads bone vectors directly from an ImageSkeletonData object.
    
    Args:
        skeleton_object (ImageSkeletonData): The skeleton data object containing bone vectors.
        
    Returns:
        np.ndarray: A numpy array containing the bone vectors.
    """
    bv_array = []
    for bv in skeleton_object.bone_vectors:
        b_dict = bv.to_dict()
        x = b_dict.get('x')
        x = x if x is not None else 0.0
        y = b_dict.get('y')
        y = y if y is not None else 0.0
        z = b_dict.get('z')
        z = z if z is not None else 0.0
        c = b_dict.get('confidence')
        c = c if c is not None else 0.0
        bv_array.append(np.array([b_dict.get('start', -1), b_dict.get('end', -1), x, y, z, c]))
    return np.array(bv_array)
