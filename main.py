import cv2
import argparse
import time
import os
import sys
from models.face_detection import YoloV8FaceDetector
from models.face_tracking import DeepSortFaceTracker
from models.face_expr import EmotionRecognizer


def main(video_path):
    """
    Main function to run face detection, tracking, and emotion recognition on a video.
    """
    print("Initializing modules...")
    try:
        # Initialize your existing detector and tracker classes
        detector = YoloV8FaceDetector()
        tracker = DeepSortFaceTracker(max_age=50, n_init=3)
        
        # Initialize the new EmotionRecognizer class with the correct model paths
        emotion_recognizer = EmotionRecognizer()
        print("All models initialized successfully.")
    except Exception as e: # Catch broader exception during initialization
        print(f"Error during model initialization: {e}")
        sys.exit(1)

    # Open video
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    
    print(f"Video Info: {frame_width}x{frame_height} @ {fps} FPS")

    frame_num = 0 # To track frame number, was 'frame_count' in your original
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("End of video stream or error reading frame.")
            break

        frame_num += 1 # Increment frame number
        start_time = time.time()
        
        # 1. Detect faces using your YoloV8FaceDetector
        # This returns a list of (x1, y1, x2, y2, confidence)
        detections = detector.detect(frame)
        
        # 2. Track faces using your DeepSortFaceTracker
        # This is expected to return a list of (track_id, bbox) tuples, where bbox is (x1, y1, x2, y2)
        tracked_faces = tracker.update_tracks(detections, frame)

        # 3. Analyze emotions for each tracked face
        for track_id, bbox in tracked_faces:
            x1, y1, x2, y2 = bbox
            
            # Clamp coordinates within frame size and convert to int
            x1 = max(0, int(x1))
            y1 = max(0, int(y1))
            x2 = min(frame.shape[1], int(x2))
            y2 = min(frame.shape[0], int(y2))

            face_crop = frame[y1:y2, x1:x2]
            
            # Add a check for valid crop size before passing to emotion model
            if face_crop.size == 0 or face_crop.shape[0] < 10 or face_crop.shape[1] < 10:
                continue # Skip if crop is empty or too small

            # Predict emotion using the EmotionRecognizer class's infer method
            emotion, confidence = emotion_recognizer.infer(face_crop)
            print(emotion)

            # --- Draw results on frame ---
            # You can keep your preferred drawing logic here, or use simple fixed color
            color = (0, 255, 0) # Green for bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            
            label = f"ID: {track_id} | {emotion} ({confidence:.2f})"
            
            # Adjust text position
            text_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
            text_x = x1
            text_y = y1 - 10
            if text_y < text_size[1] + 5: # If text goes above frame, put it below bbox
                text_y = y2 + text_size[1] + 5

            cv2.putText(frame, label, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX,
                        0.6, (255, 255, 0), 2) # Yellow for text (as in your original)

        # 4. Display FPS
        end_time = time.time()
        processing_fps = 1 / (end_time - start_time)
        cv2.putText(frame, f"FPS: {processing_fps:.2f}", (20, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2) # Red for FPS
        
        # Show the frame
        cv2.imshow('Face Tracking + Emotion Recognition', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()
    print("Processing finished.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Face detection, tracking, and emotion analysis.")
    parser.add_argument('--video', type=str, required=True, 
                        help="Path to the input video file (e.g., --video sample_video.mp4) or 0 for webcam.")
    args = parser.parse_args()

    # Handle webcam input as integer 0
    if args.video.isdigit() and int(args.video) == 0:
        video_input = 0
    else:
        video_input = args.video
        # Optional: Add a check if the video file exists
        if not os.path.exists(video_input) and video_input != 0:
            print(f"Error: Video file not found at {video_input}")
            sys.exit(1)

    main(video_input)
