# 📄 Data Format Documentation v2.1 (.pei, .pev, .pei2, .pev2, .peiz, .pevz, .pei2z, .pev2z)

Version 2.1 introduces native support for **26D pose estimation data** (x, y coordinates only) through specialized classes and file formats. It maintains full support for the 3D formats introduced in version 2.0.

> 📝 **Official Schema**: [schema-v2.1.json](./schema-v2.1.json)

## 🆕 2D Format Highlights
- **Specialized Classes**: `PEImage2D`, `PEVideo2D`, `ImageSkeletonData2D`, `VideoSkeletonData2D`.
- **Coordinate System**: Uses only `x` and `y`.
- **Data Key**: Uses `poseestimationpoints` instead of `skeletonpoints` for 2D structures.
- **Extensions**:
    - **Images**: `.pei2` (uncompressed), `.pei2z` (compressed).
    - **Videos**: `.pev2` (uncompressed), `.pev2z` (compressed).

---

## 🖼️ Image Format v2.1 (2D Support)

The 2D image format uses the `poseestimationpoints` key.

```json
{
  "origin": "rtmpose",
  "HumanDetectionModel": "YOLOv8",
  "PoseEstimationModel": "RTMPose_2D",
  "persons": [
    {
      "person_id": 0,
      "BoundingBox": [100.0, 200.0, 50.0, 150.0],
      "poseestimationpoints": [
        { "id": 0, "x": 0.23, "y": 0.61 },
        { "id": 1, "x": 0.28, "y": 0.66 }
      ]
    }
  ]
}
```

---

## 🎞️ Video Format v2.1 (2D Support)

For 2D videos, each frame contains persons with 2D points.

```json
{
  "origin": "rtmpose",
  "frames": [
    {
      "frame": 0,
      "persons": [
        {
          "person_id": 0,
          "poseestimationpoints": [
            { "id": 0, "x": 0.23, "y": 0.61 }
          ]
        }
      ]
    }
  ]
}
```

---

## 🏷️ Metadata Fields
Available at the root or within person objects:
- `HumanDetectionModel`: (str) Model used to detect humans.
- `PoseEstimationModel`: (str) Model used for pose estimation.
- `Pose3DGenerationMethod`: (str) [3D only] Method/Algorithm for 3D generation.
- `3DLiftingModel`: (str) [3D only] Model used for 3D lifting from 2D.
- `BoundingBox`: (list) [x_min, y_min, width, height] of the person.

---

## 🏗️ Architectural Classes

### 3D Support (v2.0+)
- `PEImage` / `PEVideo`
- `ImageSkeletonData` / `VideoSkeletonData`
- uses `skeletonpoints` (x, y, z)

### 2D Support (v2.1+)
- `PEImage2D` / `PEVideo2D`
- `ImageSkeletonData2D` / `VideoSkeletonData2D`
- uses `poseestimationpoints` (x, y)

---

## 📦 File Extensions & Compression

| Type | 3D Extensions | 2D Extensions | Compression | 
| :--- | :--- | :--- | :--- |
| **Image** | `.pei`, `.peiz` | `.pei2`, `.pei2z` | GZIP |
| **Video** | `.pev`, `.pevz` | `.pev2`, `.pev2z` | GZIP |

### Usage in Python
```python
# 2D Saving
image2d.save_in_compressed_file("output.pei2z")
video2d.save_in_compressed_file("output.pev2z")

# 2D Loading
from pose_estimation_recognition_utils import load_image_skeleton_from_compressed_file2D
data = load_image_skeleton_from_compressed_file2D("output.pei2z", "0-17")
```

---

## 📌 Implementation Notes
- The 2D loaders (`...2D`) are optimized for `(x, y)` data and return numpy arrays of shape `(N, 2)`.
- The `poseestimationpoints` key is the new standard for 2D data to distinguish it from 3D `skeletonpoints`.
- Backward compatibility: 2D loaders can also fall back to reading `skeletonpoints` if present in a 2D context.
