# 📄 Data Format Documentation v2.0: Rich Metadata & Multi-Person Support

Version 2.0 introduces optional metadata fields for model tracking and native support for multiple persons in a single image or video.

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

1. **`PEImage` / `PEVideo`**: Will now support a dictionary of metadata.
2. **`MultiPersonImage` / `MultiPersonVideo`**: New classes to handle the `persons` array logic.
3. **Backward Compatibility**: Single-person files will still be supported by wrapping them or using the legacy classes.

---

## 📌 Implementation Notes
- `person_id` is essential for tracking the same individual across frames in a video.
- Metadata at the root applies to all persons in the file unless overridden.
