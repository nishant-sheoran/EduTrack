# Classroom Engagement Detection System

This project performs **real-time analysis of student engagement** in a classroom or video environment using Intel-optimized models. It detects and tracks students' faces, classifies their emotions, and determines whether they are visually engaged based on head pose.

---

## 🔧 Components

### 1. **Face Detection**
- **Model Used:** YOLOv8 face (converted to ONNX for Intel optimization)
- **Role:** Detects bounding boxes for student faces in each frame.
- **Code:** `models/face_detection.py`
- **Class:** `YoloV8FaceDetector`

### 2. **Face Tracking**
- **Algorithm Used:** DeepSORT
- **Role:** Assigns consistent `track_id`s to each detected face to maintain identity over frames.
- **Code:** `models/face_tracking.py`
- **Class:** `DeepSortFaceTracker`

### 3. **Face Expression Recognition**
- **Model Used:** `emotion-recognition-retail-0003` (Intel OpenVINO)
- **Role:** Classifies student emotions into categories like `neutral`, `happy`, `surprise`, `fear`, `anger`, etc.
- **Code:** `models/face_expression.py`
- **Class:** `EmotionRecognizer`

### 4. **Face Direction / Head Pose Estimation**
- **Model Used:** `head-pose-estimation-adas-0001` (Intel OpenVINO)
- **Role:** Estimates the head angles: `yaw`, `pitch`, `roll` to determine where the student is looking.
- **Code:** `models/face_direction.py`
- **Class:** `HeadPoseEstimator`

---

## ▶️ Main Script

### File: `main.py`

### Workflow:
1. Loads all four models and initializes processing.
2. Reads input from webcam or video file.
3. For every frame:
   - Detects and tracks faces.
   - For each face:
     - Crops the face.
     - Runs emotion classification.
     - Runs head pose estimation.
     - Determines if student is **Engaged** or **Disengaged** based on:
       - Head turned away (yaw/pitch beyond threshold)
       - Emotion is confused/disengaged (`surprise`, `fear`, etc.)
   - Tracks how many consecutive frames a student has been disengaged.
   - Every **10 frames**, prints:
     ```
     ID: <track_id>, Emotion: <emotion>, Engagement: <Engaged/Disengaged>
     ```
   - Every **50 frames**, updates attendance with newly seen track IDs and prints:
     ```
     [Frame 50] Attendance so far: <number_of_students_detected>
     ```

### At End of Execution:
Prints a summary like:
--- Final Attendance Summary ---
Unique students detected: 6
Student IDs: [0, 2, 3, 4, 5, 6]
Processing finished.


---

## 📈 Variables Printed for Integration

| Variable              | Type   | Description |
|-----------------------|--------|-------------|
| `track_id`            | `int`  | Unique ID assigned to each student (used for tracking across frames) |
| `emotion`             | `str`  | Detected emotion label (e.g. `neutral`, `happy`, `surprise`, `fear`) |
| `status`              | `str`  | `"Engaged"` or `"Disengaged"` based on emotion and head pose |
| `unique_ids`          | `set`  | Set of unique `track_id`s detected so far — used for attendance |
| `frame_num`           | `int`  | Current frame number |
| `yaw`, `pitch`        | `float`| Head angles — used to infer if the student is looking away |

These values can be used in:
- **Frontend dashboards**
- **Analytics tools**
- **Graphs** (gauge meters showing attention)
- **Heatmaps** of disengagement over time

---

## 📦 Input

Run the script using:

```bash
python main.py --video 0               # for webcam
python main.py --video sample.mp4     # for video file
