import os
import sys
import numpy as np

# Add the package path to sys.path
package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if package_path not in sys.path:
    sys.path.insert(0, package_path)

from pose_estimation_recognition_utils import (
    PEImage, PEVideo, ImageSkeletonData, VideoSkeletonData, SkeletonDataPoint,
    load_image_skeleton_from_compressed_file,
    load_video_skeleton_from_compressed_file
)

def test_image_compression():
    print("Testing Image Compression (.peiz)...")
    points = [SkeletonDataPoint(i, i*1.0, i*2.0, i*3.0) for i in range(5)]
    img_data = ImageSkeletonData(person_id=1)
    for p in points:
        img_data.add_data_point(p)
    
    pe_img = PEImage(origin="test_origin", data=img_data)
    pe_img.HumanDetectionModel = "TestModel"
    
    filename = "test_image.peiz"
    pe_img.save_in_compressed_file(filename)
    
    # Check if file exists
    assert os.path.exists(filename)
    print(f"File {filename} created. Size: {os.path.getsize(filename)} bytes")
    
    # Load and verify
    loaded_data = load_image_skeleton_from_compressed_file(filename, "0-4")
    assert loaded_data.shape == (5, 3)
    assert np.allclose(loaded_data[1], [1.0, 2.0, 3.0])
    
    os.remove(filename)
    print("Image Compression Test Passed!")

def test_video_compression():
    print("\nTesting Video Compression (.pevz)...")
    pe_vid = PEVideo(origin="test_video_origin")
    
    for f in range(3):
        points = [SkeletonDataPoint(i, f*1.0, i*1.0, 0.0) for i in range(2)]
        frame = VideoSkeletonData(frame=f)
        for p in points:
            frame.add_data_point(p)
        pe_vid.add_frame(frame)
    
    filename = "test_video.pevz"
    pe_vid.save_in_compressed_file(filename)
    
    # Check if file exists
    assert os.path.exists(filename)
    print(f"File {filename} created. Size: {os.path.getsize(filename)} bytes")
    
    # Load and verify
    loaded_data = load_video_skeleton_from_compressed_file(filename, "0-1")
    assert loaded_data.shape == (3, 2, 3)
    # Frame 1, Point 1 should be [1.0, 1.0, 0.0]
    assert np.allclose(loaded_data[1, 1], [1.0, 1.0, 0.0])
    
    os.remove(filename)
    print("Video Compression Test Passed!")

if __name__ == "__main__":
    try:
        test_image_compression()
        test_video_compression()
        print("\nAll Compression Tests Passed Successfully!")
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"\nCompression Test Failed: {e}")
        sys.exit(1)
