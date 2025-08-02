# 📄 Data Format Documentation: 3D Skeleton Points

This project uses JSON files to store 3D skeleton data, supporting both:
- **Single-frame (image-based)** skeletons
- **Multi-frame (video-based)** skeletons

---

## 🖼️ Single Frame Format (Image)

### 🔹 Format 1: Without joint names

```json
{
  "origin": "mediapipe",
  "skeletonpoints": [
    { "id": 0, "x": 0.23, "y": 0.61, "z": 0.12 },
    { "id": 1, "x": 0.28, "y": 0.66, "z": 0.10 }
  ]
}
```

### 🔹 Format 2: With joint names

```json
{
  "origin": "mediapipe",
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
  "origin": "mediapipe",
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
  "origin": "mediapipe",
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

## 💾 Saving Example Image (Python)

```python
# Image data
img_data = ImageSkeletonData()
img_data.add_data_point(SkeletonDataPoint(0, 0.23, 0.61, 0.12))

save_obj = PEImage(origion="mediapipe")
save_obj.set_data(img_data)
json_str = save_obj.to_json()


# Save to file
with open("image.pei", "w") as f:
    f.write(json_str)
```

## 💾 Saving Example Video (Python)

```python
# frame data
frame_data = VideoSkeletonData(frame=0)
frame_data.add_data_point(SkeletonDataPoint(0, 0.23, 0.61, 0.12))

# Video data
video_data = PEVideo(origin="mediapipe")
video_data.add_frame(frame)
json_str = video_data.to_json()

# Save to file
with open("video.pev", "w") as f:
    f.write(json_str)
```

---

## 📌 Notes

- `id` must be unique **within each frame**.
- `name` is optional but helps with semantic understanding and model alignment.
- The order of joints should be consistent across frames.
- `VideoSkeletonData` enables frame-wise animation and analysis of skeleton sequences.
