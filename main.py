import cv2
import argparse
import time
import os
import sys
from collections import defaultdict

from models.face_detection import YoloV8FaceDetector
from models.face_tracking import DeepSortFaceTracker
from models.face_expression import EmotionRecognizer
from models.face_direction import HeadPoseEstimator


def main(video_path):
    print("Initializing modules...")
    try:
        detector = YoloV8FaceDetector()
        tracker = DeepSortFaceTracker(max_age=50, n_init=3)
        emotion_recognizer = EmotionRecognizer()
        pose_estimator = HeadPoseEstimator()
        print("All models initialized successfully.")
    except Exception as e:
        print(f"Error during model initialization: {e}")
        sys.exit(1)

    dissociation_tracker = defaultdict(lambda: {'count': 0, 'status': 'Unknown'})
    DISSOCIATION_FRAME_THRESHOLD = 6
    YAW_THRESHOLD = 33
    PITCH_THRESHOLD = 23

    # Attendance and control variables
    unique_ids = set()
    PRINT_INTERVAL = 10
    ATTENDANCE_UPDATE_INTERVAL = 50

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    print(f"Video Info: {frame_width}x{frame_height} @ {fps} FPS")

    frame_num = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("End of video stream or error reading frame.")
            break

        frame_num += 1
        start_time = time.time()

        detections = detector.detect(frame)
        tracked_faces = tracker.update_tracks(detections, frame)

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

            emotion, confidence = emotion_recognizer.infer(face_crop)
            yaw, pitch, roll = pose_estimator.predict_angles(face_crop)

            emotion = emotion.lower()
            is_looking_away = (abs(yaw) > YAW_THRESHOLD) or (abs(pitch) > PITCH_THRESHOLD)
            is_confused_or_surprised = emotion in ['surprise', 'fear', 'disgust', 'anger']

            current_tracker = dissociation_tracker[track_id]

            if is_looking_away or is_confused_or_surprised:
                current_tracker['count'] += 1
            else:
                current_tracker['count'] = 0
                current_tracker['status'] = 'Engaged'

            if current_tracker['count'] > DISSOCIATION_FRAME_THRESHOLD:
                current_tracker['status'] = 'Disengaged'

            status = current_tracker['status']

            # Add to attendance every 50 frames (including frame 0)
            if frame_num % ATTENDANCE_UPDATE_INTERVAL == 0:
                unique_ids.add(track_id)

            # Print individual status every 10 frames
            if frame_num % PRINT_INTERVAL == 0:
                print(f"[Frame {frame_num}] ID: {track_id}, Emotion: {emotion}, Engagement: {status}")

        # Print attendance update every 50 frames
        if frame_num % ATTENDANCE_UPDATE_INTERVAL == 0:
            print(f"[Frame {frame_num}] Attendance so far: {len(unique_ids)} students")

        end_time = time.time()

    cap.release()
    print("\n--- Final Attendance Summary ---")
    print(f"Unique students detected: {len(unique_ids)}")
    print(f"Student IDs: {sorted(unique_ids)}")
    print("Processing finished.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Face detection, tracking, emotion, and dissociation analysis.")
    parser.add_argument('--video', type=str, required=True,
                        help="Path to the input video file (e.g., sample.mp4) or '0' for webcam.")
    args = parser.parse_args()

    video_input = 0 if args.video == '0' else args.video

    if video_input != 0 and not os.path.exists(video_input):
        print(f"Error: Video file not found at {video_input}")
        sys.exit(1)

    main(video_input)
