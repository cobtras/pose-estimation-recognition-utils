# 📄 Data Format Documentation v3.0 (.pei, .pev, .peiz, .pevz)

Version 3.0 introduces major structural upgrades for spatial and temporal analysis, including topology representation (SkeletonGraph), calculated geometrical bone vectors with masking, and kinematics properties (velocity, acceleration).

> 📝 **Official Schema**: [schema-v3.0.json](./schema-v3.0.json)

## 🆕 New Features in v3.0

### 1. SkeletonGraph (Topology)
The `graph` object defines the invariant topological structure of the skeleton, preventing repeating edge definitions.
- `edges`: Array of integer pairs representing connected points (e.g. `[[0, 1], [1, 2]]`).
- `edge_types` (Optional): Dictionary mapping stringified edges to semantic types (e.g. `"0_1": "arm"`).

### 2. Kinematics Properties
Individual data points now optionally store their physical kinematics calculated over time (in `PEVideo`):
- `velocity`, `velocity_x`, `velocity_y`, `velocity_z`
- `acceleration`, `acceleration_x`, `acceleration_y`, `acceleration_z`

### 3. Bone Vectors
Computed geometrical connections between joints based on the `graph`.
- Represented as an array of `bone_vectors` inside `person`, `frame`, or root.
- Includes `start`, `end`, `x`, `y`, `z`, and `confidence`.
- Missing or low-visibility bones are **masked** using `null` coordinate values and `confidence=0.0`. Valid bones receive a confidence equal to the minimum of their two connected points.

---

## 🖼️ Image Format v3.0 (Multi-Person with Graph & Bones)

```json
{
  "origin": "mediapipe",
  "PoseEstimationModel": "RTMPose",
  "graph": {
    "edges": [[0, 1], [1, 2]]
  },
  "persons": [
    {
      "person_id": 0,
      "BoundingBox": [100.0, 200.0, 50.0, 150.0],
      "skeletonpoints": [
        { "id": 0, "x": 10.0, "y": 20.0, "confidence": 0.9 },
        { "id": 1, "x": 12.0, "y": 25.0, "confidence": 0.8 },
        { "id": 2, "x": 14.0, "y": 30.0, "confidence": 0.6 }
      ],
      "bone_vectors": [
        { "start": 0, "end": 1, "x": 2.0, "y": 5.0, "confidence": 0.8 },
        { "start": 1, "end": 2, "x": 2.0, "y": 5.0, "confidence": 0.6 }
      ]
    }
  ]
}
```

---

## 🎞️ Video Format v3.0 (Kinematics & Interpolation)

In videos, calculating kinematics or bone vectors applies temporal interpolation automatically where possible. Missing points that are temporarily lost will produce masked output or be smoothly interpolated.

```json
{
  "origin": "mediapipe",
  "graph": {
    "edges": [[0, 1]]
  },
  "frames": [
    {
      "frame": 0,
      "persons": [
        {
          "person_id": 0,
          "skeletonpoints": [
            { "id": 0, "x": 10.0, "y": 20.0, "velocity_x": 0.5, "velocity_y": 1.2 }
          ],
          "bone_vectors": [
            { "start": 0, "end": 1, "x": null, "y": null, "confidence": 0.0 }
          ]
        }
      ]
    }
  ]
}
```

---

## 🏗️ Architectural Backwards Compatibility
File parsing seamlessly falls back to legacy implementations when single-person formats matching `1.0` or `2.0` syntax are detected. Standard formats use UTF-8 and compress easily via natively integrated GZIP functionality (`.peiz` / `.pevz`).
