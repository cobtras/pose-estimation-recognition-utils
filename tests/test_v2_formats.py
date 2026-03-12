import json
import os
import sys

# Ensure we can import from the current directory, prioritizing it
sys.path.insert(0, os.path.abspath('.'))

import pose_estimation_recognition_utils
print(f"Loading package from: {pose_estimation_recognition_utils.__file__}")

from pose_estimation_recognition_utils import (
    PEImage, ImageSkeletonData, SkeletonDataPoint,
    PEVideo, VideoSkeletonData
)

def test_v2_image_multi_person():
    print("Testing Multi-Person Image Format v2.0...")
    
    # Create Image 1 with 2 persons
    p1 = ImageSkeletonData(person_id=0, BoundingBox=[10, 20, 30, 40])
    p1.add_data_point(SkeletonDataPoint(0, 0.1, 0.2, 0.3))
    
    p2 = ImageSkeletonData(person_id=1)
    p2.add_data_point(SkeletonDataPoint(0, 0.5, 0.6, 0.7))
    
    img = PEImage(origin="test_tool", HumanDetectionModel="YOLOv8")
    img.add_person(p1)
    img.add_person(p2)
    
    json_out = img.to_json()
    data = json.loads(json_out)
    
    assert data["origin"] == "test_tool"
    assert data["HumanDetectionModel"] == "YOLOv8"
    assert len(data["persons"]) == 2
    assert data["persons"][0]["person_id"] == 0
    assert data["persons"][0]["BoundingBox"] == [10, 20, 30, 40]
    print("Multi-Person Image Format v2.0: PASS")

def test_v2_video_multi_person():
    print("Testing Multi-Person Video Format v2.0...")
    
    v = PEVideo(origin="vid_tool", PoseEstimationModel="RTMPose")
    
    # Frame 0
    f0 = VideoSkeletonData(frame=0)
    p1 = ImageSkeletonData(person_id=0)
    p1.add_data_point(SkeletonDataPoint(0, 0.1, 0.1, 0.1))
    f0.add_person(p1)
    v.add_frame(f0)
    
    json_out = v.to_json()
    data = json.loads(json_out)
    
    assert data["origin"] == "vid_tool"
    assert data["PoseEstimationModel"] == "RTMPose"
    assert data["frames"][0]["frame"] == 0
    assert len(data["frames"][0]["persons"]) == 1
    assert data["frames"][0]["persons"][0]["person_id"] == 0
    print("Multi-Person Video Format v2.0: PASS")

def test_v2_legacy_compatibility():
    print("Testing Legacy Compatibility...")
    
    # Legacy Image
    p = ImageSkeletonData()
    p.add_data_point(SkeletonDataPoint(0, 0.1, 0.2, 0.3))
    img = PEImage(origin="legacy", data=p)
    
    data = json.loads(img.to_json())
    assert "skeletonpoints" in data
    assert "persons" not in data
    
    # Legacy Video
    f = VideoSkeletonData(frame=0)
    f.add_data_point(SkeletonDataPoint(0, 0.1, 0.2, 0.3))
    vid = PEVideo(origin="legacy")
    vid.add_frame(f)
    
    data = json.loads(vid.to_json())
    assert "skeletonpoints" in data["frames"][0]
    assert "persons" not in data["frames"][0]
    print("Legacy Compatibility: PASS")

if __name__ == "__main__":
    try:
        test_v2_image_multi_person()
        test_v2_video_multi_person()
        test_v2_legacy_compatibility()
        print("\nAll skeleton v2.0 tests passed successfully!")
    except Exception as e:
        print(f"\nTests failed: {e}")
        sys.exit(1)
