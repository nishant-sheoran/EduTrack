import cv2
import time
import threading
from collections import defaultdict
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.face_detection import YoloV8FaceDetector
from models.face_tracking import DeepSortFaceTracker
from models.face_expression import EmotionRecognizer
from models.face_direction import HeadPoseEstimator

app = FastAPI()

# CORS for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Shared state for Streamlit to access
realtime_data = {
    "present_ids": [],
    "engagement": []
}

def run_video_analysis(video_path):
    print("Initializing models...")
    detector = YoloV8FaceDetector()
    tracker = DeepSortFaceTracker(max_age=50, n_init=3)
    emotion_recognizer = EmotionRecognizer()
    pose_estimator = HeadPoseEstimator()
    print("Models loaded.")

    dissociation_tracker = defaultdict(lambda: {'count': 0, 'status': 'Unknown'})
    DISSOCIATION_FRAME_THRESHOLD = 6
    YAW_THRESHOLD = 33
    PITCH_THRESHOLD = 23

    unique_ids = set()
    PRINT_INTERVAL = 10
    ATTENDANCE_UPDATE_INTERVAL = 50

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return

    frame_num = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("End of video or cannot read frame.")
            break

        frame_num += 1
        detections = detector.detect(frame)
        tracked_faces = tracker.update_tracks(detections, frame)

        engagement_output = []

        for track_id, bbox in tracked_faces:
            x1, y1, x2, y2 = map(int, [
                max(0, bbox[0]),
                max(0, bbox[1]),
                min(frame.shape[1], bbox[2]),
                min(frame.shape[0], bbox[3])
            ])

            face_crop = frame[y1:y2, x1:x2]
            if face_crop.size == 0 or face_crop.shape[0] < 20 or face_crop.shape[1] < 20:
                continue

            emotion, _ = emotion_recognizer.infer(face_crop)
            yaw, pitch, _ = pose_estimator.predict_angles(face_crop)

            emotion = emotion.lower()
            is_looking_away = abs(yaw) > YAW_THRESHOLD or abs(pitch) > PITCH_THRESHOLD
            is_disengaged_emotion = emotion in ['surprise', 'fear', 'disgust', 'anger']

            current_tracker = dissociation_tracker[track_id]
            if is_looking_away or is_disengaged_emotion:
                current_tracker['count'] += 1
            else:
                current_tracker['count'] = 0
                current_tracker['status'] = 'Engaged'

            if current_tracker['count'] > DISSOCIATION_FRAME_THRESHOLD:
                current_tracker['status'] = 'Disengaged'

            # Attendance
            if frame_num % ATTENDANCE_UPDATE_INTERVAL == 0:
                unique_ids.add(track_id)

            if frame_num % PRINT_INTERVAL == 0:
                print(f"[Frame {frame_num}] ID: {track_id}, Emotion: {emotion}, Engagement: {current_tracker['status']}")

            engagement_output.append({
                "id": track_id,
                "emotion": emotion,
                "engagement": current_tracker['status']
            })

        if frame_num % PRINT_INTERVAL == 0:
            realtime_data["present_ids"] = list(unique_ids)
            realtime_data["engagement"] = engagement_output

        if frame_num % ATTENDANCE_UPDATE_INTERVAL == 0:
            print(f"[Frame {frame_num}] Attendance: {len(unique_ids)} students")

    cap.release()
    print("Video processing complete.")

# FastAPI endpoint
@app.get("/api/classroom/realtime")
def get_realtime_engagement(subject: str = ""):
    return realtime_data

# Start the processing thread
def start_background_processing(video_path=r"test_images\test_video3.mp4"):  # <-- change to 0 for webcam
    t = threading.Thread(target=run_video_analysis, args=(video_path,), daemon=True)
    t.start()

# Kick off when server starts
start_background_processing()
