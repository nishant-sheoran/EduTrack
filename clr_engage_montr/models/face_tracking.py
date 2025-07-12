# models/face_tracker.py

from deep_sort_realtime.deepsort_tracker import DeepSort

class DeepSortFaceTracker:
    """
    A wrapper class for the DeepSORT algorithm to track detected faces.
    """
    def __init__(self, max_age=30, n_init=3, nms_max_overlap=1.0):
        """
        Initializes the DeepSORT tracker.

        Args:
            max_age (int): The maximum number of consecutive frames a track can be lost for.
            n_init (int): The number of consecutive frames a track must be detected for to be confirmed.
            nms_max_overlap (float): The NMS overlap threshold for the tracker.
        """
        self.tracker = DeepSort(
            max_age=max_age,
            n_init=n_init,
            nms_max_overlap=nms_max_overlap,
            max_cosine_distance=0.3,
            nn_budget=None,
            override_track_class=None,
            embedder="mobilenet",
            half=True,
            bgr=True,
        )
        print("Face Tracker (DeepSORT) initialized successfully.")

    def update_tracks(self, raw_detections, frame):
        """
        Updates the tracker with new detections from a frame.

        Args:
            raw_detections (list): A list of detections from the face detector.
                                   Expected format: [([x, y, w, h], score, class_name), ...]
            frame (np.ndarray): The current video frame (required by DeepSORT for feature extraction).

        Returns:
            list: A list of active tracks. Each track is a tuple containing:
                  (track_id, [x1, y1, x2, y2]).
        """
        # The deep-sort-realtime library expects detections in a specific format:
        # A list of tuples, where each tuple is ([left, top, w, h], confidence, detection_class).
        # Our YoloV8FaceDetector's output format is already compatible.
        
        # Update the tracker with the new detections
        tracks = self.tracker.update_tracks(raw_detections, frame=frame)
        
        tracked_faces = []
        for track in tracks:
            if not track.is_confirmed():
                continue
            
            track_id = track.track_id
            ltrb = track.to_ltrb() # Gets bounding box in [left, top, right, bottom] format
            
            # Convert to integer coordinates for drawing
            bbox = [int(val) for val in ltrb]
            
            tracked_faces.append((track_id, bbox))
            
        return tracked_faces