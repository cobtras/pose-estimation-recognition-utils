# 📄 Data Format Documentation v2.0 (.pei, .pev, .peiz, .pevz)

Version 2.0 introduces optional metadata fields for model tracking and native support for multiple persons in a single image or video.

> 📝 **Official Schema**: [schema-v2.0.json](./schema-v2.0.json)

## 🏷️ New Optional Metadata Fields
These fields can be included at the root of the JSON or within specific person objects:
- `HumanDetectionModel`: (str) Model used to detect humans.
- `PoseEstimationModel`: (str) Model used for 2D pose estimation.
- `Pose3DGenerationMethod`: (str) Method/Algorithm for 3D generation.
- `3DLiftingModel`: (str) Model used for 3D lifting from 2D.
- `BoundingBox`: (list) [x_min, y_min, width, height] of the person.

---

## 🖼️ image Format v2.0 (Multi-Person)

The `persons` array allows tracking multiple people in a single frame.

```json
{
  "origin": "mediapipe",
  "HumanDetectionModel": "YOLOv8",
  "PoseEstimationModel": "RTMPose",
  "persons": [
    {
      "person_id": 0,
      "BoundingBox": [100.0, 200.0, 50.0, 150.0],
      "skeletonpoints": [
        { "id": 0, "x": 0.23, "y": 0.61, "z": 0.12 },
        { "id": 1, "x": 0.28, "y": 0.66, "z": 0.10 }
      ]
    },
    {
      "person_id": 1,
      "BoundingBox": [300.0, 210.0, 55.0, 140.0],
      "skeletonpoints": [
        { "id": 0, "x": 0.24, "y": 0.62, "z": 0.13 },
        { "id": 1, "x": 0.29, "y": 0.67, "z": 0.11 }
      ]
    }
  ]
}
```

---

## 🎞️ Video Format v2.0 (Multi-Person)

In videos, each frame contains a `persons` array to track individuals over time.

```json
{
  "origin": "mediapipe",
  "HumanDetectionModel": "YOLOv8",
  "frames": [
    {
      "frame": 0,
      "persons": [
        {
          "person_id": 0,
          "skeletonpoints": [
            { "id": 0, "x": 0.23, "y": 0.61, "z": 0.12 }
          ]
        },
        {
          "person_id": 1,
          "skeletonpoints": [
            { "id": 0, "x": 0.24, "y": 0.62, "z": 0.13 }
          ]
        }
      ]
    },
    {
      "frame": 1,
      "persons": [
        {
          "person_id": 0,
          "skeletonpoints": [
            { "id": 0, "x": 0.25, "y": 0.63, "z": 0.14 }
          ]
        }
      ]
    }
  ]
}
```

---

## 🏗️ Architectural Changes

1. **`PEImage` / `PEVideo`**: Support metadata fields and multi-person tracking via the `persons` array.
2. **`save_in_compressed_file`**: New method for GZIP compression.
3. **Backward Compatibility**: Single-person files are still supported and automatically handled by loaders.

---

## 📦 Compressed Formats (.peiz, .pevz)
Version 2.0 supports compressed storage using **GZIP**:
- **Images**: `.peiz` (Compressed `.pei`)
- **Videos**: `.pevz` (Compressed `.pev`)

These files contain the exact same JSON structure but are significantly smaller on disk.

### Usage in Python
```python
# Saving
image.save_in_compressed_file("data.peiz")
video.save_in_compressed_file("data.pevz")

# Loading
from pose_estimation_recognition_utils import load_image_skeleton_from_compressed_file
data = load_image_skeleton_from_compressed_file("data.peiz", "0-32")
```

---

## 📌 Implementation Notes
- `person_id` is essential for tracking the same individual across frames in a video.
- Metadata at the root applies to all persons in the file unless overridden.
