# main.py

import cv2
import argparse
import time

from models.face_detection import YoloV8FaceDetector
from models.face_tracking import DeepSortFaceTracker

def main(video_path):
    """
    Main function to run face detection and tracking on a video.

    Args:
        video_path (str): The path to the input video file.
    """
    # Initialize the detector and tracker
    detector = YoloV8FaceDetector()
    tracker = DeepSortFaceTracker(max_age=50, n_init=3)

    # Open the video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    
    print(f"Video Info: {frame_width}x{frame_height} @ {fps} FPS")

    # Optional: Video writer to save the output
    # output_path = video_path.replace('.mp4', '_tracked.mp4')
    # out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        start_time = time.time()
        
        # 1. Detect faces in the current frame
        detections = detector.detect(frame)
        
        # 2. Update the tracker with the new detections
        tracked_faces = tracker.update_tracks(detections, frame)

        # 3. Draw bounding boxes and track IDs on the frame
        for track_id, bbox in tracked_faces:
            x1, y1, x2, y2 = bbox
            # Draw bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            # Put track ID
            label = f"Face ID: {track_id}"
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        end_time = time.time()
        processing_fps = 1 / (end_time - start_time)

        # Display FPS on the frame
        cv2.putText(frame, f"FPS: {processing_fps:.2f}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        # Display the resulting frame
        cv2.imshow('Face Tracking', frame)
        
        # Optional: Write the frame to the output video
        # out.write(frame)

        # Press 'q' to exit the video stream
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        frame_count += 1

    # Release everything when done
    cap.release()
    # out.release()
    cv2.destroyAllWindows()
    print("Processing finished.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run face detection and tracking on a video.")
    parser.add_argument('--video', type=str, required=True, help="Path to the input video file.")
    args = parser.parse_args()
    
    main(args.video)