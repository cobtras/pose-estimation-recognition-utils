# 📄 Data Format Documentation: 3D Skeleton Points

This project uses JSON files to store 3D skeleton data, supporting both:
- **Single-frame (image-based)** skeletons
- **Multi-frame (video-based)** skeletons

---

## 🖼️ Single Frame Format

### 🔹 Format 1: Without joint names

```json
{
  "skeletonpoints": [
    { "id": 0, "x": 0.23, "y": 0.61, "z": 0.12 },
    { "id": 1, "x": 0.28, "y": 0.66, "z": 0.10 }
  ]
}
```

### 🔹 Format 2: With joint names

```json
{
  "skeletonpoints": [
    { "id": 0, "name": "left_shoulder", "x": 0.23, "y": 0.61, "z": 0.12 },
    { "id": 1, "name": "right_shoulder", "x": 0.28, "y": 0.66, "z": 0.10 }
  ]
}
```

> 📦 Class: `ImageSkeletonData`  
> 📌 Data points: `SkeletonDataPoint` or `SkeletonDataPointWithName`  
> 🔧 Methods: `.add_data_point()`, `.to_json()`

---

## 🎞️ Multi-Frame Format (Video)

Each frame stores its own list of 3D joint positions.

### 🔹 Format 1: Without joint names

```json
{
  "frames": [
    {
      "skeletonpoints": [
        { "id": 0, "x": 0.23, "y": 0.61, "z": 0.12 },
        { "id": 1, "x": 0.28, "y": 0.66, "z": 0.10 }
      ]
    },
    {
      "skeletonpoints": [
        { "id": 0, "x": 0.24, "y": 0.62, "z": 0.13 },
        { "id": 1, "x": 0.29, "y": 0.67, "z": 0.11 }
      ]
    }
  ]
}
```

### 🔹 Format 2: With joint names

```json
{
  "frames": [
    {
      "skeletonpoints": [
        { "id": 0, "name": "left_shoulder", "x": 0.23, "y": 0.61, "z": 0.12 },
        { "id": 1, "name": "right_shoulder", "x": 0.28, "y": 0.66, "z": 0.10 }
      ]
    },
    {
      "skeletonpoints": [
        { "id": 0, "name": "left_shoulder", "x": 0.24, "y": 0.62, "z": 0.13 },
        { "id": 1, "name": "right_shoulder", "x": 0.29, "y": 0.67, "z": 0.11 }
      ]
    }
  ]
}
```

> 📦 Class: `VideoSkeletonData`  
> 🔁 Internally stores a list of `ImageSkeletonData` frames  
> 🔧 Methods: `.add_frame()`, `.to_json()`

---

## 💾 Saving Example (Python)

```python
# Image data
img_data = ImageSkeletonData()
img_data.add_data_point(SkeletonDataPoint(0, 0.23, 0.61, 0.12))
json_str = img_data.to_json()

# Video data
video_data = VideoSkeletonData()
video_data.add_frame(img_data)
json_str = video_data.to_json()

# Save to file
with open("skeleton_data.json", "w") as f:
    f.write(json_str)
```

---

## 📌 Notes

- `id` must be unique **within each frame**.
- `name` is optional but helps with semantic understanding and model alignment.
- The order of joints should be consistent across frames.
- `VideoSkeletonData` enables frame-wise animation and analysis of skeleton sequences.
