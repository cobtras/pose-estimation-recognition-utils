import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pose_estimation_recognition_utils import SkeletonGraph, SkeletonDataPoint, ImageSkeletonData, PEImage, VideoSkeletonData, PEVideo

graph = SkeletonGraph(edges=[(0, 1), (1, 2)])

# Test PEImage
img_data = ImageSkeletonData()
p0 = SkeletonDataPoint(0, 1.0, 2.0, 0.0, confidence=0.9)
p1 = SkeletonDataPoint(1, 2.0, 3.0, 0.0, confidence=0.8)
p2 = SkeletonDataPoint(2, 0.0, 0.0, 0.0, confidence=0.9) # invalid

img_data.add_data_point(p0)
img_data.add_data_point(p1)
img_data.add_data_point(p2)

pe_img = PEImage(origin="test", data=img_data, graph=graph)
pe_img.calculate_bone_vectors(min_confidence=0.5)

assert len(pe_img.get_data().bone_vectors) == 2
b01 = pe_img.get_data().bone_vectors[0]
b12 = pe_img.get_data().bone_vectors[1]
print("PEImage b01:", b01.to_dict())
print("PEImage b12:", b12.to_dict())

assert b01.x == 1.0 and b01.y == 1.0 and b01.confidence == 0.8
assert b12.x is None and b12.confidence == 0.0

# Test PEVideo Interpolation
pe_vid = PEVideo(origin="test", graph=graph)

f0 = VideoSkeletonData(frame=0)
f0.add_data_point(SkeletonDataPoint(0, 10.0, 10.0, 0.0, confidence=0.9))
f0.add_data_point(SkeletonDataPoint(1, 20.0, 20.0, 0.0, confidence=0.9))
pe_vid.add_frame(f0)

f1 = VideoSkeletonData(frame=1)
f1.add_data_point(SkeletonDataPoint(0, 0.0, 0.0, 0.0, confidence=0.9)) # P0 missing this frame
# P1 missing entirely
pe_vid.add_frame(f1)

f2 = VideoSkeletonData(frame=2)
f2.add_data_point(SkeletonDataPoint(0, 30.0, 30.0, 0.0, confidence=0.9))
f2.add_data_point(SkeletonDataPoint(1, 40.0, 40.0, 0.0, confidence=0.9))
pe_vid.add_frame(f2)

pe_vid.calculate_bone_vectors(interpolate=True)

for i, f in enumerate(pe_vid.data):
    bv = f.bone_vectors[0]
    print(f"Frame {i} b01:", bv.to_dict())
    if i == 0:
        assert bv.x == 10.0 and bv.y == 10.0
    if i == 1:
        assert bv.x == 10.0 and bv.y == 10.0 # Interpolated between (10,10) and (10,10)
    if i == 2:
        assert bv.x == 10.0 and bv.y == 10.0
        
print("Success!")
